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
# TODOS LOS CORTES SE HACEN A 33.5, en las cuatro escaleras, aunque dos sean de
# 34 y dos de 33.  Idea de Rene: trabajar en serie con una sola puesta de sierra.
#
# Se puede porque la baranda NO se arma al angulo: se arma a plomo.  Los postes
# van parados sobre el stringer, asi que el cap sale al angulo de verdad solo,
# lo pongan como lo pongan.  El 33.5 es el angulo de la SIERRA, no el de la
# baranda.  Media pulgada de grado deja estos huecos en las juntas:
#     punta del pique (tubo de 1")  ...  1/64"
#     punta del poste (2" de ancho) ...  1/32"
#     largo del pique / de la V     ...  1/64"
#     cuadro del dibujo (24" ancho) ...  0.30" fuera de paralelo, no se ve
# Todos los tapa la soldadura.
#
# Lo que NO se comparte no es por el angulo sino POR EL LARGO de cada escalera:
# el ancho del pano, el riel de cada pano y el cap corrido.
ANG_CORTE = 33.5
CUADRO_E = 24.0      # el cuadro del dibujo de escalera. Mas chico que el del
                     # balcon porque con los postes a 4 pies las bahias son mas
                     # cortas y el de 30-1/4 no cabe.

def reparto(horiz, ca):
    """Cuantos panos van.  Manda el centro a centro de CC_MAX, pero ademas el
       reparto tiene que ser IMPAR y de 5 para arriba, para que salga el patron
       pique-dibujo-pique-dibujo-pique: pique en las dos puntas, dibujos
       alternados y nunca dos pegados.  Rene los quiere alternados como en el
       balcon, no uno solo en el medio."""
    n = 1
    while True:
        bay = (horiz - POST_W * (n + 1)) / n
        if (bay + POST_W) / ca <= CC_MAX:
            break
        n += 1
    n = max(n, 5)
    if n % 2 == 0: n += 1                    # impar: pique en las dos puntas
    bay = (horiz - POST_W * (n + 1)) / n
    assert (bay + POST_W) / ca <= CC_MAX, "mas panos y aun asi pasa del centro a centro"
    return n, bay

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
    i_dib = [i for i in range(n) if i % 2 == 1]      # alternados: 1, 3, 5...
    g['i_dib'] = i_dib
    g['n_dib'] = len(i_dib)
    cad = [('P',)]
    for i in range(n):
        cad += [('D' if i in i_dib else 'L', bay), ('P',)]
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
    ad = math.radians(ANG_CORTE)                   # el CUADRO va al angulo unico
    cad_, tad = math.cos(ad), math.tan(ad)
    g['ca_d'], g['ta_d'] = cad_, tad
    V = 40 - 2 / cad_        # la V y los piques, al angulo de corte: salen iguales
    g['largo_pique'] = V     # en las cuatro escaleras
    H = LUZ / cad_
    P4 = [(0, 0), (LUZ, 0), (LUZ, LUZ), (0, LUZ)]
    Pc = [(x, y + x * tad) for x, y in P4]
    def dd(p, q): return math.hypot(q[0] - p[0], q[1] - p[1])
    D1, D2 = dd(Pc[0], Pc[2]), dd(Pc[1], Pc[3])
    u1 = (Pc[2][0] - Pc[0][0], Pc[2][1] - Pc[0][1])
    u2 = (Pc[3][0] - Pc[1][0], Pc[3][1] - Pc[1][1])
    th = math.degrees(math.acos(abs(u1[0]*u2[0] + u1[1]*u2[1]) / (D1 * D2)))
    desc = (TUBO / 2) / math.sin(math.radians(th))
    g['th'] = th
    # angulos de las puntas, contra el lado a plomo y contra el acostado.
    # Tienen que sumar el angulo de la esquina del paralelogramo o algo esta mal.
    aD1 = math.degrees(math.atan(1 + tad))
    d1_v, d1_h = 90 - aD1, aD1 - ANG_CORTE
    assert abs((d1_v + d1_h) - (90 - ANG_CORTE)) < 1e-6, "la punta de la D1 no cuadra con la esquina"
    dD2 = math.degrees(math.atan2(1 - tad, -1))
    d2_h, d2_v = abs((180 + ANG_CORTE) - dD2), abs(90 - dD2)
    assert abs((d2_v + d2_h) - (90 + ANG_CORTE)) < 1e-6, "la punta de la D2 no cuadra con la esquina"
    g['d1_v'], g['d1_h'], g['d2_v'], g['d2_h'] = d1_v, d1_h, d2_v, d2_h
    # LOS ROMBOS DE ADENTRO, CON LAS 4 CARAS IGUALES. Rene: "que las cuatro
    # caras sean iguales para no pasar trabajo a la hora de cortar".
    # Antes eran cuadros cizallados: 2 caras a plomo y 2 acostadas, distintas.
    # Ahora el lado es la MEDIA de las dos, y las 4 salen del mismo largo.
    # Un rombo con 2 lados a plomo y 2 a ANG_CORTE del mismo largo CIERRA SOLO,
    # sea cual sea el largo: los vectores se cancelan. No hay nada que ajustar.
    esc_q = CUADRO_E / 30.25
    for _od, _k in ((Q2_OD, 'q2'), (Q3_OD, 'q3')):
        _c = _od * esc_q - TUBO                  # centro a centro del cuadro cizallado
        _lado = (_c + _c / cad_) / 2             # la media de la cara a plomo y la acostada
        g[_k + '_lado'] = _lado
        g[_k + '_alto'] = _lado                  # a plomo
        g[_k + '_ancho'] = _lado * cad_          # en horizontal
    q2, q3 = g['q2_lado'], g['q3_lado']
    ag, ob = (90 - ANG_CORTE) / 2, (90 + ANG_CORTE) / 2
    pz = [
      ("V",  2, V,           f"lado del cuadro &#183; A PLOMO &#183; las 2 puntas a {ANG_CORTE:g}&#176;, paralelas"),
      ("H",  2, H,           f"tapa del cuadro &#183; ACOSTADA a {ANG_CORTE:g}&#176; &#183; las 2 puntas a plomo"),
      ("D1", 1, D1,          f"diagonal larga, entera &#183; punta en los 2 lados: "
                             f"<b>{d1_v:.0f}&#176;</b> contra la V y <b>{d1_h:.0f}&#176;</b> contra la H"),
      ("D2", 2, D2/2 - desc, f"media diagonal corta &#183; por fuera <b>{d2_v:.0f}&#176;</b> contra la V "
                             f"y <b>{d2_h:.0f}&#176;</b> contra la H &#183; por dentro muere a ras contra la D1"),
      ("C2", 4, q2,          f"rombo grande &#183; <b>LAS 4 IGUALES</b> &#183; 2 a plomo y 2 acostadas "
                             f"&#183; cada una {ag:.2f}&#176; de un lado y {ob:.2f}&#176; del otro"),
      ("C3", 4, q3,          f"rombo chico &#183; <b>LAS 4 IGUALES</b> &#183; 2 a plomo y 2 acostadas "
                             f"&#183; cada una {ag:.2f}&#176; de un lado y {ob:.2f}&#176; del otro"),
    ]
    if g['n_fl']:
        pz.insert(1, ("B", 2*g['n_fl'], V,
                      f"pique de flanco &#183; A PLOMO &#183; las 2 puntas a {ANG_CORTE:g}&#176;"))
    g['piezas'] = pz
    g['n_piezas'] = sum(q for _, q, _, _ in pz)

    # el poste sale entero del angulo de corte, para que las 4 escaleras lleven
    # EL MISMO largo. El cap se asienta 1/64 mas alto o mas bajo segun la
    # escalera; eso no lo mide nadie y lo absorbe la junta.
    y_cap_b_corte = GUARD - CAP / cad_
    g['post_cara_larga'] = y_cap_b_corte + (POST_W / 2) * tad + 6.0
    g['post_cara_corta'] = y_cap_b_corte - (POST_W / 2) * tad + 6.0
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
            # --- EL CUADRO va al angulo unico ANG_CORTE, no al de la escalera.
            # Se dibuja alrededor del centro de la bahia, con su propia cizalla.
            tad = g['ta_d']
            cxm = (v1 + v2 + TUBO) / 2
            C0 = S(cxm, (g['y_riel_t'] + g['y_cap_b']) / 2)
            def Sd(u, w):                       # u horizontal, w a plomo, desde el centro
                return C0[0] + u*sc, C0[1] - (u*tad + w)*sc
            def barra(p, q, esp=TUBO):
                A, B = Sd(*p), Sd(*q)
                return (f'<line x1="{A[0]:.1f}" y1="{A[1]:.1f}" x2="{B[0]:.1f}" y2="{B[1]:.1f}" '
                        f'stroke="{ALU}" stroke-width="{esp*sc:.1f}" stroke-linecap="butt"/>'
                        f'<line x1="{A[0]:.1f}" y1="{A[1]:.1f}" x2="{B[0]:.1f}" y2="{B[1]:.1f}" '
                        f'stroke="{NEG}" stroke-width="0.7"/>')
            h2 = CUADRO_E/2 - TUBO/2
            L2 = g['luz_cuadro']/2
            for w in (-h2, h2):                                   # las 2 H
                o.append(barra((-L2, w), (L2, w)))
            for pq, qq in (((-L2, -L2), (L2, L2)), ((-L2, L2), (L2, -L2))):
                o.append(barra(pq, qq))                           # la X
            for k in ('q2', 'q3'):                                # los 2 rombos
                hw, hh = g[k+'_ancho']/2, g[k+'_alto']/2
                for A, B in (((-hw,-hh),(hw,-hh)), ((hw,-hh),(hw,hh)),
                             ((hw,hh),(-hw,hh)), ((-hw,hh),(-hw,-hh))):
                    o.append(barra(A, B))

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
        if k == 'D':
            continue                     # el dibujo se ve solo, no hace falta rotularlo
        p = S(x0 + luz/2, g['y_riel_t'] + 4.5)
        o.append(f'<text x="{p[0]:.1f}" y="{p[1]:.1f}" font-size="11.5" font-weight="800" '
                 f'fill="{NEG}" text-anchor="middle" '
                 f'transform="rotate({ang_p:.1f} {p[0]:.1f} {p[1]:.1f})">'
                 f'{g["n_piq"]} PIQUES</text>')

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




