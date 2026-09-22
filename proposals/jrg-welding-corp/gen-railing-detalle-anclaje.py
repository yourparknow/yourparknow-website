#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DETALLE DE ANCLAJE de los postes.
   El poste de esquina no tiene fascia plana detras de ninguna de sus dos caras:
   queda por fuera de las dos. Por eso lleva DOS OREJAS en L, una por cara.
   Los dos tornillos de cada oreja van UNO ENCIMA DEL OTRO para que los dos
   queden lejos de la punta del rim (ahi es donde raja la madera)."""
import importlib.util, pathlib

HERE = pathlib.Path("/home/user/yourparknow-website/proposals/jrg-welding-corp")
spec = importlib.util.spec_from_file_location("gsec", HERE / "gen-railing-secciones.py")
G = importlib.util.module_from_spec(spec); spec.loader.exec_module(G)
fr = G.fr

NEG, ROJO, VERDE, NAR = "#1b2a41", "#b91c1c", "#0f766e", "#c8571b"
MAD, MAD2 = "#e4d5b7", "#c9b48d"        # fascia / rim
ALU = "#9fb0c0"                          # aluminio

# ------------------------------------------------------------------ la oreja
# Rene no quiere tornillo pasante: no sabe que hay detras de la fascia.  Va
# TIRAFONDO, que enrosca en la madera y no sale por el otro lado.  Eso obliga
# a revisar el arranque, porque un tirafondo aguanta mucho menos que un pasante.
OREJA_L  = 3.5      # largo de la oreja, hacia adentro del deck
OREJA_H  = 5.5      # alto de la oreja. No crece con la fascia: los tirafondos
                    # siguen a 3" y 5" bajo el deck, que es donde hace el par.
OREJA_E  = 0.25     # espesor
BORDE    = 2.25     # del filo de la esquina al eje de los tirafondos
TORN     = 0.5      # tirafondo de 1/2"
TORN_L   = 5.0      # largo del tirafondo
ROSCA    = 3.25     # rosca que queda metida en madera solida
PROF     = (3.0, 5.0)   # a que profundidad va cada tirafondo, bajo el piso del deck
SEP_V    = PROF[1] - PROF[0]
BAJA     = G.EMBED  # lo que baja el poste por debajo del deck. Sale del dato,
                    # no tecleado: Rene midio la fascia en obra y los postes
                    # salieron de 51, o sea que bajan 10, no 6.
RIM      = 2.5      # fascia + rim joist
BLOQUEO  = 3.0      # bloqueo solido detras del rim: dos 2x juntos

# ---- carga de codigo: 200 lb empujando arriba del poste, en cualquier direccion
CARGA, ALTO = 200.0, 42.0
MOM = CARGA * ALTO
_s = sum(d * d for d in PROF)
TIRO = MOM * max(PROF) / _s          # lo que tira el tirafondo de abajo
# NDS, arranque de tirafondo: W = 1800 x G^1.5 x D^0.75, por pulgada de rosca.
# G = 0.55 es pino del sur tratado, que es de lo que se hacen los decks aqui.
G_SYP, G_SPF = 0.55, 0.42
def _cap(G): return 1800 * G ** 1.5 * TORN ** 0.75 * ROSCA
CAP_SYP, CAP_SPF = _cap(G_SYP), _cap(G_SPF)

assert CAP_SYP > TIRO, "en pino tratado el tirafondo NO da: hay que bajar mas el poste"
assert OREJA_H + 0.5 <= BAJA, "la oreja no cabe en lo que baja el poste"
assert BORDE + TORN * 1.5 <= OREJA_L, "el agujero queda muy al filo de la oreja"
assert max(PROF) + TORN * 2 <= 0.5 + OREJA_H, "el tirafondo de abajo se sale de la oreja"
assert min(PROF) - TORN * 2 >= 0.5, "el tirafondo de arriba se sale de la oreja"
assert BORDE / TORN >= 4.0, "el tirafondo queda muy cerca de la punta del rim: raja"
assert TORN_L <= OREJA_E + 1.0 + RIM - 1.0 + BLOQUEO, "el tirafondo sale por el otro lado"

# ============================================================ VISTA EN PLANTA
def planta():
    k = 24.0
    OX, OY = 430.0, 210.0                      # la esquina del deck, en pantalla
    def sx(x): return OX + x * k
    def sy(y): return OY - y * k
    def R(x0, y0, x1, y1, f, s=NEG, w=1.2):
        return (f'<rect x="{sx(min(x0,x1)):.1f}" y="{sy(max(y0,y1)):.1f}" '
                f'width="{abs(x1-x0)*k:.1f}" height="{abs(y1-y0)*k:.1f}" '
                f'fill="{f}" stroke="{s}" stroke-width="{w}"/>')
    o = ['<svg viewBox="0 0 792 470" xmlns="http://www.w3.org/2000/svg">',
         '<defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" '
         f'markerHeight="5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{ROJO}"/>'
         '</marker>'
         '<pattern id="blq" width="7" height="7" patternTransform="rotate(45)" '
         'patternUnits="userSpaceOnUse"><line x1="0" y1="0" x2="0" y2="7" '
         'stroke="#8a7350" stroke-width="2"/></pattern></defs>']

    # --- fascia + rim, en L alrededor de la esquina
    o.append(R(-8, -RIM, 0, 0, MAD))
    o.append(R(-RIM, -8, 0, -RIM, MAD))
    o.append(f'<text x="{sx(-5.2):.0f}" y="{sy(-1.5):.0f}" font-size="11.5" '
             f'text-anchor="middle" fill="#6b5734">FASCIA + RIM</text>')

    # --- bloqueo solido que hay que meter en obra
    o.append(R(-7.6, -5.0, -RIM, -RIM, "url(#blq)", "#8a7350", 1.2))
    o.append(R(-5.0, -8.0, -RIM, -5.0, "url(#blq)", "#8a7350", 1.2))   # y en la otra direccion
    o.append(f'<text x="{sx(-5.9):.0f}" y="{sy(-5.9):.0f}" font-size="11.5" font-weight="800" '
             f'text-anchor="middle" fill="#8a5a17">BLOQUEO S&#211;LIDO</text>')
    o.append(f'<text x="{sx(-5.9):.0f}" y="{sy(-6.55):.0f}" font-size="10.5" '
             f'text-anchor="middle" fill="#8a5a17">dos 2&#215; juntos &#183; lo mete el carpintero</text>')

    # --- por donde corre cada baranda
    o.append(f'<line x1="{sx(-8):.1f}" y1="{sy(1):.1f}" x2="{sx(-0.1):.1f}" y2="{sy(1):.1f}" '
             f'stroke="{NEG}" stroke-width="6" opacity=".22"/>')
    o.append(f'<line x1="{sx(1):.1f}" y1="{sy(-0.1):.1f}" x2="{sx(1):.1f}" y2="{sy(-8):.1f}" '
             f'stroke="{NEG}" stroke-width="6" opacity=".22"/>')
    o.append(f'<text x="{sx(-5.4):.0f}" y="{sy(1)-10:.0f}" font-size="11" text-anchor="middle" '
             f'fill="{NEG}" opacity=".75">BARANDA</text>')
    o.append(f'<text x="{sx(1.5):.0f}" y="{sy(-5.4):.0f}" font-size="11" text-anchor="start" '
             f'fill="{NEG}" opacity=".75">BARANDA</text>')

    # --- las dos orejas, en el plano de cada fascia
    o.append(R(-OREJA_L, 0, 0, OREJA_E, ALU, ROJO, 2.2))
    o.append(R(0, -OREJA_L, OREJA_E, 0, ALU, ROJO, 2.2))
    # --- el poste, por fuera de las dos fascias
    o.append(R(0, 0, 2, 2, ALU, NEG, 2.2))
    o.append(f'<text x="{sx(1):.0f}" y="{sy(1)+4:.0f}" font-size="12" font-weight="800" '
             f'text-anchor="middle" fill="{NEG}">2&#215;2</text>')

    # --- los tornillos (en planta se ve uno: el otro va debajo)
    for cx, cy in ((-BORDE, OREJA_E/2), (OREJA_E/2, -BORDE)):
        o.append(f'<circle cx="{sx(cx):.1f}" cy="{sy(cy):.1f}" r="{TORN*k/2:.1f}" '
                 f'fill="#fff" stroke="{ROJO}" stroke-width="2"/>')
        o.append(f'<line x1="{sx(cx)-12:.1f}" y1="{sy(cy):.1f}" x2="{sx(cx)+12:.1f}" '
                 f'y2="{sy(cy):.1f}" stroke="{ROJO}" stroke-width="0.7"/>')
        o.append(f'<line x1="{sx(cx):.1f}" y1="{sy(cy)-12:.1f}" x2="{sx(cx):.1f}" '
                 f'y2="{sy(cy)+12:.1f}" stroke="{ROJO}" stroke-width="0.7"/>')

    # --- cotas arriba del poste
    def cotaH(x0, x1, y, t):
        yy = sy(y)
        return (f'<line x1="{sx(x0):.1f}" y1="{yy:.1f}" x2="{sx(x1):.1f}" y2="{yy:.1f}" '
                f'stroke="{ROJO}" stroke-width="1.2" marker-start="url(#a)" marker-end="url(#a)"/>'
                f'<text x="{sx((x0+x1)/2):.1f}" y="{yy-6:.1f}" font-size="13" '
                f'font-weight="800" fill="{ROJO}" text-anchor="middle">{t}</text>')
    o.append(cotaH(-OREJA_L, 0, 2.6, f'{fr(OREJA_L)}"'))
    o.append(cotaH(-BORDE, 0, 3.7, f'{fr(BORDE)}"'))
    o.append(f'<text x="{sx(-1.12):.0f}" y="{sy(4.25):.0f}" font-size="10.5" fill="{ROJO}" '
             f'text-anchor="middle">al eje de los tirafondos</text>')
    for x in (-OREJA_L, -BORDE, 0.0):
        o.append(f'<line x1="{sx(x):.1f}" y1="{sy(0.35):.1f}" x2="{sx(x):.1f}" y2="{sy(3.85):.1f}" '
                 f'stroke="{ROJO}" stroke-width="0.6" stroke-dasharray="3 3"/>')

    # --- rotulos con guia, todos dentro de la hoja
    def guia(px, py, tx, ty, txt, anc):
        dx = 6 if anc == "start" else -6
        return (f'<line x1="{sx(px):.1f}" y1="{sy(py):.1f}" x2="{tx+dx}" y2="{ty}" '
                f'stroke="{ROJO}" stroke-width="0.9"/>'
                f'<circle cx="{sx(px):.1f}" cy="{sy(py):.1f}" r="2.4" fill="{ROJO}"/>'
                f'<text x="{tx}" y="{ty+4}" font-size="11.5" '
                f'font-weight="700" fill="{ROJO}" text-anchor="{anc}">{txt}</text>')
    o.append(guia(-1.5, OREJA_E, 545, 120, 'OREJA 1/4" &#215; 3-1/2" &#215; 5-1/2" DE ALTO', "start"))
    o.append(guia(OREJA_E, -1.5, 545, 300, "LA OTRA OREJA, IGUAL", "start"))
    o.append(guia(-BORDE, OREJA_E/2, 250, 120, "2 TIRAFONDOS, UNO ENCIMA DEL OTRO", "end"))

    o.append(f'<text x="396" y="456" font-size="13" font-weight="800" text-anchor="middle" '
             f'fill="{NEG}">EN PLANTA &#183; POSTE DE ESQUINA</text>')
    o.append('</svg>')
    return "".join(o)


# =============================================================== VISTA DE LADO
def alzado():
    k = 26.0
    OX, OY = 330.0, 175.0                      # OY = cara de arriba del deck
    def sx(x): return OX + x * k
    def sy(y): return OY - y * k
    def R(x0, y0, x1, y1, f, s=NEG, w=1.2):
        return (f'<rect x="{sx(min(x0,x1)):.1f}" y="{sy(max(y0,y1)):.1f}" '
                f'width="{abs(x1-x0)*k:.1f}" height="{abs(y1-y0)*k:.1f}" '
                f'fill="{f}" stroke="{s}" stroke-width="{w}"/>')
    o = ['<svg viewBox="0 0 792 434" xmlns="http://www.w3.org/2000/svg">',
         '<defs><marker id="b" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" '
         f'markerHeight="5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{ROJO}"/>'
         '</marker></defs>']

    # --- deck y rim.  OJO: los dos se acaban en la esquina (x = 0)
    o.append(R(-9.2, 0, 0, 0.85, MAD2))
    o.append(R(-9.2, -BAJA - 1.5, 0, 0, MAD))
    o.append(f'<text x="{sx(-4.6):.0f}" y="{sy(0.28):.0f}" font-size="11" fill="#6b5734" '
             f'text-anchor="middle">PISO DEL DECK</text>')
    o.append(f'<text x="{sx(-7.6):.0f}" y="{sy(-6.15):.0f}" font-size="11.5" '
             f'text-anchor="middle" fill="#6b5734">RIM + FASCIA</text>')
    o.append(f'<text x="{sx(-7.6):.0f}" y="{sy(-6.8):.0f}" font-size="10.5" '
             f'text-anchor="middle" fill="#6b5734">(2&#215;8 m&#237;nimo)</text>')

    # --- poste, cortado arriba
    o.append(R(0, -BAJA, 2, 8.4, ALU, NEG, 2.2))
    o.append(f'<path d="M {sx(0):.1f} {sy(7.5):.1f} q {k*0.5:.1f} {-k*0.32:.1f} {k:.1f} 0 '
             f'q {k*0.5:.1f} {k*0.32:.1f} {k:.1f} 0" fill="none" stroke="{NEG}" stroke-width="1.6"/>')
    o.append(f'<text x="{sx(1):.0f}" y="{sy(5.0):.0f}" font-size="12" font-weight="800" '
             f'text-anchor="middle" fill="{NEG}">POSTE</text>')
    o.append(f'<text x="{sx(1):.0f}" y="{sy(4.2):.0f}" font-size="10.5" '
             f'text-anchor="middle" fill="{NEG}">2&#215;2&#215;.090</text>')

    # --- lo que explica todo: detras del poste no hay madera
    o.append(f'<line x1="{sx(2.25):.1f}" y1="{sy(-5.9):.1f}" x2="{sx(5.4):.1f}" y2="{sy(-5.9):.1f}" '
             f'stroke="{ROJO}" stroke-width="0.9"/>')
    o.append(f'<text x="{sx(5.6):.0f}" y="{sy(-5.75):.0f}" font-size="11.5" font-weight="800" '
             f'fill="{ROJO}">DETR&#193;S DEL POSTE NO HAY MADERA:</text>')
    o.append(f'<text x="{sx(5.6):.0f}" y="{sy(-6.35):.0f}" font-size="11.5" font-weight="800" '
             f'fill="{ROJO}">la fascia se acab&#243; en la esquina</text>')

    # --- oreja
    y0 = -0.5
    y1 = y0 - OREJA_H
    o.append(R(-OREJA_L, y1, 0, y0, ALU, ROJO, 2.4))
    o.append(f'<line x1="{sx(0):.1f}" y1="{sy(y0):.1f}" x2="{sx(0):.1f}" y2="{sy(y1):.1f}" '
             f'stroke="{ROJO}" stroke-width="5"/>')
    o.append(f'<line x1="{sx(0):.1f}" y1="{sy((y0+y1)/2):.1f}" x2="{sx(2.6):.1f}" '
             f'y2="{sy(-1.35):.1f}" stroke="{ROJO}" stroke-width="0.9"/>')
    o.append(f'<text x="{sx(2.8):.0f}" y="{sy(-1.2):.0f}" font-size="11.5" font-weight="800" '
             f'fill="{ROJO}">SOLDADA AL POSTE, CORD&#211;N CORRIDO</text>')

    # --- tornillos
    yb1, yb2 = -PROF[0], -PROF[1]
    for yb in (yb1, yb2):
        o.append(f'<circle cx="{sx(-BORDE):.1f}" cy="{sy(yb):.1f}" r="{TORN*k/2:.1f}" '
                 f'fill="#fff" stroke="{ROJO}" stroke-width="2"/>')
        o.append(f'<line x1="{sx(-BORDE)-13:.1f}" y1="{sy(yb):.1f}" x2="{sx(-BORDE)+13:.1f}" '
                 f'y2="{sy(yb):.1f}" stroke="{ROJO}" stroke-width="0.7"/>')
        o.append(f'<line x1="{sx(-BORDE):.1f}" y1="{sy(yb)-13:.1f}" x2="{sx(-BORDE):.1f}" '
                 f'y2="{sy(yb)+13:.1f}" stroke="{ROJO}" stroke-width="0.7"/>')

    # --- cotas verticales, escalonadas para que no se pisen
    def cotaV(x, ya, yb, t, sub=None):
        e = (f'<line x1="{sx(x):.1f}" y1="{sy(ya):.1f}" x2="{sx(x):.1f}" y2="{sy(yb):.1f}" '
             f'stroke="{ROJO}" stroke-width="1.2" marker-start="url(#b)" marker-end="url(#b)"/>'
             f'<text x="{sx(x)-7:.1f}" y="{sy((ya+yb)/2)+4:.1f}" font-size="13" font-weight="800" '
             f'fill="{ROJO}" text-anchor="end">{t}</text>')
        if sub:
            e += (f'<text x="{sx(x)-7:.1f}" y="{sy((ya+yb)/2)+18:.1f}" font-size="10.5" '
                  f'fill="{ROJO}" text-anchor="end">{sub}</text>')
        return e
    o.append(cotaV(-OREJA_L - 0.7, y0, y1, f'{fr(OREJA_H)}"'))
    o.append(cotaV(-OREJA_L - 3.1, yb1, yb2, f'{fr(SEP_V)}"', "entre tornillos"))
    for y in (y0, y1, yb1, yb2):
        o.append(f'<line x1="{sx(-OREJA_L-3.3):.1f}" y1="{sy(y):.1f}" x2="{sx(-OREJA_L+0.2):.1f}" '
                 f'y2="{sy(y):.1f}" stroke="{ROJO}" stroke-width="0.5" stroke-dasharray="3 3"/>')

    # --- cotas a la derecha
    def cotaD(ya, yb, t, sub=None):
        x = 5.0
        e = (f'<line x1="{sx(x):.1f}" y1="{sy(ya):.1f}" x2="{sx(x):.1f}" y2="{sy(yb):.1f}" '
             f'stroke="{ROJO}" stroke-width="1.2" marker-start="url(#b)" marker-end="url(#b)"/>'
             f'<text x="{sx(x)+8:.1f}" y="{sy((ya+yb)/2)+4:.1f}" font-size="13" font-weight="800" '
             f'fill="{ROJO}">{t}</text>')
        if sub:
            e += (f'<text x="{sx(x)+8:.1f}" y="{sy((ya+yb)/2)+18:.1f}" font-size="10.5" '
                  f'fill="{ROJO}">{sub}</text>')
        return e
    o.append(cotaD(-BAJA, 0, f'{fr(BAJA)}"', "baja el poste"))
    o.append(cotaD(0, 7.2, '42"', "arriba del deck (cortado)"))
    for y in (0.0, -BAJA):
        o.append(f'<line x1="{sx(-9.2):.1f}" y1="{sy(y):.1f}" x2="{sx(5.2):.1f}" y2="{sy(y):.1f}" '
                 f'stroke="{ROJO}" stroke-width="0.5" stroke-dasharray="3 3"/>')

    o.append(f'<text x="396" y="420" font-size="13" font-weight="800" text-anchor="middle" '
             f'fill="{NEG}">DE LADO &#183; LA MISMA OREJA</text>')
    o.append('</svg>')
    return "".join(o)


# ------------------------------------------------------------------ cantidades
esquinas = []
for cfg in G.EDIFICIOS:
    for _, gr in cfg['grupos']:
        for s in gr:
            for txt in (s['izq'], s['der']):
                # OJO: A-1 dice "arranca en el poste de esquina con C-1", que tambien
                # es llevar el poste. Antes se colaba por no decir "lleva el poste"
                # y ese poste de esquina se quedaba sin orejas.
                if "ESQUINA" in txt and ("lleva el poste" in txt or "arranca en el poste" in txt):
                    esquinas.append((s['name'], cfg['slug']))
NE = len(esquinas)
NOMB = {"pool-house": "Pool House", "caballeriza": "Caballeriza 1", "caballeriza-2": "Caballeriza 2"}
filas = "".join(
    f"<tr><td><b>{n}</b></td><td>{NOMB[sl]}</td><td>2 orejas</td><td>4 tirafondos 1/2&#215;5</td></tr>"
    for n, sl in esquinas)

pies_barra = NE * 2 * OREJA_H / 12.0

HTML = f"""<!DOCTYPE html><html lang="es"><head><meta charset="UTF-8">
<title>Detalle de anclaje de los postes</title><style>
 *{{margin:0;padding:0;box-sizing:border-box}}
 body{{font-family:'Segoe UI',-apple-system,Helvetica,Arial,sans-serif;color:{NEG};background:#fff;font-size:13px}}
 .page{{max-width:10.2in;margin:0 auto;padding:.3in .35in}}
 @media print{{@page{{size:letter landscape;margin:.3in .35in}}.page{{padding:0;max-width:none}}
              .pb{{page-break-before:always}}.dw{{page-break-inside:avoid}}}}
 .hd{{display:flex;justify-content:space-between;align-items:center;border-bottom:4px solid {NEG};
     padding-bottom:6px;margin-bottom:10px}}
 h1{{font-size:20px;letter-spacing:.5px}} .hd .m{{font-size:12px;font-weight:700;text-align:right}}
 .dw{{border:2px solid {NEG};border-radius:5px;margin-bottom:12px}}
 .dw .dt{{background:{NEG};color:#fff;font-size:13px;padding:5px 11px;font-weight:700}}
 .dw svg{{display:block;width:100%;height:auto;background:#fff}}
 table{{width:100%;border-collapse:collapse;font-size:12.5px;margin-bottom:10px}}
 th{{background:#41505f;color:#fff;padding:4px 9px;text-align:left;font-size:11px}}
 td{{border:1px solid #d3dae1;padding:4px 9px}}
 .warn{{border-left:5px solid {ROJO};background:#fff5f5;padding:9px 13px;font-size:12.5px;margin:9px 0}}
 .big{{display:flex;gap:10px;margin:9px 0}}
 .big div{{flex:1;border:2px solid {NEG};border-radius:5px;padding:7px 10px;text-align:center}}
 .big b{{display:block;font-size:26px;color:{ROJO};line-height:1.1}}
 .big span{{font-size:10px;text-transform:uppercase;letter-spacing:.7px;font-weight:700}}
 ul{{margin:5px 0 5px 20px}} li{{margin:3px 0}}
</style></head><body><div class="page">

  <div class="hd"><h1>DETALLE DE ANCLAJE &#8212; POSTE DE ESQUINA</h1>
    <div class="m">OREJAS SOLDADAS EN L<br>LOS {NE} POSTES DE ESQUINA DE LOS 4 BALCONES</div></div>

  <div class="big">
    <div><b>{NE}</b><span>postes de esquina</span></div>
    <div><b>{NE*2}</b><span>orejas</span></div>
    <div><b>{NE*2*2}</b><span>tirafondos 1/2&#215;5</span></div>
    <div><b>{fr(OREJA_L)}&#215;{fr(OREJA_H)}</b><span>cada oreja, 1/4"</span></div>
  </div>

  <div class="warn"><b>Por qu&#233; el poste de esquina lleva orejas y los dem&#225;s no.</b>
  El poste va por fuera de la fascia, atornillado contra ella. En la esquina, la fascia de un lado
  se acaba y la del otro tambi&#233;n: el poste queda por fuera de las dos y <b>no toca madera por
  ninguna de sus dos caras</b>. Las orejas son las que alcanzan la madera.</div>

  <div class="dw"><div class="dt">1 &#183; EN PLANTA &#8212; se ven las dos orejas</div>{planta()}</div>

  <div class="pb"></div>
  <div class="hd"><h1>DETALLE DE ANCLAJE &#8212; DE LADO</h1>
    <div class="m">LOS DOS TIRAFONDOS VAN UNO ENCIMA DEL OTRO</div></div>

  <div class="dw"><div class="dt">2 &#183; DE LADO &#8212; la oreja dentro de las 6" que baja el poste</div>{alzado()}</div>

  <div class="warn"><b>Los dos tirafondos van uno encima del otro, no uno al lado del otro.</b>
  As&#237; los dos quedan a <b>{fr(BORDE)}" de la punta del rim</b> ({BORDE/TORN:.0f} di&#225;metros)
  y la madera no se abre. Y de paso, separados en vertical, son los que hacen la pareja que
  aguanta el empuj&#243;n de arriba del poste: el de abajo tira y el poste apoya contra la fascia
  arriba.</div>

  <h2 style="font-size:13px;background:{NEG};color:#fff;padding:4px 10px;margin:11px 0 6px">
    La cuenta del tirafondo</h2>
  <table>
    <tr><th style="width:52%">Concepto</th><th style="width:24%">Valor</th><th>De d&#243;nde sale</th></tr>
    <tr><td>Empuje de c&#243;digo arriba del poste</td><td><b>{CARGA:.0f} lb</b></td>
        <td>guarda residencial, en cualquier direcci&#243;n</td></tr>
    <tr><td>Momento en la l&#237;nea del deck</td><td><b>{MOM:.0f} lb&#183;pulg</b></td>
        <td>{CARGA:.0f} lb &#215; {ALTO:.0f}"</td></tr>
    <tr><td><b>Tiro del tirafondo de abajo</b> (a {fr(max(PROF))}" bajo el deck)</td>
        <td><b style="color:{ROJO}">{TIRO:.0f} lb</b></td>
        <td>el poste apoya arriba y el de abajo tira</td></tr>
    <tr><td>Aguanta un {fr(TORN)}" con {fr(ROSCA)}" de rosca en <b>pino del sur tratado</b></td>
        <td><b style="color:#0f766e">{CAP_SYP:.0f} lb</b></td><td>NDS, arranque, G=0.55</td></tr>
    <tr style="background:#fff5f5"><td>Lo mismo pero en <b>abeto blando (SPF)</b></td>
        <td><b style="color:{ROJO}">{CAP_SPF:.0f} lb</b></td>
        <td><b>NO DA</b> &#8212; ver la nota de abajo</td></tr>
  </table>

  <div class="warn"><b>Esto sirve si el rim es pino del sur tratado</b>, que es de lo que se hacen
  los decks aqu&#237;. Aguanta {CAP_SYP:.0f} lb contra las {TIRO:.0f} que le pide el c&#243;digo:
  pasa con {100*(CAP_SYP/TIRO-1):.0f}% de holgura. <b>Si el rim resulta ser abeto blando</b>
  (madera clara, blandita, del norte), <b>solo aguanta {CAP_SPF:.0f} lb y NO da.</b> En ese caso
  hay que <b>bajar el poste 9" en vez de 6"</b> y correr el tirafondo de abajo a 8": ah&#237; el
  tiro baja a 755 lb y vuelve a dar. <b>M&#237;rale la madera al rim antes de empezar a taladrar.</b></div>

  <h2 style="font-size:13px;background:{NEG};color:#fff;padding:4px 10px;margin:11px 0 6px">
    C&#243;mo se hace</h2>
  <ul>
    <li><b>Oreja:</b> placa de aluminio <b>6061-T6 de 1/4"</b>, <b>{fr(OREJA_L)}" de largo
        &#215; {fr(OREJA_H)}" de alto</b>. Sale de barra plana de 1/4"&#215;{fr(OREJA_H)}" cortada
        a {fr(OREJA_L)}. Hacen falta <b>{pies_barra:.1f} pies</b> de esa barra.</li>
    <li><b>Se suelda</b> a ras de la cara del poste, cord&#243;n corrido por los dos cantos,
        dentro de las {fr(BAJA)}" que el poste baja por debajo del deck. Arriba queda 1/2" libre
        para que la oreja no choque con el piso del deck.</li>
    <li><b>Las dos orejas miran hacia adentro del deck</b>, una por cada cara del poste que da a
        una fascia. Quedan en L. En taller se sueldan las dos antes de pintar.</li>
    <li><b>Tirafondos:</b> <b>{fr(TORN)}" &#215; {fr(TORN_L)}" inoxidable 316</b>, que enroscan en la
        madera. <b>NO son pasantes</b>: no salen por el otro lado, as&#237; que no importa lo que
        haya detr&#225;s de la fascia. <b>Hay que pretaladrar</b>: agujero gu&#237;a de 5/16" en la
        madera y de 9/16" en la oreja. Sin pretaladrar, la madera raja y el tirafondo no agarra.</li>
    <li><b>Bloqueo:</b> en cada esquina, <b>dos 2&#215; clavados juntos</b> ({fr(BLOQUEO)}" de grueso)
        detr&#225;s del rim, en las dos direcciones. <b>De esto depende todo el anclaje:</b> el
        tirafondo necesita {fr(ROSCA)}" de rosca en madera s&#243;lida y el rim solo le da 1-1/2".</li>
    <li><b>El rim tiene que ser 2&#215;8 o m&#225;s</b>, para que quepan las {fr(BAJA)}" que baja el
        poste con la oreja adentro.</li>
  </ul>

  <div class="warn"><b>Si el trabajo lleva permiso:</b> el poste de guarda se calcula con
  <b>200 lb empujando arriba</b>, en cualquier direcci&#243;n. El anclaje a fascia es justamente
  el punto que el inspector mira. Este detalle est&#225; hecho para eso &#8212; bloqueo s&#243;lido, tirafondo de {fr(TORN)}" y el par en vertical &#8212; pero <b>si el permiso pide c&#225;lculo
  firmado, esta hoja hay que pasarla por el ingeniero</b>, no la firmo yo.</div>

  <div class="pb"></div>
  <div class="hd"><h1>QU&#201; POSTE LLEVA OREJAS</h1>
    <div class="m">{NE} POSTES DE ESQUINA</div></div>
  <table>
    <tr><th style="width:14%">Secci&#243;n</th><th style="width:26%">Balc&#243;n</th>
        <th style="width:20%">Lleva</th><th>Tornillos</th></tr>
    {filas}
  </table>
  <p style="font-size:12.5px"><b>Los otros {79-NE} postes no llevan oreja:</b> van en tramo recto o
  mueren contra la pared, y ah&#237; la fascia les corre por detr&#225;s de la cara completa, as&#237;
  que se atornillan directo por la cara del poste, <b>dos tirafondos de {fr(TORN)}"&#215;{fr(TORN_L)}"
  uno encima del otro</b>, a las mismas {fr(PROF[0])}" y {fr(PROF[1])}" bajo el deck, y con el mismo
  bloqueo detr&#225;s. La cuenta de arriba es la misma para ellos.</p>

</div></body></html>"""

out = HERE / "railing-detalle-anclaje.html"
out.write_text(HTML, encoding="utf-8")
print("escrito:", out.name)
print(f"  {NE} postes de esquina · {NE*2} orejas de {fr(OREJA_L)}×{fr(OREJA_H)}×1/4 · "
      f"{NE*2*2} tornillos de {fr(TORN)}\" SS316")
print(f"  tornillo a {fr(BORDE)}\" de la punta del rim = {BORDE/TORN:.0f} diámetros  OK")
print(f"  barra plana 1/4×{fr(OREJA_H)}: {pies_barra:.1f} pies")
