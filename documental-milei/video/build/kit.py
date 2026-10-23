"""Piezas reutilizables: estilos, gráficos SVG y llamadas GSAP para las escenas."""

C = dict(bg="#0D1117", panel="#141B24", grid="#26323F", ink="#EEE8DD", mute="#A7AFBC", dim="#838D9C",
         amber="#E2A63B", sky="#79AEDB", coral="#D8735A")

COMMON_CSS = """
#root { position:absolute; inset:0; background:%(bg)s; color:%(ink)s; font-family:'Inter',sans-serif; overflow:hidden; }
.stage { position:absolute; inset:0; }
.abs { position:absolute; }
.kicker { font-family:'IBM Plex Mono',monospace; font-size:21px; letter-spacing:.18em; text-transform:uppercase; color:%(amber)s; }
.h1 { font-family:'Playfair Display',serif; font-weight:600; letter-spacing:-.01em; }
.body { font-size:27px; line-height:1.38; color:%(ink)s; }
.mute { color:%(mute)s; }
.mono { font-family:'IBM Plex Mono',monospace; }
.src { font-family:'IBM Plex Mono',monospace; font-size:19px; line-height:1.45; color:%(mute)s; }
.chip { font-family:'IBM Plex Mono',monospace; font-size:18px; letter-spacing:.06em; color:%(ink)s; border:1px solid %(grid)s; padding:6px 12px; border-radius:3px; white-space:nowrap; }
.chip.part { color:%(amber)s; border-color:%(amber)s; }
.ptitle { font-family:'Playfair Display',serif; font-size:34px; font-weight:600; color:%(ink)s; }
.psub { font-family:'IBM Plex Mono',monospace; font-size:18px; color:%(mute)s; margin-top:8px; letter-spacing:.04em; }
.num { font-variant-numeric:tabular-nums; }
.note { font-family:'IBM Plex Mono',monospace; font-size:18px; line-height:1.5; color:%(ink)s; border-left:3px solid %(amber)s; padding:8px 0 8px 18px; }
svg text { font-family:'Inter',sans-serif; font-variant-numeric:tabular-nums; }
svg .lbl { fill:%(mute)s; font-size:21px; }
svg .lbl2 { fill:%(dim)s; font-size:17px; font-family:'IBM Plex Mono',monospace; }
svg .val { fill:%(ink)s; font-size:24px; font-weight:600; }
svg .valb { fill:%(ink)s; font-size:30px; font-weight:700; }
.prog { position:absolute; left:120px; right:120px; top:1006px; height:3px; display:flex; gap:8px; }
.prog i { flex:1; background:%(grid)s; }
.prog i.on { background:%(amber)s; }
.progl { position:absolute; right:120px; top:96px; font-family:'IBM Plex Mono',monospace; font-size:16px; color:%(dim)s; letter-spacing:.12em; }
.w { display:inline-block; }
""" % C

PRELUDE = r"""
const tl = gsap.timeline({ paused: true });
const fmt = (v, d) => { const s = Math.abs(v).toFixed(d).split('.'); s[0] = s[0].replace(/\B(?=(\d{3})+(?!\d))/g, '.'); return (v < 0 ? '−' : '') + s.join(','); };
const G = {
  inn: (s, t, d = 0.6) => tl.fromTo(s, { opacity: 0, filter: 'blur(8px)' }, { opacity: 1, filter: 'blur(0px)', duration: d, ease: 'power3.out' }, t),
  up: (s, t, d = 0.8) => tl.fromTo(s, { opacity: 0, y: 26 }, { opacity: 1, y: 0, duration: d, ease: 'expo.out' }, t),
  out: (s, t, d = 0.3) => tl.to(s, { opacity: 0, filter: 'blur(6px)', duration: d, ease: 'power2.in' }, t),
  dim: (s, t, o = 0.22) => tl.to(s, { opacity: o, duration: 0.6, ease: 'power2.inOut' }, t),
  vbar: (s, t, neg) => tl.fromTo(s, { scaleY: 0, transformOrigin: neg ? '50% 0%' : '50% 100%' }, { scaleY: 1, duration: 1.1, ease: 'expo.out', transformOrigin: neg ? '50% 0%' : '50% 100%' }, t),
  hbar: (s, t, neg) => tl.fromTo(s, { scaleX: 0, transformOrigin: neg ? '100% 50%' : '0% 50%' }, { scaleX: 1, duration: 1.1, ease: 'expo.out', transformOrigin: neg ? '100% 50%' : '0% 50%' }, t),
  draw: (s, t, d = 0.9) => tl.fromTo(s, { strokeDashoffset: 1 }, { strokeDashoffset: 0, duration: d, ease: 'power2.inOut' }, t),
  dot: (s, t) => tl.fromTo(s, { scale: 0, transformOrigin: '50% 50%' }, { scale: 1, duration: 0.5, ease: 'back.out(1.6)', transformOrigin: '50% 50%' }, t),
  cu: (s, to, d, pre, suf, t, dur = 1.4) => { const o = { v: 0 }; tl.fromTo(o, { v: 0 }, { v: to, duration: dur, ease: 'power2.out', onUpdate: () => { const el = document.querySelector(s); if (el) el.textContent = pre + fmt(o.v, d) + suf; } }, t); },
  words: (s, t) => tl.fromTo(s + ' .w', { opacity: 0, filter: 'blur(6px)' }, { opacity: 1, filter: 'blur(0px)', duration: 0.3, stagger: 0.07, ease: 'power2.out' }, t),
};
"""


