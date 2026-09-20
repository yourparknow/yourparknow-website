#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera railing-secciones-frente.html : planos de fabricacion, vista de frente,
   una seccion por bloque, con cadena de cotas completa."""
from fractions import Fraction

OUT = "/home/user/yourparknow-website/proposals/jrg-welding-corp/railing-secciones-pool-house.html"

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
# ---------------------------------------------------------------- plantilla
def PLANTILLA(titulo, meta, aviso, tot_dib, tot_lis, tot_piq, tot_pos,
              nsec, res, tabla_corte, tabla_piques, pies, tiras, cuerpo):
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>{titulo}</title>
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
    <h1>{titulo}</h1>
    <div class="doc-meta">{meta}<br>TODAS LAS SECCIONES A LA MISMA ESCALA</div>
  </div>

  <div class="big">
    <div><b>{tot_dib}</b><span>dibujitos a cortar</span></div>
    <div><b>{tot_lis}</b><span>pa&#241;os de piques</span></div>
    <div><b>{tot_piq}</b><span>piques de 38"</span></div>
    <div><b>{tot_pos}</b><span>postes de 48"</span></div>
    <div><b>{nsec}</b><span>secciones soldadas</span></div>
  </div>

  <div class="warn">{aviso}</div>

  <h2>Reparto de las corridas</h2>
  <table>
    <tr><th style="width:12%">Balc&#243;n</th><th style="width:14%">Corrida</th>
        <th style="width:22%">Largo total</th><th>Secciones soldadas</th></tr>
    {res}
  </table>

  <h2>Corte de los {tot_dib} dibujitos &#8212; lista completa</h2>
  <table>
    <tr><th style="width:7%">Pieza</th><th style="width:13%">Secci&#243;n</th><th style="width:13%">Largo de corte</th>
        <th style="width:10%">Por dibujo</th><th style="width:11%">Total {tot_dib}</th><th>Nota</th></tr>
    {tabla_corte}
  </table>
  <p style="font-size:11px"><b>Material 1&#215;1&#215;1/16 para los dibujitos: {pies} pies lineales &#8776; {tiras} tiras de 20'</b>
  (sin contar desperdicio de corte ni los piques de los pa&#241;os lisos).</p>

  <div class="warn"><b>Los largos C2 y C3 ya llevan descontado el material de la X.</b>
  C2 = 19-1/16 punta larga / 17-1/16 cara corta. C3 = 9-5/16 punta larga / 7-5/16 cara corta.
  <b>No le quites despunte</b>: asientan a ras contra la diagonal.</div>
{cuerpo}

  <div class="pb"></div>
  <div class="doc-header">
    <h1>TABLA DE PIQUES &#8212; MARCAS SOBRE EL RIEL</h1>
    <div class="doc-meta">MEDIR SIEMPRE DESDE LA PUNTA IZQUIERDA DEL RIEL &#183; NO ENCADENAR</div>
  </div>
  <table>
    <tr><th style="width:9%">Luz</th><th style="width:9%">Panel</th><th style="width:7%">Veces</th>
        <th style="width:7%">Piques</th><th style="width:9%">Luz entre piques</th>
        <th>Marcas al CENTRO de cada pique, desde la punta izquierda del riel</th></tr>
    {tabla_piques}
  </table>
  <p style="font-size:11px; margin-bottom:6px">Las marcas est&#225;n redondeadas al <b>1/16</b> m&#225;s cercano y cada una se
  mide <b>desde la punta izquierda del riel</b>, no de pique en pique &#8212; as&#237; el error no se acumula.
  La "luz entre piques" es solo de referencia: <b>manda la marca</b>.</p>

  <h2>Reglas que no se rompen</h2>
  <ul>
    <li><b>El cuadro del dibujito es siempre el mismo</b> (30-1/4 × 30-1/4, luz 28-1/4) y sus <b>17 piezas
        son id&#233;nticas en todos</b>. Casi todos van en pa&#241;o de luz 46" (panel 45-1/2").
        <b>Uno solo es distinto:</b> el de la corrida L de la caballeriza 1 va en luz 43" (panel 42-1/2"),
        con las luces de flanco apretadas a 2-9/16 en vez de 3-5/16. Mismas piezas, riel m&#225;s corto.</li>
    <li><b>Ninguna esquina lleva dibujo</b> &#8212; siempre pa&#241;o de piques, para poder ajustar en obra. <b>&#218;nica excepci&#243;n:</b> el lateral B del balc&#243;n 1 arranca con dibujo pegado a la pared de la casa.</li>
    <li><b>Marcar los piques con el flex&#243;metro corrido</b> desde la punta izquierda del riel usando la tabla de arriba.
        No medir de pique en pique: se acumula el error.</li>
    <li><b>La secci&#243;n se suelda completa con sus postes</b> y los rieles se cortan a la luz exacta.</li>
    <li><b>Los empates se hacen en el poste, nunca a media bah&#237;a</b> &#8212; ver hoja de detalles D-1 a D-4.</li>
    <li><b>Tapar el interior de los tubos antes del horno de power coating</b> o los insets no entran despu&#233;s.</li>
    <li><b>En obra no se suelda nada.</b> Todo empate es mec&#225;nico (tornillos SS316).</li>
  </ul>

</div>
</body>
</html>"""
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

