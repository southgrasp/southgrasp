import os
OUT = os.path.dirname(os.path.abspath(__file__))
GREEN, SAGE, APRICOT, INK, CREAM = "#4A7C59", "#9AAD8E", "#E8C39E", "#2F4A38", "#F4F1EA"

# --- Symbol (120x120): 4枚の「しずく」で構成した花 ---
# 各しずく = 3つの角を半径s/2で丸め、中心側の角だけを残した正方形。
# 香りのしずく / 花びら / 四方に広がる穏やかさ を、円と正方形だけで表現。
S, G = 54, 6            # セルサイズ, セル間の余白 (2*S + G*2 + 余白 = 120)
R = S / 2
DROP = f"M{S} {S} H{R} A{R} {R} 0 0 1 0 {R} A{R} {R} 0 0 1 {R} 0 A{R} {R} 0 0 1 {S} {R} Z"
def symbol(x=0, y=0, s=1.0, mono=None):
    o = (120 - 2*S - G) / 2
    c = 60
    cols = [APRICOT, SAGE, GREEN, GREEN] if not mono else [mono]*4
    # 左上→右上→右下→左下（中心まわりに90°ずつ回転）
    petals = "".join(
        f'<path d="{DROP}" fill="{col}" transform="rotate({90*i} {c} {c}) translate({o} {o})"/>'
        for i, col in enumerate([cols[0], cols[1], cols[3], cols[2]]))
    return f'<g transform="translate({x} {y}) scale({s})">{petals}</g>'

# --- Wordmark: 丸いストローク端の幾何学モノライン (cap height 40) ---
H, SW, GAP = 40, 5, 13
glyphs = {
    "L": (22, "M0 0 V40 H22"),
    "A": (32, "M0 40 L16 0 L32 40 M6.4 24 H25.6"),
    "N": (28, "M0 40 V0 L28 40 V0"),
    "D": (30, "M0 0 H10 A20 20 0 0 1 10 40 H0 Z"),
    "Y": (30, "M0 0 L15 20 L30 0 M15 20 V40"),
}
def wordmark(x, y, s=1.0, color=INK, text="LANDAY"):
    parts, cx = [], 0
    for ch in text:
        w, d = glyphs[ch]
        parts.append(f'<path transform="translate({cx} 0)" d="{d}"/>')
        cx += w + GAP
    width = cx - GAP
    g = f'''<g transform="translate({x} {y}) scale({s})" fill="none" stroke="{color}" stroke-width="{SW}" stroke-linecap="round" stroke-linejoin="round">
  {"".join(parts)}
</g>'''
    return g, width * s

def svg(w, h, body, bg=None):
    b = f'<rect width="{w}" height="{h}" fill="{bg}"/>' if bg else ""
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">{b}{body}</svg>\n'

def write(name, content):
    open(os.path.join(OUT, name), "w").write(content)

# symbol only
write("landay-symbol.svg", svg(120, 120, symbol()))

# horizontal: symbol + wordmark
wm, ww = wordmark(0, 0)
pad = 20
sym_s = 0.9
W = int(pad + 120*sym_s + 22 + ww + pad + 4)
Hh = int(120*sym_s + pad*2)
ty = pad + (120*sym_s)*0.5 - H/2   # 文字の中心をシンボルの視覚的重心に合わせる
wm, _ = wordmark(pad + 120*sym_s + 22, ty)
write("landay-logo-horizontal.svg", svg(W, Hh, symbol(pad, pad, sym_s) + wm))

# vertical: symbol above wordmark
s2 = 0.6
_, ww2 = wordmark(0, 0, s2)
Wv = int(max(ww2, 120) + pad*2 + 4)
wm2, _ = wordmark((Wv - ww2)/2, pad + 120 + 22, s2)
Hv = int(pad + 120 + 22 + H*s2 + pad + 4)
write("landay-logo-vertical.svg", svg(Wv, Hv, symbol((Wv-120)/2, pad) + wm2))

# reversed (on dark) & mono
wm3, _ = wordmark(pad + 120*sym_s + 22, ty, color=CREAM)
write("landay-logo-horizontal-reverse.svg", svg(W, Hh, symbol(pad, pad, sym_s, mono=CREAM) + wm3, bg="#232C25"))
wm4, _ = wordmark(pad + 120*sym_s + 22, ty, color=INK)
write("landay-logo-horizontal-mono.svg", svg(W, Hh, symbol(pad, pad, sym_s, mono=INK) + wm4))
print(W, Hh, Wv, Hv)
