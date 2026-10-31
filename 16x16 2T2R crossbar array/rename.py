import sys

def get_row(y):
    # Y-coordinate cutoffs separating the 16 rows
    cutoffs = [2400, 3300, 4200, 4900, 5700, 6600, 7400, 8300, 9100, 9900, 10900, 11600, 12500, 13300, 14200]
    for r, cutoff in enumerate(cutoffs, 1):
        if y < cutoff: return r
    return 16

def get_col(x):
    # X-coordinate cutoffs separating the 16 columns
    cutoffs = [1000, 1800, 2500, 3400, 4200, 4800, 5800, 6600, 7200, 8100, 8900, 9500, 10500, 11300, 11900]
    for c, cutoff in enumerate(cutoffs, 1):
        if x < cutoff: return c
    return 16

def get_pn(row, y):
    # Y-coordinate cutoffs separating Positive (top) and Negative (bottom) branches within each row
    pn_cutoffs = {
        1: 2200, 2: 3050, 3: 3900, 4: 4600, 5: 5450, 6: 6250,
        7: 7200, 8: 8050, 9: 8900, 10: 9700, 11: 10550, 12: 11400,
        13: 12250, 14: 13100, 15: 13900, 16: 14700
    }
    return 'N' if y > pn_cutoffs[row] else 'P'

def update_netlist(input_file, output_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    out_lines = []
    current_comp = None
    current_x = 0
    current_y = 0

    for line in lines:
        if line.startswith("SYMBOL "):
            out_lines.append(line)
            # Detect transistors, resistors, and memristors
            if "nmos" in line or "res" in line or "MEM_YAKOPCIC" in line:
                parts = line.strip().split()
                # Updated component mapping: M for transistor, R for resistor, X for memristor
                current_comp = "M" if "nmos" in line else "R" if "res" in line else "X"
                # X and Y coordinates are the 3rd and 4th elements in the LTspice SYMBOL line
                current_x = int(parts[2])
                current_y = int(parts[3])
            else:
                current_comp = None
        elif line.startswith("SYMATTR InstName") and current_comp:
            row = get_row(current_y)
            col = get_col(current_x)
            pn = get_pn(row, current_y)
            
            new_name = f"{current_comp}{row}_{col}{pn}"
            out_lines.append(f"SYMATTR InstName {new_name}\n")
            current_comp = None  # Reset after renaming to preserve other attributes
        else:
            out_lines.append(line)

    with open(output_file, 'w') as f:
        f.writelines(out_lines)
    print(f"Successfully processed schematic into {output_file}")

if __name__ == "__main__":
    if len(sys.argv) == 3:
        update_netlist(sys.argv[1], sys.argv[2])
    else:
        print("Usage: python rename.py <input.asc> <output.asc>")