def dibujito(x0, luz=46.0):
    """motif decorativo. x0 = cara del poste izquierdo, luz = ancho de la bahia.
       El CUADRO no cambia nunca (30-1/4, luz 28-1/4): solo se aprietan las luces
       de flanco, asi que las 17 piezas son iguales en todos los dibujitos."""
    o = []
    panel = luz - 2 * GAP_PANEL
    L = x0 + GAP_PANEL                 # borde del panel
    cx = x0 + luz / 2                  # centro de la bahia
    cy = 20.0                          # centro vertical del campo
    # riel inferior
    o.append(rect(L, Y_RAIL_T, panel, RAIL_T, ST_LT))
    # cadena: g + 1(B) + g + 1(V) + 28-1/4 + 1(V) + g + 1(B) + g = panel
    t_ = 1.0
    g_ = (panel - 4 * t_ - 28.25) / 4
    b1 = L + g_
    v1 = b1 + t_ + g_
    v2 = v1 + t_ + 28.25
    b2 = v2 + t_ + g_
    assert abs((b2 + t_ + g_) - (L + panel)) < 1e-9, "cadena del dibujito no cierra"
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
            o.append(dibujito(x0, luz))
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
# ---------------------------------------------------------------- datos
# elemento: ('P',) poste  |  ('D',luz) dibujo  |  ('L',luz) pano de piques
D = 46.0
def S(name, elems, izq, der, nota=""):
    return dict(name=name, elems=elems, izq=izq, der=der, nota=nota)

ESQ, EMP, PARED = "ESQUINA", "EMPATE RECTO", "REMATE CONTRA LA PARED"

