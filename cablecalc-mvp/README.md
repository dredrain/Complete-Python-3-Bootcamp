# CableCalc — LV Cable Sizing & Voltage-Drop Report (IEC 60364)

> Drop in your cable schedule (CSV). Get a stamped, revision-controlled cable
> calculation report (ampacity per IEC 60364-5-52 + voltage drop) in seconds.

This is the **MVP / product seed** described in `../INGRESOS_PASIVOS_ESTRATEGIA.md`
(Vía 1). It is a clean-room implementation — no proprietary code from `ariadne`
or any employer tooling — built to be sold as a digital download.

## Why someone pays for this

Every electrical engineer in data centers, renewables and industry does cable
sizing by hand in fragile Excel sheets. This tool does it deterministically,
applies the correction factors correctly, and produces a **client-ready PDF/HTML
report with a revision stamp** — the exact deliverable an oficina técnica issues.

## Quick start

```bash
cd cablecalc-mvp
python3 cli.py sample_cable_schedule.csv \
    --project "AWS DC Aragon - Bldg A" --revision B \
    --author "D. Martin Mateos" --out report.html
# open report.html and print to PDF
```

No dependencies — Python 3.8+ standard library only. Tests: `python3 tests/test_engine.py`.

## What it computes (per cable)

1. **Design current** `Ib` (1- or 3-phase).
2. **Required capacity** `Iz' = Ib / (Ca · Cg)` with ambient (Ca) and grouping (Cg)
   correction factors from IEC 60364-5-52.
3. **Conductor selection**: smallest standard size whose tabulated `Iz ≥ Iz'`.
4. **Voltage drop** `ΔU = k · Ib · L · (R·cosφ + X·sinφ)`; auto-upsizes if the
   percentage exceeds the per-cable limit.

Input columns: `tag, load_kw, voltage_v, length_m, phases, power_factor,
conductor, insulation, method, ambient_c, circuits_grouped, vd_limit_pct`
(only the first four are mandatory).

## Scope of the MVP (be honest with buyers)

- Ampacity dataset: **Cu / XLPE**, installation methods **C and E**, 30 °C base —
  a representative subset of IEC 60364-5-52. Aluminium, PVC and more methods are
  stubbed in `cablecalc/data.py` and easy to extend.
- This is an engineering aid, **not a certified design tool**. The report says so.

## Productization checklist (turn this into income)

- [ ] Resolve the **IP/employer question** first (see strategy doc, section 5).
- [ ] Extend `data.py`: Al, PVC, methods A/B/D/F, full Ca/Cg/soil tables.
- [ ] Add a one-page landing + Gumroad/Lemon Squeezy checkout.
- [ ] Tiered pricing idea:
  - **Lite** (€29, one-off): CSV → HTML/PDF report, Cu/XLPE.
  - **Pro** (€99, one-off): full material/method tables, branded report, batch boards.
  - **Team** (€19/mo or €190/yr): updates, multi-project, support.
- [ ] Collect 3–5 testimonials from colleagues to seed credibility.
- [ ] Optional v2: web app (upload SLD/CSV in browser) for true recurring SaaS.

## Files

```
cablecalc-mvp/
├── cablecalc/
│   ├── data.py      # IEC reference tables (cited; extend here)
│   ├── engine.py    # current, ampacity selection, voltage drop
│   └── report.py    # HTML (printable to PDF) + Markdown report
├── cli.py           # command-line entry point
├── sample_cable_schedule.csv
├── tests/test_engine.py
└── LICENSE-COMMERCIAL.md
```

## Disclaimer

Provided "as is". Results must be verified against the applicable edition of the
relevant standards (IEC 60364-5-52 and related) and the cable manufacturer's
datasheet by a qualified engineer before use in any real installation.
