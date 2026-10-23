"""Genera guion/guion.md y guion/cifras.md desde narracion.json, timing.json y data.py."""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from data import FIGS, ND
from kit import fmt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
G = os.path.join(ROOT, "..", "guion")
N = json.load(open(os.path.join(G, "narracion.json")))
T = json.load(open(os.path.join(ROOT, "build", "timing.json")))
S = {s["id"]: s for s in T["scenes"]}
tc = lambda x: f"{int(x // 60)}:{x % 60:04.1f}"

out = ["# Guion de narración · «Argentina 2023–2026»", "",
       "Documental de análisis económico y social sobre la presidencia de Javier Milei (10/12/2023 – corte de datos 23/10/2026).",
       f"Duración total: {tc(T['total'])} · 1920×1080 · 30 fps. Narración en español rioplatense (voz sintética), tono profesional y neutral.", "",
       "Los tiempos indican el inicio de cada frase en el video final. Cada cifra leída figura en `cifras.md` con su período exacto y su fuente.", ""]
out += ["## 00 · Portada (0:00 – 0:06)", "", "*Sin narración.* Título «Argentina 2023–2026», subtítulo y fecha de corte de datos. Entra la música.", ""]
for sc in N["escenas"]:
    s = S[sc["id"]]
    out.append(f"## {sc['id'][1:].zfill(2)} · {sc['titulo']} ({tc(s['start'])} – {tc(s['start'] + s['duration'])})")
    out.append("")
    for f in sc["frases"]:
        out.append(f"- **{tc(s['start'] + s['cues'][f['id']][0])}** — {f['texto']}")
    out.append("")
o = T["outro"]
out += [f"## Créditos ({tc(o['start'])} – {tc(T['total'])})", "", "*Sin narración.* Fuentes de los datos, aclaraciones metodológicas y créditos técnicos. La música se desvanece.", ""]
open(os.path.join(G, "guion.md"), "w").write("\n".join(out))

rows = ["# Listado de cifras utilizadas", "",
        "Todas las cifras provienen del Excel «milei_2023_2026_indicadores_y_fuentes.xlsx» (corte 23/10/2026). "
        "Se indica el período exacto, la hoja de origen y la fuente original. Las filas marcadas como **cálculo** son derivaciones explícitas de cifras del Excel. "
        "Los valores de 2026 son parciales salvo indicación.", "",
        "| Indicador | Valor | Unidad | Período exacto | Organismo | Hoja Excel | Nota | Fuente |", "|---|---|---|---|---|---|---|---|"]
for f in FIGS:
    v = f["val"]
    if isinstance(v, (int, float)):
        d = 0 if isinstance(v, int) else (3 if f["key"] == "sipa_jul26" else 1)
        v = fmt(v, d, sign=f["unit"].startswith("%") and v > 0 and "var" in f["ind"].lower())
    note = ("**cálculo** · " if f["calc"] else "") + f["note"]
    rows.append(f"| {f['ind']} | {v} | {f['unit']} | {f['period']} | {f['org']} | {f['sheet']} | {note} | [enlace]({f['url']}) |")
rows += ["", "## Indicadores sin dato verificable (N/D)", "",
         "Se muestran en pantalla como N/D. N/D significa ausencia de cifra homogénea verificada en la base, nunca cero.", ""]
for k, items in ND.items():
    rows.append(f"- **{k.capitalize()}**: " + "; ".join(items))
rows += ["", "## Advertencias metodológicas aplicadas", "",
         "1. **Años completos vs. 2026 parcial**: 2023–2025 son años o períodos cerrados; 2026 se presenta con su mes, trimestre o semestre exacto y con rayado en los gráficos.",
         "2. **Recuperación vs. crecimiento**: el índice del PBI (2023 = 100) muestra que la suba de 2025 primero compensó la caída de 2024; el nivel 2025 queda ≈ 3 % sobre 2023. La serie no incluye años previos, por lo que no se afirma nada sobre máximos históricos.",
         "3. **Índices normalizados**: PBI 2023 = 100 e índices por división industrial son normalizaciones construidas encadenando tasas del INDEC; no son el PBI en pesos ni el IPI base 2004.",
         "4. **Inversión**: la FBCF es inversión total (pública y privada), usada como proxy.",
         "5. **Inflación**: mensual, interanual y acumulada no se comparan entre sí. Para 2024–2025 el Excel trae sólo diciembre como dato mensual; no se completan los otros meses.",
         "6. **Empleo**: T4 2023–2025 vs T2 2026 puede incluir estacionalidad. Informalidad: T1 vs T1 (IIEP).",
         "7. **Salarios**: variaciones acumuladas de CEPA con base noviembre 2023 (previa al salto de precios de diciembre); el resultado depende de la base elegida.",
         "8. **Pobreza**: 31 aglomerados urbanos; se comparan semestres equivalentes (1S 2025 → 1S 2026: +0,7 p.p.).",
         "9. **Gasto**: el gasto consolidado (Ministerio de Economía, con obras sociales) sólo es comparable 2023–2024. La OPC estima 33,0 % del PBI para 2024 con otra cobertura: no se fusionan. La ejecución de la Administración Nacional 2026 tiene otro perímetro.",
         "10. **Exportaciones**: 2026 = enero–septiembre, no comparable con años completos; el INDEC revisa cifras entre informes (2025: 87.077 en enero 2026 vs 87.111 en septiembre 2026).",
         "11. **Educación, salud y seguridad**: Aprender no equivale a alfabetización; estadísticas vitales con rezago (último dato 2024); delitos registrados dependen de la denuncia; femicidios son el extremo letal de la violencia de género.",
         "12. **Causalidad**: los datos describen resultados observados; no prueban por sí solos el efecto de políticas del gobierno.",
         "13. **Contexto no numérico**: la mención a la sequía de 2023 es contexto para interpretar el rebote del agro en 2024; no se usa ninguna cifra externa al Excel."]
open(os.path.join(G, "cifras.md"), "w").write("\n".join(rows) + "\n")
print("ok")