# ================================ POOL HOUSE ================================
PH_B1 = [
 S("A-1", [('P',),('L',30.5625),('P',),('D',D),('P',),('L',39.5),('P',)],
   "ESQUINA ①  (arranca en el poste de esquina con C-1)", "EMPATE RECTO ③  (junta al centro del poste)"),
 S("A-2", [('D',D),('P',),('L',39.5),('P',),('D',D),('P',)],
   "EMPATE RECTO ③  (arranca en paño, apoya en el poste de A-1)", "EMPATE RECTO ⑦  (junta al centro del poste)"),
 S("A-3", [('L',39.5),('P',),('D',D),('P',),('L',30.5625),('P',)],
   "EMPATE RECTO ⑦  (arranca en paño)", "ESQUINA ②  (lleva el poste de esquina con B-1)"),
 S("B-1", [('L',28.5),('P',),('D',D),('P',),('L',28.5),('P',),('D',D),('P',)],
   "ESQUINA ②  (arranca en paño, apoya en el poste de A-2)", "REMATE CONTRA LA CASA ⑥  (placa 4×4×1/4)"),
 S("C-1", [('L',44.5),('P',),('D',D),('P',),('L',44.625),('P',)],
   "ESQUINA ①  (arranca en paño, apoya en el poste de A-1)", "EMPATE RECTO ④  (junta al centro del poste)"),
 S("C-2", [('D',D),('P',),('L',44.5),('P',)],
   "EMPATE RECTO ④  (arranca en paño)", "ARRANQUE DE ESCALERA ⑤"),
]
PH_B2 = [
 S("D-1", [('P',),('L',37.0),('P',),('D',D),('P',),('L',37.0),('P',)],
   "ESQUINA con F-1  (lleva el poste de esquina)", "EMPATE RECTO  (junta al centro del poste)"),
 S("D-2", [('D',D),('P',),('L',37.25),('P',),('D',D),('P',)],
   "EMPATE RECTO  (arranca en paño)", "EMPATE RECTO  (junta al centro del poste)"),
 S("D-3", [('L',37.0),('P',),('D',D),('P',),('L',37.0),('P',)],
   "EMPATE RECTO  (arranca en paño)", "ESQUINA con E-1  (lleva el poste de esquina)"),
 S("E-1", [('L',47.8125),('P',),('D',D),('P',),('L',47.8125),('P',)],
   "ESQUINA  (arranca en paño, apoya en el poste de D-3)", "REMATE CONTRA LA CASA  (placa 4×4×1/4)"),
 S("F-1", [('L',45.25),('P',),('D',D),('P',),('L',45.25),('P',)],
   "ESQUINA  (arranca en paño, apoya en el poste de D-1)", "EMPATE RECTO  (junta al centro del poste)"),
 S("F-2", [('D',D),('P',),('L',45.25),('P',)],
   "EMPATE RECTO  (arranca en paño)", "ARRANQUE DE ESCALERA  (198\" a 33°)"),
]

# ================================ CABALLERIZA ===============================
c1, c2, c3 = 45.5, 44.6875, 47.5625   # c1 = panos del 193 ; c2 = panos del 191-3/8
c4 = 47.75
CB = [
 S("G-1", [('P',),('D',D),('P',),('L',c1),('P',),('D',D),('P',),('L',c1),('P',)],
   "REMATE CONTRA LA PARED DE LA CABALLERIZA  (placa 4×4×1/4)", "ESQUINA con H-1  (lleva el poste de esquina)",
   "Sale de la pared con dibujo. 195\" menos las 2\" = 193\". Mide 16'-1\"."),
 S("H-1", [('L',c3),('P',),('D',D),('P',),('L',c3),('P',)],
   "ESQUINA  (arranca en paño, apoya en el poste de G-1)", "EMPATE RECTO  (junta al centro del poste)"),
 S("H-2", [('D',D),('P',),('L',c4),('P',),('D',D),('P',)],
   "EMPATE RECTO  (arranca en paño)", "EMPATE RECTO  (junta al centro del poste)"),
 S("H-3", [('L',c3),('P',),('D',D),('P',),('L',c3),('P',)],
   "EMPATE RECTO  (arranca en paño)", "ESQUINA con J-1  (lleva el poste de esquina)"),
 S("J-1", [('L',25.0),('P',),('D',D),('P',),('L',25.0),('P',)],
   "ESQUINA  (arranca en paño, apoya en el poste de H-3)", "ESQUINA con K-1  (lleva el poste de esquina)"),
 S("K-1", [('L',22.375),('P',),('D',D),('P',),('L',22.375),('P',)],
   "ESQUINA  (arranca en paño, apoya en el poste de J-1)", "ESQUINA con L-1  (lleva el poste de esquina)"),
 S("L-1", [('D',43.0),('P',)],
   "ESQUINA  (arranca en paño, apoya en el poste de K-1)", "ESQUINA con M-1  (lleva el poste de esquina)",
   "Dibujo especial de 43\" de luz: el cuadro es el mismo, solo se aprietan las luces de flanco a 2-9/16."),
 S("M-1", [('L',25.0),('P',)],
   "ESQUINA  (arranca en paño, apoya en el poste de L-1)", "REMATE CONTRA LA PARED DE LA CABALLERIZA  (placa 4×4×1/4)"),
]