# ------------------------------------------ DATOS PARA ARMAR EL DIBUJO
def armado(g):
    """Coordenadas para TIZAR el dibujo en la mesa, y el angulo real de cada
       corte en grados del escuadre. Sin esto el taller no puede armarlo:
       cuatro de los cortes pasan de 59 grados y no los hace la sierra."""
    ta, ang = g['ta_d'], ANG_CORTE   # el cuadro va al angulo unico
    C = CUADRO_E
    def W(x, yp): return (x, x*ta + yp)          # a coordenadas de la mesa
    marcas = []
    for nom, an, al in (("Cuadro de afuera", C, C),
                        ("Rombo grande Q2", g['q2_ancho'], g['q2_alto']),
                        ("Rombo chico Q3", g['q3_ancho'], g['q3_alto'])):
        dx, dy = (C - an) / 2, (C - al) / 2
        esq = [(dx, dy), (dx+an, dy), (dx+an, dy+al), (dx, dy+al)]
        for et, (x, yp) in zip(("abajo izq", "abajo der", "arriba der", "arriba izq"), esq):
            X, Y = W(x, yp)
            marcas.append((nom, et, X, Y))
    a1 = math.degrees(math.atan(1 + ta))
    cortes = [
      ("V",  ang, ang, "las 2 puntas paralelas &#183; sierra", False),
      ("B",  ang, ang, "las 2 puntas paralelas &#183; sierra", False),
      ("H",  ang, ang, "las 2 puntas paralelas &#183; sierra", False),
      ("D1", a1, 90-(a1-ang), "punta de 2 caras &#183; <b>a mano</b>", True),
      ("D2", a1, 90-(a1-ang), "punta de afuera &#183; <b>a mano</b> &#183; la de adentro a ras contra la D1", True),
      ("C2a / C3a", (90+ang)/2, (90+ang)/2, "esquina abierta del rombo &#183; <b>a mano</b>", True),
      ("C2p / C3p", (90+ang)/2, (90+ang)/2, "esquina cerrada del rombo &#183; <b>a mano</b>", True),
    ]
    return marcas, cortes


