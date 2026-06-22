# Gumroad setup — go live in an afternoon

This guide turns the MVP into a product you can sell. The landing page
(`index.html`) already has Gumroad checkout buttons wired; you just create the
products and paste your links.

---

## 0. Before you start (15 min)
- [ ] Confirm the IP/employer question is settled (you said it's clear).
- [ ] Decide your seller name → it becomes `https://YOURNAME.gumroad.com`.
- [ ] Have a way to get paid (Gumroad pays via PayPal/bank; set this in Settings → Payments).

## 1. Package the product (10 min)
Create one ZIP per tier from the `cablecalc-mvp/` folder:

```bash
cd cablecalc-mvp
# Pro = full engine
zip -r CableCalc-Pro-v0.2.zip cablecalc cli.py sample_cable_schedule.csv README.md LICENSE-COMMERCIAL.md
```

- **Lite**: same ZIP is fine for v0 — just describe the reduced scope, or ship a
  trimmed `data.py` (Cu/XLPE only). Easiest: sell Pro first, add Lite later.
- Include the `README.md` and `LICENSE-COMMERCIAL.md` in every ZIP.

## 2. Create the Gumroad products (20 min)
For each tier: Gumroad → **Products → New product → Digital product**.

| Tier | Price | URL/permalink | Upload |
|------|-------|---------------|--------|
| Lite | €29 (one-off) | `cablecalc-lite` | `CableCalc-Lite-v0.2.zip` |
| Pro  | €99 (one-off) | `cablecalc-pro`  | `CableCalc-Pro-v0.2.zip` |
| Team | €190/yr (membership) | `cablecalc-team` | `CableCalc-Pro-v0.2.zip` + updates |

The permalinks above match the links already in `index.html`. Keep them, or
change them and update the three `gumroad-button` hrefs in `index.html`.

### Ready-to-paste product descriptions

**CableCalc Pro (€99)**
> Stop sizing cables in fragile spreadsheets. CableCalc reads your cable schedule
> (CSV) and produces a stamped, revision-controlled calculation report in seconds:
> design current, ampacity per IEC 60364-5-52 (copper & aluminium, XLPE & PVC,
> installation methods B1/C/E/F), voltage drop, and short-circuit withstand
> (adiabatic, IEC 60364-4-43) — with automatic up-sizing until every check passes.
> Output is a clean HTML report you print to PDF and attach to your submittal.
>
> Python 3.8+, no dependencies. Includes sample schedules and full docs.
> Engineering aid — not a certified design tool; verify against the standard and
> manufacturer data. 14-day no-questions refund.

**CableCalc Lite (€29)** — same, trimmed to "copper/XLPE, ampacity + voltage drop".

**CableCalc Team (€190/yr)** — "Everything in Pro, plus a year of updates
(new material/method tables) and email support."

### Settings to enable
- [ ] **Receipt / content**: add a short "Getting started" note (the Quick start
      from `README.md`).
- [ ] **Refund policy**: 14 days (matches the landing FAQ).
- [ ] **License keys** (Pro/Team): Gumroad can auto-generate a license key per sale
      — turn it on so each buyer gets one (pairs with `LICENSE-COMMERCIAL.md`).

## 3. Publish the landing page (10 min)
The landing is a single static file — host it free:

- **GitHub Pages**: push `cablecalc-mvp/landing/` to a repo, enable Pages on that
  folder. URL like `https://YOURNAME.github.io/cablecalc/`.
- Or skip it: Gumroad gives every product its own page. The landing just converts better.

Then replace the three `https://YOURNAME.gumroad.com/l/...` links in `index.html`
with your real product URLs. The Gumroad embed script gives you overlay checkout
automatically (buyers never leave the page).

## 4. Get the first sales (the real goal)
- [ ] Post the sample report + landing link to 5–10 engineer contacts. Ask: "would
      this save you time? what would you pay?"
- [ ] Share in 1–2 niche communities (electrical engineering / data center / PV
      subreddits, LinkedIn, eng-tips). Lead with the *sample report*, not the pitch.
- [ ] Offer the first 10 buyers a discount code (Gumroad → Discounts) for testimonials.

## 5. What to build next, driven by what buyers ask for
- Windows `.exe` (PyInstaller) so non-Python users can buy.
- Exact tabulated PVC/Al ampacities + buried method D.
- Excel input instead of CSV (your audience lives in Excel).

---
**Reminder:** keep the disclaimer visible. You're selling a time-saving calculation
aid, not certified designs — that framing protects you and is honest with buyers.
