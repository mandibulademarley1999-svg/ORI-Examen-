"""Genera index.html y compositions/*.html a partir de data.py y timing.json.

Uso (desde video/): python3 build/build.py
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from kit import C, Scene, fmt, words, panel_head, vbars, hbars, line, COMMON_CSS, PRELUDE
from data import FIG, ND

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = json.load(open(os.path.join(ROOT, "build", "timing.json")))
S = {s["id"]: s for s in T["scenes"]}
V = lambda k: FIG[k]["val"]
A, SKY, CO, MU = C["amber"], C["sky"], C["coral"], C["mute"]


def scene(sid, idx):
    s = S[sid]
    return Scene(sid, idx, s["title"], s["duration"], s["cues"])


def bignum(id_, value_html, label, period, size=118, color=None):
    color = color or C["ink"]
    return (f'<div id="{id_}"><div class="h1 num" style="font-size:{size}px;line-height:1;color:{color}">{value_html}</div>'
            f'<div class="body" style="margin-top:14px;font-size:26px">{label}</div>'
            f'<div class="chip" style="display:inline-block;margin-top:12px">{period}</div></div>')


# ---------------------------------------------------------------- 01
def s1():
    sc = scene("s1", 1)
    c = sc.c
    # portada
    sc.add(f'''<div id="s1-cover" class="abs" style="left:160px;top:300px;width:1600px">
  <div class="kicker">Documental · análisis de datos</div>
  <div class="h1" style="font-size:124px;line-height:1.04;margin-top:26px">Argentina <span style="color:{A}">2023–2026</span></div>
  <div class="body" style="font-size:40px;margin-top:26px">Economía y sociedad durante la presidencia de Javier Milei</div>
  <div class="src" style="font-size:20px;margin-top:40px">Indicadores oficiales y académicos · diciembre 2023 – octubre 2026 · corte de datos: 23/10/2026</div>
</div>''')
    sc.j("G.inn('#s1-cover .body', 0.8, 0.8); G.inn('#s1-cover .src', 1.6, 0.8); G.out('#s1-cover', 5.1, 0.5);")
    sc.lead = 6.0  # el encabezado aparece cuando empieza la voz
    sc.chapter(card=False)
    # fecha de asunción
    sc.group("date", 120, 300, 1200, 260, f'''<div class="h1 num" style="font-size:150px;line-height:1">10 · 12 · 2023</div>
<div class="body mute" style="margin-top:18px">Asunción presidencial de Javier Milei</div>''', c("s1a", 0.2), c("s1b", -0.4))
    # cifras de base, una a una
    cols = [("ipc_m_dic23", "Inflación mensual", "diciembre 2023", c("s1b", 0.5)),
            ("ipc_ia_dic23", "Inflación interanual", "dic 2023 vs dic 2022", c("s1b", 4.2)),
            ("pob_2s23", "Pobreza (personas)", "2.º semestre 2023", c("s1c", 0.6)),
            ("desoc_t4_23", "Desocupación", "4.º trimestre 2023", c("s1c", 4.4))]
    for i, (k, lab, per, t) in enumerate(cols):
        x = 120 + i * 425
        sc.add(f'<div id="s1-k{i}" class="abs" style="left:{x}px;top:300px;width:400px;border-left:2px solid {C["grid"]};padding-left:26px">'
               f'<div class="h1 num" style="font-size:96px;line-height:1"><span id="s1-n{i}">0</span><span style="font-size:56px"> %</span></div>'
               f'<div class="body" style="margin-top:16px;font-size:26px">{lab}</div>'
               f'<div class="chip" style="display:inline-block;margin-top:12px">{per}</div></div>')
        sc.j(f"G.up('#s1-k{i}', {t}); G.cu('#s1-n{i}', {V(k)}, 1, '', '', {t + 0.05});")
    sc.j(f"G.dim('#s1-k0, #s1-k1, #s1-k2, #s1-k3', {c('s1d', 0.2)}, 0.35);")
    # banda temporal
    yrs = [("2023", "Línea de base", "mayormente gestión anterior", False),
           ("2024", "Primer año", "año completo", False),
           ("2025", "Segundo año", "año completo", False),
           ("2026", "Parcial", "último mes o trimestre disponible", True)]
    band = ""
    for i, (y, a, b, part) in enumerate(yrs):
        bg = f"repeating-linear-gradient(45deg, {A}33 0 6px, transparent 6px 14px)" if part else C["panel"]
        bd = A if part else C["grid"]
        band += (f'<div id="s1-y{i}" class="abs" style="left:{i * 420}px;top:0;width:404px;height:150px;background:{bg};border-top:3px solid {bd};padding:20px 24px">'
                 f'<div class="h1 num" style="font-size:44px;color:{A if part else C["ink"]}">{y}</div>'
                 f'<div class="body" style="font-size:23px;margin-top:6px">{a}</div><div class="src" style="margin-top:2px">{b}</div></div>')
        sc.j(f"G.up('#s1-y{i}', {c('s1d', 0.3 + i * 0.25)});")
    sc.add(f'<div id="s1-band" class="abs" style="left:120px;top:600px;width:1680px;height:150px">{band}</div>')
    sc.group("caus", 120, 790, 1680, 80, '<div class="note">Los datos describen resultados observados: no demuestran por sí solos causalidad del gobierno.</div>', c("s1d", 6.5))
    sc.source("a", "Fuentes: INDEC — IPC (informe septiembre 2026) y EPH. Cada cifra indica su período exacto.", c("s1b", 0.5))
    return sc


# ---------------------------------------------------------------- 02
def s2():
    sc = scene("s2", 2); c = sc.c; sc.chapter()
    t_out = c("s2d", -0.3)
    bars = vbars(sc, "s2g", 700, 560, [
        dict(label="2024", sub="anual", v=V("pib_24"), t=c("s2a", 1.4), color=SKY),
        dict(label="2025", sub="anual", v=V("pib_25"), t=c("s2a", 4.6), color=A),
        dict(label="2026", sub="1.er sem., interanual", v=V("pib_1s26"), t=c("s2c", 0.6), partial=True, color=A),
    ], -2, 5, d=1, sign=True, suffix=" %")
    sc.group("pa", 120, 250, 700, 640, panel_head("Variación real del PBI", "% respecto del período anterior") + bars, c("s2a", 0.2), t_out)
    sc.group("pa26", 590, 330, 260, 60, '<div class="chip part">2026 = PARCIAL</div>', c("s2c", 1.2), t_out)
    # índice de nivel
    idx = line(sc, "s2i", 820, 470, [
        dict(label="2023", sub="base", v=100.0, t=c("s2b", 0.6)),
        dict(label="2024", sub="anual", v=V("pib_idx_24"), t=c("s2b", 1.6), above=False),
        dict(label="2025", sub="anual", v=V("pib_idx_25"), t=c("s2b", 3.0)),
    ], 96, 105, color=A, d=1, left=60, right=60, ref=(100, "nivel 2023 = 100", c("s2b", 0.4)))
    sc.group("pb", 980, 250, 820, 600, panel_head("Nivel del PBI · índice 2023 = 100", "normalización ilustrativa con tasas reales del INDEC") + idx, c("s2b", 0.0), t_out)
    sc.group("pbn1", 1010, 420, 360, 90, f'<div class="note" style="border-color:{SKY}">2025: primero recupera la caída de 2024</div>', c("s2b", 4.6), t_out)
    sc.group("pbn2", 1440, 628, 360, 100, '<div class="note">≈ +3 % sobre 2023. Sin años previos en la serie: no compara con máximos históricos.</div>', c("s2b", 6.6), t_out)
    sc.source("a", "Fuente: INDEC — Avance del nivel de actividad, 2.º trim. 2026 (revisiones 2025). El índice no es el PBI en pesos constantes.", c("s2a", 0.4), t_out)
    # sectores 2024 + inversión
    t = c("s2d", 0.2)
    sect = hbars(sc, "s2s", 820, [
        dict(label="Agro", v=V("vab_agro_24"), t=t + 0.6, color=A),
        dict(label="Minas y canteras", v=V("vab_minas_24"), t=t + 0.8, color=A),
        dict(label="Hoteles y restaurantes", v=V("vab_hot_24"), t=t + 1.0, color=A),
        dict(label="Comercio", v=V("vab_com_24"), t=t + 1.2, color=SKY),
        dict(label="Industria manufacturera", v=V("vab_ind_24"), t=t + 1.4, color=SKY),
        dict(label="Construcción", v=V("vab_cons_24"), t=t + 1.6, color=SKY),
    ], -20, 35, sign=True, suffix=" %", labw=300, rowh=62)
    sc.group("pc", 120, 250, 820, 600, panel_head("Valor agregado por sector · 2024", "variación real anual") + '<div style="height:34px"></div>' + sect
             + f'<div class="src" style="margin-top:26px">2.º trim. 2026, interanual: minería +16,4 % · agro +6,9 % · industria −2,1 %</div>', t)
    inv = vbars(sc, "s2f", 700, 470, [
        dict(label="2024", sub="anual", v=V("fbcf_24"), t=c("s2d", 5.4), color=SKY),
        dict(label="2025", sub="anual", v=V("fbcf_25"), t=c("s2d", 5.8), color=A),
        dict(label="2026", sub="2.º trim., interanual", v=V("fbcf_t2_26"), t=c("s2d", 6.2), partial=True, color=SKY),
    ], -20, 20, sign=True, suffix=" %")
    sc.group("pd", 1100, 250, 700, 640, panel_head("Inversión total (FBCF)", "PROXY · incluye inversión pública y privada") + inv, c("s2d", 5.0))
    sc.group("pdn", 1100, 866, 700, 50, '<div class="src" style="color:#EEE8DD">Nivel 2025 ≈ 96,2 (2023 = 100) · cálculo propio encadenando −17,2 % y +16,2 %</div>', c("s2d", 6.6))
    sc.source("b", "Fuente: INDEC — Cuentas nacionales (INDEC Informa mayo 2026; avance 2.º trimestre 2026).", c("s2d", 0.4), top=956)
    return sc


# ---------------------------------------------------------------- 03
def s3():
    sc = scene("s3", 3); c = sc.c; sc.chapter()
    months = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep"]
    m26 = [2.9, 2.9, 3.4, 2.6, 2.1, 1.9, 2.1, 1.7, 1.9]  # INFLACION_MENSUAL, 2026
    items = [dict(label="Dic 23", v=V("ipc_m_dic23"), t=c("s3a", 0.8), color=SKY),
             dict(label="Dic 24", v=V("ipc_m_dic24"), t=c("s3a", 5.2), color=A),
             dict(label="Dic 25", v=V("ipc_m_dic25"), t=c("s3b", 7.5), color=A)]
    items += [dict(label=m, v=v, t=c("s3c", 0.8 + i * 0.18), partial=True, color=A, vcls="lbl") for i, (m, v) in enumerate(zip(months, m26))]
    chart = vbars(sc, "s3m", 1000, 560, items, 0, 27, d=1, suffix="", barw=0.62, bottom=70)
    sc.group("pa", 120, 250, 1000, 640, panel_head("Inflación mensual (IPC nacional)", "% · diciembres de cada año y meses de 2026") + chart, c("s3a", 0.2))
    sc.css.append("#s3 .lbl2{}")
    sc.group("pab", 120, 878, 1000, 40, f'<div class="src"><span style="display:inline-block;width:255px;border-top:1px solid {MU};padding-top:4px">sólo diciembres</span><span style="display:inline-block;width:690px;margin-left:30px;border-top:1px solid {A};padding-top:4px;color:{A}">2026 mes a mes (ene–sep) · parcial</span></div>', c("s3c", 0.6))
    # interanual
    ia = [("Dic 2023", V("ipc_ia_dic23"), c("s3b", 0.4), False), ("Dic 2024", V("ipc_ia_dic24"), c("s3b", 3.2), False),
          ("Dic 2025", V("ipc_ia_dic25"), c("s3b", 7.2), False), ("Sep 2026", V("ipc_ia_sep26"), c("s3d", 0.8), True)]
    rows = ""
    for i, (lab, v, t, part) in enumerate(ia):
        w = v / 211.4 * 300
        st = f"background:repeating-linear-gradient(45deg,{A} 0 5px,{A}33 5px 11px)" if part else f"background:{SKY if i == 0 else A}"
        rows += (f'<div id="s3-r{i}" style="display:flex;align-items:center;height:78px">'
                 f'<div class="src" style="width:120px;color:{C["ink"]}">{lab}</div>'
                 f'<div id="s3-rb{i}" style="height:34px;width:{max(w, 3):.0f}px;{st}"></div>'
                 f'<div class="h1 num" style="font-size:38px;margin-left:16px">{fmt(v)} %</div></div>')
        sc.j(f"G.inn('#s3-r{i}', {t}, 0.4); G.hbar('#s3-rb{i}', {t}, false);")
    sc.group("pb", 1220, 250, 600, 420, panel_head("Inflación interanual", "% · vs mismo mes del año anterior") + '<div style="height:24px"></div>' + rows, c("s3b", 0.0))
    sc.group("pbn", 1220, 690, 580, 110, f'<div class="note">Sep 2026 (33,4 %) supera a dic 2025 (31,5 %): la baja interanual se detuvo.</div>', c("s3d", 2.0))
    sc.group("pbc", 1220, 820, 580, 60, f'<div class="chip part" style="display:inline-block">Acumulado ene–sep 2026: 23,6 %</div>', c("s3c", 6.4))
    sc.source("a", "Fuente: INDEC — IPC, informe sep. 2026. Mensual, interanual y acumulado responden a preguntas distintas.", c("s3a", 0.4), top=956)
    return sc


# ---------------------------------------------------------------- 04
def s4():
    sc = scene("s4", 4); c = sc.c; sc.chapter()
    t_out = c("s4c", -0.3)
    des = line(sc, "s4d", 900, 470, [
        dict(label="T4 2023", sub="", v=V("desoc_t4_23"), t=c("s4a", 1.0)),
        dict(label="T4 2024", sub="", v=V("desoc_t4_24"), t=c("s4a", 2.6)),
        dict(label="T4 2025", sub="", v=V("desoc_t4_25"), t=c("s4a", 4.4)),
        dict(label="T2 2026", sub="otro trimestre", v=V("desoc_t2_26"), t=c("s4a", 8.0)),
    ], 4, 9, color=A, left=70, right=70, dashed_from=3, suffix=" %")
    sc.group("pa", 120, 250, 900, 600, panel_head("Desocupación (EPH, 31 aglomerados)", "% de la población económicamente activa") + des, c("s4a", 0.2), t_out)
    sc.group("pan", 120, 860, 900, 50, '<div class="src">Tasa de empleo: 45,8 % (T4 2023) → 45,0 % (T2 2026). T2 vs T4: posible efecto estacional.</div>', c("s4a", 9.0), t_out)
    inf = vbars(sc, "s4i", 560, 470, [
        dict(label="T1 2024", v=V("inf_t1_24"), t=c("s4b", 0.5), color=SKY),
        dict(label="T1 2026", v=V("inf_t1_26"), t=c("s4b", 1.6), color=A, partial=True),
    ], 0, 50, suffix=" %", barw=0.42)
    sc.group("pb", 1200, 250, 600, 600, panel_head("Informalidad laboral", "% de ocupados · IIEP (UBA-CONICET)") + inf, c("s4b", 0.0), t_out)
    sc.source("a", "Fuentes: INDEC — EPH, mercado de trabajo; IIEP UBA-CONICET — Panorama del empleo informal (jun. 2026).", c("s4a", 0.4), t_out, top=956)
    t = c("s4c", 0.3)
    sal = hbars(sc, "s4s", 1200, [
        dict(label="Privado registrado · jun 2026", v=V("sal_priv"), t=t + 0.8, color=SKY),
        dict(label="Total registrado · jun 2026", v=V("sal_tot"), t=t + 1.4, color=A),
        dict(label="Público registrado · jun 2026", v=V("sal_pub"), t=t + 2.0, color=SKY),
        dict(label="Salario mínimo (SMVM) · sep 2026", v=V("smvm"), t=t + 5.6, color=A),
    ], -45, 0, suffix=" %", labw=440, rowh=96)
    sc.group("pc", 120, 250, 1300, 520, panel_head("Salario real vs. noviembre de 2023", "variación acumulada, deflactada por IPC · CEPA con datos del INDEC") + '<div style="height:40px"></div>' + sal, t)
    sc.group("pcn", 120, 770, 1300, 120, '<div class="note">Base: noviembre de 2023, previa al salto de precios de diciembre (25,5 % mensual). Con otra base, el resultado cambia. Cobertura y metodología: CEPA.</div>', c("s4d", 0.2))
    sc.group("pcc", 1480, 300, 330, 400, f'''<div class="src">Personas con trabajo registrado</div>
<div class="h1 num" style="font-size:66px;margin-top:8px">12,726 M</div><div class="chip" style="display:inline-block;margin-top:10px">julio 2026 · SIPA</div>
<div class="src" style="margin-top:14px">Sin serie 2023–2025 comparable en la base: no se calcula variación.</div>''', t + 3.0)
    sc.source("b", "Fuentes: CEPA, «1.000 días de Milei en 10 indicadores» (sobre INDEC); Secretaría de Trabajo, SIPA.", t + 0.4, top=956)
    return sc


# ---------------------------------------------------------------- 05
def s5():
    sc = scene("s5", 5); c = sc.c; sc.chapter()
    labs = [("2.º sem", "2023"), ("1.er sem", "2024"), ("2.º sem", "2024"), ("1.er sem", "2025"), ("2.º sem", "2025"), ("1.er sem", "2026")]
    pv = [V("pob_2s23"), V("pob_1s24"), V("pob_2s24"), V("pob_1s25"), V("pob_2s25"), V("pob_1s26")]
    iv = [11.9, 18.1, 8.2, 6.9, 6.3, 7.5]  # POBREZA_DESIGUALDAD, indigencia por semestre
    tp = [c("s5a", 0.6), c("s5a", 2.2), c("s5b", 0.4), c("s5b", 1.4), c("s5b", 2.6), c("s5b", 6.0)]
    ti = [c("s5c", 0.3) + i * 0.3 for i in range(6)]
    W, H = 1180, 600
    pov = line(sc, "s5p", W, H, [dict(label=a, sub=b, v=v, t=t) for (a, b), v, t in zip(labs, pv, tp)], 0, 60, color=A, left=60, right=60, suffix=" %")
    ind = line(sc, "s5x", W, H, [dict(label=a, sub=b, v=v, t=t, above=False) for (a, b), v, t in zip(labs, iv, ti)], 0, 60, color=SKY, left=60, right=60,
               labels_below=False, show_x=False, vcls="lbl")
    sc.group("pa", 120, 250, W, 680, panel_head("Pobreza e indigencia (personas)", "% · EPH, 31 aglomerados urbanos · por semestre")
             + f'<div style="position:relative;height:{H}px">'
             + f'<div style="position:absolute;inset:0">{pov}</div><div style="position:absolute;inset:0">{ind}</div></div>', c("s5a", 0.2))
    sc.group("pk", 480, 395, 300, 60, f'<div class="chip part">Pico de la serie · 52,9 %</div>', c("s5a", 3.4))
    sc.group("pil", 1180, 640, 160, 40, f'<div class="src" style="color:{SKY}">indigencia</div>', c("s5c", 0.4))
    side = f'''<div class="src">Pobreza infantil (0–14 años)</div>
<div class="h1 num" style="font-size:40px;margin-top:6px">58,4 → 41,3 → 44,5 %</div>
<div class="src" style="margin-top:4px">2.º sem 2023 · 2.º sem 2025 · 1.er sem 2026</div>
<div class="src" style="margin-top:40px">Coeficiente de Gini (0 a 1)</div>
<div class="h1 num" style="font-size:40px;margin-top:6px">0,435 → 0,427 → 0,428</div>
<div class="src" style="margin-top:4px">T4 2023 · T4 2025 · T2 2026</div>
<div class="note" style="margin-top:40px">1.er sem 2025 → 1.er sem 2026: 31,6 % → 32,3 % (+0,7 p.p.). Comparar semestres iguales.</div>'''
    sc.group("ps", 1400, 280, 420, 620, side, c("s5c", 1.4))
    sc.source("a", "Fuentes: INDEC — Pobreza e indigencia (EPH) y Gini; pobreza infantil: Chequeado sobre INDEC.", c("s5a", 0.4), top=956)
    return sc


# ---------------------------------------------------------------- 06
def s6():
    sc = scene("s6", 6); c = sc.c; sc.chapter()
    # barras apiladas por jurisdicción
    jur = [("Nación", 22.1, 18.1, A), ("Provincias + CABA", 16.1, 14.5, SKY), ("Municipios", 3.4, 3.0, MU)]
    H = 420; k = H / 45
    cols = ""
    for yi, (yr, tot) in enumerate([("2023", V("gpc_23")), ("2024", V("gpc_24"))]):
        segs, acc = "", 0
        for ji, (nm, a, b, col) in enumerate(jur):
            v = a if yi == 0 else b
            segs += (f'<div id="s6-j{yi}{ji}" style="position:absolute;left:0;width:150px;bottom:{acc * k:.1f}px;height:{v * k - 3:.1f}px;background:{col}">'
                     f'<span class="num" style="position:absolute;left:14px;top:8px;font-size:22px;font-weight:600;color:{C["bg"]}">{fmt(v)}</span></div>')
            sc.j(f"G.vbar('#s6-j{yi}{ji}', {c('s6a', 1.0 + yi * 3.2 + ji * 0.3)}, false);")
            acc += v
        cols += (f'<div style="position:absolute;left:{yi * 260}px;bottom:70px;width:150px;height:{H}px">{segs}'
                 f'<div id="s6-t{yi}" class="h1 num" style="position:absolute;left:0;bottom:{acc * k + 12:.0f}px;font-size:44px">{fmt(tot)} %</div></div>'
                 f'<div class="lbl mono" style="position:absolute;left:{yi * 260}px;bottom:24px;width:150px;text-align:center;font-size:22px;color:{MU}">{yr}</div>')
        sc.j(f"G.inn('#s6-t{yi}', {c('s6a', 2.0 + yi * 3.2)});")
    legend = "".join(f'<div style="display:flex;align-items:center;gap:10px;margin-bottom:12px"><i style="width:16px;height:16px;background:{col};display:inline-block"></i><span class="src" style="color:{C["ink"]}">{nm}</span></div>' for nm, a, b, col in jur)
    sc.group("pa", 120, 250, 760, 660, panel_head("Gasto público consolidado", "% del PBI · tres niveles de gobierno, con obras sociales")
             + f'<div style="position:relative;height:560px">{cols}<div style="position:absolute;left:520px;top:200px">{legend}</div></div>', c("s6a", 0.2))
    # composición funcional
    fun = [("Servicios sociales", 69.4, A), ("Funcionamiento del Estado", 16.1, SKY), ("Servicios económicos", 9.2, MU), ("Deuda pública", 5.3, C["coral"])]
    bar, lab, acc = "", "", 0
    for i, (nm, v, col) in enumerate(fun):
        bar += f'<div id="s6-f{i}" style="position:absolute;left:{acc / 100 * 860:.1f}px;top:0;width:{v / 100 * 860 - 3:.1f}px;height:70px;background:{col}"></div>'
        lab += (f'<div id="s6-fl{i}" style="display:flex;justify-content:space-between;border-bottom:1px solid {C["grid"]};padding:9px 0">'
                f'<span class="src" style="color:{C["ink"]}"><i style="width:12px;height:12px;background:{col};display:inline-block;margin-right:10px"></i>{nm}</span>'
                f'<span class="num" style="font-size:24px;font-weight:600">{fmt(v)} %</span></div>')
        sc.j(f"G.hbar('#s6-f{i}', {c('s6b', 0.3 + i * 0.25)}, false); G.inn('#s6-fl{i}', {c('s6b', 0.5 + i * 0.25)}, 0.4);")
        acc += v
    t_out = c("s6d", -0.3)
    sc.group("pb", 940, 250, 860, 460, panel_head("Composición funcional del gasto · 2024", "% del gasto consolidado total")
             + f'<div style="position:relative;height:70px;margin-top:30px">{bar}</div><div style="margin-top:22px">{lab}</div>', c("s6b", 0.0), t_out)
    sc.group("pbn", 940, 760, 860, 120, '<div class="note">La OPC estima 33,0 % del PBI en 2024, con otra cobertura: no se fusiona con el 35,6 %.</div>', c("s6c", 0.3), t_out)
    t = c("s6d", 0.1)
    apn = hbars(sc, "s6x", 860, [
        dict(label="Gasto total devengado", v=V("apn_26"), t=t + 0.6, color=A),
        dict(label="Subsidios a la energía", v=V("apn_energia"), t=t + 2.6, color=SKY),
        dict(label="Subsidios al transporte", v=V("apn_transp"), t=t + 3.0, color=SKY),
        dict(label="Intereses de la deuda", v=V("apn_int"), t=t + 4.4, color=A),
    ], -25, 32, sign=True, suffix=" %", labw=300, rowh=84)
    sc.group("pc", 940, 250, 860, 640, panel_head("Administración Nacional · ene–sep 2026", "variación real interanual · OPC") + '<div style="height:40px"></div>' + apn
             + '<div class="src" style="margin-top:34px">Perímetro distinto: APN ≠ gasto consolidado. 2025–2026 consolidado: sin dato publicado.</div>', t)
    sc.source("a", "Fuentes: Ministerio de Economía — Gasto Público Consolidado 2009–2024; OPC — Ejecución APN, sep. 2026.", c("s6a", 0.4), top=956)
    return sc


# ---------------------------------------------------------------- 07
def s7():
    sc = scene("s7", 7); c = sc.c; sc.chapter()
    xs = [("2023", "anual", V("x_23"), 20643, 30.9), ("2024", "anual", V("x_24"), 22062, 27.7),
          ("2025", "anual", V("x_25"), 23380, 26.8), ("2026", "ene–sep", V("x_26"), 20415, 26.4)]
    H, W = 400, 820; k = H / 95000
    cols = ""
    for i, (y, sub, tot, moi, sh) in enumerate(xs):
        part = i == 3
        st = f"background:repeating-linear-gradient(45deg,{A} 0 5px,{A}33 5px 11px)" if part else f"background:{A}"
        x = 40 + i * 195
        cols += (f'<div id="s7-b{i}" style="position:absolute;left:{x}px;bottom:80px;width:120px;height:{tot * k:.1f}px;{st}"></div>'
                 f'<div id="s7-m{i}" style="position:absolute;left:{x}px;bottom:80px;width:120px;height:{moi * k:.1f}px;background:{SKY}"></div>'
                 f'<div id="s7-v{i}" class="num" style="position:absolute;left:{x - 30}px;width:180px;text-align:center;bottom:{tot * k + 92:.0f}px;font-size:28px;font-weight:700">{fmt(tot, 0)}</div>'
                 f'<div id="s7-s{i}" class="num mono" style="position:absolute;left:{x - 30}px;width:180px;text-align:center;bottom:{80 + moi * k / 2 - 12:.0f}px;font-size:19px;font-weight:700;color:{C["bg"]}">MOI {fmt(sh)} %</div>'
                 f'<div class="mono" style="position:absolute;left:{x - 30}px;width:180px;text-align:center;bottom:30px;font-size:21px;color:{MU}">{y}<br><span style="font-size:15px;color:{C["dim"]}">{sub}</span></div>')
        ta = c("s7a", 1.0 + i * 1.4) if i < 3 else c("s7a", 8.4)
        sc.j(f"G.vbar('#s7-b{i}', {ta}, false); G.inn('#s7-v{i}', {ta + 0.5}, 0.4); G.vbar('#s7-m{i}', {c('s7b', 0.2 + i * 0.25)}, false); G.inn('#s7-s{i}', {c('s7b', 0.6 + i * 0.25)}, 0.4);")
    sc.group("pa", 120, 250, W, 660, panel_head("Exportaciones de bienes", "millones USD FOB · celeste: manufacturas industriales (MOI)")
             + f'<div style="position:relative;height:580px">{cols}</div>', c("s7a", 0.2))
    sc.group("pan", 760, 412, 230, 60, '<div class="chip part">2026 = 9 MESES</div>', c("s7a", 9.2))
    t_out = c("s7d", -0.3)
    ipi = vbars(sc, "s7i", 820, 470, [
        dict(label="2023", sub="anual", v=V("ipi_23"), t=c("s7c", 0.5), color=MU),
        dict(label="2024", sub="anual", v=V("ipi_24"), t=c("s7c", 1.2), color=SKY),
        dict(label="2025", sub="anual", v=V("ipi_25"), t=c("s7c", 4.0), color=A),
        dict(label="2026", sub="ene–ago, interanual", v=V("ipi_26"), t=c("s7c", 7.0), color=SKY, partial=True),
    ], -11, 4, sign=True, suffix=" %")
    sc.group("pb", 1000, 250, 820, 640, panel_head("Producción industrial (IPI manufacturero)", "variación %") + ipi, c("s7c", 0.0), t_out)
    t = c("s7d", 0.0)
    div = hbars(sc, "s7d", 820, [
        dict(label="Otro equipo de transporte", v=114.0, t=t + 4.2, color=A),
        dict(label="Refinación de petróleo", v=104.2, t=t + 4.4, color=A),
        dict(label="Alimentos y bebidas", v=101.3, t=t + 4.6, color=A),
        dict(label="Caucho y plástico", v=79.0, t=t + 1.6, color=SKY),
        dict(label="Minerales no metálicos", v=78.1, t=t + 1.8, color=SKY),
        dict(label="Productos de metal", v=78.0, t=t + 1.0, color=SKY),
        dict(label="Productos textiles", v=76.4, t=t + 0.8, color=SKY),
    ], 70, 118, base=100.0, labw=300, rowh=56)
    sc.group("pc", 1000, 250, 820, 600, panel_head("Nivel 2025 por división · 2023 = 100", "índices construidos en la base encadenando tasas INDEC") + '<div style="height:30px"></div>' + div, t)
    sc.group("pcu", 1000, 836, 820, 60, '<div class="chip part" style="display:inline-block">Capacidad instalada utilizada: 59,6 % (ago 2025) → 58,5 % (ago 2026)</div>', c("s7d", 7.6))
    sc.source("a", "Fuentes: INDEC — Intercambio comercial argentino (sep. 2026, con revisiones); IPI manufacturero; capacidad instalada.", c("s7a", 0.4), top=956)
    return sc


# ---------------------------------------------------------------- 08
def s8():
    sc = scene("s8", 8); c = sc.c; sc.chapter()
    nd = lambda items: "".join(f'<div style="display:flex;justify-content:space-between;border-bottom:1px solid {C["grid"]};padding:7px 0"><span class="src">{x}</span><span class="mono" style="font-size:15px;color:{C["dim"]};border:1px solid {C["dim"]};padding:1px 6px">N/D</span></div>' for x in items)
    colw = 520
    heads = [("Educación", ND["educacion"]), ("Salud", ND["salud"]), ("Seguridad", None)]
    for i, (h, items) in enumerate(heads):
        x = 120 + i * 580
        inner = f'<div class="ptitle">{h}</div>'
        if items:
            inner += f'<div class="psub">sin serie homogénea verificada</div><div style="margin-top:14px">{nd(items)}</div>'
        sc.group(f"c{i}", x, 250, colw, 300, inner, c("s8a", 0.4 + i * 0.3))
    # educación
    sc.group("ed", 120, 520, colw, 380, f'''<div class="src">Aprender 6.º grado · satisfactorio + avanzado</div>
<div style="display:flex;gap:40px;margin-top:14px">
<div><div class="body" style="font-size:22px">Lengua</div><div class="h1 num" style="font-size:52px">66,4 → <span style="color:{A}">76,9</span> %</div></div></div>
<div style="margin-top:14px"><div class="body" style="font-size:22px">Matemática</div><div class="h1 num" style="font-size:52px">51,5 → <span style="color:{A}">55,0</span> %</div></div>
<div class="chip" style="display:inline-block;margin-top:14px">2023 → 2025</div>
<div class="src" style="margin-top:14px">Resultados de prueba: no equivalen a tasa de alfabetización.</div>''', c("s8b", 0.4))
    sc.group("sa", 700, 520, colw, 380, f'''<div class="src">Mortalidad infantil · por 1.000 nacidos vivos</div>
<div class="h1 num" style="font-size:52px;margin-top:6px">8,0 → <span style="color:{SKY}">8,5</span></div>
<div class="src" style="margin-top:20px">Mortalidad materna · por 10.000 nacidos vivos</div>
<div class="h1 num" style="font-size:52px;margin-top:6px">3,2 → <span style="color:{SKY}">4,4</span></div>
<div class="chip" style="display:inline-block;margin-top:14px">2023 → 2024 · último dato</div>
<div class="src" style="margin-top:14px">Hogares sólo con sistema público: 17,4 % (2.º sem 2025).</div>''', c("s8b", 4.4))
    sc.group("se", 1280, 330, colw, 580, f'''<div class="src">Homicidios dolosos · cada 100.000 hab.</div>
<div class="h1 num" style="font-size:52px;margin-top:6px">4,4 · 3,8 · <span style="color:{A}">3,6</span></div>
<div class="chip" style="display:inline-block;margin-top:10px">2023 · 2024 · 2025</div>
<div class="src" style="margin-top:26px">Víctimas directas de femicidio (CSJN)</div>
<div class="h1 num" style="font-size:52px;margin-top:6px">250 · 228 · <span style="color:{A}">200</span></div>
<div class="chip" style="display:inline-block;margin-top:10px">2023 · 2024 · 2025</div>
<div class="src" style="margin-top:26px">Robos denunciados: −21,6 % en 2025 vs 2024. Los registros dependen de denuncia y clasificación.</div>''', c("s8c", 0.4))
    sc.source("a", "Fuentes: Argentinos por la Educación (Aprender); Min. de Salud — DEIS; INDEC — EPH; Min. de Seguridad — SNIC; CSJN.", c("s8a", 0.4), top=956)
    return sc


# ---------------------------------------------------------------- 09
def s9():
    sc = scene("s9", 9); c = sc.c; sc.chapter()
    rows = [
        ("Inflación mensual", "25,5 %", "dic 23", "1,9 %", "sep 26", "s9a", 0.4),
        ("Inflación interanual", "211,4 %", "dic 23", "33,4 %", "sep 26", "s9a", 0.7),
        ("Pobreza (personas)", "41,7 %", "2S 23", "32,3 %", "1S 26 · pico 52,9 %", "s9a", 1.6),
        ("PBI real (2023 = 100)", "100", "2023", "103,1", "2025 · 1S 26 +2,2 %", "s9a", 3.4),
        ("Gasto consolidado", "41,6 % PBI", "2023", "35,6 % PBI", "2024", "s9a", 4.6),
        ("Exportaciones", "66.789 M USD", "2023", "87.111 M USD", "2025", "s9a", 5.2),
        ("Desocupación", "5,7 %", "T4 23", "7,9 %", "T2 26", "s9b", 0.6),
        ("Informalidad", "40,8 %", "T1 24", "44,2 %", "T1 26", "s9b", 1.6),
        ("Salario registrado real", "base", "nov 23", "−8,2 %", "jun 26", "s9b", 2.8),
        ("Industria (IPI)", "−9,4 %", "2024", "−2,7 %", "ene–ago 26", "s9b", 4.4),
        ("Inversión (FBCF)", "−17,2 %", "2024", "−11,1 %", "T2 26 i.a.", "s9b", 5.0),
    ]
    html = (f'<div style="display:grid;grid-template-columns:330px 250px 340px;gap:0;border-bottom:1px solid {C["grid"]};padding-bottom:8px">'
            f'<span class="src">Indicador</span><span class="src">Inicio</span><span class="src">Último dato disponible</span></div>')
    for i, (ind, a, pa, b, pb, k, off) in enumerate(rows):
        html += (f'<div id="s9-r{i}" style="display:grid;grid-template-columns:330px 250px 340px;align-items:baseline;border-bottom:1px solid {C["grid"]};padding:9px 0">'
                 f'<span style="font-size:23px">{ind}</span>'
                 f'<span class="num" style="font-size:24px">{a} <span class="mono" style="font-size:16px;color:{C["dim"]}">{pa}</span></span>'
                 f'<span class="num" style="font-size:24px;font-weight:700;color:{A}">{b} <span class="mono" style="font-size:16px;color:{MU};font-weight:400">{pb}</span></span></div>')
        sc.j(f"G.inn('#s9-r{i}', {c(k, off)}, 0.45);")
    sc.group("tab", 120, 236, 940, 700, html, c("s9a", 0.0))
    ch = [("Sostener la desinflación", "la interanual de sep 26 (33,4 %) superó a la de dic 25 (31,5 %)"),
          ("Recuperar el empleo formal", "informalidad 44,2 % · desocupación 7,9 %"),
          ("Recuperar industria e inversión", "IPI y FBCF por debajo de 2023"),
          ("Completar estadísticas", "N/D: reservas netas, PBI por habitante, inversión pública, educación y salud reales")]
    side = '<div class="kicker">Desafíos pendientes</div>'
    for i, (a, b) in enumerate(ch):
        side += f'<div id="s9-c{i}" style="margin-top:24px;border-left:3px solid {A};padding-left:18px"><div style="font-size:27px;font-weight:600">{a}</div><div class="src" style="margin-top:4px">{b}</div></div>'
        sc.j(f"G.up('#s9-c{i}', {c('s9c', 0.4 + i * 1.3)});")
    sc.group("side", 1160, 250, 640, 640, side, c("s9c", 0.2))
    sc.j(f"G.dim('#s9-tab', {c('s9c', 0.0)}, 0.35); G.out('#s9-tab, #s9-side, #s9-src-a', {c('s9d', 0.2)}, 0.4);")
    sc.group("end", 120, 0, 1680, 1080, f'''<div style="position:absolute;inset:0;background:{C["bg"]}"></div>
<div class="h1" style="position:absolute;left:0;right:0;top:420px;text-align:center;font-size:62px;line-height:1.25">2026 sigue abierto.<br><span style="color:{A}">El balance dependerá de los próximos datos oficiales.</span></div>''', c("s9d", 0.6))
    sc.source("a", "Inicio y último dato con períodos distintos: leer cada fila con su período. Fuentes en cada capítulo y en los créditos.", c("s9a", 0.4), top=956)
    return sc


# ---------------------------------------------------------------- créditos
def outro(dur):
    srcs = ["INDEC — Cuentas nacionales, IPC, EPH, IPI, comercio exterior, capacidad instalada",
            "Ministerio de Economía — Gasto Público Consolidado 2009–2024 · recaudación ARCA",
            "Oficina de Presupuesto del Congreso (OPC)", "BCRA · Secretaría de Energía · Secretaría de Trabajo (SIPA)",
            "IIEP UBA-CONICET · CEPA (sobre INDEC) · Chequeado (sobre INDEC)",
            "Ministerio de Salud — DEIS · Ministerio de Seguridad — SNIC · CSJN — Oficina de la Mujer",
            "Argentinos por la Educación (pruebas Aprender)"]
    lis = "".join(f'<div id="o-l{i}" class="body" style="font-size:25px;margin-top:10px">{s}</div>' for i, s in enumerate(srcs))
    js = "\n".join(f"G.inn('#o-l{i}', {0.5 + i * 0.18}, 0.5);" for i in range(len(srcs)))
    return f'''<template>
<style>{COMMON_CSS}</style>
<div id="root" data-composition-id="outro" data-width="1920" data-height="1080">
<div id="o-stage" class="stage clip" data-start="0" data-duration="{dur}" data-track-index="1">
<div id="o-fade" class="stage">
<div class="abs" style="left:160px;top:140px;width:1600px">
<div id="o-k" class="kicker">Fuentes de los datos</div>
<div style="margin-top:28px">{lis}</div>
<div id="o-n" class="src" style="margin-top:56px;font-size:19px;color:{C["ink"]}">Base: «Presidencia de Javier Milei · Observatorio 2023–2026», 51 indicadores, 59 fuentes. Corte: 23 de octubre de 2026.<br>N/D indica ausencia de cifra verificable, nunca cero. Las cifras de 2026 son parciales. Los datos no establecen causalidad.</div>
<div id="o-c" class="src" style="margin-top:40px">Animación y composición: HyperFrames (HeyGen) · GSAP · Narración: voz sintética (Kokoro) · Música: original</div>
</div></div></div></div>
<script>
(() => {{
{PRELUDE}
tl.fromTo('#o-fade', {{ opacity: 0 }}, {{ opacity: 1, duration: 0.6 }}, 0);
G.inn('#o-k', 0.2);
{js}
G.inn('#o-n', 2.2, 0.8); G.inn('#o-c', 3.0, 0.8);
tl.to('#o-fade', {{ opacity: 0, duration: 1.2, ease: 'power2.in' }}, {dur - 1.4});
window.__timelines["outro"] = tl;
}})();
</script>
</template>
'''


def index():
    hosts, audio = [], []
    for i, s in enumerate(T["scenes"]):
        hosts.append(f'''      <div id="{s["id"]}" data-composition-id="{s["id"]}" data-composition-src="compositions/{s["id"]}.html" data-start="{s["start"]}" data-duration="{s["duration"]}" data-track-index="1" data-track-kind="graphics" data-width="1920" data-height="1080"></div>''')
        audio.append(f'''      <audio id="vo-{s["id"]}" class="clip" src="assets/audio/vo_{s["id"]}.mp3" data-start="{round(s["start"] + s["voStart"], 2)}" data-duration="{s["voMedia"]}" data-track-index="3" data-volume="1"></audio>''')
    o = T["outro"]
    hosts.append(f'''      <div id="outro" data-composition-id="outro" data-composition-src="compositions/outro.html" data-start="{o["start"]}" data-duration="{o["duration"]}" data-track-index="1" data-track-kind="graphics" data-width="1920" data-height="1080"></div>''')
    total = T["total"]
    return f'''<!doctype html>
<html lang="es" data-resolution="landscape">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <title>Argentina 2023–2026 · documental de datos</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1920px; height: 1080px; overflow: hidden; background: {C["bg"]}; }}
      #root {{ position: relative; width: 100%; height: 100%; background: {C["bg"]}; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{total}" data-width="1920" data-height="1080">
{chr(10).join(hosts)}
{chr(10).join(audio)}
      <audio id="bgm" class="clip" src="assets/audio/bgm.mp3" data-start="0" data-duration="{total}" data-track-index="4" data-volume="1"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
'''


if __name__ == "__main__":
    os.makedirs(os.path.join(ROOT, "compositions"), exist_ok=True)
    for fn in (s1, s2, s3, s4, s5, s6, s7, s8, s9):
        sc = fn()
        open(os.path.join(ROOT, "compositions", sc.sid + ".html"), "w").write(sc.render())
    open(os.path.join(ROOT, "compositions", "outro.html"), "w").write(outro(T["outro"]["duration"]))
    open(os.path.join(ROOT, "index.html"), "w").write(index())
    print("ok", T["total"])
