# Estrategia de Ingresos Pasivos — Daniel Martín Mateos

> Documento generado por Claude Code el 2026-06-22.
> Basado en: CV actualizado (Senior Electrical Engineer · Data Centers) + metadatos de los
> repos de GitHub (`ariadne`, `cable_expert`, `autoBGT`, `fichaje`, `Node_Equations`).
> **Pendiente de afinar con el código real** de esos repos (la sesión no tiene acceso de
> lectura a ellos todavía — ver sección "Qué necesito para profundizar").

---

## 1. Tu perfil, en una frase

Híbrido **ingeniero eléctrico senior + desarrollador** que ya **construye y despliega
software real** en dos de los nichos mejor pagados y con mayor demanda del momento:

- **Construcción eléctrica de data centers hyperscale** — AWS Europe (Spain) Region, Aragón,
  interfaz directa con AWS y Arup, coordinación multi-contratista en UTE.
- **Renovables utility-scale** — eólica (GE Vernova) y PV (132–492 MWp).

Doble grado (Eléctrica + Mecánica), IEC/NFPA, inglés técnico C1. Y, lo más raro y valioso:
**capacidad demostrada de convertir tu conocimiento de dominio en herramientas que la gente
usa** (AutoSU adoptado internamente, motor de cálculo de cables, sync Procore→Jira).

## 2. La tesis central

**No tienes que inventar un producto nuevo. Ya lo construiste.** La vía de ingresos pasivos
con mayor encaje con tu perfil es **productizar lo que ya tienes** para el nicho que conoces
desde dentro:

| Activo existente | Qué es | Potencial de producto |
|---|---|---|
| **Ariadne** | "Untangle your cable mesh" — routing/sizing de cables (Python, networkx) | ⭐ El producto estrella. Cálculo y routing de cables LV/MV desde SLD. |
| **cable_expert** | Base de conocimiento/cálculo de cables (IEC) | Motor de reglas + documentación; el "cerebro" normativo de Ariadne. |
| **AutoSU / autoBGT** | Automatización de submittals (Office→PDF, merge, naming) | Tool para oficinas técnicas de construcción (⚠ ver riesgo IP). |

El nicho —ingeniería eléctrica de data centers y renovables— tiene tres propiedades de oro:
1. **Presupuestos enormes** y poca sensibilidad al precio de una herramienta de 50–500 €.
2. **Dolor real y repetitivo** (cálculo de cables, voltage drop, submittals) que tú sufres.
3. **Competencia floja**: las alternativas son Excel artesanal o software caro tipo ETAP/Cable HV.

## 3. Las vías, rankeadas por encaje × esfuerzo

### Vía 1 — Productizar Ariadne (RECOMENDADA)
El cálculo de cables LV/MV (ampacidad IEC 60364/60502, voltage drop, agrupamiento, bandeja)
es un dolor universal del sector. Modelos posibles, de menor a mayor "pasividad":

- **Descarga de pago** (Gumroad / Lemon Squeezy): ejecutable o plantilla con licencia. Construyes
  una vez, vendes muchas. ~Más pasivo, menos margen recurrente.
- **Micro-SaaS por suscripción**: app web (subes SLD/lista de cables → informe de cálculo IEC
  con sellado de revisión). Recurrente y escalable; requiere más mantenimiento.
- **Licencia a empresas/UTEs**: licencia anual por equipo. Pocos clientes, tickets altos. El más
  rentable dado tu acceso al sector, aunque menos "pasivo" (implica venta).

