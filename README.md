# Ternary Weight Encoding in Analog Memristor Crossbar Arrays

## 1\. Project Overview

This project explores the implementation of quantized Neural Networks—specifically using ternary weights ($-1, 0, +1$)—mapped onto analog memristive crossbar arrays. The primary objective is to evaluate and compare the reliability, accuracy, and area-efficiency of two distinct 16x16 crossbar architectures:

1. **A Differential 2T2R Architecture**
2. **A Single-Ended 1T1R Architecture with a Reference Column**

By simulating these structures under conditions that approximate real-world non-idealities, this study aims to determine whether the highly area-efficient 1T1R architecture can approach software-level accuracy, or if the 2T2R architecture is strictly necessary to yield reliable inference results.

## 2\. Concept and Architectures

To represent ternary weights in an analog medium where conductance ($G$) can only be positive, we must employ subtraction. This project investigates two topologies to achieve this:

### 2.1. The 2T2R Architecture (Spatial Subtraction)

In this structure, each logical weight is represented by two physical 1T1R cells: a positive cell ($G\_P$) and a negative cell ($G\_N$). The logical weight is derived from the difference in their conductances ($G\_{net} = G\_P - G\_N$).

* **Weight** $+1$**:** $G\_P$ is programmed to a Low Resistance State (LRS), and $G\_N$ to a High Resistance State (HRS).
* **Weight** $0$**:** Both $G\_P$ and $G\_N$ are programmed to HRS.
* **Weight** $-1$**:** $G\_P$ is programmed to HRS, and $G\_N$ to LRS.

### 2.2. The 1T1R Architecture with Reference (Reference-based Subtraction)

To halve the area footprint, this architecture represents each weight with a single memristor. A dedicated reference column is added to the edge of the array, with every cell permanently programmed to an intermediate conductance state ($G\_{MID}$).

* **Weight** $+1$**:** Cell programmed to LRS. ($G > G\_{MID}$)
* **Weight** $0$**:** Cell programmed to the intermediate state. ($G \\approx G\_{MID}$)
* **Weight** $-1$**:** Cell programmed to HRS. ($G < G\_{MID}$)

The final weight is resolved at the periphery by subtracting the shared reference current from the active column's bitline current.

## 3\. Principles of Operation (VMM and Read/Write Mechanics)

The crossbar array functions as a passive analog engine for Vector-Matrix Multiplication (VMM). The operations are governed by fundamental circuit laws acting on applied voltage pulses.

### 3.1. Matrix Multiplication via Physics

