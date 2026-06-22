"""CableCalc MVP - LV cable sizing & voltage-drop calculator (IEC 60364 basis)."""

from .engine import CableInput, CableResult, design_current, size_cable, voltage_drop

__all__ = [
    "CableInput", "CableResult", "design_current", "size_cable", "voltage_drop",
]
__version__ = "0.1.0"
