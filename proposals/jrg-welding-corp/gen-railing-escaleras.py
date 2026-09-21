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


CC_MAX = 48.0        # centro a centro de poste, POR LA PENDIENTE. Regla de Rene.
CUADRO_E = 26.0      # el cuadro del dibujo de escalera. Mas chico que el del
                     # balcon porque con los postes a 4 pies las bahias son mas
                     # cortas y el de 30-1/4 no cabe.

def reparto(horiz, ca):
    """cuantos panos caben con el centro a centro por debajo de CC_MAX."""
    n = 1
    while True:
        bay = (horiz - POST_W * (n + 1)) / n
        if (bay + POST_W) / ca <= CC_MAX:
            return n, bay
        n += 1

def piques_en(panel, lim=ESFERA):
    """cuantos piques hacen falta en un panel de ese ancho (medido EN HORIZONTAL)"""
    n = 0
    while (panel - n * TUBO) / (n + 1) + GAP > lim:
        n += 1
    return n, (panel - n * TUBO) / (n + 1)

def flancos(panel):
    """el cuadro va centrado; cada flanco se rellena con los piques que hagan
       falta para que la luz libre no pase de ESFERA."""
    hueco = (panel - CUADRO_E) / 2
    assert hueco > 0, "el cuadro no cabe en la bahia"
    n, g = piques_en(hueco + TUBO, ESFERA)   # el hueco mas un tubo virtual
    n = max(n - 1, 0)
    while (hueco - n * TUBO) / (n + 1) + GAP > ESFERA:
        n += 1
    g = (hueco - n * TUBO) / (n + 1)
    assert abs((n * TUBO + (n + 1) * g) - hueco) < 1e-9, "el flanco no cierra"
    return n, g