# ---------------------------------------------- PLANO DEL DIBUJO, EN GRANDE
def detalle_dibujo(g, VW=792, VH=500):
    """El dibujo solo, en grande, con todas las medidas y cada pieza con su letra."""
    ta, ca = g['ta_d'], g['ca_d']   # el cuadro va al angulo unico
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
    for k in ('q2', 'q3'):
        hw, hh = g[k+'_ancho']/2, g[k+'_alto']/2
        for A, B in (((cx-hw, cy-hh), (cx+hw, cy-hh)), ((cx+hw, cy-hh), (cx+hw, cy+hh)),
                     ((cx+hw, cy+hh), (cx-hw, cy+hh)), ((cx-hw, cy+hh), (cx-hw, cy-hh))):
            o.append(tubo(A, B))
    # --- letras de cada pieza
    o.append(et((h, 0), (h, CUADRO_E), "V", 4, NEG, 15))
    o.append(et((CUADRO_E-h, 0), (CUADRO_E-h, CUADRO_E), "V", 4, NEG, 15))
    o.append(et((TUBO, h), (CUADRO_E-TUBO, h), "H", 4, NEG, 15))
    o.append(et((TUBO, CUADRO_E-h), (CUADRO_E-TUBO, CUADRO_E-h), "H", 4, NEG, 15))
    o.append(et((a0, TUBO), (a1*0.42, CUADRO_E*0.42), "D1", 4, NEG, 15))
    o.append(et((a0, CUADRO_E-TUBO), (a1*0.40, CUADRO_E*0.62), "D2", 4, NEG, 15))
    o.append(et((a1*0.62, CUADRO_E*0.38), (a1, TUBO), "D2", 4, NEG, 15))
    for k, lab, fs in (('q2', "C2", 12), ('q3', "C3", 11)):
        hw, hh = g[k+'_ancho']/2, g[k+'_alto']/2
        o.append(et((cx-hw, cy-hh), (cx-hw, cy+hh), lab, 4, NEG, fs))
        o.append(et((cx-hw, cy+hh), (cx+hw, cy+hh), lab, 4, NEG, fs))

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
    # las medidas de los rombos van en la tabla, no encima del dibujo
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

