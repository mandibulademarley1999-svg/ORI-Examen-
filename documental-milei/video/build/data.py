"""Módulo único de datos del documental.

Cada cifra proviene del Excel «milei_2023_2026_indicadores_y_fuentes.xlsx»
(hojas MATRIZ_2023_26, BASE_OBSERVACIONES y hojas temáticas). Cada entrada
lleva el período exacto, la hoja de origen y la fuente original. Las únicas
cifras derivadas están marcadas con calc=True y explican su cálculo.
"""

URL = {
    "pib": "https://www.indec.gob.ar/uploads/informesdeprensa/pib_09_26065D6A3612.pdf",
    "indec_informa": "https://www.indec.gob.ar/ftp/cuadros/publicaciones/indecinforma/indec_informa_05_26.pdf",
    "ipc": "https://www.indec.gob.ar/uploads/informesdeprensa/ipc_10_268C45A9444C.pdf",
    "ipc_serie": "https://www.indec.gob.ar/Nivel4/Tema/3/5/31",
    "eph": "https://www.indec.gob.ar/Nivel4/Tema/4/31/58",
    "iiep": "https://economicas.uba.ar/iiep/panorama-del-empleo-informal-y-la-pobreza-laboral-jun-2026/",
    "cepa": "https://centrocepa.com.ar/documentos/informes/846-1-000-dias-de-milei-en-10-indicadores-economicos",
    "sipa": "https://www.argentina.gob.ar/trabajo/estadisticas",
    "pobreza": "https://www.indec.gob.ar/indec/web/Nivel3-Tema-4-46",
    "chequeado": "https://chequeado.com/el-explicador/la-pobreza-aumento-al-323-en-el-primer-semestre-de-2026-y-alcanza-a-15-millones-de-personas-en-todo-el-pais/comment-page-1/",
    "gini": "https://www.indec.gob.ar/indec/web/Institucional-Indec-InformesTecnicos-37",
    "gpc": "https://www.argentina.gob.ar/economia/politicaeconomica/informe-gasto-publico-consolidado-2009-2024",
    "opc_gpc": "https://opc.gob.ar/estudios-especificos-presupuestarios/gasto-publico-consolidado-del-sector-publico-argentino-2004-2024/",
    "opc_apn": "https://opc.gob.ar/ejecucion-presupuestaria/analisis-de-la-ejecucion-presupuestaria-de-la-administracion-nacional-septiembre-2026/",
    "ica23": "https://www.indec.gob.ar/ftp/cuadros/publicaciones/anuario_estadistico_2023.pdf",
    "ica_ene25": "https://www.indec.gob.ar/uploads/informesdeprensa/ica_01_25A3C543FBCD.pdf",
    "ica_ene26": "https://www.indec.gob.ar/uploads/informesdeprensa/ica_01_26ABE4F7373E.pdf",
    "ica_sep26": "https://www.indec.gob.ar/uploads/informesdeprensa/ica_10_263F42E3F39F.pdf",
    "ipi23": "https://www.indec.gob.ar/uploads/informesdeprensa/ipi_manufacturero_02_24D4A435BCF1.pdf",
    "ipi24": "https://www.indec.gob.ar/uploads/informesdeprensa/ipi_manufacturero_02_25835136BE5C.pdf",
    "ipi25": "https://www.indec.gob.ar/uploads/informesdeprensa/ipi_manufacturero_02_267A18BBDBFC.pdf",
    "ipi26": "https://www.indec.gob.ar/indec/web/Institucional-Indec-InformesTecnicos-37",
    "ucii": "https://www.indec.gob.ar/Nivel4/Tema/3/6/15",
    "aprender": "https://argentinosporlaeducacion.org/informe/aprender-2025-resultados-de-6-grado-para-la-primaria-argentina/",
    "deis": "https://www.argentina.gob.ar/salud/deis/datos",
    "snic23_24": "https://www.argentina.gob.ar/node/179659",
    "snic25": "https://www.argentina.gob.ar/noticias/monteoliva-presento-las-estadisticas-criminales-2025-argentina-registro-la-menor-tasa-de",
    "csjn23": "https://w1.csjn.gov.ar/novedades/detalle/8323",
    "csjn24": "https://w1.csjn.gov.ar/novedades/detalle/10065",
    "csjn25": "https://w2.csjn.gov.ar/novedades/detalle/13522",
}