* **Multiplication (Ohm's Law):** When a read voltage vector ($V\_{in}$) is applied across the rows (Input Lines/Word Lines), the current through each memristor is the product of the applied voltage and the device's conductance: $I\_{cell} = V\_{in} \\cdot G$.
* **Accumulation (Kirchhoff's Current Law):** The currents from all cells in a column naturally sum together along the vertical Bitline (BL).
* **Result:** The total output current at the bottom of a column is exactly the dot product of the input voltage vector and the column's conductance weight vector: $I\_{out} = \\sum (V\_{in, i} \\cdot G\_{i})$.

### 3.2. Read and Write Pulses

* **Write Phase:** Precise, higher-amplitude voltage pulses are applied to the Wordlines and Bitlines to push the memristor's internal state variable to the desired target ($G\_{LRS}$, $G\_{HRS}$, or $G\_{MID}$). The 1T1R approach specifically requires highly calibrated partial pulses to reliably halt the state variable at $G\_{MID}$.
* **Read Phase:** To perform inference without causing read-disturb (unintentional programming of the device), highly constrained, sub-threshold voltage pulses (e.g., $<50\\text{ mV}$) are applied. The devices operate in their linear hyperbolic-sine subthreshold region, acting as passive resistors.

## 4\. Testbench Configuration and Example

To rigorously validate the MAC operations of both architectures, the SPICE simulation is tested against a specific, challenging 16x16 weight matrix ($W$) and an input read vector ($x$).

The target ternary matrix $W$ cycles through all possible states to test dynamic ranges and cumulative errors across the bitlines:

```
Matrix W:
-1 +0 +1 -1 +0 +1 -1 +0 +1 -1 +0 +1 -1 +0 +1 -1
+0 +1 -1 +0 +1 -1 +0 +1 -1 +0 +1 -1 +0 +1 -1 +0
+1 -1 +0 +1 -1 +0 +1 -1 +0 +1 -1 +0 +1 -1 +0 +1
-1 +0 +1 -1 +0 +1 -1 +0 +1 -1 +0 +1 -1 +0 +1 -1
+0 +1 -1 +0 +1 -1 +0 +1 -1 +0 +1 -1 +0 +1 -1 +0
+1 -1 +0 +1 -1 +0 +1 -1 +0 +1 -1 +0 +1 -1 +0 +1
-1 +0 +1 -1 +0 +1 -1 +0 +1 -1 +0 +1 -1 +0 +1 -1
+0 +1 -1 +0 +1 -1 +0 +1 -1 +0 +1 -1 +0 +1 -1 +0
+1 -1 +0 +1 -1 +0 +1 -1 +0 +1 -1 +0 +1 -1 +0 +1
-1 +0 +1 -1 +0 +1 -1 +0 +1 -1 +0 +1 -1 +0 +1 -1
+0 +1 -1 +0 +1 -1 +0 +1 -1 +0 +1 -1 +0 +1 -1 +0
+1 -1 +0 +1 -1 +0 +1 -1 +0 +1 -1 +0 +1 -1 +0 +1
-1 +0 +1 -1 +0 +1 -1 +0 +1 -1 +0 +1 -1 +0 +1 -1
+0 +1 -1 +0 +1 -1 +0 +1 -1 +0 +1 -1 +0 +1 -1 +0
+1 -1 +0 +1 -1 +0 +1 -1 +0 +1 -1 +0 +1 -1 +0 +1
-1 +0 +1 -1 +0 +1 -1 +0 +1 -1 +0 +1 -1 +0 +1 -1
```

The corresponding read vector $x$ applies sub-threshold voltages (in millivolts) to the 16 rows to execute the inference phase:
$x = \[50\\text{m}, 25\\text{m}, 40\\text{m}, 10\\text{m}, 0\\text{m}, 35\\text{m}, 20\\text{m}, 45\\text{m}, 15\\text{m}, 30\\text{m}, 5\\text{m}, 50\\text{m}, 20\\text{m}, 10\\text{m}, 40\\text{m}, 25\\text{m}]$

By comparing the software-computed dot product of $W^T \\cdot x$ against the analog currents extracted during the SPICE transient read phase, we can precisely quantify the accuracy drop introduced by the hardware.

## 5\. Research Goals and Comparative Analysis

The ultimate goal of this project is to bridge the gap between idealized algorithmic quantization (like BitNet 1.58-bit) and the physical realities of analog hardware.

**Simulation Goals:**

1. **Incorporate Real-World Non-Idealities:** The SPICE simulations (utilizing the Yakopcic memristor model) will incorporate realistic constraints such as wire resistance, parasitic capacitance, and threshold variations to observe how analog errors propagate through MAC operations.
2. **Accuracy vs. Area Trade-off Analysis:**

   * The **1T1R + Reference** structure drastically reduces the physical surface area and power consumption but is highly susceptible to variations, as resolving a "$0$" weight requires the active cell to perfectly match the $G\_{MID}$ of the reference column.
   * The **2T2R** structure consumes twice the area but offers higher noise margins and intrinsic compensation for common-mode noise.
3. **Conclusion:** We seek to determine if the 1T1R architecture's accuracy yield is resilient enough under non-ideal conditions to justify its massive area savings, or if the 2T2R architecture remains the necessary standard for achieving software-equivalent reliability in ternary hardware accelerators.

## 6\. Project Folder Structure

Below is an overview of the project's directories and the specific purpose of each file:

* **`16x16 1T1R crossbar array/`**: Contains all files related to the single-ended 1T1R architecture and its reference column.

  * `Trenery-1T1R.asc`: The primary LTspice schematic file for the 1T1R crossbar array testbench.
  * `MEM\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_YAKOPCIC.asy`: The visual LTspice component symbol for the memristor.
  * `memristor\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_yakopcic.sub`: The underlying SPICE subcircuit definition containing the physics and parameters of the memristor model.
  * `directives.txt`: Contains necessary LTspice simulation directives (e.g., transistor models, transient analysis parameters).
* **`16x16 2T2R crossbar array/`**: Contains all files related to the differential 2T2R architecture.

  * `Trenery-2T2R.asc`: The primary LTspice schematic file for the 2T2R crossbar array testbench.
  * `Voltage\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_Values.txt`: A temporary text file containing experimental voltage values used for the read/write pulse stimuli (currently a work in progress and not yet finalized).
  * `MEM\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_YAKOPCIC.asy` \& `memristor\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_yakopcic.sub`: Local copies of the memristor symbol and subcircuit definition required for the local schematic to compile.
  * `directives.txt`: LTspice simulation directives specific to this array.
* **`Yakopcic-Memristor-Model/`**: A standalone reference directory containing the original, unmodified Yakopcic memristor model files sourced from GitHub.
* **`README.md`**: This main documentation file.