# ============================================================ EMPALME
def empalme(g, VW=792, VH=470):
    """El encuentro del balcon con la escalera, EN EL TALLER: las dos piezas
       dibujadas juntas con sus alturas y el corte del nudillo. Si estas dos
       no salen del taller para encontrarse, en obra no hay nada que hacer."""
    ta, ca, ang = g['ta'], g['ca'], g['ang']
    izq, der = 21.0, 26.0                       # cuanto se ve de cada lado
    mx, my = 96, 38
    ymin = -(der - 1) * ta - 6                  # lo mas bajo: la punta del poste / la escalera
    alto = GUARD - ymin
    sc = min((VW - 2*mx) / (izq + der), (VH - 2*my) / alto)
    OX = (VW - (izq + der) * sc) / 2 + izq * sc     # centrado en la hoja
    OY = VH - my
    def S(x, y):  return OX + x*sc, OY - (y - ymin)*sc
    def poly(pts, f, st=NEG, w=1.2):
        return (f'<polygon points="{" ".join(f"{a:.1f},{b:.1f}" for a,b in pts)}" '
                f'fill="{f}" stroke="{st}" stroke-width="{w}"/>')
    def y0(x): return 0.0 if x <= 1 else -(x - 1) * ta        # linea de narices

    o = ['<svg viewBox="0 0 %d %d" xmlns="http://www.w3.org/2000/svg">' % (VW, VH),
         '<defs><marker id="j" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" '
         f'markerHeight="5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{ROJO}"/>'
         '</marker></defs>']
    # deck
    o.append(poly([S(-izq, 0), S(1, 0), S(1, -2.2), S(-izq, -2.2)], "#e4ddd0", "#b09a72", 1))
    # escalones
    n = max(1, round(der * ta / 7.2))
    for i in range(n + 1):
        xa = 1 + i * der / (n + 1); xb = 1 + (i + 1) * der / (n + 1)
        A, B = S(xa, y0(xa)), S(xb, y0(xb))
        o.append(f'<path d="M {A[0]:.1f} {A[1]:.1f} L {A[0]:.1f} {B[1]:.1f} '
                 f'L {B[0]:.1f} {B[1]:.1f}" fill="none" stroke="#b09a72" stroke-width="2"/>')
    # --- BALCON: riel y cap horizontales
    o.append(poly([S(-izq, 2), S(-1, 2), S(-1, 3), S(-izq, 3)], ALU2))
    o.append(poly([S(-izq, GUARD-1), S(0, GUARD-1), S(0, GUARD), S(-izq, GUARD)], ALU2))
    # --- ESCALERA: riel y cap por la pendiente
    e0, e1 = 1.0, der
    def R(x, d): return y0(x) + d
    o.append(poly([S(e0, R(e0,2)), S(e1, R(e1,2)), S(e1, R(e1,2)+1/ca), S(e0, R(e0,2)+1/ca)], ALU2))
    o.append(poly([S(0, GUARD-1/ca), S(e1, R(e1,GUARD)-1/ca), S(e1, R(e1,GUARD)), S(0, GUARD)], ALU2))
    # --- poste del empalme
    tope = GUARD - 1/ca
    o.append(poly([S(-1, -6), S(1, -6), S(1, tope), S(-1, tope)], ALU, NEG, 1.5))
    # --- el nudillo
    A = S(0, GUARD)
    o.append(f'<circle cx="{A[0]:.1f}" cy="{A[1]:.1f}" r="5" fill="none" stroke="{ROJO}" stroke-width="1.6"/>')
    o.append(f'<line x1="{A[0]+5:.1f}" y1="{A[1]:.1f}" x2="{A[0]+186:.1f}" y2="{A[1]+54:.1f}" '
             f'stroke="{ROJO}" stroke-width="0.9"/>')
    o.append(f'<text x="{A[0]+192:.1f}" y="{A[1]+50:.1f}" font-size="12.5" font-weight="800" '
             f'fill="{ROJO}">NUDILLO DEL CAP</text>')
    o.append(f'<text x="{A[0]+192:.1f}" y="{A[1]+65:.1f}" font-size="11.5" fill="{ROJO}">'
             f'cada cap a <tspan font-weight="800">{ang/2:.2f}&#176;</tspan> del escuadre</text>')
    o.append(f'<text x="{A[0]+192:.1f}" y="{A[1]+79:.1f}" font-size="11.5" fill="{ROJO}">'
             f'los topes se juntan en {fr(GUARD)}" y se suelda</text>')
    # --- cotas de altura, a la izquierda
    xc = -izq - 1.5
    for a, b, t in ((0, 2, "2"), (2, 3, "1"), (3, GUARD-1, fr(GUARD-4)), (GUARD-1, GUARD, "1")):
        P, Q = S(xc, a), S(xc, b)
        o.append(f'<line x1="{P[0]:.1f}" y1="{P[1]:.1f}" x2="{Q[0]:.1f}" y2="{Q[1]:.1f}" '
                 f'stroke="{ROJO}" stroke-width="1.1" marker-start="url(#j)" marker-end="url(#j)"/>')
        o.append(f'<text x="{P[0]-6:.1f}" y="{(P[1]+Q[1])/2+4:.1f}" font-size="11.5" '
                 f'font-weight="800" fill="{ROJO}" text-anchor="end">{t}</text>')
    P, Q = S(xc-3.4, 0), S(xc-3.4, GUARD)
    o.append(f'<line x1="{P[0]:.1f}" y1="{P[1]:.1f}" x2="{Q[0]:.1f}" y2="{Q[1]:.1f}" '
             f'stroke="{ROJO}" stroke-width="1.3" marker-start="url(#j)" marker-end="url(#j)"/>')
    o.append(f'<text x="{P[0]-7:.1f}" y="{(P[1]+Q[1])/2:.1f}" font-size="13" font-weight="800" '
             f'fill="{ROJO}" text-anchor="middle" '
             f'transform="rotate(-90 {P[0]-7:.1f} {(P[1]+Q[1])/2:.1f})">{fr(GUARD)}" A PLOMO</text>')
    # --- rotulos
    o.append(f'<text x="{S(-izq*0.62,0)[0]:.1f}" y="{S(0,GUARD)[1]-14:.1f}" font-size="12.5" '
             f'font-weight="800" fill="{NEG}" text-anchor="middle">BARANDA DEL BALC&#211;N</text>')
    B = S(der*0.62, y0(der*0.62) + GUARD)
    o.append(f'<text x="{B[0]:.1f}" y="{B[1]-12:.1f}" font-size="12.5" font-weight="800" '
             f'fill="{NEG}" text-anchor="middle" '
             f'transform="rotate({math.degrees(math.atan(ta)):.1f} {B[0]:.1f} {B[1]-12:.1f})">'
             f'BARANDA DE LA ESCALERA &#183; {ang:g}&#176;</text>')
    P = S(-1, -6)
    o.append(f'<line x1="{P[0]:.1f}" y1="{P[1]:.1f}" x2="{P[0]-30:.1f}" y2="{P[1]+16:.1f}" '
             f'stroke="{ROJO}" stroke-width="0.9"/>')
    o.append(f'<text x="{P[0]-34:.1f}" y="{P[1]+16:.1f}" font-size="11.5" font-weight="800" '
             f'fill="{ROJO}" text-anchor="end">POSTE DEL EMPALME {fr(tope+6,32)}"</text>')
    o.append(f'<text x="{P[0]-34:.1f}" y="{P[1]+29:.1f}" font-size="10.5" fill="{ROJO}" '
             f'text-anchor="end">punta a {fr(tope,32)}" sobre el deck</text>')
    o.append(f'<text x="{P[0]-34:.1f}" y="{P[1]+41:.1f}" font-size="10.5" fill="{ROJO}" '
             f'text-anchor="end">{fr(abs(tope-(GUARD-CAP)),64)}" m&#225;s corto que los del balc&#243;n</text>')
    o.append('</svg>')
    return "".join(o)