# (clave, indicador, valor, unidad, período exacto, hoja Excel, organismo, url, calc, nota)
def D(key, ind, val, unit, period, sheet, org, url, calc=False, note=""):
    return dict(key=key, ind=ind, val=val, unit=unit, period=period, sheet=sheet, org=org, url=URL[url], calc=calc, note=note)

FIGS = [
    # 1 · Línea de base
    D("ipc_m_dic23", "Inflación mensual (IPC nacional)", 25.5, "%", "diciembre 2023", "INFLACION_MENSUAL", "INDEC", "ipc"),
    D("ipc_ia_dic23", "Inflación interanual (IPC nacional)", 211.4, "%", "diciembre 2023 vs diciembre 2022", "INFLACION_MENSUAL", "INDEC", "ipc"),
    D("pob_2s23", "Pobreza (personas, 31 aglomerados)", 41.7, "%", "2.º semestre 2023", "POBREZA_DESIGUALDAD", "INDEC", "pobreza"),
    D("desoc_t4_23", "Desocupación (EPH)", 5.7, "% PEA", "4.º trimestre 2023", "EMPLEO_INGRESOS", "INDEC", "eph"),
    # 2 · PBI
    D("pib_24", "Variación real del PBI", -1.3, "%", "2024 anual", "MATRIZ_2023_26 (3)", "INDEC", "pib"),
    D("pib_25", "Variación real del PBI", 4.5, "%", "2025 anual", "MATRIZ_2023_26 (3)", "INDEC", "pib"),
    D("pib_1s26", "Variación real del PBI", 2.2, "%", "1.er semestre 2026, interanual", "MATRIZ_2023_26 (3)", "INDEC", "pib", note="Parcial: no es variación anual."),
    D("pib_idx_24", "PBI real, índice 2023=100", 98.7, "índice", "2024 anual", "MATRIZ_2023_26 (1)", "INDEC", "pib", note="Normalización ilustrativa encadenando −1,3 %; no es el PBI en pesos."),
    D("pib_idx_25", "PBI real, índice 2023=100", 103.1, "índice", "2025 anual", "MATRIZ_2023_26 (1)", "INDEC", "pib", note="Excel: 103,1415, encadenado con +4,5 %."),
    D("vab_agro_24", "VAB agro (agricultura, ganadería, caza y silvicultura)", 32.3, "% real", "2024 anual", "BASE_OBSERVACIONES (1)", "INDEC", "indec_informa"),
    D("vab_minas_24", "VAB minas y canteras", 7.4, "% real", "2024 anual", "BASE_OBSERVACIONES (1)", "INDEC", "indec_informa"),
    D("vab_hot_24", "VAB hoteles y restaurantes", 5.3, "% real", "2024 anual", "BASE_OBSERVACIONES (1)", "INDEC", "indec_informa"),
    D("vab_com_24", "VAB comercio", -7.2, "% real", "2024 anual", "BASE_OBSERVACIONES (1)", "INDEC", "indec_informa"),
    D("vab_ind_24", "VAB industria manufacturera", -8.8, "% real", "2024 anual", "BASE_OBSERVACIONES (1)", "INDEC", "indec_informa"),
    D("vab_cons_24", "VAB construcción", -17.5, "% real", "2024 anual", "BASE_OBSERVACIONES (1)", "INDEC", "indec_informa"),
    D("vab_minas_t2_26", "VAB minas y canteras", 16.4, "% real", "2.º trimestre 2026, interanual", "PBI_POR_ACTIVIDAD", "INDEC", "pib"),
    D("vab_agro_t2_26", "VAB agro", 6.9, "% real", "2.º trimestre 2026, interanual", "PBI_POR_ACTIVIDAD", "INDEC", "pib"),
    D("vab_ind_t2_26", "VAB industria manufacturera", -2.1, "% real", "2.º trimestre 2026, interanual", "PBI_POR_ACTIVIDAD", "INDEC", "pib"),
    D("fbcf_24", "Formación bruta de capital fijo (total)", -17.2, "% real", "2024 anual", "MATRIZ_2023_26 (10)", "INDEC", "pib", note="PROXY de inversión privada: incluye inversión pública."),
    D("fbcf_25", "Formación bruta de capital fijo (total)", 16.2, "% real", "2025 anual", "MATRIZ_2023_26 (10)", "INDEC", "pib"),
    D("fbcf_t2_26", "Formación bruta de capital fijo (total)", -11.1, "% real", "2.º trimestre 2026, interanual", "MATRIZ_2023_26 (10)", "INDEC", "pib"),
    D("fbcf_idx_25", "FBCF, índice 2023=100", 96.2, "índice", "2025 anual", "cálculo propio", "INDEC", "pib", calc=True, note="100 × (1 − 0,172) × (1 + 0,162) = 96,2."),
    # 3 · Inflación
    D("ipc_m_dic24", "Inflación mensual", 2.7, "%", "diciembre 2024", "INFLACION_MENSUAL", "INDEC", "ipc"),
    D("ipc_m_dic25", "Inflación mensual", 2.8, "%", "diciembre 2025", "INFLACION_MENSUAL", "INDEC", "ipc"),
    D("ipc_m_2026", "Inflación mensual 2026 (ene a sep)", "2,9 · 2,9 · 3,4 · 2,6 · 2,1 · 1,9 · 2,1 · 1,7 · 1,9", "%", "enero a septiembre 2026", "INFLACION_MENSUAL", "INDEC", "ipc_serie"),
    D("ipc_ia_dic24", "Inflación interanual", 117.8, "%", "diciembre 2024", "INFLACION_MENSUAL", "INDEC", "ipc"),
    D("ipc_ia_dic25", "Inflación interanual", 31.5, "%", "diciembre 2025", "INFLACION_MENSUAL", "INDEC", "ipc"),
    D("ipc_ia_sep26", "Inflación interanual", 33.4, "%", "septiembre 2026 vs septiembre 2025", "INFLACION_MENSUAL", "INDEC", "ipc"),
    D("ipc_acum_sep26", "Inflación acumulada 2026", 23.6, "%", "enero a septiembre 2026", "INFLACION_MENSUAL", "INDEC", "ipc", note="Parcial: no es año cerrado."),
    # 4 · Trabajo
    D("desoc_t4_24", "Desocupación", 6.4, "% PEA", "4.º trimestre 2024", "EMPLEO_INGRESOS", "INDEC", "eph"),
    D("desoc_t4_25", "Desocupación", 7.5, "% PEA", "4.º trimestre 2025", "EMPLEO_INGRESOS", "INDEC", "eph"),
    D("desoc_t2_26", "Desocupación", 7.9, "% PEA", "2.º trimestre 2026", "EMPLEO_INGRESOS", "INDEC", "eph", note="Trimestre distinto de T4: puede haber estacionalidad."),
    D("empleo_t4_23", "Tasa de empleo", 45.8, "% población", "4.º trimestre 2023", "EMPLEO_INGRESOS", "INDEC", "eph"),
    D("empleo_t2_26", "Tasa de empleo", 45.0, "% población", "2.º trimestre 2026", "EMPLEO_INGRESOS", "INDEC", "eph"),
    D("inf_t1_24", "Informalidad laboral", 40.8, "% ocupados", "1.er trimestre 2024", "EMPLEO_INGRESOS", "IIEP UBA-CONICET", "iiep"),
    D("inf_t1_26", "Informalidad laboral", 44.2, "% ocupados", "1.er trimestre 2026", "EMPLEO_INGRESOS", "IIEP UBA-CONICET", "iiep"),
    D("sal_priv", "Salario privado registrado real", -3.5, "% acum.", "junio 2026 vs noviembre 2023", "BASE_OBSERVACIONES (21)", "CEPA sobre INDEC", "cepa", note="PROXY / cobertura distinta."),
    D("sal_tot", "Salario registrado real (total)", -8.2, "% acum.", "junio 2026 vs noviembre 2023", "MATRIZ_2023_26 (21)", "CEPA sobre INDEC", "cepa"),
    D("sal_pub", "Salario público registrado real", -16.5, "% acum.", "junio 2026 vs noviembre 2023", "BASE_OBSERVACIONES (21)", "CEPA sobre INDEC", "cepa"),
    D("smvm", "Salario mínimo, vital y móvil real", -40.8, "% acum.", "septiembre 2026 vs noviembre 2023", "MATRIZ_2023_26 (22)", "CEPA sobre INDEC", "cepa"),
    D("sipa_jul26", "Personas con trabajo registrado", 12.726, "millones", "julio 2026", "EMPLEO_INGRESOS", "Secretaría de Trabajo", "sipa", note="Sin serie 2023–25 comparable en el Excel."),
    # 5 · Pobreza
    D("pob_1s24", "Pobreza", 52.9, "% personas", "1.er semestre 2024", "POBREZA_DESIGUALDAD", "INDEC", "pobreza"),
    D("pob_2s24", "Pobreza", 38.1, "% personas", "2.º semestre 2024", "POBREZA_DESIGUALDAD", "INDEC", "pobreza"),
    D("pob_1s25", "Pobreza", 31.6, "% personas", "1.er semestre 2025", "POBREZA_DESIGUALDAD", "INDEC", "pobreza"),
    D("pob_2s25", "Pobreza", 28.2, "% personas", "2.º semestre 2025", "POBREZA_DESIGUALDAD", "INDEC", "pobreza"),
    D("pob_1s26", "Pobreza", 32.3, "% personas", "1.er semestre 2026", "POBREZA_DESIGUALDAD", "INDEC", "pobreza"),
    D("ind_serie", "Indigencia 2S23 · 1S24 · 2S24 · 1S25 · 2S25 · 1S26", "11,9 · 18,1 · 8,2 · 6,9 · 6,3 · 7,5", "% personas", "2.º sem. 2023 a 1.er sem. 2026", "POBREZA_DESIGUALDAD", "INDEC", "pobreza"),
    D("pob_inf", "Pobreza infantil (0–14 años) 2S23 · 2S25 · 1S26", "58,4 · 41,3 · 44,5", "% personas 0–14", "2.º sem. 2023 / 2.º sem. 2025 / 1.er sem. 2026", "POBREZA_DESIGUALDAD", "Chequeado sobre INDEC", "chequeado", note="Sin dato 2024 en el Excel."),
    D("gini", "Coeficiente de Gini (ingreso per cápita familiar)", "0,435 · 0,427 · 0,428", "índice 0–1", "T4 2023 / T4 2025 / T2 2026", "POBREZA_DESIGUALDAD", "INDEC", "gini"),
    # 6 · Gasto
    D("gpc_23", "Gasto público consolidado (Nación + provincias + municipios, con obras sociales)", 41.6, "% PBI", "2023 anual", "GASTO_FUNCIONAL", "Ministerio de Economía", "gpc"),
    D("gpc_24", "Gasto público consolidado", 35.6, "% PBI", "2024 anual", "GASTO_FUNCIONAL", "Ministerio de Economía", "gpc"),
    D("gpc_jur", "Por jurisdicción 2023 → 2024: Nación · Provincias+CABA · Municipios", "22,1 → 18,1 · 16,1 → 14,5 · 3,4 → 3,0", "% PBI", "2023 y 2024 anual", "GASTO_FUNCIONAL", "Ministerio de Economía", "gpc"),
    D("gpc_fun", "Composición funcional 2024: sociales · funcionamiento · económicos · deuda", "69,4 · 16,1 · 9,2 · 5,3", "% del gasto", "2024 anual", "GASTO_FUNCIONAL", "Ministerio de Economía", "gpc"),
    D("opc_24", "Gasto consolidado según OPC (otra cobertura)", 33.0, "% PBI", "2024 anual", "GASTO_FUNCIONAL / METODOLOGIA", "OPC", "opc_gpc", note="No se fusiona con la serie del Ministerio de Economía."),
    D("apn_26", "Gasto devengado Administración Nacional, var. real", -0.3, "% i.a.", "enero a septiembre 2026", "FINANZAS_FISCALES", "OPC", "opc_apn", note="APN ≠ gasto consolidado."),
    D("apn_energia", "Subsidios a la energía (APN), var. real", -21.3, "% i.a.", "enero a septiembre 2026", "FINANZAS_FISCALES", "OPC", "opc_apn"),
    D("apn_transp", "Subsidios al transporte (APN), var. real", -18.8, "% i.a.", "enero a septiembre 2026", "FINANZAS_FISCALES", "OPC", "opc_apn"),
    D("apn_int", "Intereses de deuda (APN), var. real", 28.2, "% i.a.", "enero a septiembre 2026", "FINANZAS_FISCALES", "OPC", "opc_apn"),
    # 7 · Exportaciones e industria
    D("x_23", "Exportaciones de bienes FOB", 66789, "M USD", "2023 anual", "COMERCIO_EXTERIOR", "INDEC", "ica23"),
    D("x_24", "Exportaciones de bienes FOB", 79703, "M USD", "2024 anual (revisión 2025)", "COMERCIO_EXTERIOR", "INDEC", "ica_ene26"),
    D("x_25", "Exportaciones de bienes FOB", 87111, "M USD", "2025 anual (revisión sep. 2026)", "COMERCIO_EXTERIOR", "INDEC", "ica_sep26", note="Informe de enero 2026: 87.077; revisión de septiembre: 87.111."),
    D("x_26", "Exportaciones de bienes FOB", 77267, "M USD", "enero a septiembre 2026", "COMERCIO_EXTERIOR", "INDEC", "ica_sep26", note="Nueve meses: no comparable con años completos."),
    D("moi", "Exportaciones MOI 2023 · 2024 · 2025 · ene–sep 2026", "20.643 · 22.062 · 23.380 · 20.415", "M USD", "anual / ene–sep 2026", "COMERCIO_EXTERIOR", "INDEC", "ica_sep26"),
    D("moi_share", "Participación MOI en exportaciones", "30,9 · 27,7 · 26,8 · 26,4", "% del total", "2023 / 2024 / 2025 / ene–sep 2026", "COMERCIO_EXTERIOR", "INDEC", "ica_sep26", calc=True, note="Calculado en el Excel: MOI / total."),
    D("ipi_23", "IPI manufacturero", -1.8, "% anual", "2023 anual", "MATRIZ_2023_26 (4)", "INDEC", "ipi23"),
    D("ipi_24", "IPI manufacturero", -9.4, "% anual", "2024 anual", "MATRIZ_2023_26 (4)", "INDEC", "ipi24"),
    D("ipi_25", "IPI manufacturero", 1.6, "% anual", "2025 anual", "MATRIZ_2023_26 (4)", "INDEC", "ipi25"),
    D("ipi_26", "IPI manufacturero", -2.7, "% acum.", "enero a agosto 2026 vs enero a agosto 2025", "MATRIZ_2023_26 (4)", "INDEC", "ipi26"),
    D("ipi_div", "Nivel 2025 por división (2023=100): otro eq. transporte · refinación · alimentos · caucho · min. no metálicos · prod. de metal · textiles", "114,0 · 104,2 · 101,3 · 79,0 · 78,1 · 78,0 · 76,4", "índice", "2025 anual", "INDUSTRIA_16", "INDEC", "ipi25", calc=True, note="Índices construidos en el Excel encadenando tasas 2024 y 2025."),
    D("ucii", "Utilización de la capacidad instalada", "59,6 → 58,5", "%", "agosto 2025 → agosto 2026", "CAPACIDAD_INDUSTRIAL", "INDEC", "ucii"),
    # 8 · Educación, salud, seguridad
    D("aprender_l", "Aprender 6.º grado, Lengua (satisfactorio + avanzado)", "66,4 → 76,9", "%", "2023 → 2025", "EDUCACION", "Argentinos por la Educación", "aprender", note="No equivale a tasa de alfabetización."),
    D("aprender_m", "Aprender 6.º grado, Matemática (satisfactorio + avanzado)", "51,5 → 55,0", "%", "2023 → 2025", "EDUCACION", "Argentinos por la Educación", "aprender"),
    D("mort_inf", "Mortalidad infantil", "8,0 → 8,5", "por 1.000 nacidos vivos", "2023 → 2024", "SALUD", "Ministerio de Salud, DEIS", "deis", note="Último año disponible: 2024."),
    D("mort_mat", "Mortalidad materna", "3,2 → 4,4", "por 10.000 nacidos vivos", "2023 → 2024", "SALUD", "Ministerio de Salud, DEIS", "deis"),
    D("homic", "Tasa de homicidios dolosos", "4,4 · 3,8 · 3,6", "por 100.000 hab.", "2023 · 2024 · 2025 anual", "SEGURIDAD", "Ministerio de Seguridad (SNIC)", "snic25"),
    D("robos_25", "Robos denunciados", -21.6, "% vs 2024", "2025 vs 2024", "SEGURIDAD", "Ministerio de Seguridad", "snic25", note="PROXY: depende de denuncia y clasificación."),
    D("femic", "Víctimas directas de femicidio", "250 · 228 · 200", "personas", "2023 · 2024 · 2025 anual", "SEGURIDAD", "CSJN, Oficina de la Mujer", "csjn25", note="Subconjunto letal de la violencia de género."),
]

FIG = {f["key"]: f for f in FIGS}

# Indicadores sin dato verificable en el Excel (N/D ≠ 0), citados en pantalla
ND = {
    "educacion": ["Inversión educativa real", "Tasa de alfabetización", "Abandono escolar", "Finalización secundaria"],
    "salud": ["Inversión sanitaria real", "Esperanza de vida", "Camas hospitalarias"],
    "general": ["Reservas internacionales netas", "PBI real por habitante", "Inversión pública real", "Ingreso real de los hogares"],
}
