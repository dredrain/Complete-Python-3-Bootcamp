"""
Modelo ILUSTRATIVO del curso temporal de los beneficios del mindfulness
a lo largo de 24 meses, expresado como tamaño del efecto (d de Cohen)
frente a la linea base.

IMPORTANTE / RIGOR:
- No existe un unico estudio que mida estas 7 variables mes a mes durante 2 anos.
- Los VALORES DE MESETA (asintotas) provienen de meta-analisis publicados.
- La FORMA de la curva (gran parte de la mejora en ~8 semanas y posterior
  mantenimiento) refleja el hallazgo robusto de que los efectos aparecen en los
  programas de 8 semanas y se conservan en seguimientos a largo plazo.
- Mas alla de ~12 meses la trayectoria es EXTRAPOLACION (mantenimiento), no
  medicion directa: por eso se sombrea como zona de incertidumbre.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

# d_max = tamano del efecto aproximado de meta-analisis (mejora sostenida)
# tau   = constante temporal (meses); la mayoria del efecto en ~2-3 meses
# fuente resumida en la leyenda del pie de figura
series = {
    "Reduccion del estres":   dict(dmax=0.55, tau=1.3, color="#d62728"),
    "Reduccion de rumiacion": dict(dmax=0.55, tau=1.6, color="#9467bd"),
    "Sueno (calidad)":        dict(dmax=0.45, tau=1.8, color="#1f77b4"),
    "Resiliencia":            dict(dmax=0.40, tau=2.2, color="#2ca02c"),
    "Memoria de trabajo":     dict(dmax=0.23, tau=2.0, color="#ff7f0e"),
    "Concentracion":          dict(dmax=0.18, tau=2.0, color="#8c564b"),
    "Atencion sostenida":     dict(dmax=0.12, tau=2.5, color="#7f7f7f"),
}

t = np.linspace(0, 24, 400)

fig, ax = plt.subplots(figsize=(12, 7))

# zona de extrapolacion (>12 meses): casi no hay datos medidos
ax.axvspan(12, 24, color="0.92", zorder=0)
ax.text(18, 0.59, "Zona de extrapolacion\n(mantenimiento, no medido)",
        ha="center", va="top", fontsize=9, color="0.45", style="italic")

# bandas de referencia de magnitud del efecto (Cohen)
for y, lab in [(0.2, "pequeno (0.2)"), (0.5, "medio (0.5)")]:
    ax.axhline(y, color="0.8", lw=1, ls="--", zorder=1)
    ax.text(0.1, y + 0.005, lab, fontsize=8, color="0.55")

for name, p in series.items():
    d = p["dmax"] * (1 - np.exp(-t / p["tau"]))
    ax.plot(t, d, color=p["color"], lw=2.4, label=name, zorder=3)
    ax.scatter([24], [d[-1]], color=p["color"], s=28, zorder=4)
    ax.annotate(f"d≈{p['dmax']:.2f}", (24, d[-1]), xytext=(6, 0),
                textcoords="offset points", va="center", fontsize=8,
                color=p["color"])

# marca de fin del programa estandar de 8 semanas (~2 meses)
ax.axvline(2, color="0.6", lw=1, ls=":")
ax.text(2.1, 0.02, "fin programa\n8 semanas", fontsize=8, color="0.5")

ax.set_xlim(0, 26)
ax.set_ylim(0, 0.62)
ax.set_xticks(range(0, 25, 3))
ax.set_xlabel("Meses de practica continua de mindfulness")
ax.set_ylabel("Mejora vs. linea base  (tamano del efecto, d de Cohen)")
ax.set_title("Beneficios del mindfulness a lo largo de 2 anos\n"
             "Modelo ilustrativo basado en meta-analisis (no datos de un unico estudio)",
             fontsize=13, fontweight="bold")
ax.legend(loc="center right", frameon=True, fontsize=9)
ax.grid(True, axis="y", alpha=0.25)

caption = (
    "Asintotas (d) de meta-analisis: estres y rumiacion (MBSR/MBCT) ~moderado; sueno y resiliencia "
    "pequeno-moderado;\nmemoria de trabajo g≈0.23, atencion/concentracion g≈0.12-0.18 (evidencia mixta, "
    "algunos ECA sin efecto).\nLa mayoria de la mejora ocurre en ~8 semanas y se MANTIENE; mas alla de "
    "12 meses es mantenimiento extrapolado, no medido."
)
fig.text(0.5, -0.02, caption, ha="center", va="top", fontsize=8.5, color="0.3")

plt.tight_layout()
plt.savefig("mindfulness_beneficios_2anos.png", dpi=150, bbox_inches="tight")
print("guardado: mindfulness_beneficios_2anos.png")
