"""Concatena las frases de cada escena en una pista de voz y escribe timing.json.

Uso: python3 voice_tracks.py <dir_wavs_frases> <narracion.json> <dir_proyecto>
"""
import json, os, subprocess, sys
import numpy as np, soundfile as sf

RAW, SRC, PROJ = sys.argv[1:4]
GAP = 0.6        # silencio entre frases (s)
LEAD = {"s1": 6.0}  # s1 abre con la portada
DEFAULT_LEAD = 2.2  # rótulo de capítulo antes de la voz
TAIL = 1.4

data = json.load(open(SRC))
timing = {"scenes": []}
t0 = 0.0
for sc in data["escenas"]:
    sid = sc["id"]
    parts, cues, t = [], {}, 0.0
    sr = None
    for f in sc["frases"]:
        a, sr = sf.read(os.path.join(RAW, f["id"] + ".wav"), dtype="float32")
        if parts:
            parts.append(np.zeros(int(GAP * sr), dtype="float32")); t += GAP
        cues[f["id"]] = [round(t, 3), round(t + len(a) / sr, 3)]
        parts.append(a); t += len(a) / sr
    tmp = os.path.join(RAW, f"{sid}_cat.wav")
    sf.write(tmp, np.concatenate(parts), sr)
    out = os.path.join(PROJ, "assets", "audio", f"vo_{sid}.mp3")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", tmp, "-af", "loudnorm=I=-16:TP=-1.5:LRA=7", "-ar", "48000", "-ac", "1", "-b:a", "192k", out], check=True)
    lead = LEAD.get(sid, DEFAULT_LEAD)
    dur = round(lead + t + TAIL, 2)
    timing["scenes"].append({"id": sid, "title": sc["titulo"], "start": round(t0, 2), "duration": dur,
                             "voStart": lead, "voDuration": round(t, 3),
                             "cues": {k: [round(v[0] + lead, 3), round(v[1] + lead, 3)] for k, v in cues.items()}})
    t0 += dur
timing["outro"] = {"start": round(t0, 2), "duration": 12.0}
timing["total"] = round(t0 + 12.0, 2)
json.dump(timing, open(os.path.join(PROJ, "build", "timing.json"), "w"), indent=1, ensure_ascii=False)
print("total", timing["total"])
for s in timing["scenes"]:
    print(s["id"], s["start"], s["duration"])
