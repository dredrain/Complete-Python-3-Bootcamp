"""Tests for the cable sizing engine. Run: python -m pytest  (or python tests/test_engine.py)"""

import os
import sys
from math import sqrt

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cablecalc import CableInput, design_current, size_cable, voltage_drop  # noqa: E402
from cablecalc import short_circuit  # noqa: E402
from cablecalc.engine import ac_resistance  # noqa: E402
from cablecalc import data  # noqa: E402


def approx(a, b, tol=1e-3):
    return abs(a - b) <= tol * max(1.0, abs(b))


def test_design_current_three_phase():
    # 100 kW, 400 V, pf 1.0 -> 100000 / (sqrt(3)*400) = 144.34 A
    ib = design_current(100, 400, 3, 1.0)
    assert approx(ib, 100000 / (sqrt(3) * 400)), ib


def test_design_current_single_phase():
    ib = design_current(3.5, 230, 1, 0.9)
    assert approx(ib, 3500 / (230 * 0.9)), ib


def test_ac_resistance_temperature_rise():
    # Cu 50 mm2: R20=0.387; at 90C factor = 1 + 0.00393*70 = 1.2751
    r = ac_resistance("Cu", 50, 90)
    assert approx(r, 0.387 * 1.2751), r


def test_voltage_drop_monotonic_in_length():
    base = dict(tag="t", load_kw=50, voltage_v=400, length_m=50)
    short = CableInput(**base)
    long = CableInput(**{**base, "length_m": 100})
    ib = design_current(50, 400, 3, 0.9)
    assert voltage_drop(long, 50, ib) > voltage_drop(short, 50, ib)


def test_sizing_picks_adequate_ampacity():
    # 75 kW @ 400 V, pf 0.9 -> Ib ~ 120 A. Method E, 30C, 1 circuit.
    c = CableInput(tag="F1", load_kw=75, voltage_v=400, length_m=10,
                   method="E", ambient_c=30, circuits_grouped=1, vd_limit_pct=5)
    r = size_cable(c)
    assert r.ampacity_ok and r.vd_ok and r.ok
    assert r.iz_table_a >= r.iz_required_a
    assert approx(r.ib_a, 75000 / (sqrt(3) * 400 * 0.9), tol=1e-6)


def test_long_run_forces_upsize_for_voltage_drop():
    # Long length with tight VD limit must yield a larger size than a short run.
    short = size_cable(CableInput(tag="s", load_kw=55, voltage_v=400,
                                  length_m=10, vd_limit_pct=2))
    long = size_cable(CableInput(tag="l", load_kw=55, voltage_v=400,
                                 length_m=200, vd_limit_pct=2))
    assert long.size_mm2 > short.size_mm2
    assert long.vd_pct <= 2.0 + 1e-9 or not long.vd_ok


def test_grouping_and_ambient_reduce_capacity():
    relaxed = size_cable(CableInput(tag="a", load_kw=60, voltage_v=400,
                                    length_m=20, ambient_c=30, circuits_grouped=1))
    derated = size_cable(CableInput(tag="b", load_kw=60, voltage_v=400,
                                    length_m=20, ambient_c=45, circuits_grouped=4))
    assert derated.iz_required_a > relaxed.iz_required_a
    assert derated.size_mm2 >= relaxed.size_mm2


def test_aluminium_needs_larger_section_than_copper():
    base = dict(load_kw=90, voltage_v=400, length_m=30, method="E",
                ambient_c=30, circuits_grouped=1, vd_limit_pct=5)
    cu = size_cable(CableInput(tag="cu", conductor="Cu", **base))
    al = size_cable(CableInput(tag="al", conductor="Al", **base))
    assert al.size_mm2 >= cu.size_mm2
    assert al.ok and cu.ok


def test_pvc_capacity_below_xlpe():
    # Same size/method: PVC tabulated ampacity must be lower than XLPE.
    assert data.IZ["Cu"]["PVC"]["C"][50] < data.IZ["Cu"]["XLPE"]["C"][50]


def test_all_methods_supported():
    for m in ("B1", "C", "E", "F"):
        r = size_cable(CableInput(tag=m, load_kw=40, voltage_v=400,
                                  length_m=20, method=m))
        assert r.ok, m


def test_short_circuit_min_section_formula():
    # 20 kA, 0.1 s, Cu/XLPE k=143 -> S_min = 20000*sqrt(0.1)/143 = 44.2 mm2
    smin = short_circuit.min_cross_section(20000, 0.1, "Cu", "XLPE")
    assert approx(smin, 20000 * (0.1 ** 0.5) / 143), smin


def test_short_circuit_forces_upsize():
    # Small load but huge fault current must drive a large section.
    no_sc = size_cable(CableInput(tag="a", load_kw=10, voltage_v=400,
                                  length_m=10, iscc_ka=0))
    with_sc = size_cable(CableInput(tag="b", load_kw=10, voltage_v=400,
                                    length_m=10, iscc_ka=30, fault_time_s=0.2))
    assert with_sc.size_mm2 > no_sc.size_mm2
    assert with_sc.scc_ok and with_sc.size_mm2 >= with_sc.smin_scc_mm2


def test_max_disconnection_time_roundtrip():
    # If S == S_min then t_max should equal the fault time.
    smin = short_circuit.min_cross_section(15000, 0.3, "Al", "PVC")
    tmax = short_circuit.max_disconnection_time(smin, 15000, "Al", "PVC")
    assert approx(tmax, 0.3), tmax


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    failed = 0
    for fn in fns:
        try:
            fn()
            print(f"PASS {fn.__name__}")
        except AssertionError as e:
            failed += 1
            print(f"FAIL {fn.__name__}: {e}")
    print(f"\n{len(fns) - failed}/{len(fns)} passed")
    raise SystemExit(1 if failed else 0)