# ============================== CABALLERIZA 2 ==============================
# letras N, P, Q, R -- me salto la O y la I: en plano impreso se leen como 0 y 1
n1, n2, n3 = 47.4375, 47.625, 29.125   # del croquis 1: corridas 441-3/8 y 191-3/8
CB2 = [
 S("N-1", [('L',n1),('P',),('D',D),('P',),('L',n1),('P',)],
   "ESQUINA  (arranca en paño, apoya en el poste de P-1)",
   "EMPATE RECTO  (junta al centro del poste)"),
 S("N-2", [('D',D),('P',),('L',n2),('P',),('D',D),('P',)],
   "EMPATE RECTO  (arranca en paño)", "EMPATE RECTO  (junta al centro del poste)"),
 S("N-3", [('L',n1),('P',),('D',D),('P',),('L',n1),('P',)],
   "EMPATE RECTO  (arranca en paño)", "ESQUINA con P-1  (lleva el poste de esquina)"),
 S("P-1", [('P',),('D',D),('P',),('L',c2),('P',),('D',D),('P',),('L',c2),('P',)],
   "REMATE CONTRA LA PARED DE LA CABALLERIZA  (placa 4×4×1/4)", "ESQUINA con N-1  (lleva el poste de esquina)",
   "Sale de la pared con dibujo. 193-3/8 menos las 2\" = 191-3/8."),
 S("Q-1", [('L',22.5),('P',),('D',D),('P',),('L',22.5),('P',)],
   "ESQUINA  (arranca en paño, apoya en el poste de N-3)", "HUECO DE LA ESCALERA  (27\", sigue de madera)"),
 S("R-1", [('L',44.0),('P',)],
   "ESQUINA  (arranca en paño, apoya en el poste de Q-1)",
   "REMATE CONTRA LA PARED DE LA CABALLERIZA  (placa 4×4×1/4)"),
]

def largo(sec):
    return sum(POST if e[0] == 'P' else e[1] for e in sec['elems'])

EDIFICIOS = [
 dict(slug="pool-house", titulo="POOL HOUSE — BARANDA · SECCIONES DE FRENTE",
      meta="BALCÓN 1 + BALCÓN 2 · REV. 3 · SEPT 20, 2026",
      grupos=[("POOL HOUSE — BALCÓN 1 (el de la escalera)", PH_B1),
              ("POOL HOUSE — BALCÓN 2 (el largo de la derecha)", PH_B2)],
      corridas=[("Balcón 1","A",383.625,["A-1","A-2","A-3"]), ("Balcón 1","B",159.0,["B-1"]),
                ("Balcón 1","C",237.625,["C-1","C-2"]), ("Balcón 2","D",389.25,["D-1","D-2","D-3"]),
                ("Balcón 2","E",149.625,["E-1"]), ("Balcón 2","F",239.75,["F-1","F-2"])],
      aviso="<b>OJO — esta hoja es SOLO del Pool House, y falta la escalera.</b> "
            "Los dibujitos de aquí son los de los dos balcones planos del Pool House. "
            "La caballeriza va en hoja aparte, con las letras G a la M (no se repite ninguna letra entre edificios). "
            "Los rombos de la escalera van aparte (otro ángulo, otras medidas) y no están contados aquí. "
            "Las <b>2\"</b> se descuentan en los paños que mueren contra la casa: corrida B = 159\" (161 medidas) y corrida E = 149-5/8\" (151-5/8 medidas). El largo D queda en 389-1/4\", como lo mediste."),
 dict(slug="caballeriza", titulo="CABALLERIZA — BARANDA · SECCIONES DE FRENTE",
      meta="BALCÓN EN U · REV. 1 · SEPT 20, 2026",
      grupos=[("CABALLERIZA — SECCIONES G a M", CB)],
      corridas=[("Caballeriza","G",193.0,["G-1"]), ("Caballeriza","H",442.0,["H-1","H-2","H-3"]),
                ("Caballeriza","J",104.0,["J-1"]), ("Caballeriza","K",98.75,["K-1"]),
                ("Caballeriza","L",47.0,["L-1"]), ("Caballeriza","M",29.0,["M-1"])],
      aviso="<b>OJO — esta hoja es SOLO de la caballeriza.</b> "
            "Las letras G a la M no se repiten en el Pool House, así que en el taller no hay forma de confundir "
            "dos secciones. La corrida G ya trae descontadas las <b>2\"</b> (195 − 2 = 193). "
            "<b>Falta confirmar el orden en que se encadenan las corridas</b> alrededor del edificio: "
            "los largos y el despiece no cambian, pero sí cambia cuál sección lleva cada poste de esquina."),
 dict(slug="caballeriza-2", titulo="CABALLERIZA — LADO 2 · BARANDA · SECCIONES DE FRENTE",
      meta="LADO CON EL PAÑO SIN MEDIR · REV. 2 · SEPT 20, 2026",
      grupos=[("CABALLERIZA LADO 2 — SECCIONES N a R", CB2)],
      corridas=[("Caballeriza 2","P",191.375,["P-1"]),
                ("Caballeriza 2","N",441.375,["N-1","N-2","N-3"]),
                ("Caballeriza 2","Q", 99.0,["Q-1"]),
                ("Caballeriza 2","R", 48.0,["R-1"])],
      aviso="<b>OJO — esta hoja es SOLO de la caballeriza 2, el cuarto balcón.</b> "
            "Las letras N, P, Q y R no se repiten en ninguna otra hoja. "
            "<b>Falta confirmar el orden en que se encadenan las corridas</b> alrededor del edificio: "
            "los largos y el despiece no cambian, solo cuál sección lleva cada poste de esquina. "
            "El pañito del signo de interrogación no está en esta hoja: falta medirlo."),
]