# ---- EL DIBUJO: una sola vez, porque los {TOT_DIB} salen identicos
TOT_DIB = sum(geo(x)["n_dib"] * x["cant"] for x in ESCALERAS)
GD = geo(ESCALERAS[0])              # da igual cual: el dibujo es el mismo
_marcas, _cortes = armado(GD)
marcas_html = "".join(
    f"<tr><td>{'<b>'+nom+'</b>' if i%4==0 else ''}</td><td>{et}</td>"
    f"<td class='n'>{fr(X,16)}\"</td><td class='n'>{fr(Y,16)}\"</td>"
    f"<td>{'&#8212;' if i%4 else 'el cero del tizado' if nom.startswith('Cuadro') else 'centrado en el cuadro'}</td></tr>"
    for i, (nom, et, X, Y) in enumerate(_marcas))
cortes_html = "".join(
    f"<tr style=\"background:{'#fff5f5' if duro else '#fff'}\"><td><b>{pz}</b></td>"
    f"<td class='n'>{x:.1f}&#176;</td><td class='n'>{y:.1f}&#176;</td><td>{nota}</td></tr>"
    for pz, x, y, nota, duro in _cortes)
piezas = "".join(
    f"<tr><td><b>{c}</b></td><td>1&#215;1&#215;1/16</td><td class='n'>{fr(L,32)}\"</td>"
    f"<td class='n'><b>{q}</b></td><td class='n'>{q*TOT_DIB}</td><td>{d}</td></tr>"
    for c, q, L, d in GD['piezas'])