def fmt(v, d=1, sign=False):
    s = f"{abs(v):,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    if v < 0:
        return "−" + s
    return ("+" if sign and v > 0 else "") + s


def words(text):
    return " ".join(f'<span class="w">{w}</span>' for w in text.split(" "))


class Scene:
    def __init__(self, sid, idx, title, duration, cues, lead=2.2):
        self.sid, self.idx, self.title, self.dur, self.cues, self.lead = sid, idx, title, duration, cues, lead
        self.html, self.js, self.css = [], [], []

    def c(self, k, off=0.0):
        return round(self.cues[k][0] + off, 2)

    def add(self, h):
        self.html.append(h)

    def j(self, s):
        self.js.append(s)

    def id(self, s):
        return f"{self.sid}-{s}"

    # ----- piezas comunes -----
    def chapter(self, card=True):
        sid, n = self.sid, self.idx
        if card:
            self.add(f'''<div id="{sid}-card" class="abs" style="left:0;right:0;top:330px;text-align:center">
  <div class="h1 num" style="font-size:150px;color:{C['amber']};line-height:1">{n:02d}</div>
  <div class="h1" style="font-size:66px;margin-top:22px">{self.title}</div></div>''')
            self.j(f"G.inn('#{sid}-card', 0.15, 0.7); G.out('#{sid}-card', 1.75, 0.35);")
        self.add(f'''<div id="{sid}-head" class="abs" style="left:120px;top:84px">
  <div class="kicker">Capítulo {n:02d} / 09</div>
  <div class="h1" style="font-size:50px;margin-top:10px">{words(self.title)}</div></div>''')
        t0 = 2.0 if card else self.lead
        self.j(f"G.inn('#{sid}-head .kicker', {t0}); G.words('#{sid}-head .h1', {t0 + 0.1});")
        segs = "".join(f'<i class="{"on" if i + 1 <= n else ""}"></i>' for i in range(9))
        self.add(f'<div id="{sid}-prog" class="prog">{segs}</div><div id="{sid}-progl" class="progl">ARGENTINA 2023–2026 · DATOS AL 23/10/2026</div>')
        self.j(f"G.inn('#{sid}-prog', {t0}); G.inn('#{sid}-progl', {t0});")

    def source(self, key, text, t, t_out=None, top=None):
        i = self.id("src-" + key)
        self.add(f'<div id="{i}" class="abs src" style="left:120px;top:952px;width:1680px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{text}</div>')
        self.j(f"G.inn('#{i}', {t});")
        if t_out:
            self.j(f"G.out('#{i}', {t_out});")

    def group(self, key, x, y, w, h, inner, t, t_out=None, how="inn"):
        i = self.id(key)
        self.add(f'<div id="{i}" class="abs" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px">{inner}</div>')
        self.j(f"G.{how}('#{i}', {t});")
        if t_out:
            self.j(f"G.out('#{i}', {t_out});")
        return i

    def render(self):
        body = "\n".join(self.html)
        js = "\n".join(self.js)
        end = round(self.dur - 0.45, 2)
        css = COMMON_CSS + "\n".join(self.css)
        fade_in = "" if self.sid == "s1" else f"tl.fromTo('#{self.sid}-fade', {{ opacity: 0 }}, {{ opacity: 1, duration: 0.45, ease: 'power2.out' }}, 0);" 
        return f'''<template>
<style>{css}</style>
<div id="root" data-composition-id="{self.sid}" data-width="1920" data-height="1080">
<div id="{self.sid}-stage" class="stage clip" data-start="0" data-duration="{self.dur}" data-track-index="1">
<div id="{self.sid}-fade" class="stage">
{body}
</div>
</div>
</div>
<script>
(() => {{
{PRELUDE}
{fade_in}
{js}
tl.to('#{self.sid}-fade', {{ opacity: 0, duration: 0.4, ease: 'power2.in' }}, {end});
window.__timelines["{self.sid}"] = tl;
}})();
</script>
</template>
'''


