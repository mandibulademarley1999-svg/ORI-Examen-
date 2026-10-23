"""Música instrumental original y discreta (pad + piano suave), determinística.

Uso: python3 music.py <duracion_s> <salida.wav>
"""
import sys
import numpy as np, soundfile as sf
from scipy.signal import fftconvolve, butter, sosfilt

DUR = float(sys.argv[1]); OUT = sys.argv[2]
SR = 44100
rng = np.random.default_rng(2023)
n = int(DUR * SR)
t = np.arange(n) / SR

def hz(m): return 440.0 * 2 ** ((m - 69) / 12)

# Progresión lenta en re menor: Dm9 – B♭maj7 – Fmaj7/A – C/G (8 s por acorde)
CHORDS = [[50, 57, 60, 64, 65], [46, 53, 57, 62, 65], [45, 53, 57, 60, 64], [43, 50, 55, 60, 62]]
CH = 8.0
L = np.zeros(n); R = np.zeros(n)

def env(length, a, r):
    e = np.ones(length)
    ai, ri = int(a * SR), int(r * SR)
    e[:ai] = np.linspace(0, 1, ai) ** 2
    e[-ri:] *= np.linspace(1, 0, ri) ** 2
    return e

k = 0
start = 0.0
while start < DUR:
    notes = CHORDS[k % 4]
    s0 = int(start * SR); length = min(int((CH + 3) * SR), n - s0)
    if length <= SR: break
    tt = np.arange(length) / SR
    if length < int(6 * SR): break
    e = env(length, 2.8, 3.0)
    for i, m in enumerate(notes):
        f = hz(m + 12 if i else m)
        for det, pan in ((-0.0012, 0.3), (0.0012, 0.7)):
            ph = rng.uniform(0, 2 * np.pi)
            w = np.sin(2 * np.pi * f * (1 + det) * tt + ph) + 0.18 * np.sin(4 * np.pi * f * (1 + det) * tt + ph)
            g = (0.05 if i else 0.07) * e
            L[s0:s0 + length] += w * g * (1 - pan); R[s0:s0 + length] += w * g * pan
    # piano suave: arpegio esparcido
    arp = notes[1:] + [notes[2] + 12]
    for j in range(4):
        pt = start + 1.0 + j * 1.9 + rng.uniform(-0.05, 0.05)
        if pt >= DUR - 1: break
        m = arp[(j * 2 + k) % len(arp)] + 12
        f = hz(m); p0 = int(pt * SR); pl = min(int(4.5 * SR), n - p0)
        pt_ = np.arange(pl) / SR
        dec = np.exp(-pt_ * 1.6) * np.minimum(1, pt_ / 0.008)
        w = (np.sin(2 * np.pi * f * pt_) + 0.35 * np.sin(4 * np.pi * f * pt_) * np.exp(-pt_ * 2.5) + 0.12 * np.sin(6 * np.pi * f * pt_) * np.exp(-pt_ * 4))
        pan = 0.35 + 0.3 * ((j + k) % 3) / 2
        L[p0:p0 + pl] += 0.045 * w * dec * (1 - pan); R[p0:p0 + pl] += 0.045 * w * dec * pan
    start += CH; k += 1

# bajo sostenido
bass = np.zeros(n)
for k in range(int(np.ceil(DUR / CH))):
    s0 = int(k * CH * SR); length = min(int((CH + 2) * SR), n - s0)
    if length <= SR: break
    tt = np.arange(length) / SR
    if length < int(4.6 * SR): break
    bass[s0:s0 + length] += 0.06 * np.sin(2 * np.pi * hz(CHORDS[k % 4][0] - 12) * tt) * env(length, 2.0, 2.5)
L += bass; R += bass

sos = butter(4, 3800, "low", fs=SR, output="sos")
L = sosfilt(sos, L); R = sosfilt(sos, R)
# reverb: IR de ruido con decaimiento exponencial
ir_len = int(3.2 * SR); it = np.arange(ir_len) / SR
irL = rng.standard_normal(ir_len) * np.exp(-it * 2.2); irR = rng.standard_normal(ir_len) * np.exp(-it * 2.2)
irL /= np.sqrt((irL ** 2).sum()); irR /= np.sqrt((irR ** 2).sum())
wetL = fftconvolve(L, irL)[:n]; wetR = fftconvolve(R, irR)[:n]
L = 0.55 * L + 0.45 * wetL; R = 0.55 * R + 0.45 * wetR
fade = np.ones(n); fi, fo = int(4 * SR), int(7 * SR)
fade[:fi] = np.linspace(0, 1, fi); fade[-fo:] = np.linspace(1, 0, fo)
st = np.stack([L * fade, R * fade], 1)
st /= np.abs(st).max() / 0.8
sf.write(OUT, st.astype("float32"), SR)
print("ok", OUT, st.shape[0] / SR)