g = GD
DIBUJO_HTML = f"""  <div class="pb"></div>
  <div class="hd"><h1>EL DIBUJO DE {ANG_CORTE:g}&#176; &#8212; PLANO EN GRANDE</h1>
    <div class="m">{TOT_DIB} en total &#183; <b>TODOS IGUALES</b>, en las 4 barandas<br>
    todas las piezas de 1&#215;1&#215;1/16</div></div>

  <div class="dw"><div class="dt">EL DIBUJO SOLO, CON SUS MEDIDAS
      <span class="r">cada pieza con su letra, igual que en la tabla</span></div>
    {detalle_dibujo(g)}</div>

  <table>
    <tr><th style="width:9%">Pieza</th><th style="width:15%">Perfil</th><th style="width:13%">Largo de corte</th>
        <th style="width:10%">Por dibujo</th><th style="width:9%">Los {TOT_DIB}</th><th>C&#243;mo se corta</th></tr>
    {piezas}
  </table>
  <div class="pb"></div>
  <div class="hd"><h1>EL DIBUJO DE {ANG_CORTE:g}&#176; &#8212; C&#211;MO SE ARMA</h1>
    <div class="m">esto es lo que hace falta en el banco<br>tizado en la mesa + &#225;ngulo de cada corte</div></div>

  <div class="warn"><b>Este dibujo NO se arma cortando y juntando.</b> Va <b>tizado en la mesa</b>:
  se marca el paralelogramo con las medidas de abajo, se acuestan las piezas encima y ah&#237; mismo
  se marcan las puntas de las diagonales y de los rombos. <b>Cuatro de los cortes pasan de
  59&#176; del escuadre y la sierra no llega</b> &#8212; esos van a esmeril.</div>

  <h2 style="font-size:12px;background:{NEG};color:#fff;padding:4px 10px;margin:11px 0 6px;
     text-transform:uppercase;letter-spacing:.6px">1 &#183; Tizado en la mesa</h2>
  <p style="font-size:12.5px;margin-bottom:7px">Tira <b>dos l&#237;neas a plomo separadas
  {fr(CUADRO_E)}"</b>. El punto de abajo de la l&#237;nea izquierda es el <b>cero</b>. Desde ah&#237;,
  cada esquina se marca as&#237;: <b>a lo ancho</b> (horizontal, desde el cero) y
  <b>de alto</b> (a plomo, desde el cero).</p>
  <table>
    <tr><th style="width:24%">Pieza</th><th style="width:19%">Esquina</th>
        <th style="width:19%">A lo ancho</th><th style="width:19%">De alto</th><th>Nota</th></tr>
    {marcas_html}
  </table>

  <h2 style="font-size:12px;background:{NEG};color:#fff;padding:4px 10px;margin:11px 0 6px;
     text-transform:uppercase;letter-spacing:.6px">2 &#183; &#193;ngulo de cada corte</h2>
  <p style="font-size:12.5px;margin-bottom:7px">En <b>grados del escuadre</b>: lo que se le mete
  a la sierra. Cero es corte recto.</p>
  <table>
    <tr><th style="width:18%">Pieza</th><th style="width:16%">Punta 1</th>
        <th style="width:16%">Punta 2</th><th>C&#243;mo</th></tr>
    {cortes_html}
  </table>

  <div class="warn"><b>{g['n_piezas']} piezas por dibujo.</b> El cuadro mide
  <b>{fr(CUADRO_E)}" a plomo &#215; {fr(CUADRO_E)}" en horizontal</b> (luz de adentro {fr(g['luz_cuadro'])}")
  y flota <b>{fr(g['flot'],32)}" a plomo</b> por debajo del cap y otro tanto por encima del riel.
  Las <b>V</b> y los piques van <b>a plomo</b>; las <b>H</b> y los dos rombos <b>siguen la
  pendiente</b>.</div>

"""

