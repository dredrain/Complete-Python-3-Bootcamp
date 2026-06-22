"""Short-circuit thermal withstand (adiabatic method).

IEC 60364-4-43 / IEC 60909 basis. The adiabatic equation gives the minimum
conductor cross-section that survives a short circuit without exceeding the
insulation limit temperature:

    S_min = (I_scc * sqrt(t)) / k          [mm^2]

equivalently the permitted disconnection time for a given section:

    t_max = (k * S / I_scc) ** 2           [s]

where:
    I_scc  prospective short-circuit current through the cable [A]
    t      fault clearance time [s]
    k      material/insulation constant [A*s^0.5 / mm^2] (IEC 60364-4-43 Table 43A)
    S      conductor cross-section [mm^2]
"""

from math import sqrt

from . import data


def k_factor(conductor, insulation):
    try:
        return data.K_SCC[conductor][insulation]
    except KeyError:
        raise ValueError(f"No k constant for {conductor}/{insulation}.")


def min_cross_section(iscc_a, fault_time_s, conductor, insulation):
    """Minimum cross-section (mm^2) to withstand the fault adiabatically."""
    k = k_factor(conductor, insulation)
    return (iscc_a * sqrt(fault_time_s)) / k


def max_disconnection_time(size_mm2, iscc_a, conductor, insulation):
    """Maximum permitted clearance time (s) for a given section."""
    k = k_factor(conductor, insulation)
    return (k * size_mm2 / iscc_a) ** 2


def withstands(size_mm2, iscc_a, fault_time_s, conductor, insulation):
    """True if the section survives the fault (S >= S_min)."""
    return size_mm2 >= min_cross_section(iscc_a, fault_time_s, conductor, insulation)
