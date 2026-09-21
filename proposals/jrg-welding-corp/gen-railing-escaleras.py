#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PLANOS DE FABRICACION DE LAS 4 BARANDAS DE ESCALERA DEL POOL HOUSE.

   Baranda de 42" A PLOMO, igual que el balcon.  Los postes y los piques van a
   plomo; el cap y el riel siguen la pendiente.  El dibujo va ACOSTADO: es el
   mismo dibujo del balcon pero cizallado con la pendiente.  Eso no es gusto
   mio -- con el cuadro derecho el cap se lo come (sobre las 30-1/4 de ancho
   del cuadro, a 34 grados el cap sube 20-3/8).

   Todo sale de una sola transformacion:  (x, y a plomo)  ->  (x, x*tan(a) + y)
   Asi, cualquier pieza a plomo del balcon sigue a plomo y con el mismo largo, y
   cualquier pieza horizontal se acuesta con la pendiente.  Por eso las medidas
   cuadran solas y no hay que teclear ni un numero."""
import math, pathlib, importlib.util

HERE = pathlib.Path("/home/user/yourparknow-website/proposals/jrg-welding-corp")
spec = importlib.util.spec_from_file_location("gsec", HERE / "gen-railing-secciones.py")
G = importlib.util.module_from_spec(spec); spec.loader.exec_module(G)
fr, feet = G.fr, G.feet

NEG, ROJO, VERDE, NAR = "#1b2a41", "#b91c1c", "#0f766e", "#c8571b"
ALU, ALU2, PIQ = "#9fb0c0", "#7b8d9e", "#e5e7eb"

GUARD, PISO, TUBO = 42.0, 2.0, 1.0      # 42 a plomo, 2 del piso al riel, tubo de 1
CAP, RIEL = 1.0, 1.0                    # espesor del 2x1 visto de canto
POST_W, GAP = 2.0, 0.25                 # poste 2x2 ; holgura del panel por lado
CUADRO, LUZ_CUADRO = 30.25, 28.25       # el cuadro del dibujo, como en el balcon
Q2_OD, Q3_OD = 20.5, 10.75
LUZ_DIB = 46.0                          # la bahia del dibujo, EN HORIZONTAL
ESFERA = 3.75                           # luz libre maxima que me permito (codigo: 4")

ESCALERAS = [
 dict(n="ESCALERA DEL BALCÓN 1", rake=185.5, ang=34.0, cant=2, corr="C"),
 dict(n="ESCALERA DEL BALCÓN 2", rake=198.0, ang=33.0, cant=2, corr="F"),
]


def geo(e):
    """toda la geometria de una escalera, con las cadenas verificadas."""
    a  = math.radians(e['ang'])
    ca, ta = math.cos(a), math.tan(a)
    g = dict(e)
    g['a'], g['ca'], g['ta'] = a, ca, ta
    g['horiz'] = e['rake'] * ca
    g['rise']  = e['rake'] * math.sin(a)
    # alturas A PLOMO sobre la linea de narices
    g['y_riel_b'] = PISO
    g['y_riel_t'] = PISO + RIEL / ca            # el 2x1 acostado sube 1/cos a plomo
    g['y_cap_t']  = GUARD
    g['y_cap_b']  = GUARD - CAP / ca
    g['campo']    = g['y_cap_b'] - g['y_riel_t']
    g['flot']     = (g['campo'] - CUADRO) / 2
    assert g['flot'] > 2.0, "el cuadro no cabe en el campo"

    # reparto: pano liso + DIBUJO 46 + pano liso, todo en HORIZONTAL
    w = (g['horiz'] - 4 * POST_W - LUZ_DIB) / 2
    g['w'] = w
    cad = [('P',), ('L', w), ('P',), ('D', LUZ_DIB), ('P',), ('L', w), ('P',)]
    g['cad'] = cad
    assert abs(sum(POST_W if c[0] == 'P' else c[1] for c in cad) - g['horiz']) < 1e-9, \
        "la cadena horizontal de la escalera no cierra"

    # piques del pano liso.  La esfera se mide EN HORIZONTAL.
    panel = w - 2 * GAP
    n = 1
    while (panel - n * TUBO) / (n + 1) + GAP > ESFERA:
        n += 1
    sep = (panel - n * TUBO) / (n + 1)
    g['n_piq'], g['sep'] = n, sep
    assert abs((n * TUBO + (n + 1) * sep) - panel) < 1e-9, "el pano liso no cierra"
    g['marca'] = (TUBO + sep) / ca              # de marca a marca SOBRE el riel inclinado

    # ---- piezas del dibujo acostado
    V = g['campo']                               # a plomo, 2 cortes paralelos a la pendiente
    H = LUZ_CUADRO / ca                          # acostada, 2 cortes a plomo
    c = LUZ_CUADRO
    P = [(0, 0), (c, 0), (c, c), (0, c)]         # luz del cuadro, en coordenadas a plomo
    Pc = [(x, y + x * ta) for x, y in P]         # cizallada
    def dd(p, q): return math.hypot(q[0] - p[0], q[1] - p[1])
    D1, D2 = dd(Pc[0], Pc[2]), dd(Pc[1], Pc[3])
    v1 = (Pc[2][0] - Pc[0][0], Pc[2][1] - Pc[0][1])
    v2 = (Pc[3][0] - Pc[1][0], Pc[3][1] - Pc[1][1])
    th = math.degrees(math.acos(abs(v1[0]*v2[0] + v1[1]*v2[1]) / (D1 * D2)))
    desc = (TUBO / 2) / math.sin(math.radians(th))
    g['th'] = th
    # rombos concentricos: cizallados, el lado a plomo no cambia y el otro se acuesta
    q2, q3 = Q2_OD - TUBO, Q3_OD - TUBO          # centro a centro, como en el balcon
    g['piezas'] = [
      ("V",  2, V,            f"vertical del cuadro &#183; a plomo &#183; 2 cortes a {e['ang']:g}&#176; paralelos"),
      ("B",  2, V,            f"pique de flanco &#183; a plomo &#183; 2 cortes a {e['ang']:g}&#176; paralelos"),
      ("H",  2, H,            "horizontal del cuadro &#183; acostada &#183; 2 cortes a plomo"),
      ("D1", 1, D1,           f"diagonal larga entera &#183; puntas a {(180-th)/2:.0f}&#176;"),
      ("D2", 2, D2/2 - desc,  f"media diagonal corta &#183; muere contra la D1"),
      ("C2p",2, q2,           f"rombo Q2 &#183; los dos lados A PLOMO &#183; {(90-e['ang'])/2:.0f}&#176; y {(90+e['ang'])/2:.0f}&#176;"),
      ("C2a",2, q2/ca,        f"rombo Q2 &#183; los dos lados ACOSTADOS &#183; {(90-e['ang'])/2:.0f}&#176; y {(90+e['ang'])/2:.0f}&#176;"),
      ("C3p",2, q3,           f"rombo Q3 &#183; los dos lados A PLOMO &#183; {(90-e['ang'])/2:.0f}&#176; y {(90+e['ang'])/2:.0f}&#176;"),
      ("C3a",2, q3/ca,        f"rombo Q3 &#183; los dos lados ACOSTADOS &#183; {(90-e['ang'])/2:.0f}&#176; y {(90+e['ang'])/2:.0f}&#176;"),
    ]
    assert sum(q for _, q, _, _ in g['piezas']) == 17, "el dibujo tiene que llevar 17 piezas"

    # ---- postes: a plomo, con la punta cortada a la pendiente
    # la cara de abajo del cap, en el eje del poste, va a GUARD - CAP/ca
    g['post_cara_larga'] = g['y_cap_b'] + (POST_W / 2) * ta + 6.0
    g['post_cara_corta'] = g['y_cap_b'] - (POST_W / 2) * ta + 6.0
    assert abs((g['post_cara_larga'] - g['post_cara_corta']) - POST_W * ta) < 1e-9

    # ---- cap y riel: de punta a punta de la corrida, por la pendiente
    g['cap_largo']  = e['rake']
    g['riel_largo'] = [ (w - 2*GAP) / ca, (LUZ_DIB - 2*GAP) / ca, (w - 2*GAP) / ca ]
    return g


# ------------------------------------------------------------------ dibujo
def alzado(g, VW=792, VH=575):
    """Vista de frente de la escalera completa, con la pendiente de verdad."""
    mx, my = 86, 52
    sc = min((VW - 2*mx) / g['horiz'], (VH - 2*my) / (g['rise'] + GUARD + 14))
    OX, OY = (VW - g['horiz']*sc) / 2, VH - my
    def S(x, yp):
        """x horizontal, yp a plomo sobre la linea de narices -> pantalla"""
        return OX + x*sc, OY - (x*g['ta'] + yp)*sc
    def poly(pts, fill, stroke=NEG, w=1.1):
        d = " ".join(f"{a:.1f},{b:.1f}" for a, b in pts)
        return f'<polygon points="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{w}"/>'
    def banda(x0, x1, y0, y1, fill, stroke=NEG, w=1.1):
        return poly([S(x0, y0), S(x1, y0), S(x1, y1), S(x0, y1)], fill, stroke, w)

    o = []
    # escalones
    hh = g['rise'] / round(g['rise'] / 7.2)
    nn = round(g['rise'] / hh)
    bb = g['horiz'] / nn
    for i in range(nn):
        x0, x1 = i*bb, (i+1)*bb
        p1 = S(x0, 0); p2 = S(x1, 0)
        o.append(f'<path d="M {p1[0]:.1f} {p1[1]:.1f} L {p1[0]:.1f} {p2[1]:.1f} '
                 f'L {p2[0]:.1f} {p2[1]:.1f}" fill="none" stroke="#b09a72" stroke-width="2.4"/>')

    # recorrido
    x = 0.0
    posts, bays = [], []
    for c in g['cad']:
        if c[0] == 'P': posts.append(x); x += POST_W
        else:           bays.append((x, c[0], c[1])); x += c[1]

    # riel de abajo y cap, corridos
    o.append(banda(0, g['horiz'], g['y_riel_b'], g['y_riel_t'], ALU2))
    o.append(banda(0, g['horiz'], g['y_cap_b'],  g['y_cap_t'],  ALU2))

    # panos
    for x0, k, luz in bays:
        L = x0 + GAP
        if k == 'L':
            for i in range(g['n_piq']):
                xx = L + g['sep'] + i*(TUBO + g['sep'])
                o.append(banda(xx, xx+TUBO, g['y_riel_t'], g['y_cap_b'], PIQ, ALU2, 0.7))
        else:
            panel = luz - 2*GAP
            gg = (panel - 4*TUBO - LUZ_CUADRO) / 4
            b1 = L + gg; v1 = b1 + TUBO + gg; v2 = v1 + TUBO + LUZ_CUADRO; b2 = v2 + TUBO + gg
            assert abs((b2 + TUBO + gg) - (L + panel)) < 1e-9, "el dibujo no cierra en la bahia"
            for xx in (b1, b2):
                o.append(banda(xx, xx+TUBO, g['y_riel_t'], g['y_cap_b'], PIQ, ALU2, 0.7))
            for xx in (v1, v2):
                o.append(banda(xx, xx+TUBO, g['y_riel_t'], g['y_cap_b'], ALU, NEG, 0.9))
            yb, yt = g['y_riel_t'] + g['flot'], g['y_cap_b'] - g['flot']
            for yy in (yb, yt - TUBO):
                o.append(banda(v1+TUBO, v2, yy, yy+TUBO, ALU, NEG, 0.9))
            # la X
            ia, ib = v1 + TUBO, v2
            for p, q in (((ia, yb+TUBO), (ib, yt-TUBO)), ((ia, yt-TUBO), (ib, yb+TUBO))):
                A, B = S(*p), S(*q)
                o.append(f'<line x1="{A[0]:.1f}" y1="{A[1]:.1f}" x2="{B[0]:.1f}" y2="{B[1]:.1f}" '
                         f'stroke="{NEG}" stroke-width="{TUBO*sc:.1f}"/>')
            # rombos concentricos, cizallados
            cxm, cym = (ia+ib)/2, (yb+yt)/2
            for od in (Q2_OD, Q3_OD):
                s2 = (od - TUBO)/2
                pts = [S(cxm-s2, cym-s2), S(cxm+s2, cym-s2), S(cxm+s2, cym+s2), S(cxm-s2, cym+s2)]
                d = " ".join(f"{p[0]:.1f},{p[1]:.1f}" for p in pts)
                o.append(f'<polygon points="{d}" fill="none" stroke="{NEG}" '
                         f'stroke-width="{TUBO*sc:.1f}"/>')

    # postes a plomo
    for px in posts:
        top = g['y_cap_b']
        o.append(poly([S(px, -6), S(px+POST_W, -6),
                       S(px+POST_W, top), S(px, top)], ALU, NEG, 1.4))

    # ---- cotas
    def cotaR(x0, x1, off, txt):
        """cota paralela a la pendiente, por encima del cap"""
        A = S(x0, GUARD + off); B = S(x1, GUARD + off)
        m = ((A[0]+B[0])/2, (A[1]+B[1])/2)
        ang = math.degrees(math.atan2(B[1]-A[1], B[0]-A[0]))
        return (f'<line x1="{A[0]:.1f}" y1="{A[1]:.1f}" x2="{B[0]:.1f}" y2="{B[1]:.1f}" '
                f'stroke="{ROJO}" stroke-width="1.2" marker-start="url(#e)" marker-end="url(#e)"/>'
                f'<text x="{m[0]:.1f}" y="{m[1]-5:.1f}" font-size="12.5" font-weight="800" '
                f'fill="{ROJO}" text-anchor="middle" transform="rotate({ang:.1f} {m[0]:.1f} {m[1]:.1f})">{txt}</text>')
    cen = [p + POST_W/2 for p in posts]
    for A, B in zip(cen, cen[1:]):
        o.append(cotaR(A, B, 4, f'{fr((B-A)/g["ca"])}"'))
    o.append(cotaR(0, g['horiz'], 17, f'{fr(g["rake"])}"  POR LA PENDIENTE  &#183;  {g["ang"]:g}&#176;'))

    # 42 a plomo, en el poste de abajo
    A, B = S(POST_W/2, 0), S(POST_W/2, GUARD)
    o.append(f'<line x1="{A[0]-34:.1f}" y1="{A[1]:.1f}" x2="{B[0]-34:.1f}" y2="{B[1]:.1f}" '
             f'stroke="{ROJO}" stroke-width="1.2" marker-start="url(#e)" marker-end="url(#e)"/>')
    o.append(f'<text x="{A[0]-40:.1f}" y="{(A[1]+B[1])/2:.1f}" font-size="13" font-weight="800" '
             f'fill="{ROJO}" text-anchor="middle" '
             f'transform="rotate(-90 {A[0]-40:.1f} {(A[1]+B[1])/2:.1f})">42" A PLOMO</text>')

    # que es cada pano: DENTRO del pano, acostado con la pendiente
    ang_p = math.degrees(math.atan2(-g['ta']*sc, sc))
    for x0, k, luz in bays:
        p = S(x0 + luz/2, g['y_riel_t'] + 4.5)
        o.append(f'<text x="{p[0]:.1f}" y="{p[1]:.1f}" font-size="11.5" font-weight="800" '
                 f'fill="{NAR if k=="D" else NEG}" text-anchor="middle" '
                 f'transform="rotate({ang_p:.1f} {p[0]:.1f} {p[1]:.1f})">'
                 f'{"DIBUJO ACOSTADO" if k=="D" else str(g["n_piq"])+" PIQUES"}</text>')

    p = S(g['horiz'], GUARD)
    o.append(f'<text x="{min(p[0]+10, VW-6):.1f}" y="{p[1]-6:.1f}" font-size="11.5" font-weight="800" '
             f'fill="{ROJO}" text-anchor="end">ARRIBA: empata en el poste del balc&#243;n</text>')
    p = S(0, 0)
    o.append(f'<text x="{p[0]-6:.1f}" y="{p[1]+17:.1f}" font-size="11.5" font-weight="800" '
             f'fill="{ROJO}">ABAJO: poste propio con placa</text>')

    return ('<svg viewBox="0 0 %d %d" xmlns="http://www.w3.org/2000/svg">' % (VW, VH)
            + '<defs><marker id="e" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" '
              f'markerHeight="5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{ROJO}"/>'
              '</marker></defs>' + "".join(o) + '</svg>')


# ------------------------------------------------------------------ HTML
CSS = f"""
 *{{margin:0;padding:0;box-sizing:border-box}}
 body{{font-family:'Segoe UI',-apple-system,Helvetica,Arial,sans-serif;color:{NEG};background:#fff;font-size:13px}}
 .page{{max-width:10.2in;margin:0 auto;padding:.3in .35in}}
 @media print{{@page{{size:letter landscape;margin:.3in .35in}}.page{{padding:0;max-width:none}}
              .pb{{page-break-before:always}}.dw{{page-break-inside:avoid}}}}
 .hd{{display:flex;justify-content:space-between;align-items:center;border-bottom:4px solid {NEG};
     padding-bottom:6px;margin-bottom:9px}}
 h1{{font-size:20px;letter-spacing:.5px}} .hd .m{{font-size:12px;font-weight:700;text-align:right}}
 .dw{{border:2px solid {NEG};border-radius:5px;margin-bottom:11px}}
 .dw .dt{{background:{NEG};color:#fff;font-size:12.5px;padding:5px 10px;font-weight:700;display:flex}}
 .dw .dt .r{{margin-left:auto;font-weight:400}}
 .dw svg{{display:block;width:100%;height:auto;background:#fff}}
 table{{width:100%;border-collapse:collapse;font-size:12.5px;margin-bottom:9px}}
 th{{background:#41505f;color:#fff;padding:4px 9px;text-align:left;font-size:11px}}
 td{{border:1px solid #d3dae1;padding:4px 9px}}
 td.n{{text-align:right;white-space:nowrap;font-weight:700}}
 .warn{{border-left:5px solid {ROJO};background:#fff5f5;padding:9px 13px;font-size:12.5px;margin:9px 0}}
 .big{{display:flex;gap:9px;margin:9px 0}}
 .big div{{flex:1;border:2px solid {NEG};border-radius:5px;padding:7px 9px;text-align:center}}
 .big b{{display:block;font-size:22px;color:{ROJO};line-height:1.1}}
 .big span{{font-size:9.5px;text-transform:uppercase;letter-spacing:.6px;font-weight:700}}
 h2{{font-size:12px;background:{NEG};color:#fff;padding:4px 10px;margin:11px 0 6px;
    text-transform:uppercase;letter-spacing:.6px}}
"""

cuerpo = ""
for i, e in enumerate(ESCALERAS):
    g = geo(e)
    salto = '<div class="pb"></div>' if i else ''
    piezas = "".join(
        f"<tr><td><b>{c}</b></td><td>1&#215;1&#215;1/16</td><td class='n'>{fr(L,32)}\"</td>"
        f"<td class='n'><b>{q}</b></td><td class='n'>{q*e['cant']}</td><td>{d}</td></tr>"
        for c, q, L, d in g['piezas'])
    cuerpo += f"""
  {salto}
  <div class="hd"><h1>{e['n']}</h1><div class="m">PLANO DE FABRICACI&#211;N &#183; BARANDA DE 42" A PLOMO
    <br>{fr(e['rake'])}" por la pendiente a {e['ang']:g}&#176; &#183; <b>{e['cant']} iguales</b></div></div>

  <div class="big">
    <div><b>{fr(e['rake'])}"</b><span>por la pendiente</span></div>
    <div><b>{e['ang']:g}&#176;</b><span>pendiente</span></div>
    <div><b>{feet(g['rise'])}</b><span>sube</span></div>
    <div><b>{feet(g['horiz'])}</b><span>corre en planta</span></div>
    <div><b>4</b><span>postes (3 propios)</span></div>
    <div><b>1</b><span>dibujo acostado</span></div>
  </div>

  <div class="dw">
    <div class="dt">VISTA DE FRENTE &#8212; pa&#241;o de piques, dibujo, pa&#241;o de piques
      <span class="r">las cotas de arriba son de centro a centro de poste, POR LA PENDIENTE</span></div>
    {alzado(g)}
  </div>

  <h2>Lo que se corta &#8212; una escalera (hay {e['cant']} iguales)</h2>
  <table>
    <tr><th style="width:11%">Pieza</th><th style="width:19%">Perfil</th><th style="width:13%">Largo de corte</th>
        <th style="width:8%">Cant.</th><th style="width:9%">Las {e['cant']}</th><th>C&#243;mo se corta</th></tr>
    <tr><td><b>POSTE</b></td><td>2&#215;2&#215;.090</td><td class="n">{fr(g['post_cara_larga'],32)}"</td>
        <td class="n"><b>3</b></td><td class="n">{3*e['cant']}</td>
        <td>a plomo. Punta de arriba cortada a <b>{e['ang']:g}&#176;</b>:
            cara larga {fr(g['post_cara_larga'],32)}", cara corta {fr(g['post_cara_corta'],32)}".
            Abajo corte recto. El cuarto poste, el de arriba, es el del balc&#243;n.</td></tr>
    <tr><td><b>CAP</b></td><td>2&#215;1&#215;.090 de plano</td><td class="n">{fr(g['cap_largo'])}"</td>
        <td class="n"><b>1</b></td><td class="n">{e['cant']}</td>
        <td>corrido de punta a punta, por la pendiente</td></tr>
    <tr><td><b>RIEL</b></td><td>2&#215;1&#215;.090 acostado</td><td class="n">{fr(g['riel_largo'][0],32)}"</td>
        <td class="n"><b>2</b></td><td class="n">{2*e['cant']}</td>
        <td>de los dos pa&#241;os de piques &#183; medido por la pendiente</td></tr>
    <tr><td><b>RIEL</b></td><td>2&#215;1&#215;.090 acostado</td><td class="n">{fr(g['riel_largo'][1],32)}"</td>
        <td class="n"><b>1</b></td><td class="n">{e['cant']}</td>
        <td>del pa&#241;o del dibujo &#183; medido por la pendiente</td></tr>
    <tr><td><b>PIQUE</b></td><td>1&#215;1&#215;1/16</td><td class="n">{fr(g['campo'],32)}"</td>
        <td class="n"><b>{2*g['n_piq']}</b></td><td class="n">{2*g['n_piq']*e['cant']}</td>
        <td><b>a plomo</b> &#183; las dos puntas cortadas a <b>{e['ang']:g}&#176;</b>, paralelas entre s&#237;
            (las dos caras miden igual)</td></tr>
  </table>

  <h2>El dibujo acostado de {e['ang']:g}&#176; &#8212; 17 piezas, todas de 1&#215;1</h2>
  <table>
    <tr><th style="width:11%">Pieza</th><th style="width:19%">Perfil</th><th style="width:13%">Largo de corte</th>
        <th style="width:8%">Por dibujo</th><th style="width:9%">Las {e['cant']}</th><th>C&#243;mo se corta</th></tr>
    {piezas}
  </table>

  <div class="warn"><b>El cuadro flota {fr(g['flot'],32)}" A PLOMO</b> por debajo del cap y
  otro tanto por encima del riel, y mide <b>{fr(CUADRO)}" a plomo</b> &#215; <b>{fr(CUADRO)}" en
  horizontal</b>, igual que el del balc&#243;n. Lo &#250;nico que cambia es que se acuesta.
  La luz libre entre piques del pa&#241;o liso es de <b>{fr(g['sep']+GAP,32)}" medida en horizontal</b>
  (as&#237; es como pasa la esfera), y sobre el riel inclinado eso son marcas
  <b>cada {fr(g['marca'],32)}"</b>.</div>
"""

TOT = sum(e['cant'] for e in ESCALERAS)
HTML = f"""<!DOCTYPE html><html lang="es"><head><meta charset="UTF-8">
<title>Escaleras del Pool House &#8212; fabricaci&#243;n</title><style>{CSS}</style></head>
<body><div class="page">

  <div class="hd"><h1>LAS {TOT} BARANDAS DE ESCALERA &#183; POOL HOUSE</h1>
    <div class="m">BARANDA DE 42" A PLOMO, IGUAL QUE EL BALC&#211;N<br>
    2 de {fr(ESCALERAS[0]['rake'])}" a 34&#176; &#183; 2 de {fr(ESCALERAS[1]['rake'])}" a 33&#176;</div></div>

  <div class="warn"><b>OJO CON UNA COSA, antes de cortar.</b> Estos planos est&#225;n hechos
  tomando que <b>las 185-1/2" y las 198" las mediste POR LA PENDIENTE</b>, con la cinta pegada al
  stringer. Si es as&#237;, la escalera del balc&#243;n 1 <b>sube {feet(geo(ESCALERAS[0])['rise'])}</b>
  y la del balc&#243;n 2 <b>sube {feet(geo(ESCALERAS[1])['rise'])}</b>. Mide del piso de abajo al deck:
  si te da eso, seguimos. <b>Si te da como 10 pies y medio, entonces me diste la corrida en planta
  y estas hojas hay que rehacerlas.</b></div>

  <div class="warn"><b>Por qu&#233; el dibujo va acostado y no derecho.</b> El cap sigue la
  pendiente. Sobre las {fr(CUADRO)}" de ancho que tiene el cuadro, a 34&#176; el cap
  <b>sube 20-3/8"</b>. El campo es de {fr(geo(ESCALERAS[0])['campo'],32)}". O sea que si dejas el
  cuadro derecho, el cap se lo come por el lado de abajo: no cabe. Por eso el dibujo se acuesta con
  la pendiente &#8212; los piques y los lados del cuadro siguen <b>a plomo</b>, y el de arriba y el
  de abajo van <b>paralelos a la escalera</b>.</div>

  <div class="warn"><b>Estos dibujos NO son los 32 que ya tienes armados.</b> Aquellos son de los
  balcones. Las escaleras llevan <b>{TOT} dibujos nuevos</b>, y no son todos iguales entre s&#237;:
  <b>2 son de 34&#176; y 2 son de 33&#176;</b>, con medidas de corte distintas. No los mezcles.</div>
{cuerpo}
</div></body></html>"""

out = HERE / "railing-escaleras.html"
out.write_text(HTML, encoding="utf-8")
print("escrito:", out.name)
for e in ESCALERAS:
    g = geo(e)
    print(f"  {e['n']}:  {fr(e['rake'])}\" a {e['ang']:g}°  x{e['cant']}")
    print(f"      sube {feet(g['rise'])}  ·  corre {feet(g['horiz'])}  ·  campo {fr(g['campo'],32)}\"")
    print(f"      panos (horizontal): {fr(g['w'])} + DIBUJO 46 + {fr(g['w'])}"
          f"   ·  {g['n_piq']} piques cada liso, luz {fr(g['sep']+GAP,32)}\"")
    print(f"      postes {fr(g['post_cara_larga'],32)}\" cara larga / {fr(g['post_cara_corta'],32)}\" corta")