cuerpo = ""
for i, e in enumerate(ESCALERAS):
    g = geo(e)
    salto = '<div class="pb"></div>' if i else ''
    _marcas, _cortes = armado(g)
    # marcas del pano liso: SIEMPRE desde la punta de abajo del riel, no de
    # pique en pique, para que el error no se acumule. Lo pidio asi desde el principio.
    _mk = [(g['sep'] + i*(TUBO + g['sep']) + TUBO/2) / g['ca'] for i in range(g['n_piq'])]
    assert abs((_mk[-1]*g['ca'] + TUBO/2 + g['sep']) - g['panel']) < 1e-9, "las marcas no cierran"
    marcas_riel = " &nbsp;<span style='color:#c8571b'>|</span>&nbsp; ".join(fr(m,16) for m in _mk)
    marcas_html = "".join(
        f"<tr><td>{'<b>'+nom+'</b>' if i%4==0 else ''}</td><td>{et}</td>"
        f"<td class='n'>{fr(X,16)}\"</td><td class='n'>{fr(Y,16)}\"</td>"
        f"<td>{'&#8212;' if i%4 else 'el cero del tizado' if nom.startswith('Cuadro') else 'centrado en el cuadro'}</td></tr>"
        for i, (nom, et, X, Y) in enumerate(_marcas))
    cortes_html = "".join(
        f"<tr style=\"background:{'#fff5f5' if duro else '#fff'}\"><td><b>{pz}</b></td>"
        f"<td class='n'>{x:.1f}&#176;</td><td class='n'>{y:.1f}&#176;</td><td>{nota}</td></tr>"
        for pz, x, y, nota, duro in _cortes)
    piezas = "".join(
        f"<tr><td><b>{c}</b></td><td>1&#215;1&#215;1/16</td><td class='n'>{fr(L,32)}\"</td>"
        f"<td class='n'><b>{q}</b></td><td class='n'>{q*e['cant']*g['n_dib']}</td><td>{d}</td></tr>"
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
    <div><b>{g['n_dib']}</b><span>dibujos</span></div>
  </div>

  <div class="dw">
    <div class="dt">VISTA DE FRENTE &#8212; {g['n_bay']} pa&#241;os &#183; {g['n_dib']} dibujos alternados
      <span class="r">centro a centro {fr(g['cc'])}" POR LA PENDIENTE &#183; l&#237;mite 48"</span></div>
    {alzado(g)}
  </div>

  <div class="pb"></div>
  <div class="hd"><h1>EMPALME CON EL BALC&#211;N &#8212; {e['n'].replace("ESCALERA DEL ","")}</h1>
    <div class="m">LAS DOS BARANDAS JUNTAS &#183; {e['ang']:g}&#176;<br>
    esto es lo que tiene que salir del taller para que se encuentren</div></div>
  <div class="dw"><div class="dt">EL ENCUENTRO, A ESCALA
      <span class="r">alturas sobre el piso del deck</span></div>{empalme(g)}</div>
  <table>
    <tr><th style="width:30%">Cara</th><th style="width:18%">Balc&#243;n</th>
        <th style="width:18%">Escalera</th><th>Qu&#233; pasa</th></tr>
    <tr><td><b>Tope del cap</b></td><td class="n">{fr(GUARD)}"</td>
        <td class="n">{fr(GUARD)}"</td>
        <td style="color:#0f766e"><b>COINCIDEN.</b> Es la cara que se ve de frente.</td></tr>
    <tr><td><b>Panza del riel</b></td><td class="n">2"</td><td class="n">2"</td>
        <td style="color:#0f766e"><b>COINCIDEN.</b> La otra cara que se ve.</td></tr>
    <tr><td>Panza del cap</td><td class="n">{fr(GUARD-CAP)}"</td>
        <td class="n">{fr(g['y_cap_b'],32)}"</td>
        <td>nudillo de {fr(abs((GUARD-CAP)-g['y_cap_b']),64)}" &#183; va por dentro, se suelda</td></tr>
    <tr><td>Tope del riel</td><td class="n">3"</td><td class="n">{fr(g['y_riel_t'],32)}"</td>
        <td>nudillo de {fr(abs(3-g['y_riel_t']),64)}" &#183; va por dentro, se suelda</td></tr>
  </table>
  <div class="warn"><b>El nudillo del cap:</b> los dos caps se cortan a
  <b>{e['ang']/2:.2f}&#176; del escuadre</b> y se juntan por el tope, en las {fr(GUARD)}".
  Si los cortas los dos a <b>{ANG_CORTE/2:.2f}&#176;</b> (el &#225;ngulo &#250;nico) te queda un hueco de
  1/64" a lo ancho del cap, que lo tapa la soldadura.<br>
  <b>El poste del empalme es m&#225;s corto que los del balc&#243;n:</b>
  <b>{fr(g['y_cap_b']+6,32)}"</b>, con la punta a {fr(g['y_cap_b'],32)}" sobre el deck &#8212; porque el
  cap de la escalera, al ir acostado, tiene la panza m&#225;s abajo que el del balc&#243;n.</div>

  <div class="pb"></div>
  <div class="hd"><h1>{e['n']} &#8212; LO QUE SE CORTA</h1>
    <div class="m">una escalera &#183; hay {e['cant']} iguales</div></div>
  <table>
    <tr><th style="width:11%">Pieza</th><th style="width:19%">Perfil</th><th style="width:13%">Largo de corte</th>
        <th style="width:8%">Cant.</th><th style="width:9%">Las {e['cant']}</th><th>C&#243;mo se corta</th></tr>
    <tr><td><b>POSTE</b></td><td>2&#215;2&#215;.090</td><td class="n">{fr(g['post_cara_larga'],32)}"</td>
        <td class="n"><b>{g['n_bay']}</b></td><td class="n">{g['n_bay']*e['cant']}</td>
        <td>a plomo. Punta de arriba cortada a <b>{ANG_CORTE:g}&#176;</b>:
            cara larga {fr(g['post_cara_larga'],32)}", cara corta {fr(g['post_cara_corta'],32)}".
            Abajo corte recto. El poste de m&#225;s arriba es el del balc&#243;n.</td></tr>
    <tr><td><b>CAP</b></td><td>2&#215;1&#215;.090 de plano</td><td class="n">{fr(g['cap_largo'])}"</td>
        <td class="n"><b>1</b></td><td class="n">{e['cant']}</td>
        <td>corrido de punta a punta, por la pendiente</td></tr>
    <tr><td><b>RIEL</b></td><td>2&#215;1&#215;.090 acostado</td><td class="n">{fr(g['riel_pano'],32)}"</td>
        <td class="n"><b>{g['n_bay']}</b></td><td class="n">{g['n_bay']*e['cant']}</td>
        <td>uno por pa&#241;o &#183; medido por la pendiente</td></tr>
    <tr><td><b>PIQUE</b></td><td>1&#215;1&#215;1/16</td><td class="n">{fr(g['campo'],32)}"</td>
        <td class="n"><b>{(g['n_bay']-g['n_dib'])*g['n_piq']}</b></td>
        <td class="n">{(g['n_bay']-g['n_dib'])*g['n_piq']*e['cant']}</td>
        <td><b>a plomo</b> &#183; las 2 puntas a <b>{e['ang']:g}&#176;</b>, paralelas entre s&#237;
            (las dos caras miden igual) &#183; {g['n_piq']} por pa&#241;o liso</td></tr>
  </table>
  <h2 style="font-size:12px;background:{NEG};color:#fff;padding:4px 10px;margin:11px 0 6px;
     text-transform:uppercase;letter-spacing:.6px">Marcas de los piques sobre el riel inclinado</h2>
  <p style="font-size:12.5px;margin-bottom:6px">Las <b>{g['n_piq']} marcas van al centro de cada
  pique</b> y <b>todas se miden desde la punta de abajo del riel</b>, no de pique en pique
  &#8212; as&#237; el error no se acumula. Medidas <b>sobre el riel</b>, que va inclinado.</p>
  <table><tr><th style="width:15%">Riel</th><th>Marcas desde la punta de abajo</th></tr>
    <tr><td><b>{fr(g['riel_pano'],32)}"</b></td>
        <td style="font-family:Consolas,monospace;font-size:11.5px">{marcas_riel}</td></tr></table>

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
{DIBUJO_HTML}
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
