"""Reference data for LV cable calculations.

Sources / basis:
  * Conductor DC resistance at 20 C: IEC 60228 (max values, class 2 stranded).
  * AC resistance at operating temperature derived via temperature coefficient.
  * Current-carrying capacity (Iz): representative subset of IEC 60364-5-52
    reference tables for copper XLPE (90 C) at 30 C ambient.
  * Ambient (Ca) and grouping (Cg) correction factors: IEC 60364-5-52
    Tables B.52.14 and B.52.17 (representative subset).

IMPORTANT: This is a representative dataset for an MVP. It does NOT replace the
full standard. Verify against the applicable edition of IEC 60364-5-52 and the
cable manufacturer's datasheet before issuing a certified design.
"""

# Temperature coefficient of resistance (per K)
ALPHA = {"Cu": 0.00393, "Al": 0.00403}

# Max operating temperature by insulation (deg C)
MAX_OP_TEMP = {"PVC": 70, "XLPE": 90}

# IEC 60228 conductor DC resistance at 20 C, ohm/km (copper, class 2)
R20_CU = {
    1.5: 12.1, 2.5: 7.41, 4: 4.61, 6: 3.08, 10: 1.83, 16: 1.15,
    25: 0.727, 35: 0.524, 50: 0.387, 70: 0.268, 95: 0.193, 120: 0.153,
    150: 0.124, 185: 0.0991, 240: 0.0754, 300: 0.0601,
}

# IEC 60228 conductor DC resistance at 20 C, ohm/km (aluminium, class 2)
R20_AL = {
    16: 1.91, 25: 1.20, 35: 0.868, 50: 0.641, 70: 0.443, 95: 0.320,
    120: 0.253, 150: 0.206, 185: 0.164, 240: 0.125, 300: 0.100,
}

R20 = {"Cu": R20_CU, "Al": R20_AL}

# Typical AC reactance, ohm/km (multicore / trefoil, 50 Hz). Representative.
REACTANCE = {
    1.5: 0.115, 2.5: 0.110, 4: 0.107, 6: 0.100, 10: 0.094, 16: 0.090,
    25: 0.086, 35: 0.083, 50: 0.083, 70: 0.082, 95: 0.082, 120: 0.080,
    150: 0.080, 185: 0.080, 240: 0.079, 300: 0.079,
}

# Current-carrying capacity Iz (A) - copper, XLPE (90 C), 30 C ambient.
# Keyed by installation method, 3 loaded conductors. IEC 60364-5-52 subset.
IZ_CU_XLPE_3PH = {
    # Method C: clipped direct / in conduit on a wall (Table B.52.5)
    "C": {
        1.5: 20, 2.5: 27, 4: 37, 6: 48, 10: 66, 16: 88, 25: 117, 35: 144,
        50: 175, 70: 222, 95: 269, 120: 312, 150: 358, 185: 408, 240: 481, 300: 553,
    },
    # Method E: multicore cable on a perforated tray (Table B.52.5)
    "E": {
        1.5: 23, 2.5: 31, 4: 42, 6: 54, 10: 75, 16: 100, 25: 133, 35: 164,
        50: 198, 70: 253, 95: 306, 120: 354, 150: 407, 185: 464, 240: 546, 300: 628,
    },
}

# Ambient air temperature correction factor Ca for XLPE (90 C), ref 30 C.
# IEC 60364-5-52 Table B.52.14 (subset).
CA_XLPE = {
    10: 1.15, 15: 1.12, 20: 1.08, 25: 1.04, 30: 1.00, 35: 0.96,
    40: 0.91, 45: 0.87, 50: 0.82, 55: 0.76, 60: 0.71,
}

# Grouping correction factor Cg, number of circuits, single layer bunched.
# IEC 60364-5-52 Table B.52.17 (subset, method C/E reference).
CG = {1: 1.00, 2: 0.80, 3: 0.70, 4: 0.65, 5: 0.60, 6: 0.57, 7: 0.54,
      8: 0.52, 9: 0.50, 12: 0.45, 16: 0.41, 20: 0.38}

# Standard conductor sizes (mm^2), ascending
STANDARD_SIZES = [1.5, 2.5, 4, 6, 10, 16, 25, 35, 50, 70, 95, 120, 150, 185, 240, 300]


def nearest_factor(table, value):
    """Return the conservative (lower-current) factor for an off-table value."""
    keys = sorted(table)
    if value <= keys[0]:
        return table[keys[0]]
    if value >= keys[-1]:
        return table[keys[-1]]
    # pick the next key >= value for ambient (more conservative => smaller factor)
    for k in keys:
        if k >= value:
            return table[k]
    return table[keys[-1]]
