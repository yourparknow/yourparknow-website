#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera railing-secciones-frente.html : planos de fabricacion, vista de frente,
   una seccion por bloque, con cadena de cotas completa."""
from fractions import Fraction

OUT = "/home/user/yourparknow-website/proposals/jrg-welding-corp/railing-secciones-frente.html"

# ---------------------------------------------------------------- fracciones
def fr(x, den=32):
    """decimal -> pulgadas con fraccion de taller (denominador POTENCIA DE 2)."""
    assert den in (2, 4, 8, 16, 32, 64), "el taller solo lee mitades, cuartos, octavos..."
    f = Fraction(round(x * den), den)      # Fraction reduce solo: 8/32 -> 1/4
    whole = int(f)
    rem = f - whole
    if rem == 0:
        return f"{whole}"
    if whole == 0:
        return f"{rem.numerator}/{rem.denominator}"
    return f"{whole}-{rem.numerator}/{rem.denominator}"

def feet(x):
    ft = int(x // 12)
    inch = x - ft * 12
    if abs(inch) < 1e-9:
        return f"{ft}'-0\""
    return f"{ft}'-{fr(inch)}\""

# ---------------------------------------------------------------- geometria
POST = 2.0          # poste 2x2
CAP_T = 1.0         # cap 1" de alto
RAIL_T = 1.0        # riel inferior 1" de alto
FLOOR = 2.0         # luz del piso al riel
GUARD = 42.0        # piso a tope del cap
POST_LEN = 48.0     # poste total (42 + 6 a la fascia)
CAMPO = 38.0        # luz libre entre riel y cap
Y_CAP_B = 1.0       # cara inferior del cap
Y_RAIL_T = 39.0     # cara superior del riel
Y_RAIL_B = 40.0
Y_DECK = 42.0
GAP_PANEL = 0.25    # holgura por lado: panel = luz - 1/2

def piques_de(luz):
    """devuelve (n, luz_entre_piques) para un pano liso de `luz` entre caras de poste."""
    W = luz - 2 * GAP_PANEL           # ancho del panel soldado
    n = 1
    while True:
        g = (W - n) / (n + 1)
        if g + GAP_PANEL < 4.0:       # luz libre real contra el poste
            return n, g
        n += 1

# ---------------------------------------------------------------- secciones
# elemento: ('P',) poste  |  ('D',luz) dibujo  |  ('L',luz) liso
D = 46.0
def S(name, balcon, elems, izq, der, nota=""):
    return dict(name=name, balcon=balcon, elems=elems, izq=izq, der=der, nota=nota)

SECCIONES = [
 S("A-1", 1, [('P',),('L',45.375),('P',),('D',D),('P',),('L',45.4375),('P',),('D',D),('P',)],
   "ESQUINA ①  (arranca en el poste de esquina con C-1)", "EMPATE RECTO ③  (junta al centro del poste)"),
 S("A-2", 1, [('D',D),('P',),('L',45.4375),('P',),('D',D),('P',),('L',45.375),('P',)],
   "EMPATE RECTO ③  (arranca en paño, apoya en el poste de A-1)", "ESQUINA ②  (lleva el poste de esquina con B-1)"),
 S("B-1", 1, [('L',29.5),('P',),('D',D),('P',),('D',D),('P',),('L',29.5),('P',)],
   "ESQUINA ②  (arranca en paño, apoya en el poste de A-2)", "REMATE CONTRA LA CASA ⑥  (placa 4×4×1/4)"),
 S("C-1", 1, [('L',44.5),('P',),('D',D),('P',),('L',44.625),('P',)],
   "ESQUINA ①  (arranca en paño, apoya en el poste de A-1)", "EMPATE RECTO ④  (junta al centro del poste)"),
 S("C-2", 1, [('D',D),('P',),('L',44.5),('P',)],
   "EMPATE RECTO ④  (arranca en paño)", "ARRANQUE DE ESCALERA ⑤"),
 S("D-1", 2, [('P',),('L',36.625),('P',),('D',D),('P',),('L',36.625),('P',)],
   "ESQUINA con F-1  (lleva el poste de esquina)", "EMPATE RECTO  (junta al centro del poste)",
   "Esta corrida ya trae descontadas las 2\" en la esquina."),
 S("D-2", 2, [('D',D),('P',),('L',36.75),('P',),('D',D),('P',)],
   "EMPATE RECTO  (arranca en paño)", "EMPATE RECTO  (junta al centro del poste)"),
 S("D-3", 2, [('L',36.625),('P',),('D',D),('P',),('L',36.625),('P',)],
   "EMPATE RECTO  (arranca en paño)", "ESQUINA con E-1  (lleva el poste de esquina)"),
 S("E-1", 2, [('L',24.8125),('P',),('D',D),('P',),('D',D),('P',),('L',24.8125),('P',)],
   "ESQUINA  (arranca en paño, apoya en el poste de D-3)", "REMATE CONTRA LA CASA  (placa 4×4×1/4)"),
 S("F-1", 2, [('L',45.25),('P',),('D',D),('P',),('L',45.25),('P',)],
   "ESQUINA  (arranca en paño, apoya en el poste de D-1)", "EMPATE RECTO  (junta al centro del poste)"),
 S("F-2", 2, [('D',D),('P',),('L',45.25),('P',)],
   "EMPATE RECTO  (arranca en paño)", "REMATE CONTRA LA CASA  (placa 4×4×1/4)"),
]

CORRIDAS = {
 1: [("A", 383.625, ["A-1","A-2"]), ("B", 161.0, ["B-1"]), ("C", 237.625, ["C-1","C-2"])],
 2: [("D", 387.25, ["D-1","D-2","D-3"]), ("E", 151.625, ["E-1"]), ("F", 239.75, ["F-1","F-2"])],
}

# ---------------------------------------------------------------- verificacion
def largo(sec):
    t = 0.0
    for e in sec['elems']:
        t += POST if e[0] == 'P' else e[1]
    return t

for s in SECCIONES:
    s['largo'] = largo(s)

BY = {s['name']: s for s in SECCIONES}

def chk(bal):
    for run, total, secs in CORRIDAS[bal]:
        suma = sum(BY[n]['largo'] for n in secs)
        # la seccion que arranca en pano no trae el poste de esquina de la corrida vecina
        got = suma + (2.0 if BY[secs[0]]['elems'][0][0] != 'P' else 0.0)
        assert abs(got - total) < 1e-9, (run, got, total)
        print(f"  corrida {run}: secciones {suma:8.4f} + esquina = {got:8.4f}  vs medido {total:8.4f}  OK")
print("VERIFICACION DE CORRIDAS")
chk(1); chk(2)

tot_dib = sum(1 for s in SECCIONES for e in s['elems'] if e[0] == 'D')
tot_lis = sum(1 for s in SECCIONES for e in s['elems'] if e[0] == 'L')
tot_pos = sum(1 for s in SECCIONES for e in s['elems'] if e[0] == 'P')
tot_piq = 0
anchos = {}
for s in SECCIONES:
    for e in s['elems']:
        if e[0] == 'L':
            n, g = piques_de(e[1])
            tot_piq += n
            anchos.setdefault(e[1], [0, n, g])
            anchos[e[1]][0] += 1
print(f"TOTALES: {tot_dib} dibujitos · {tot_lis} paños de piques ({tot_piq} piques) · {tot_pos} postes")

# ---------------------------------------------------------------- dibujo SVG
SC = 3.55                      # px por pulgada
OX, OY = 74, 44                # origen del dibujo dentro del svg
VW, VH = 792, 302              # viewBox fijo: todas las secciones a la MISMA escala

ST_DARK, ST_MID, ST_LT = "#4b5563", "#6b7280", "#9aa5b1"
DIM = "#b91c1c"
def X(v): return OX + v * SC
def Y(v): return OY + v * SC

def rect(x, y, w, h, fill, stroke="#374151", sw=0.5):
    return (f'<rect x="{X(x):.2f}" y="{Y(y):.2f}" width="{w*SC:.2f}" height="{h*SC:.2f}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')

def dibujito(x0):
    """motif decorativo en una bahia de 46 de luz. x0 = cara del poste izquierdo."""
    o = []
    L = x0 + GAP_PANEL                 # borde del panel
    cx = x0 + 23.0                     # centro de la bahia
    cy = 20.0                          # centro vertical del campo
    # riel inferior
    o.append(rect(L, Y_RAIL_T, 45.5, RAIL_T, ST_LT))
    # cadena del panel: 3-5/16 + 1(B) + 3-5/16 + 1(V) + 28-1/4 + 1(V) + 3-5/16 + 1(B) + 3-5/16 = 45-1/2
    g_, t_ = 3.3125, 1.0
    b1 = L + g_
    v1 = b1 + t_ + g_
    v2 = v1 + t_ + 28.25
    b2 = v2 + t_ + g_
    assert abs((b2 + t_ + g_) - (L + 45.5)) < 1e-9, "cadena del dibujito no cierra"
    for xx in (b1, b2):                       # piques de flanco B (1x1)
        o.append(rect(xx, Y_CAP_B, 1, CAMPO, "#e5e7eb"))
    o.append(rect(v1, Y_CAP_B, 1, CAMPO, ST_MID))
    o.append(rect(v2, Y_CAP_B, 1, CAMPO, ST_MID))
    # horizontales H del cuadro
    for yy in (4.875, 34.125):
        o.append(rect(v1+1, yy, 28.25, 1, ST_MID))
    # X a 45
    a, b = v1 + 1, v2
    o.append(f'<g stroke="{ST_MID}" stroke-width="{SC:.2f}" stroke-linecap="butt">'
             f'<line x1="{X(a):.2f}" y1="{Y(5.875):.2f}" x2="{X(b):.2f}" y2="{Y(34.125):.2f}"/>'
             f'<line x1="{X(a):.2f}" y1="{Y(34.125):.2f}" x2="{X(b):.2f}" y2="{Y(5.875):.2f}"/></g>')
    # rombos concentricos Q2 (20-1/2 o.d.) y Q3 (10-3/4 o.d.)
    for od, col in ((20.5, ST_MID), (10.75, "#374151")):
        s = od - 1.0                   # centro a centro
        o.append(f'<rect x="{X(cx-s/2):.2f}" y="{Y(cy-s/2):.2f}" width="{s*SC:.2f}" '
                 f'height="{s*SC:.2f}" fill="none" stroke="{col}" stroke-width="{SC:.2f}"/>')
    return "".join(o)

def pano_liso(x0, luz):
    n, g = piques_de(luz)
    o = [rect(x0 + GAP_PANEL, Y_RAIL_T, luz - 0.5, RAIL_T, ST_LT)]
    for i in range(n):
        xx = x0 + GAP_PANEL + g + i * (1 + g)
        o.append(rect(xx, Y_CAP_B, 1, CAMPO, "#e5e7eb"))
    return "".join(o), n, g

def svg_seccion(sec):
    o = ['<defs><marker id="m%s" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" '
         'markerHeight="5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" '
         'fill="%s"/></marker></defs>' % (sec['name'].replace('-',''), DIM)]
    mid = sec["name"].replace("-", "")
    MK = f'url(#m{mid})'
    T = sec['largo']

    # deck
    o.append(f'<rect x="{X(-6):.2f}" y="{Y(Y_DECK):.2f}" width="{(T+12)*SC:.2f}" '
             f'height="{2.2*SC:.2f}" fill="#d6cfc2" stroke="#8a6a42" stroke-width="1"/>')

    # recorrido de elementos
    x = 0.0
    bays, posts = [], []
    for e in sec['elems']:
        if e[0] == 'P':
            posts.append(x)
            x += POST
        else:
            bays.append((x, e[0], e[1]))
            x += e[1]

    # panos primero (van por detras de los postes)
    labels = []
    for x0, kind, luz in bays:
        if kind == 'D':
            o.append(dibujito(x0))
            labels.append((x0 + luz/2, "DIBUJO", luz))
        else:
            s, n, g = pano_liso(x0, luz)
            o.append(s)
            labels.append((x0 + luz/2, f"{n} PIQUES", luz))

    # cap corrido
    o.append(rect(-0.0 if sec['elems'][0][0] == 'P' else -1.0, 0, T + (0 if sec['elems'][0][0]=='P' else 1) + 1, CAP_T, "#8a97a2"))
    # postes
    for px in posts:
        o.append(rect(px, Y_CAP_B, POST, POST_LEN - 1, "#cbd5dd", "#374151", 0.8))

    # etiqueta de cada bahia
    for cxx, txt, luz in labels:
        o.append(f'<text x="{X(cxx):.2f}" y="{Y(3.4):.2f}" font-size="6.6" font-weight="bold" '
                 f'fill="#1b2a41" text-anchor="middle">{txt}</text>')

    # ---- cota superior: largo total
    y1 = OY - 26
    o.append(f'<line x1="{X(0):.2f}" y1="{y1}" x2="{X(T):.2f}" y2="{y1}" stroke="{DIM}" '
             f'stroke-width="1.1" marker-start="{MK}" marker-end="{MK}"/>')
    o.append(f'<line x1="{X(0):.2f}" y1="{y1-5}" x2="{X(0):.2f}" y2="{Y(Y_DECK):.2f}" stroke="{DIM}" stroke-width="0.4" stroke-dasharray="2 2"/>')
    o.append(f'<line x1="{X(T):.2f}" y1="{y1-5}" x2="{X(T):.2f}" y2="{Y(Y_DECK):.2f}" stroke="{DIM}" stroke-width="0.4" stroke-dasharray="2 2"/>')
    o.append(f'<text x="{X(T/2):.2f}" y="{y1-6}" font-size="11.5" font-weight="bold" fill="{DIM}" '
             f'text-anchor="middle">LARGO DE LA SECCIÓN = {fr(T)}"  ({feet(T)})</text>')

    # ---- cadena inferior de luces
    yb = Y(POST_LEN) + 20
    marks = [0.0]
    x = 0.0
    for e in sec['elems']:
        x += POST if e[0] == 'P' else e[1]
        marks.append(x)
    for m in marks:
        o.append(f'<line x1="{X(m):.2f}" y1="{yb-6}" x2="{X(m):.2f}" y2="{yb+6}" stroke="{DIM}" stroke-width="0.6"/>')
    o.append(f'<line x1="{X(0):.2f}" y1="{yb}" x2="{X(T):.2f}" y2="{yb}" stroke="{DIM}" stroke-width="0.7"/>')
    x = 0.0
    for e in sec['elems']:
        w = POST if e[0] == 'P' else e[1]
        if e[0] == 'P':
            o.append(f'<text x="{X(x+1):.2f}" y="{yb+15}" font-size="6" font-weight="bold" '
                     f'fill="{DIM}" text-anchor="middle">2</text>')
        else:
            o.append(f'<text x="{X(x+w/2):.2f}" y="{yb-4}" font-size="8.4" font-weight="bold" '
                     f'fill="{DIM}" text-anchor="middle">{fr(w)}</text>')
        x += w

    # ---- acumulado al centro de cada poste
    ya = yb + 36
    o.append(f'<line x1="{X(0):.2f}" y1="{ya}" x2="{X(T):.2f}" y2="{ya}" stroke="#0f766e" stroke-width="0.7"/>')
    o.append(f'<text x="{X(0)-6:.2f}" y="{ya+3}" font-size="6.4" fill="#0f766e" font-weight="bold" text-anchor="end">0</text>')
    for px in posts:
        c = px + 1.0
        o.append(f'<line x1="{X(c):.2f}" y1="{ya-5}" x2="{X(c):.2f}" y2="{ya+5}" stroke="#0f766e" stroke-width="0.6"/>')
        o.append(f'<text x="{X(c):.2f}" y="{ya-8}" font-size="7" font-weight="bold" fill="#0f766e" '
                 f'text-anchor="middle">{fr(c)}</text>')

    # ---- cotas verticales izquierda
    xl = X(0) - 20
    for (a, b, txt, off) in ((0, Y_DECK, '42" GUARD', 0),):
        o.append(f'<line x1="{xl}" y1="{Y(a):.2f}" x2="{xl}" y2="{Y(b):.2f}" stroke="{DIM}" '
                 f'stroke-width="0.9" marker-start="{MK}" marker-end="{MK}"/>')
        o.append(f'<text x="{xl-5}" y="{Y((a+b)/2):.2f}" font-size="8.5" font-weight="bold" fill="{DIM}" '
                 f'transform="rotate(-90 {xl-5} {Y((a+b)/2):.2f})" text-anchor="middle">{txt}</text>')
    xl2 = X(0) - 8
    for (a, b, txt) in ((0,1,'1'), (1,39,'38'), (39,40,'1'), (40,42,'2'), (42,48,'6')):
        o.append(f'<line x1="{xl2}" y1="{Y(a):.2f}" x2="{xl2}" y2="{Y(b):.2f}" stroke="{DIM}" stroke-width="0.6"/>')
        o.append(f'<line x1="{xl2-3}" y1="{Y(a):.2f}" x2="{xl2+3}" y2="{Y(a):.2f}" stroke="{DIM}" stroke-width="0.5"/>')
        o.append(f'<line x1="{xl2-3}" y1="{Y(b):.2f}" x2="{xl2+3}" y2="{Y(b):.2f}" stroke="{DIM}" stroke-width="0.5"/>')
        o.append(f'<text x="{xl2-4}" y="{Y((a+b)/2)+2.4:.2f}" font-size="6.6" font-weight="bold" '
                 f'fill="{DIM}" text-anchor="end">{txt}</text>')
    # ---- leyenda al pie
    o.append(f'<text x="{X(0):.2f}" y="{ya+21}" font-size="7" fill="#444">'
             f'<tspan fill="{DIM}" font-weight="bold">ROJO</tspan> = luz entre caras de poste (poste = 2") '
             f'&#160;·&#160; <tspan fill="#0f766e" font-weight="bold">VERDE</tspan> = acumulado corrido al centro '
             f'de cada poste desde la punta izquierda &#160;·&#160; '
             f'<tspan fill="#8a6a42" font-weight="bold">POSTE 2×2×.090 × 48"</tspan> (42 arriba + 6 abajo)</text>')
    return "\n".join(o), MK

# ---------------------------------------------------------------- HTML
def bloque(sec):
    body, _ = svg_seccion(sec)
    nd = sum(1 for e in sec['elems'] if e[0] == 'D')
    nl = sum(1 for e in sec['elems'] if e[0] == 'L')
    npz = sum(1 for e in sec['elems'] if e[0] == 'P')
    npq = 0
    for e in sec['elems']:
        if e[0] == 'L':
            npq += piques_de(e[1])[0]
    # largo del cap: +/- 1 en cada extremo de empate recto
    cap = sec['largo']
    if 'EMPATE' in sec['der']: cap -= 1
    if sec['elems'][0][0] != 'P': cap += 1
    nota = f' &nbsp;·&nbsp; <b>{sec["nota"]}</b>' if sec['nota'] else ''
    return f"""
  <div class="drawing">
    <div class="dt"><span class="sn">SECCIÓN {sec['name']}</span>
      BALCÓN {sec['balcon']} &nbsp;·&nbsp; {fr(sec['largo'])}" ({feet(sec['largo'])}) &nbsp;·&nbsp;
      {npz} postes &nbsp;·&nbsp; {nd} dibujo{'s' if nd!=1 else ''} &nbsp;·&nbsp;
      {nl} paño{'s' if nl!=1 else ''} de piques ({npq} piques){nota}
    </div>
    <svg viewBox="0 0 {VW} {VH}" xmlns="http://www.w3.org/2000/svg">{body}</svg>
    <div class="ends"><span><b>IZQUIERDA:</b> {sec['izq']}</span><span><b>DERECHA:</b> {sec['der']}</span>
      <span><b>CAP CORRIDO:</b> {fr(cap)}"</span></div>
  </div>"""

# --- tabla de piques
filas = []
for w in sorted(anchos, reverse=True):
    veces, n, g = anchos[w]
    panel = w - 0.5
    marcas = [g + i * (1 + g) + 0.5 for i in range(n)]
    # control: el ultimo pique debe quedar a `g` de la punta derecha del panel
    assert abs((marcas[-1] + 0.5 + g) - panel) < 1e-9, ("no cierra", w)
    ms = " &nbsp;<span style='color:#c8571b'>|</span>&nbsp; ".join(fr(m, 16) for m in marcas)
    filas.append(f"<tr><td><b>{fr(w)}\"</b></td><td>{fr(panel)}\"</td><td>{veces}</td>"
                 f"<td><b>{n}</b></td><td>~{fr(g,32)}\"</td><td class='mk'>{ms}</td></tr>")
tabla_piques = "\n".join(filas)

# --- corte de los 16 dibujitos
PZ = [("V",  2, 38.0,      "1×1×1/16", "vertical del cuadro · corte recto"),
      ("B",  2, 38.0,      "1×1×1/16", "pique de flanco · corte recto"),
      ("H",  2, 28.25,     "1×1×1/16", "horizontal del cuadro · corte recto"),
      ("D1", 1, 39.9375,   "1×1×1/16", "diagonal entera · 45°/45° punta a punta"),
      ("D2", 2, 19.4375,   "1×1×1/16", "media diagonal · 45° un lado, recta el otro"),
      ("C2", 4, 19.0625,   "1×1×1/16", "rombo Q2 · 45°/45° · cara corta 17-1/16"),
      ("C3", 4, 9.3125,    "1×1×1/16", "rombo Q3 · 45°/45° · cara corta 7-5/16")]
N_DIB = tot_dib
fil2, pies = [], 0.0
for cod, q, L, sec_, desc in PZ:
    tq = q * N_DIB
    pies += tq * L / 12.0
    fil2.append(f"<tr><td><b>{cod}</b></td><td>{sec_}</td><td class='n'>{fr(L)}\"</td>"
                f"<td class='n'>{q}</td><td class='n'><b>{tq}</b></td><td>{desc}</td></tr>")
tabla_corte = "\n".join(fil2)
tiras = int(-(-pies // 20)) + 1   # tiras de 20'
print(f"1x1 para {N_DIB} dibujitos: {pies:.1f} pies  ->  ~{tiras} tiras de 20'")

res_rows = []
for bal in (1, 2):
    for run, total, secs in CORRIDAS[bal]:
        ss = " + ".join(secs)
        res_rows.append(f"<tr><td>Balcón {bal}</td><td><b>Corrida {run}</b></td>"
                        f"<td class='n'>{fr(total)}\" ({feet(total)})</td><td>{ss}</td></tr>")
res = "\n".join(res_rows)

bloques_b1 = "\n".join(bloque(s) for s in SECCIONES if s['balcon'] == 1)
bloques_b2 = "\n".join(bloque(s) for s in SECCIONES if s['balcon'] == 2)

HTML = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Secciones de Baranda — Vista de Frente</title>
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ font-family:'Segoe UI', -apple-system, Helvetica, Arial, sans-serif; color:#222; background:#fff; font-size:12px; }}
  .page {{ max-width:10.2in; margin:0 auto; padding:0.3in 0.35in; }}
  @media print {{ @page {{ size:letter landscape; margin:0.3in 0.35in; }} .page {{ padding:0; max-width:none; }}
                 .pb {{ page-break-before:always; }} .drawing {{ page-break-inside:avoid; }} }}
  .doc-header {{ display:flex; justify-content:space-between; align-items:center;
                border-bottom:3px solid #1b2a41; padding-bottom:6px; margin-bottom:8px; }}
  .doc-meta {{ text-align:right; font-size:11.5px; font-weight:700; color:#1b2a41; }}
  h1 {{ font-size:15px; color:#1b2a41; letter-spacing:.5px; }}
  .drawing {{ border:1.4px solid #1b2a41; border-radius:4px; margin:0 0 9px; }}
  .drawing .dt {{ background:#1b2a41; color:#fff; font-size:10px; padding:3px 9px; }}
  .drawing .dt .sn {{ font-size:13px; font-weight:800; letter-spacing:1px; margin-right:10px; }}
  .drawing svg {{ display:block; width:100%; height:auto; background:#fdfdfb; }}
  .ends {{ display:flex; gap:14px; font-size:9px; color:#333; padding:3px 9px;
           border-top:1px solid #dfe4ea; background:#f7f9fb; }}
  .ends span {{ flex:1; }} .ends span:last-child {{ flex:0 0 auto; color:#b91c1c; }}
  table {{ width:100%; border-collapse:collapse; margin:5px 0 10px; font-size:11px; }}
  th {{ background:#1b2a41; color:#fff; padding:4px 7px; text-align:left; }}
  td {{ border:1px solid #cfd6dd; padding:3.5px 7px; vertical-align:top; }}
  td.n {{ text-align:right; white-space:nowrap; }}
  td.mk {{ font-family:'Consolas','Courier New',monospace; font-size:10px; letter-spacing:-.2px; }}
  h2 {{ font-size:12px; color:#fff; background:#1b2a41; padding:3px 9px; margin:10px 0 5px;
        text-transform:uppercase; letter-spacing:.6px; border-radius:2px; }}
  .big {{ display:flex; gap:10px; margin:8px 0 4px; }}
  .big div {{ flex:1; border:2px solid #1b2a41; border-radius:5px; padding:7px 10px; text-align:center; }}
  .big b {{ display:block; font-size:26px; color:#b91c1c; line-height:1.1; }}
  .big span {{ font-size:10px; text-transform:uppercase; letter-spacing:.7px; color:#1b2a41; font-weight:700; }}
  .warn {{ border-left:4px solid #b91c1c; background:#fff5f5; padding:7px 11px; font-size:11px; margin:7px 0; }}
  ul {{ margin:4px 0 4px 18px; font-size:11px; }} li {{ margin:2px 0; }}
</style>
</head>
<body>
<div class="page">

  <div class="doc-header">
    <h1>BARANDA — PLANOS DE SECCIONES · VISTA DE FRENTE</h1>
    <div class="doc-meta">BALCÓN 1 + BALCÓN 2 · REV. 1 · SEPT 20, 2026<br>
    TODAS LAS SECCIONES A LA MISMA ESCALA</div>
  </div>

  <div class="big">
    <div><b>{tot_dib}</b><span>dibujitos a cortar</span></div>
    <div><b>{tot_lis}</b><span>paños de piques</span></div>
    <div><b>{tot_piq}</b><span>piques de 38"</span></div>
    <div><b>{tot_pos}</b><span>postes de 48"</span></div>
    <div><b>{len(SECCIONES)}</b><span>secciones soldadas</span></div>
  </div>

  <div class="warn"><b>OJO — falta la escalera.</b> Estos {tot_dib} dibujitos son los de los dos balcones planos.
  Los rombos de la escalera van aparte (otro ángulo, otras medidas) y no están contados aquí.
  El balcón largo de la derecha ya trae descontadas las <b>2"</b> de la esquina: corrida D = {fr(387.25)}".</div>

  <h2>Reparto de las corridas</h2>
  <table>
    <tr><th style="width:12%">Balcón</th><th style="width:14%">Corrida</th>
        <th style="width:22%">Largo total</th><th>Secciones soldadas</th></tr>
    {res}
  </table>

  <h2>Corte de los {tot_dib} dibujitos — lista completa (cortar ahora)</h2>
  <table>
    <tr><th style="width:7%">Pieza</th><th style="width:13%">Sección</th><th style="width:13%">Largo de corte</th>
        <th style="width:10%">Por dibujo</th><th style="width:11%">Total {tot_dib}</th><th>Nota</th></tr>
    {tabla_corte}
  </table>
  <p style="font-size:11px"><b>Material 1×1×1/16 para los dibujitos: {pies:.0f} pies lineales ≈ {tiras} tiras de 20'</b>
  (sin contar desperdicio de corte ni los piques de los paños lisos).</p>

  <div class="warn"><b>Los largos C2 y C3 ya llevan descontado el material de la X.</b>
  C2 = 19-1/16 punta larga / 17-1/16 cara corta. C3 = 9-5/16 punta larga / 7-5/16 cara corta.
  <b>No le quites despunte</b>: asientan a ras contra la diagonal.</div>

  <div class="pb"></div>
  <div class="doc-header">
    <h1>SECCIONES — BALCÓN 1 (el de la escalera)</h1>
    <div class="doc-meta">VISTA DE FRENTE · COTAS EN PULGADAS</div>
  </div>
{bloques_b1}

  <div class="pb"></div>
  <div class="doc-header">
    <h1>SECCIONES — BALCÓN 2 (el largo de la derecha)</h1>
    <div class="doc-meta">VISTA DE FRENTE · COTAS EN PULGADAS · CORRIDA D CON LAS 2" DESCONTADAS</div>
  </div>
{bloques_b2}

  <div class="pb"></div>
  <div class="doc-header">
    <h1>TABLA DE PIQUES — MARCAS SOBRE EL RIEL</h1>
    <div class="doc-meta">MEDIR SIEMPRE DESDE LA PUNTA IZQUIERDA DEL RIEL · NO ENCADENAR</div>
  </div>
  <table>
    <tr><th style="width:9%">Luz</th><th style="width:9%">Panel</th><th style="width:7%">Veces</th>
        <th style="width:7%">Piques</th><th style="width:9%">Luz entre piques</th>
        <th>Marcas al CENTRO de cada pique, desde la punta izquierda del riel</th></tr>
    {tabla_piques}
  </table>
  <p style="font-size:11px; margin-bottom:6px">Las marcas están redondeadas al <b>1/16</b> más cercano y cada una se
  mide <b>desde la punta izquierda del riel</b>, no de pique en pique — así el error no se acumula.
  La "luz entre piques" es solo de referencia: <b>manda la marca</b>.</p>

  <h2>Reglas que no se rompen</h2>
  <ul>
    <li><b>Todo paño decorado es idéntico: luz 46", panel 45-1/2".</b> Los {tot_dib} dibujitos son intercambiables.</li>
    <li><b>Ninguna esquina ni remate lleva dibujo.</b> Siempre paño de piques, para poder ajustar en obra.</li>
    <li><b>Marcar los piques con el flexómetro corrido</b> desde la punta izquierda del riel usando la tabla de arriba.
        No medir de pique en pique: se acumula el error.</li>
    <li><b>La sección se suelda completa con sus postes</b> y los rieles se cortan a la luz exacta.</li>
    <li><b>Los empates se hacen en el poste, nunca a media bahía</b> — ver hoja de detalles D-1 a D-4.</li>
    <li><b>Tapar el interior de los tubos antes del horno de power coating</b> o los insets no entran después.</li>
    <li><b>En obra no se suelda nada.</b> Todo empate es mecánico (tornillos SS316).</li>
  </ul>

</div>
</body>
</html>"""

open(OUT, "w", encoding="utf-8").write(HTML)
print("escrito:", OUT, len(HTML), "bytes")