# ---------------------------------------------------------------- bloque HTML
def bloque(sec, edificio):
    body, _ = svg_seccion(sec)
    nd  = sum(1 for e in sec['elems'] if e[0] == 'D')
    nl  = sum(1 for e in sec['elems'] if e[0] == 'L')
    npz = sum(1 for e in sec['elems'] if e[0] == 'P')
    npq = sum(piques_de(e[1])[0] for e in sec['elems'] if e[0] == 'L')
    # cap corrido: solo el empate recto (junta al centro del poste) mueve el largo
    cap = sec['largo']
    if 'EMPATE' in sec['izq']: cap += 1
    if 'EMPATE' in sec['der']: cap -= 1
    nota = f' &nbsp;·&nbsp; <b>{sec["nota"]}</b>' if sec['nota'] else ''
    return f"""
  <div class="drawing">
    <div class="dt"><span class="sn">SECCIÓN {sec['name']}</span>
      {edificio} &nbsp;·&nbsp; {fr(sec['largo'])}" ({feet(sec['largo'])}) &nbsp;·&nbsp;
      {npz} poste{'s' if npz != 1 else ''} &nbsp;·&nbsp; {nd} dibujo{'s' if nd != 1 else ''} &nbsp;·&nbsp;
      {nl} paño{'s' if nl != 1 else ''} de piques ({npq} piques){nota}
    </div>
    <svg viewBox="0 0 {VW} {VH}" xmlns="http://www.w3.org/2000/svg">{body}</svg>
    <div class="ends"><span><b>IZQUIERDA:</b> {sec['izq']}</span><span><b>DERECHA:</b> {sec['der']}</span>
      <span><b>CAP CORRIDO:</b> {fr(cap)}"</span></div>
  </div>"""

PZ = [("V",  2, 38.0,    "vertical del cuadro · corte recto"),
      ("B",  2, 38.0,    "pique de flanco · corte recto"),
      ("H",  2, 28.25,   "horizontal del cuadro · corte recto"),
      ("D1", 1, 39.9375, "diagonal entera · 45°/45° punta a punta"),
      ("D2", 2, 19.4375, "media diagonal · 45° un lado, recta el otro"),
      ("C2", 4, 19.0625, "rombo Q2 · 45°/45° · cara corta 17-1/16"),
      ("C3", 4, 9.3125,  "rombo Q3 · 45°/45° · cara corta 7-5/16")]

