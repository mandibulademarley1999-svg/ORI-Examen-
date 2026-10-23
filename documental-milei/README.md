# Argentina 2023–2026 · documental de datos

Video documental (≈ 5:31, 1920×1080, 30 fps) de análisis económico y social sobre la presidencia de Javier Milei, desde el 10/12/2023 hasta el corte de datos del 23/10/2026. Única fuente de cifras: `milei_2023_2026_indicadores_y_fuentes.xlsx` y las fuentes originales que cita.

## Entregables

| Archivo | Contenido |
|---|---|
| `guion/guion.md` | Guion de narración con tiempos de cada frase |
| `guion/storyboard.md` | Sistema visual y escena por escena |
| `guion/cifras.md` | Todas las cifras usadas: valor, período exacto, hoja del Excel, organismo, URL y advertencias metodológicas |
| `guion/narracion.json` | Texto fuente de la narración (por frase) |
| `video/` | Proyecto HyperFrames (index.html + `compositions/`) |
| `video/renders/argentina-2023-2026.mp4` | Video final |

## Cómo se construye

```bash
cd video
# 1. voz (Kokoro local, fonética es-419 con yeísmo rehilado rioplatense), una pista por escena + timing.json
python3 build/voice_tracks.py <wavs_por_frase> ../guion/narracion.json .
# 2. música original
python3 build/music.py <duracion_s> bgm_raw.wav   # luego loudnorm a −31 LUFS → assets/audio/bgm.mp3
# 3. escenas HyperFrames desde el módulo único de datos (build/data.py)
python3 build/build.py && python3 build/docs.py
# 4. verificación y render
npx hyperframes check && npx hyperframes render --quality delivery --output renders/argentina-2023-2026.mp4
```

Los gráficos se generan como SVG/HTML a partir de `build/data.py`; cada animación GSAP está sincronizada con el inicio de la frase que menciona el dato (`build/timing.json`).

## Limitaciones conocidas

- La narración es voz sintética local (Kokoro, voz `ef_dora`) con fonética latinoamericana y "sh" rioplatense; no es un locutor humano ni una voz HeyGen (no había credenciales HeyGen en el entorno). Puede re-locutarse reemplazando `assets/audio/vo_s*.mp3` manteniendo los tiempos.
- La música es una composición original generada por código (`build/music.py`).
