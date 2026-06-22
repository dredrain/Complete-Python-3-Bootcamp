"""LV cable sizing and voltage-drop engine (IEC 60364 basis).

Workflow per cable:
  1. Compute required Iz' = Ib / (Ca * Cg)
  2. Select the smallest standard size whose tabulated Iz >= Iz'
  3. Compute voltage drop at the selected size; if it exceeds the limit,
     step up until both ampacity and voltage-drop checks pass.
"""

from dataclasses import dataclass, field
from math import sqrt

from . import data


@dataclass
class CableInput:
    tag: str
    load_kw: float          # active power, kW
    voltage_v: float        # line voltage, V
    length_m: float
    phases: int = 3         # 3 or 1
    power_factor: float = 0.9
    conductor: str = "Cu"   # "Cu" or "Al"
    insulation: str = "XLPE"
    method: str = "E"       # installation method (C, E ...)
    ambient_c: float = 30.0
    circuits_grouped: int = 1
    vd_limit_pct: float = 5.0


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
    ampacity_ok: bool
    vd_ok: bool
    notes: list = field(default_factory=list)

    @property
    def ok(self):
        return self.ampacity_ok and self.vd_ok


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
    if cable.conductor != "Cu" or cable.insulation != "XLPE":
        raise ValueError(
            "MVP ampacity dataset only covers Cu/XLPE; extend data.py for others."
        )
    if cable.method not in data.IZ_CU_XLPE_3PH:
        raise ValueError(f"Unsupported installation method '{cable.method}'.")
    return data.IZ_CU_XLPE_3PH[cable.method]


def size_cable(cable: CableInput) -> CableResult:
    ib = design_current(cable.load_kw, cable.voltage_v, cable.phases, cable.power_factor)
    ca = data.nearest_factor(data.CA_XLPE, cable.ambient_c)
    cg = data.nearest_factor(data.CG, cable.circuits_grouped)
    iz_required = ib / (ca * cg)

    iz_table = _iz_table(cable)
    notes = []

    chosen = None
    for size in data.STANDARD_SIZES:
        if size not in iz_table or size not in data.REACTANCE:
            continue
        if iz_table[size] < iz_required:
            continue
        # ampacity ok at this size; now check voltage drop
        vd = voltage_drop(cable, size, ib)
        vd_pct = vd / cable.voltage_v * 100.0
        if vd_pct <= cable.vd_limit_pct:
            chosen = (size, iz_table[size], vd, vd_pct)
            break
        else:
            notes.append(
                f"{size} mm2 meets ampacity but VD={vd_pct:.2f}% > "
                f"{cable.vd_limit_pct:.1f}%; stepping up."
            )

    if chosen is None:
        # fall back to largest size, report failure
        size = data.STANDARD_SIZES[-1]
        vd = voltage_drop(cable, size, ib)
        vd_pct = vd / cable.voltage_v * 100.0
        return CableResult(
            tag=cable.tag, ib_a=ib, iz_required_a=iz_required, ca=ca, cg=cg,
            size_mm2=size, iz_table_a=iz_table.get(size, 0.0),
            vd_volts=vd, vd_pct=vd_pct,
            ampacity_ok=iz_table.get(size, 0.0) >= iz_required,
            vd_ok=vd_pct <= cable.vd_limit_pct,
            notes=notes + ["No standard size satisfies both checks; review design."],
        )

    size, iz_t, vd, vd_pct = chosen
    return CableResult(
        tag=cable.tag, ib_a=ib, iz_required_a=iz_required, ca=ca, cg=cg,
        size_mm2=size, iz_table_a=iz_t, vd_volts=vd, vd_pct=vd_pct,
        ampacity_ok=True, vd_ok=True, notes=notes,
    )