def geo(e):
    """toda la geometria de una escalera, con las cadenas verificadas."""
    a  = math.radians(e['ang'])
    ca, ta = math.cos(a), math.tan(a)
    g = dict(e)
    g['a'], g['ca'], g['ta'] = a, ca, ta
    g['horiz'] = e['rake'] * ca
    g['rise']  = e['rake'] * math.sin(a)
    g['y_riel_b'] = PISO
    g['y_riel_t'] = PISO + RIEL / ca
    g['y_cap_t']  = GUARD
    g['y_cap_b']  = GUARD - CAP / ca
    g['campo']    = g['y_cap_b'] - g['y_riel_t']
    g['flot']     = (g['campo'] - CUADRO_E) / 2
    assert g['flot'] > 2.0, "el cuadro no cabe en el campo"

    # ---- reparto de postes: manda el centro a centro de 48 POR LA PENDIENTE
    n, bay = reparto(g['horiz'], ca)
    g['n_bay'], g['bay'] = n, bay
    g['cc'] = (bay + POST_W) / ca
    assert g['cc'] <= CC_MAX + 1e-9, f"centro a centro {g['cc']:.2f} pasa de {CC_MAX}"
    i_dib = n // 2                                   # el dibujo va en la bahia del medio
    g['i_dib'] = i_dib
    cad = [('P',)]
    for i in range(n):
        cad += [('D' if i == i_dib else 'L', bay), ('P',)]
    g['cad'] = cad
    assert abs(sum(POST_W if c[0] == 'P' else c[1] for c in cad) - g['horiz']) < 1e-9, \
        "la cadena horizontal de la escalera no cierra"
    seq = [c[0] for c in cad if c[0] != 'P']
    assert seq[0] != 'D' and seq[-1] != 'D', "la escalera arranca o termina en dibujo"
    assert not any(x == 'D' and y == 'D' for x, y in zip(seq, seq[1:])), "dos dibujos pegados"

    panel = bay - 2 * GAP
    g['panel'] = panel
    g['n_piq'], g['sep'] = piques_en(panel)
    assert abs((g['n_piq'] * TUBO + (g['n_piq'] + 1) * g['sep']) - panel) < 1e-9, "pano liso"
    g['marca'] = (TUBO + g['sep']) / ca

    # ---- la bahia del dibujo: cuadro centrado, flancos rellenos
    g['n_fl'], g['g_fl'] = flancos(panel)
    assert abs((2 * (g['n_fl'] * TUBO + (g['n_fl'] + 1) * g['g_fl']) + CUADRO_E) - panel) < 1e-9, \
        "la bahia del dibujo no cierra"

    # ---- piezas del dibujo acostado
    LUZ = CUADRO_E - 2 * TUBO                    # luz de adentro del cuadro
    g['luz_cuadro'] = LUZ
    V = g['campo']
    H = LUZ / ca
    P4 = [(0, 0), (LUZ, 0), (LUZ, LUZ), (0, LUZ)]
    Pc = [(x, y + x * ta) for x, y in P4]
    def dd(p, q): return math.hypot(q[0] - p[0], q[1] - p[1])
    D1, D2 = dd(Pc[0], Pc[2]), dd(Pc[1], Pc[3])
    u1 = (Pc[2][0] - Pc[0][0], Pc[2][1] - Pc[0][1])
    u2 = (Pc[3][0] - Pc[1][0], Pc[3][1] - Pc[1][1])
    th = math.degrees(math.acos(abs(u1[0]*u2[0] + u1[1]*u2[1]) / (D1 * D2)))
    desc = (TUBO / 2) / math.sin(math.radians(th))
    g['th'] = th
    # angulos de las puntas, contra el lado a plomo y contra el acostado.
    # Tienen que sumar el angulo de la esquina del paralelogramo o algo esta mal.
    aD1 = math.degrees(math.atan(1 + ta))
    d1_v, d1_h = 90 - aD1, aD1 - e['ang']
    assert abs((d1_v + d1_h) - (90 - e['ang'])) < 1e-6, "la punta de la D1 no cuadra con la esquina"
    dD2 = math.degrees(math.atan2(1 - ta, -1))
    d2_h, d2_v = abs((180 + e['ang']) - dD2), abs(90 - dD2)
    assert abs((d2_v + d2_h) - (90 + e['ang'])) < 1e-6, "la punta de la D2 no cuadra con la esquina"
    g['d1_v'], g['d1_h'], g['d2_v'], g['d2_h'] = d1_v, d1_h, d2_v, d2_h
    esc_q = CUADRO_E / 30.25                     # los rombos de adentro, a escala
    q2, q3 = Q2_OD * esc_q - TUBO, Q3_OD * esc_q - TUBO
    g['q2_od'], g['q3_od'] = Q2_OD * esc_q, Q3_OD * esc_q
    ag, ob = (90 - e['ang']) / 2, (90 + e['ang']) / 2
    pz = [
      ("V",  2, V,           f"lado del cuadro &#183; A PLOMO &#183; las 2 puntas a {e['ang']:g}&#176;, paralelas"),
      ("H",  2, H,           f"tapa del cuadro &#183; ACOSTADA &#183; las 2 puntas a plomo"),
      ("D1", 1, D1,          f"diagonal larga, entera &#183; punta en los 2 lados: "
                             f"<b>{d1_v:.0f}&#176;</b> contra la V y <b>{d1_h:.0f}&#176;</b> contra la H"),
      ("D2", 2, D2/2 - desc, f"media diagonal corta &#183; por fuera <b>{d2_v:.0f}&#176;</b> contra la V "
                             f"y <b>{d2_h:.0f}&#176;</b> contra la H &#183; por dentro muere a ras contra la D1"),
      ("C2p",2, q2,          f"rombo grande &#183; los 2 A PLOMO &#183; {ag:.0f}&#176; y {ob:.0f}&#176;"),
      ("C2a",2, q2/ca,       f"rombo grande &#183; los 2 ACOSTADOS &#183; {ag:.0f}&#176; y {ob:.0f}&#176;"),
      ("C3p",2, q3,          f"rombo chico &#183; los 2 A PLOMO &#183; {ag:.0f}&#176; y {ob:.0f}&#176;"),
      ("C3a",2, q3/ca,       f"rombo chico &#183; los 2 ACOSTADOS &#183; {ag:.0f}&#176; y {ob:.0f}&#176;"),
    ]
    if g['n_fl']:
        pz.insert(1, ("B", 2*g['n_fl'], V,
                      f"pique de flanco &#183; A PLOMO &#183; las 2 puntas a {e['ang']:g}&#176;"))
    g['piezas'] = pz
    g['n_piezas'] = sum(q for _, q, _, _ in pz)

    g['post_cara_larga'] = g['y_cap_b'] + (POST_W / 2) * ta + 6.0
    g['post_cara_corta'] = g['y_cap_b'] - (POST_W / 2) * ta + 6.0
    g['cap_largo']  = e['rake']
    g['riel_pano']  = (bay - 2*GAP) / ca
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
            # flancos: n_fl piques a cada lado, con su luz g_fl
            nf, gf = g['n_fl'], g['g_fl']
            x = L
            for _ in range(nf):
                x += gf
                o.append(banda(x, x+TUBO, g['y_riel_t'], g['y_cap_b'], PIQ, ALU2, 0.7)); x += TUBO
            x += gf
            v1 = x                                  # cara izquierda del cuadro
            v2 = v1 + CUADRO_E - TUBO
            assert abs((v2 + TUBO + nf*(gf+TUBO) + gf) - (L + panel)) < 1e-9, \
                "la bahia del dibujo no cierra en el alzado"
            for xx in (v1, v2):
                o.append(banda(xx, xx+TUBO, g['y_riel_t'], g['y_cap_b'], ALU, NEG, 0.9))
            x = v2 + TUBO
            for _ in range(nf):
                x += gf
                o.append(banda(x, x+TUBO, g['y_riel_t'], g['y_cap_b'], PIQ, ALU2, 0.7)); x += TUBO
            yb, yt = g['y_riel_t'] + g['flot'], g['y_cap_b'] - g['flot']
            for yy in (yb, yt - TUBO):
                o.append(banda(v1+TUBO, v2, yy, yy+TUBO, ALU, NEG, 0.9))
            ia, ib = v1 + TUBO, v2
            for pq, qq in (((ia, yb+TUBO), (ib, yt-TUBO)), ((ia, yt-TUBO), (ib, yb+TUBO))):
                A, B = S(*pq), S(*qq)
                o.append(f'<line x1="{A[0]:.1f}" y1="{A[1]:.1f}" x2="{B[0]:.1f}" y2="{B[1]:.1f}" '
                         f'stroke="{NEG}" stroke-width="{TUBO*sc:.1f}"/>')
            cxm, cym = (ia+ib)/2, (yb+yt)/2
            for od in (g['q2_od'], g['q3_od']):
                s2 = (od - TUBO)/2
                pts = [S(cxm-s2, cym-s2), S(cxm+s2, cym-s2), S(cxm+s2, cym+s2), S(cxm-s2, cym+s2)]
                d = " ".join(f"{q[0]:.1f},{q[1]:.1f}" for q in pts)
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