def build(cfg):
    secs = [s for _, g in cfg['grupos'] for s in g]
    by = {}
    for s in secs:
        s['largo'] = largo(s)
        assert s['name'] not in by, ("letra repetida", s['name'])
        by[s['name']] = s

    # --- verificacion: cada corrida tiene que cerrar contra la medida de obra
    print(f"\n== {cfg['slug'].upper()} ==")
    for _, run, total, names in cfg['corridas']:
        suma = sum(by[n]['largo'] for n in names)
        got = suma + (2.0 if by[names[0]]['elems'][0][0] != 'P' else 0.0)
        assert abs(got - total) < 1e-9, (run, got, total)
        print(f"  corrida {run}: secciones {suma:8.4f} + esquina = {got:8.4f}  vs medido {total:8.4f}  OK")

    tot_dib = sum(1 for s in secs for e in s['elems'] if e[0] == 'D')
    tot_lis = sum(1 for s in secs for e in s['elems'] if e[0] == 'L')
    tot_pos = sum(1 for s in secs for e in s['elems'] if e[0] == 'P')
    tot_piq, anchos = 0, {}
    for s in secs:
        for e in s['elems']:
            if e[0] == 'L':
                n, g = piques_de(e[1]); tot_piq += n
                anchos.setdefault(e[1], [0, n, g]); anchos[e[1]][0] += 1
    print(f"  {tot_dib} dibujitos · {tot_lis} paños ({tot_piq} piques) · {tot_pos} postes · {len(secs)} secciones")

    # --- tabla de piques (marcas corridas, no encadenadas)
    filas = []
    for w in sorted(anchos, reverse=True):
        veces, n, g = anchos[w]
        panel = w - 0.5
        marcas = [g + i * (1 + g) + 0.5 for i in range(n)]
        assert abs((marcas[-1] + 0.5 + g) - panel) < 1e-9, ("no cierra", w)
        ms = " &nbsp;<span style='color:#c8571b'>|</span>&nbsp; ".join(fr(m, 16) for m in marcas)
        filas.append(f"<tr><td><b>{fr(w)}\"</b></td><td>{fr(panel)}\"</td><td>{veces}</td>"
                     f"<td><b>{n}</b></td><td>~{fr(g,32)}\"</td><td class='mk'>{ms}</td></tr>")
    tabla_piques = "\n".join(filas)

    # --- corte de los dibujitos
    fil2, pies = [], 0.0
    for cod, q, Lg, desc in PZ:
        tq = q * tot_dib
        pies += tq * Lg / 12.0
        fil2.append(f"<tr><td><b>{cod}</b></td><td>1×1×1/16</td><td class='n'>{fr(Lg)}\"</td>"
                    f"<td class='n'>{q}</td><td class='n'><b>{tq}</b></td><td>{desc}</td></tr>")
    tabla_corte = "\n".join(fil2)
    tiras = int(-(-pies // 20)) + 1

    res = "\n".join(f"<tr><td>{et}</td><td><b>Corrida {run}</b></td>"
                    f"<td class='n'>{fr(total)}\" ({feet(total)})</td><td>{' + '.join(nm)}</td></tr>"
                    for et, run, total, nm in cfg['corridas'])

    cuerpo = ""
    for i, (h1, grupo) in enumerate(cfg['grupos']):
        cuerpo += f"""
  <div class="pb"></div>
  <div class="doc-header">
    <h1>{h1}</h1>
    <div class="doc-meta">VISTA DE FRENTE · COTAS EN PULGADAS</div>
  </div>
""" + "\n".join(bloque(s, h1.split("—")[0].strip()) for s in grupo)

    html = PLANTILLA(titulo=cfg['titulo'], meta=cfg['meta'], aviso=cfg['aviso'],
                     tot_dib=tot_dib, tot_lis=tot_lis, tot_piq=tot_piq, tot_pos=tot_pos,
                     nsec=len(secs), res=res, tabla_corte=tabla_corte,
                     tabla_piques=tabla_piques, pies=f"{pies:.0f}", tiras=tiras,
                     cuerpo=cuerpo)
    out = f"/home/user/yourparknow-website/proposals/jrg-welding-corp/railing-secciones-{cfg['slug']}.html"
    open(out, "w", encoding="utf-8").write(html)
    print(f"  escrito: {out}  ({pies:.0f} pies de 1×1 ≈ {tiras} tiras de 20')")
    return tot_dib

if __name__ == "__main__":
    total = sum(build(c) for c in EDIFICIOS)
    print(f"\nTOTAL DIBUJITOS (sin la escalera): {total}")
