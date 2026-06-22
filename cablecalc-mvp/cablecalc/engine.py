"""LV cable sizing and voltage-drop engine (IEC 60364 basis).

Workflow per cable:
  1. Compute required Iz' = Ib / (Ca * Cg)
  2. Select the smallest standard size whose tabulated Iz >= Iz'
  3. Check voltage drop; step up until within the limit.
  4. If a short-circuit current is given, check adiabatic withstand and step
     up until the section survives the fault (IEC 60364-4-43).
"""

from dataclasses import dataclass, field
from math import sqrt

from . import data, short_circuit


@dataclass
class CableInput:
    tag: str
    load_kw: float          # active power, kW
    voltage_v: float        # line voltage, V
    length_m: float
    phases: int = 3         # 3 or 1
    power_factor: float = 0.9
    conductor: str = "Cu"   # "Cu" or "Al"
    insulation: str = "XLPE"  # "XLPE" or "PVC"
    method: str = "E"       # installation method: B1, C, E, F
    ambient_c: float = 30.0
    circuits_grouped: int = 1
    vd_limit_pct: float = 5.0
    iscc_ka: float = 0.0    # prospective short-circuit current, kA (0 = skip)
    fault_time_s: float = 0.2


@dataclass
class CableResult:
    tag: str
    ib_a: float
    iz_required_a: float
    ca: float
    cg: float
    size_mm2: float
    iz_table_a: float
    vd_volts: float
    vd_pct: float
    smin_scc_mm2: float
    ampacity_ok: bool
    vd_ok: bool
    scc_ok: bool
    notes: list = field(default_factory=list)

    @property
    def ok(self):
        return self.ampacity_ok and self.vd_ok and self.scc_ok


def design_current(load_kw, voltage_v, phases, power_factor):
    """Design current Ib in amperes."""
    watts = load_kw * 1000.0
    if phases == 3:
        return watts / (sqrt(3) * voltage_v * power_factor)
    return watts / (voltage_v * power_factor)


def ac_resistance(conductor, size_mm2, op_temp_c):
    """AC resistance at operating temperature, ohm/km."""
    r20 = data.R20[conductor][size_mm2]
    return r20 * (1 + data.ALPHA[conductor] * (op_temp_c - 20))


def voltage_drop(cable: CableInput, size_mm2, ib_a):
    """Voltage drop in volts for a given conductor size."""
    op_temp = data.MAX_OP_TEMP[cable.insulation]
    r = ac_resistance(cable.conductor, size_mm2, op_temp)   # ohm/km
    x = data.REACTANCE[size_mm2]                            # ohm/km
    length_km = cable.length_m / 1000.0
    cos_phi = cable.power_factor
    sin_phi = sqrt(max(0.0, 1 - cos_phi ** 2))
    z_eff = r * cos_phi + x * sin_phi                       # ohm/km
    factor = sqrt(3) if cable.phases == 3 else 2
    return factor * ib_a * length_km * z_eff


def _iz_table(cable: CableInput):
    try:
        by_method = data.IZ[cable.conductor][cable.insulation]
    except KeyError:
        raise ValueError(
            f"Unsupported conductor/insulation '{cable.conductor}/{cable.insulation}'."
        )
    if cable.method not in by_method:
        raise ValueError(
            f"Unsupported method '{cable.method}'. Available: {data.SUPPORTED_METHODS}."
        )
    return by_method[cable.method]


def size_cable(cable: CableInput) -> CableResult:
    ib = design_current(cable.load_kw, cable.voltage_v, cable.phases, cable.power_factor)
    ca = data.nearest_factor(data.CA[cable.insulation], cable.ambient_c)
    cg = data.nearest_factor(data.CG, cable.circuits_grouped)
    iz_required = ib / (ca * cg)

    iz_table = _iz_table(cable)
    iscc_a = cable.iscc_ka * 1000.0
    smin = (short_circuit.min_cross_section(
                iscc_a, cable.fault_time_s, cable.conductor, cable.insulation)
            if iscc_a > 0 else 0.0)
    notes = []

    candidate_sizes = [s for s in data.STANDARD_SIZES
                       if s in iz_table and s in data.REACTANCE]

    chosen = None
    for size in candidate_sizes:
        if iz_table[size] < iz_required:
            continue
        vd = voltage_drop(cable, size, ib)
        vd_pct = vd / cable.voltage_v * 100.0
        if vd_pct > cable.vd_limit_pct:
            notes.append(f"{size:g} mm2: VD={vd_pct:.2f}% > "
                         f"{cable.vd_limit_pct:.1f}%; stepping up.")
            continue
        if iscc_a > 0 and size < smin:
            notes.append(f"{size:g} mm2: below S_min={smin:.1f} mm2 "
                         f"for {cable.iscc_ka:g} kA fault; stepping up.")
            continue
        chosen = (size, iz_table[size], vd, vd_pct)
        break

    if chosen is None:
        size = candidate_sizes[-1]
        vd = voltage_drop(cable, size, ib)
        vd_pct = vd / cable.voltage_v * 100.0
        return CableResult(
            tag=cable.tag, ib_a=ib, iz_required_a=iz_required, ca=ca, cg=cg,
            size_mm2=size, iz_table_a=iz_table[size], vd_volts=vd, vd_pct=vd_pct,
            smin_scc_mm2=smin,
            ampacity_ok=iz_table[size] >= iz_required,
            vd_ok=vd_pct <= cable.vd_limit_pct,
            scc_ok=(iscc_a == 0 or size >= smin),
            notes=notes + ["No standard size satisfies all checks; review design."],
        )

    size, iz_t, vd, vd_pct = chosen
    return CableResult(
        tag=cable.tag, ib_a=ib, iz_required_a=iz_required, ca=ca, cg=cg,
        size_mm2=size, iz_table_a=iz_t, vd_volts=vd, vd_pct=vd_pct,
        smin_scc_mm2=smin, ampacity_ok=True, vd_ok=True,
        scc_ok=(iscc_a == 0 or size >= smin), notes=notes,
    )