# ---------------------------------------------- PLANO DEL DIBUJO, EN GRANDE
def detalle_dibujo(g, VW=792, VH=500):
    """El dibujo solo, en grande, con todas las medidas y cada pieza con su letra."""
    ta, ca = g['ta'], g['ca']
    LUZ = g['luz_cuadro']
    ancho = CUADRO_E
    alto_total = CUADRO_E + CUADRO_E * ta          # lo que ocupa el rombo de alto
    mx, my = 168, 78
    sc = min((VW - 2*mx) / ancho, (VH - 2*my) / alto_total)
    OX = (VW - ancho*sc) / 2
    OY = VH - my - 8
    def S(x, y):                                   # x horizontal, y a plomo
        return OX + x*sc, OY - (x*ta + y)*sc
    def tubo(p, q, w=TUBO):
        A, B = S(*p), S(*q)
        return (f'<line x1="{A[0]:.1f}" y1="{A[1]:.1f}" x2="{B[0]:.1f}" y2="{B[1]:.1f}" '
                f'stroke="{ALU}" stroke-width="{w*sc:.1f}" stroke-linecap="butt"/>'
                f'<line x1="{A[0]:.1f}" y1="{A[1]:.1f}" x2="{B[0]:.1f}" y2="{B[1]:.1f}" '
                f'stroke="{NEG}" stroke-width="0.8"/>')
    def rot(p, q):
        A, B = S(*p), S(*q)
        return math.degrees(math.atan2(B[1]-A[1], B[0]-A[0])), ((A[0]+B[0])/2, (A[1]+B[1])/2)
    def et(p, q, txt, dy=-6, col=ROJO, fs=12.5):
        an, m = rot(p, q)
        if an > 90 or an < -90: an += 180
        return (f'<text x="{m[0]:.1f}" y="{m[1]+dy:.1f}" font-size="{fs}" font-weight="800" '
                f'fill="{col}" text-anchor="middle" '
                f'transform="rotate({an:.1f} {m[0]:.1f} {m[1]:.1f})">{txt}</text>')

    o = ['<svg viewBox="0 0 %d %d" xmlns="http://www.w3.org/2000/svg">' % (VW, VH),
         '<defs><marker id="f" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" '
         f'markerHeight="5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{ROJO}"/>'
         '</marker></defs>']
    h = TUBO/2
    # --- las dos V, a plomo
    for x in (h, CUADRO_E - h):
        o.append(tubo((x, 0), (x, CUADRO_E)))
    # --- las dos H, acostadas
    for y in (h, CUADRO_E - h):
        o.append(tubo((TUBO, y), (CUADRO_E - TUBO, y)))
    # --- la X
    a0, a1 = TUBO, CUADRO_E - TUBO
    o.append(tubo((a0, TUBO), (a1, CUADRO_E - TUBO)))
    o.append(tubo((a0, CUADRO_E - TUBO), (a1, TUBO)))
    # --- los dos rombos
    cx = cy = CUADRO_E/2
    for od in (g['q2_od'], g['q3_od']):
        r = (od - TUBO)/2
        for A, B in (((cx-r, cy-r), (cx+r, cy-r)), ((cx+r, cy-r), (cx+r, cy+r)),
                     ((cx+r, cy+r), (cx-r, cy+r)), ((cx-r, cy+r), (cx-r, cy-r))):
            o.append(tubo(A, B))
    # --- letras de cada pieza
    o.append(et((h, 0), (h, CUADRO_E), "V", 4, NEG, 15))
    o.append(et((CUADRO_E-h, 0), (CUADRO_E-h, CUADRO_E), "V", 4, NEG, 15))
    o.append(et((TUBO, h), (CUADRO_E-TUBO, h), "H", 4, NEG, 15))
    o.append(et((TUBO, CUADRO_E-h), (CUADRO_E-TUBO, CUADRO_E-h), "H", 4, NEG, 15))
    o.append(et((a0, TUBO), (a1*0.42, CUADRO_E*0.42), "D1", 4, NEG, 15))
    o.append(et((a0, CUADRO_E-TUBO), (a1*0.40, CUADRO_E*0.62), "D2", 4, NEG, 15))
    o.append(et((a1*0.62, CUADRO_E*0.38), (a1, TUBO), "D2", 4, NEG, 15))
    r2 = (g['q2_od'] - TUBO)/2
    o.append(et((cx-r2, cy-r2), (cx-r2, cy+r2), "C2p", 4, NEG, 12))
    o.append(et((cx-r2, cy+r2), (cx+r2, cy+r2), "C2a", 4, NEG, 12))
    r3 = (g['q3_od'] - TUBO)/2
    o.append(et((cx-r3, cy-r3), (cx-r3, cy+r3), "C3p", 4, NEG, 11))
    o.append(et((cx-r3, cy+r3), (cx+r3, cy+r3), "C3a", 4, NEG, 11))

    # --- cotas
    # ancho horizontal, abajo
    A, B = S(0, -2.6), S(CUADRO_E, -2.6)
    o.append(f'<line x1="{A[0]:.1f}" y1="{A[1]:.1f}" x2="{B[0]:.1f}" y2="{B[1]:.1f}" '
             f'stroke="{ROJO}" stroke-width="1.2" marker-start="url(#f)" marker-end="url(#f)"/>')
    o.append(et((0,-2.6), (CUADRO_E,-2.6), f'{fr(CUADRO_E)}"  EN HORIZONTAL', -7))
    # alto a plomo, a la izquierda
    A, B = S(-2.2, 0), S(-2.2, CUADRO_E)
    o.append(f'<line x1="{A[0]:.1f}" y1="{A[1]:.1f}" x2="{B[0]:.1f}" y2="{B[1]:.1f}" '
             f'stroke="{ROJO}" stroke-width="1.2" marker-start="url(#f)" marker-end="url(#f)"/>')
    m = ((A[0]+B[0])/2, (A[1]+B[1])/2)
    o.append(f'<text x="{m[0]-8:.1f}" y="{m[1]:.1f}" font-size="12.5" font-weight="800" '
             f'fill="{ROJO}" text-anchor="middle" transform="rotate(-90 {m[0]-8:.1f} {m[1]:.1f})">'
             f'{fr(CUADRO_E)}"  A PLOMO</text>')
    # luz de adentro
    o.append(et((TUBO, CUADRO_E-TUBO*2.6), (CUADRO_E-TUBO, CUADRO_E-TUBO*2.6),
                        f'luz de adentro {fr(LUZ)}"', -5, ROJO, 11.5))
    # los rombos
    o.append(et((cx-r2, cy-r2), (cx+r2, cy-r2), f'{fr(g["q2_od"],32)}"', 14, ROJO, 11))
    o.append(et((cx-r3, cy-r3), (cx+r3, cy-r3), f'{fr(g["q3_od"],32)}"', 13, ROJO, 10.5))
    # angulo
    p = (VW - 150.0, 34.0)
    o.append(f'<text x="{p[0]:.1f}" y="{p[1]:.1f}" font-size="15" font-weight="800" '
             f'fill="{ROJO}">PENDIENTE {g["ang"]:g}&#176;</text>')
    o.append(f'<text x="{p[0]:.1f}" y="{p[1]+15:.1f}" font-size="10.5" fill="{ROJO}">'
             f'las H y los</text>')
    o.append(f'<text x="{p[0]:.1f}" y="{p[1]+27:.1f}" font-size="10.5" fill="{ROJO}">'
             f'rombos se</text>')
    o.append(f'<text x="{p[0]:.1f}" y="{p[1]+39:.1f}" font-size="10.5" fill="{ROJO}">'
             f'acuestan asi</text>')
    o.append(f'<text x="{VW/2:.0f}" y="{VH-8}" font-size="12" font-weight="800" '
             f'fill="{NEG}" text-anchor="middle">LAS V Y LOS PIQUES VAN A PLOMO &#183; '
             f'LAS H Y LOS ROMBOS SIGUEN LA PENDIENTE</text>')
    o.append('</svg>')
    return "".join(o)


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
    <div><b>{g['n_bay']+1}</b><span>postes</span></div>
    <div><b>{fr(g['cc'])}"</b><span>centro a centro</span></div>
    <div><b>1</b><span>dibujo</span></div>
  </div>

  <div class="dw">
    <div class="dt">VISTA DE FRENTE &#8212; {g['n_bay']} pa&#241;os, el dibujo en el del medio
      <span class="r">centro a centro {fr(g['cc'])}" POR LA PENDIENTE &#183; l&#237;mite 48"</span></div>
    {alzado(g)}
  </div>

  <div class="pb"></div>
  <div class="hd"><h1>EL DIBUJO DE {e['ang']:g}&#176; &#8212; PLANO EN GRANDE</h1>
    <div class="m">{e['cant']} de estos &#183; van en {e['n'].lower()}<br>
    todas las piezas de 1&#215;1&#215;1/16</div></div>

  <div class="dw"><div class="dt">EL DIBUJO SOLO, CON SUS MEDIDAS
      <span class="r">cada pieza con su letra, igual que en la tabla</span></div>
    {detalle_dibujo(g)}</div>

  <table>
    <tr><th style="width:9%">Pieza</th><th style="width:15%">Perfil</th><th style="width:13%">Largo de corte</th>
        <th style="width:10%">Por dibujo</th><th style="width:9%">Los {e['cant']}</th><th>C&#243;mo se corta</th></tr>
    {piezas}
  </table>
  <div class="warn"><b>{g['n_piezas']} piezas por dibujo.</b> El cuadro mide
  <b>{fr(CUADRO_E)}" a plomo &#215; {fr(CUADRO_E)}" en horizontal</b> (luz de adentro {fr(g['luz_cuadro'])}")
  y flota <b>{fr(g['flot'],32)}" a plomo</b> por debajo del cap y otro tanto por encima del riel.
  Las <b>V</b> y los piques van <b>a plomo</b>; las <b>H</b> y los dos rombos <b>siguen la
  pendiente</b>.</div>

  <div class="pb"></div>
  <div class="hd"><h1>{e['n']} &#8212; LO QUE SE CORTA</h1>
    <div class="m">una escalera &#183; hay {e['cant']} iguales</div></div>
  <table>
    <tr><th style="width:11%">Pieza</th><th style="width:19%">Perfil</th><th style="width:13%">Largo de corte</th>
        <th style="width:8%">Cant.</th><th style="width:9%">Las {e['cant']}</th><th>C&#243;mo se corta</th></tr>
    <tr><td><b>POSTE</b></td><td>2&#215;2&#215;.090</td><td class="n">{fr(g['post_cara_larga'],32)}"</td>
        <td class="n"><b>{g['n_bay']}</b></td><td class="n">{g['n_bay']*e['cant']}</td>
        <td>a plomo. Punta de arriba cortada a <b>{e['ang']:g}&#176;</b>:
            cara larga {fr(g['post_cara_larga'],32)}", cara corta {fr(g['post_cara_corta'],32)}".
            Abajo corte recto. El poste de m&#225;s arriba es el del balc&#243;n.</td></tr>
    <tr><td><b>CAP</b></td><td>2&#215;1&#215;.090 de plano</td><td class="n">{fr(g['cap_largo'])}"</td>
        <td class="n"><b>1</b></td><td class="n">{e['cant']}</td>
        <td>corrido de punta a punta, por la pendiente</td></tr>
    <tr><td><b>RIEL</b></td><td>2&#215;1&#215;.090 acostado</td><td class="n">{fr(g['riel_pano'],32)}"</td>
        <td class="n"><b>{g['n_bay']}</b></td><td class="n">{g['n_bay']*e['cant']}</td>
        <td>uno por pa&#241;o &#183; medido por la pendiente</td></tr>
    <tr><td><b>PIQUE</b></td><td>1&#215;1&#215;1/16</td><td class="n">{fr(g['campo'],32)}"</td>
        <td class="n"><b>{(g['n_bay']-1)*g['n_piq']}</b></td>
        <td class="n">{(g['n_bay']-1)*g['n_piq']*e['cant']}</td>
        <td><b>a plomo</b> &#183; las 2 puntas a <b>{e['ang']:g}&#176;</b>, paralelas entre s&#237;
            (las dos caras miden igual) &#183; {g['n_piq']} por pa&#241;o liso</td></tr>
  </table>
  <div class="warn"><b>Centro a centro de poste: {fr(g['cc'])}" por la pendiente</b>, por debajo de
  las 48" que es el l&#237;mite. {g['n_bay']} pa&#241;os de <b>{fr(g['bay'])}" en horizontal</b>
  ({fr(g['bay']/g['ca'],32)}" por la pendiente). En el pa&#241;o liso van
  <b>{g['n_piq']} piques</b> con <b>{fr(g['sep']+GAP,32)}" de luz libre medida en horizontal</b>,
  que sobre el riel inclinado son marcas cada <b>{fr(g['marca'],32)}"</b>.</div>
"""

TOT = sum(e['cant'] for e in ESCALERAS)
G1, G2 = geo(ESCALERAS[0]), geo(ESCALERAS[1])
HTML = f"""<!DOCTYPE html><html lang="es"><head><meta charset="UTF-8">
<title>Escaleras del Pool House &#8212; fabricaci&#243;n</title><style>{CSS}</style></head>
<body><div class="page">

  <div class="hd"><h1>LAS {TOT} BARANDAS DE ESCALERA &#183; POOL HOUSE</h1>
    <div class="m">BARANDA DE 42" A PLOMO, IGUAL QUE EL BALC&#211;N<br>
    2 de {fr(ESCALERAS[0]['rake'])}" a 34&#176; &#183; 2 de {fr(ESCALERAS[1]['rake'])}" a 33&#176;</div></div>

  <div class="warn"><b>LOS POSTES VAN A MENOS DE 4 PIES, medidos POR LA PENDIENTE.</b>
  La de 34&#176; lleva <b>{G1['n_bay']+1} postes</b> ({fr(G1['cc'])}" de centro a centro) y la de
  33&#176; lleva <b>{G2['n_bay']+1} postes</b> ({fr(G2['cc'])}"). El poste de m&#225;s arriba de cada
  una es el poste del balc&#243;n: la escalera se empata ah&#237; y no lleva uno propio.</div>

  <div class="warn"><b>OJO CON UNA COSA, antes de cortar.</b> Estos planos est&#225;n hechos
  tomando que <b>las 185-1/2" y las 198" las mediste POR LA PENDIENTE</b>, con la cinta pegada al
  stringer. Si es as&#237;, la de 34&#176; <b>sube {feet(G1['rise'])}</b> y la de 33&#176;
  <b>sube {feet(G2['rise'])}</b>. Mide del piso de abajo al deck: si te da eso, seguimos.
  <b>Si te da como 10 pies y medio, me diste la corrida en planta y estas hojas hay que rehacerlas.</b></div>

  <div class="warn"><b>El dibujo de la escalera es m&#225;s chico que el del balc&#243;n</b>
  &#8212; <b>{fr(CUADRO_E)}"</b> en vez de 30-1/4. No es capricho: con los postes a 4 pies las
  bah&#237;as quedan de {fr(G1['bay'])}" y {fr(G2['bay'])}" en horizontal, y el cuadro de 30-1/4
  no cabe. <b>Y va ACOSTADO</b>: el cap sigue la pendiente, y sobre el ancho del cuadro el cap sube
  m&#225;s que todo el campo, as&#237; que derecho no cabe de ninguna manera.</div>

  <div class="warn"><b>Estos dibujos NO son los 32 del balc&#243;n.</b> Son
  <b>{TOT} dibujos nuevos</b> y ni siquiera son iguales entre s&#237;: <b>2 de 34&#176;</b> y
  <b>2 de 33&#176;</b>, con medidas de corte distintas. No los mezcles.</div>
{cuerpo}
</div></body></html>"""


out = HERE / "railing-escaleras.html"
out.write_text(HTML, encoding="utf-8")
print("escrito:", out.name)
for e in ESCALERAS:
    g = geo(e)
    print(f"  {e['n']}:  {fr(e['rake'])}\" a {e['ang']:g}°  x{e['cant']}")
    print(f"      {g['n_bay']} panos de {fr(g['bay'])}\" · {g['n_bay']+1} postes · "
          f"centro a centro {fr(g['cc'])}\" por la pendiente (limite {CC_MAX:g})")
    print(f"      pano liso {g['n_piq']} piques, luz {fr(g['sep']+GAP,32)}\"  ·  "
          f"dibujo: cuadro {fr(CUADRO_E)}\", {g['n_piezas']} piezas, {g['n_fl']} pique(s) por flanco")