def panel_head(title, sub):
    return f'<div class="ptitle">{title}</div><div class="psub">{sub}</div>'


def hatch(pid, color):
    return (f'<pattern id="{pid}-h" patternUnits="userSpaceOnUse" width="11" height="11" patternTransform="rotate(45)">'
            f'<rect width="11" height="11" fill="{color}" fill-opacity="0.18"/><line x1="0" y1="0" x2="0" y2="11" stroke="{color}" stroke-width="5"/></pattern>')


def vbars(sc, pid, w, h, items, vmin, vmax, d=1, sign=False, suffix="", top=56, bottom=78, barw=0.5, guide=None):
    """items: dict(label, sub, v, t, partial, color). Devuelve SVG; agrega las animaciones."""
    ph = h - top - bottom
    y = lambda v: top + (vmax - v) / (vmax - vmin) * ph
    base = y(max(vmin, 0) if vmin >= 0 else 0)
    n = len(items); slot = w / n; bw = slot * barw
    out = [f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" style="overflow:visible"><defs>']
    cols = {it.get("color", C["amber"]) for it in items}
    for k, col in enumerate(sorted(cols)):
        out.append(hatch(f"{pid}{k}", col))
    hid = {col: f"{pid}{k}-h" for k, col in enumerate(sorted(cols))}
    out.append("</defs>")
    out.append(f'<line x1="0" x2="{w}" y1="{base:.1f}" y2="{base:.1f}" stroke="{C["mute"]}" stroke-width="1.5"/>')
    if guide is not None:
        gy = y(guide[0])
        out.append(f'<line x1="0" x2="{w}" y1="{gy:.1f}" y2="{gy:.1f}" stroke="{C["dim"]}" stroke-dasharray="6 6"/>'
                   f'<text class="lbl2" x="{w}" y="{gy - 10:.1f}" text-anchor="end">{guide[1]}</text>')
    for i, it in enumerate(items):
        v = it["v"]; col = it.get("color", C["amber"]); cx = slot * i + slot / 2
        y1, y2 = sorted([y(v), base])
        fill = f'url(#{hid[col]})' if it.get("partial") else col
        bid = f"{pid}-b{i}"
        out.append(f'<rect id="{bid}" x="{cx - bw / 2:.1f}" y="{y1:.1f}" width="{bw:.1f}" height="{max(y2 - y1, 1):.1f}" fill="{fill}" stroke="{col}" stroke-width="{2 if it.get("partial") else 0}"/>')
        vy = (y1 - 14) if v >= 0 else (y2 + 30)
        vid = f"{pid}-v{i}"
        out.append(f'<text id="{vid}" class="{it.get("vcls", "val")}" x="{cx:.1f}" y="{vy:.1f}" text-anchor="middle">{fmt(v, d, sign)}{suffix}</text>')
        lid = f"{pid}-l{i}"
        ly = h - bottom + 34
        out.append(f'<g id="{lid}"><text class="lbl" x="{cx:.1f}" y="{ly:.1f}" text-anchor="middle">{it["label"]}</text>'
                   f'<text class="lbl2" x="{cx:.1f}" y="{ly + 24:.1f}" text-anchor="middle">{it.get("sub", "")}</text></g>')
        t = it["t"]
        sc.j(f"G.vbar('#{bid}', {t}, {str(v < 0).lower()}); G.inn('#{vid}', {t + 0.55}, 0.4); G.inn('#{lid}', {t}, 0.4);")
    out.append("</svg>")
    return "".join(out)


def hbars(sc, pid, w, items, vmin, vmax, d=1, sign=False, suffix="", labw=330, rowh=58, base=0.0, barh=0.56):
    h = rowh * len(items)
    pw = w - labw - 110
    x = lambda v: labw + (v - vmin) / (vmax - vmin) * pw
    bx = x(base)
    out = [f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" style="overflow:visible"><defs>{hatch(pid, C["amber"])}</defs>']
    out.append(f'<line x1="{bx:.1f}" x2="{bx:.1f}" y1="-6" y2="{h:.1f}" stroke="{C["mute"]}" stroke-width="1.5"/>')
    for i, it in enumerate(items):
        v = it["v"]; col = it.get("color", C["amber"]); cy = rowh * i + rowh / 2
        x1, x2 = sorted([x(v), bx])
        bid, vid, lid = f"{pid}-b{i}", f"{pid}-v{i}", f"{pid}-l{i}"
        fill = f"url(#{pid}-h)" if it.get("partial") else col
        out.append(f'<text id="{lid}" class="lbl" x="0" y="{cy + 7:.1f}">{it["label"]}</text>')
        out.append(f'<rect id="{bid}" x="{x1:.1f}" y="{cy - rowh * barh / 2:.1f}" width="{max(x2 - x1, 1):.1f}" height="{rowh * barh:.1f}" fill="{fill}" stroke="{col}" stroke-width="{2 if it.get("partial") else 0}"/>')
        vx = x2 + 12 if v >= base else x1 - 12
        anchor = "start" if v >= base else "end"
        if v < base and x1 - labw < 90:
            vx, anchor = x2 + 12, "start"
        out.append(f'<text id="{vid}" class="val" x="{vx:.1f}" y="{cy + 8:.1f}" text-anchor="{anchor}">{fmt(v, d, sign)}{suffix}</text>')
        t = it["t"]
        sc.j(f"G.inn('#{lid}', {t}, 0.4); G.hbar('#{bid}', {t}, {str(v < base).lower()}); G.inn('#{vid}', {t + 0.5}, 0.4);")
    out.append("</svg>")
    return "".join(out)


def line(sc, pid, w, h, pts, vmin, vmax, color=None, d=1, suffix="", top=50, bottom=80, left=20, right=20,
         dashed_from=None, labels_below=True, show_x=True, ref=None, vcls="val"):
    """pts: dict(label, sub, v, t, above=True)."""
    color = color or C["amber"]
    n = len(pts); pw = w - left - right; ph = h - top - bottom
    X = lambda i: left + (pw * i / (n - 1) if n > 1 else pw / 2)
    Y = lambda v: top + (vmax - v) / (vmax - vmin) * ph
    out = [f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" style="overflow:visible">']
    if ref is not None:
        ry = Y(ref[0])
        out.append(f'<line id="{pid}-ref" x1="0" x2="{w}" y1="{ry:.1f}" y2="{ry:.1f}" stroke="{C["dim"]}" stroke-dasharray="6 6"/>'
                   f'<text id="{pid}-reft" class="lbl2" x="{w}" y="{ry - 10:.1f}" text-anchor="end">{ref[1]}</text>')
        sc.j(f"G.inn('#{pid}-ref', {ref[2]}); G.inn('#{pid}-reft', {ref[2]});")
    if show_x:
        out.append(f'<line x1="0" x2="{w}" y1="{h - bottom + 6:.1f}" y2="{h - bottom + 6:.1f}" stroke="{C["grid"]}"/>')
    for i in range(1, n):
        sid = f"{pid}-s{i}"
        dash = ' stroke-dasharray="1"'
        style = "stroke-dasharray:1;stroke-dashoffset:1"
        extra = ""
        out.append(f'<path id="{sid}" d="M{X(i - 1):.1f},{Y(pts[i - 1]["v"]):.1f} L{X(i):.1f},{Y(pts[i]["v"]):.1f}" pathLength="1" fill="none" stroke="{color}" stroke-width="4" stroke-linecap="round" style="{style}"/>')
        if dashed_from is not None and i >= dashed_from:
            # tramo con período distinto: punteado superpuesto en color de fondo
            out.append(f'<path id="{sid}d" d="M{X(i - 1):.1f},{Y(pts[i - 1]["v"]):.1f} L{X(i):.1f},{Y(pts[i]["v"]):.1f}" fill="none" stroke="{C["bg"]}" stroke-width="6" stroke-dasharray="10 10"/>')
            sc.j(f"G.inn('#{sid}d', {pts[i]['t']}, 0.1);")
        sc.j(f"G.draw('#{sid}', {pts[i]['t'] - 0.1}, 0.8);")
    for i, p in enumerate(pts):
        cid, vid, lid = f"{pid}-c{i}", f"{pid}-v{i}", f"{pid}-l{i}"
        out.append(f'<circle id="{cid}" cx="{X(i):.1f}" cy="{Y(p["v"]):.1f}" r="8" fill="{C["bg"]}" stroke="{color}" stroke-width="4"/>')
        vy = Y(p["v"]) - 22 if p.get("above", True) else Y(p["v"]) + 42
        out.append(f'<text id="{vid}" class="{p.get("vcls", vcls)}" x="{X(i):.1f}" y="{vy:.1f}" text-anchor="middle" fill="{color}">{fmt(p["v"], p.get("d", d))}{suffix}</text>')
        tt = p["t"] + (0.6 if i else 0)
        sc.j(f"G.dot('#{cid}', {tt}); G.inn('#{vid}', {tt + 0.15}, 0.4);")
        if labels_below:
            ly = h - bottom + 40
            out.append(f'<g id="{lid}"><text class="lbl" x="{X(i):.1f}" y="{ly:.1f}" text-anchor="middle">{p["label"]}</text>'
                       f'<text class="lbl2" x="{X(i):.1f}" y="{ly + 24:.1f}" text-anchor="middle">{p.get("sub", "")}</text></g>')
            sc.j(f"G.inn('#{lid}', {tt}, 0.4);")
    out.append("</svg>")
    return "".join(out)