> Recomendación: empezar por **descarga de pago de un módulo concreto** (p.ej. "Calculadora de
> voltage drop + ampacidad IEC con informe en PDF") para validar demanda con mínimo riesgo, y
> escalar a SaaS si hay tracción.

### Vía 2 — Plantillas y herramientas de cálculo (catálogo de productos)
Más allá de Ariadne, empaqueta tu trabajo diario en productos digitales pequeños:
calculadoras Excel/VBA (cortocircuito IEC 60909, grounding/IEC 62305, dimensionado PV),
plantillas de SLD, cable schedules, BOM/MTO, plantillas DFMEA. Venta en Gumroad.
Cada producto es pequeño, pero el catálogo compone ingresos.

### Vía 3 — Contenido de nicho como canal de captación (no ingreso directo)
Blog/LinkedIn/YouTube técnico sobre cálculo eléctrico para data centers y renovables
(PVSyst, routing de cables, IEC). No monetiza por sí mismo al principio; su función es
**alimentar de clientes** las vías 1 y 2 y construir autoridad. Semi-pasivo y compuesto.

### Vía 4 — Respaldo financiero (el verdadero ingreso pasivo de base)
Tu sueldo de ingeniero senior en un sector caliente es tu mayor activo. Reinvertir el
excedente en indexados/ETFs de acumulación globales (vía broker europeo, UCITS) es el
ingreso pasivo más fiable y verdaderamente pasivo. No usa tu perfil técnico, pero es la
base sobre la que se apoyan las demás. (No es asesoramiento financiero.)

## 4. Plan 0 → 12 meses

- **Mes 0–1 — Blindaje legal + validación.** Resolver la cuestión de IP (sección 5). Elegir
  UN módulo de Ariadne para vender. Hablar con 5–10 colegas del sector: ¿pagarían? ¿cuánto?
- **Mes 1–3 — Primer producto.** Empaquetar el módulo: licencia, informe PDF con sellado de
  revisión, landing simple, pasarela de pago (Gumroad/Lemon Squeezy). Lanzar a precio bajo.
- **Mes 3–6 — Catálogo + contenido.** Añadir 2–3 calculadoras (Vía 2). Empezar a publicar
  contenido técnico (Vía 3) que apunte a las landings.
- **Mes 6–12 — Escalar lo que funcione.** Si hay tracción, evaluar SaaS o licencia a empresa.
  En paralelo, automatizar la reinversión del excedente (Vía 4).

## 5. ⚠ Riesgo crítico: propiedad intelectual y conflicto con el empleador

Esto es lo primero que hay que resolver, antes de monetizar nada:

- **AutoSU / autoBGT / fichaje** se crearon **en/para B-Global Tech**. Con alta probabilidad
  son **propiedad del empleador** (obra por encargo). **No los vendas** sin permiso explícito
  por escrito.
- **Ariadne / cable_expert**: aunque estén en tu cuenta personal, revisa tu contrato por
  cláusulas de **cesión de invenciones, dedicación exclusiva y no competencia**. Si los
  desarrollaste con tiempo/equipo/datos de la empresa, puede haber reclamación.
- **Confidencialidad**: nunca incluyas en un producto datos, layouts o información de proyectos
  de AWS/Arup/clientes. El producto debe construirse sobre **normativa pública (IEC/NFPA) y
  conocimiento general**, no sobre material de proyecto.
- **Acción**: lee tu contrato; si hay duda, una consulta con un abogado laboralista/IP en España
  (1–2 h) es la mejor inversión antes de facturar el primer euro.

## 6. Qué necesito para profundizar (siguiente paso para Claude)

No pude leer el código de tus repos: esta sesión solo tiene acceso a
`dredrain/complete-python-3-bootcamp`. Para afinar esta estrategia con el código real
(estado de madurez de Ariadne, qué le falta para ser producto, calidad de cable_expert):

1. Añade `dredrain/ariadne` (y `cable_expert`) al alcance del entorno en Claude Code web
   (selector de repos). Doc: https://code.claude.com/docs/en/claude-code-on-the-web
2. Con acceso, puedo: auditar Ariadne, definir el MVP vendible, diseñar la landing/pricing,
   y montar el esqueleto de la pasarela de pago/licencia.

---

*Documento vivo. Próxima revisión: tras dar acceso a `ariadne` o tras tu feedback sobre qué vía priorizar.*
