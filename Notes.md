## memristor model using verilog :

https://github.com/akashlevy/WP-RRAM-SPICE-Model

## ltspice compatible memristor model

https://github.com/knowm/memristor-models-4-all

- 16x16 2T2R Yakopcic testbench sources
- Matrix convention: row r, column c; W=+1 means P high/N low.
- Write schedule: row1 P,row1 N,row2 P,row2 N,...,row16 P,row16 N.
- Each phase: 1us edge, 18us write, 6us zero/rest before next phase.
- Read: all WL P/N on at 1.8V; varied subthreshold IL read vector.

.param VWRITE=0.9 VWL=1.8 VREAD=50m
.tran 0 900u 0 10n

- Matrix W:
- -1 +0 +1 -1 +0 +1 -1 +0 +1 -1 +0 +1 -1 +0 +1 -1
- +0 +1 -1 +0 +1 -1 +0 +1 -1 +0 +1 -1 +0 +1 -1 +0
- +1 -1 +0 +1 -1 +0 +1 -1 +0 +1 -1 +0 +1 -1 +0 +1
- -1 +0 +1 -1 +0 +1 -1 +0 +1 -1 +0 +1 -1 +0 +1 -1
- +0 +1 -1 +0 +1 -1 +0 +1 -1 +0 +1 -1 +0 +1 -1 +0
- +1 -1 +0 +1 -1 +0 +1 -1 +0 +1 -1 +0 +1 -1 +0 +1
- -1 +0 +1 -1 +0 +1 -1 +0 +1 -1 +0 +1 -1 +0 +1 -1
- +0 +1 -1 +0 +1 -1 +0 +1 -1 +0 +1 -1 +0 +1 -1 +0
- +1 -1 +0 +1 -1 +0 +1 -1 +0 +1 -1 +0 +1 -1 +0 +1
- -1 +0 +1 -1 +0 +1 -1 +0 +1 -1 +0 +1 -1 +0 +1 -1
- +0 +1 -1 +0 +1 -1 +0 +1 -1 +0 +1 -1 +0 +1 -1 +0
- +1 -1 +0 +1 -1 +0 +1 -1 +0 +1 -1 +0 +1 -1 +0 +1
- -1 +0 +1 -1 +0 +1 -1 +0 +1 -1 +0 +1 -1 +0 +1 -1
- +0 +1 -1 +0 +1 -1 +0 +1 -1 +0 +1 -1 +0 +1 -1 +0
- +1 -1 +0 +1 -1 +0 +1 -1 +0 +1 -1 +0 +1 -1 +0 +1
- -1 +0 +1 -1 +0 +1 -1 +0 +1 -1 +0 +1 -1 +0 +1 -1
- Read vector x = [50m, 25m, 40m, 10m, 0m, 35m, 20m, 45m, 15m, 30m, 5m, 50m, 20m, 10m, 40m, 25m]
