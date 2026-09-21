#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Los cuatro balcones EN PLANTA, para revisar el reparto.
   Se ven los postes y cada pano: NARANJA = dibujo, BLANCO = piques rectos.
   Medida total de cada lateral. Los largos salen del generador de secciones."""
import importlib.util, pathlib, math

HERE = pathlib.Path("/home/user/yourparknow-website/proposals/jrg-welding-corp")
spec = importlib.util.spec_from_file_location("gsec", HERE / "gen-railing-secciones.py")
G = importlib.util.module_from_spec(spec); spec.loader.exec_module(G)
fr, feet, piques_de = G.fr, G.feet, G.piques_de

# ---------------------------------------------------------------- recorridos
# Los dos del Pool House viran para el MISMO lado y los dos llevan escalera
# al final del retorno largo.  Las dos caballerizas van giradas 90 en la hoja.
BAL = [
 dict(t="BALCÓN 1  ·  POOL HOUSE", esc='ESCALERA  185" a 34°',
      ini="PARED DE LA CASA", fin="ARRANQUE DE LA ESCALERA",
      pasos=[("B","N"), ("A","O"), ("C","S")]),
 dict(t="BALCÓN 2  ·  POOL HOUSE", esc='ESCALERA  198" a 33°',
      ini="PARED DE LA CASA", fin="ARRANQUE DE LA ESCALERA",
      pasos=[("E","N"), ("D","O"), ("F","S")]),
 dict(t="BALCÓN 3  ·  CABALLERIZA LADO 1", esc=None, girar=True,
      ini="PARED DE LA CABALLERIZA", fin="PARED DE LA CABALLERIZA",
      pasos=[("G","E"), ("H","N"), ("J","O"), ("K","S"), ("ESC","O"), ("M","S"), ("L","O")]),
 dict(t="BALCÓN 4  ·  CABALLERIZA LADO 2", esc=None, girar=True,
      ini="PARED DE LA CABALLERIZA", fin="PARED DE LA CABALLERIZA",
      pasos=[("P","O"), ("N","S"), ("?","E"), ("Q","N"), ("ESC","E"), ("R","S")]),
]
INCOGNITA = 108.0
HUECO_ESC = 27.0      # hueco de la escalera: 27" medido en el lado 1.  En el lado 2 lo asumo igual.
                      # Esas escaleras SIGUEN DE MADERA: no llevan baranda de aluminio.
# Lo que MIDIO en obra.  El taller fabrica 2" menos en los panos que mueren contra
# la casa: ahi el ultimo poste queda suelto, separado de la pared, sin anclaje.
MEDIDO = {"B": 161.0, "E": 151.625,      # pool house
          "G": 195.0, "P": 193.375}      # caballerizas

SEC, CORRIDA = {}, {}
for cfg in G.EDIFICIOS:
    for _, grupo in cfg['grupos']:
        for s in grupo:
            s['largo'] = G.largo(s); SEC[s['name']] = s
    for _, run, total, nombres in cfg['corridas']:
        CORRIDA[run] = (total, nombres)

def elems(run):
    """rearma la corrida completa a partir de sus secciones"""
    total, nombres = CORRIDA[run]
    el = []
    for i, nm in enumerate(nombres):
        e = SEC[nm]['elems']
        if i == 0 and e[0][0] != 'P':
            el.append(('P',))          # el poste de esquina lo lleva la corrida vecina
        el.extend(e)
    assert abs(sum(2.0 if x[0]=='P' else x[1] for x in el) - total) < 1e-9, run
    return el[::-1] if run in REVERSO else el

REVERSO = {"A","B","D","E"}   # definidas de la esquina hacia la pared; el plano va al reves
DX = {"N":(0,1), "S":(0,-1), "E":(1,0), "O":(-1,0)}
GIRO = {"N":"E", "E":"S", "S":"O", "O":"N"}

def recorrido(b):
    x = y = 0.0; out = []
    for letra, rumbo in b['pasos']:
        L = (HUECO_ESC if letra == "ESC" else
             INCOGNITA if letra == "?" else MEDIDO.get(letra, CORRIDA[letra][0]))
        dx, dy = DX[rumbo]
        p0 = (x, y); x += dx*L; y += dy*L
        out.append((letra, p0, (x, y), L))
    return out

def pies(b):
    """pies lineales de BARANDA: el hueco de la escalera no cuenta"""
    return sum(L for letra,_,_,L in recorrido(b) if letra != 'ESC')

def cuenta(b):
    d = q = 0
    for letra, *_ in recorrido(b):
        if letra == "ESC": continue                  # el hueco no lleva baranda
        if letra == "?": d += 1; q += 2; continue    # 1 dibujo entre 2 panos de piques
        for e in elems(letra):
            if e[0] == 'D': d += 1
            elif e[0] == 'L': q += 1
    return d, q

# ---------------------------------------------------------------- dibujo
NEG, NAR, ROJO = "#1b2a41", "#e07b39", "#b91c1c"
VW, VH, M = 940, 600, 112
VW_A, VH_A = 470, 660        # caballerizas: derechas como el croquis, angostas

def svg(b):
    VW, VH = (VW_A, VH_A) if b.get('girar') else (940, 600)
    tr = recorrido(b)
    xs = [p for _,a,c,_ in tr for p in (a[0], c[0])]
    ys = [p for _,a,c,_ in tr for p in (a[1], c[1])]
    w, h = max(xs)-min(xs), max(ys)-min(ys)
    sc = min((VW-2*M)/max(w,1), (VH-2*M)/max(h,1))
    ox = M + (VW-2*M - w*sc)/2 - min(xs)*sc
    oy = VH - M - (VH-2*M - h*sc)/2 + min(ys)*sc
    X = lambda v: ox + v*sc
    Y = lambda v: oy - v*sc
    o = ['<defs><marker id="pa" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" '
         f'markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{ROJO}"/>'
         '</marker></defs>']

    def perp(p0, p1, d):
        vx, vy = p1[0]-p0[0], p1[1]-p0[1]
        n = math.hypot(vx, vy) or 1
        return (-vy/n*d, vx/n*d)

    for letra, p0, p1, L in tr:
        ux = (p1[0]-p0[0])/L; uy = (p1[1]-p0[1])/L       # unitario del avance
        nx, ny = perp(p0, p1, 1.0)                        # normal unitaria
        vert = abs(p1[0]-p0[0]) < 1e-6

        def barra(t0, t1, fill, stroke, sw, gordo):
            a = (p0[0]+ux*t0, p0[1]+uy*t0); c = (p0[0]+ux*t1, p0[1]+uy*t1)
            g = gordo/2
            pts = [(a[0]+nx*g/sc, a[1]+ny*g/sc), (c[0]+nx*g/sc, c[1]+ny*g/sc),
                   (c[0]-nx*g/sc, c[1]-ny*g/sc), (a[0]-nx*g/sc, a[1]-ny*g/sc)]
            d = " ".join(f"{X(px):.1f},{Y(py):.1f}" for px, py in pts)
            o.append(f'<polygon points="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')

        if letra == "ESC":
            # hueco de la escalera: pelda\u00f1os, sin baranda
            for k in range(7):
                tt = L*(k+0.5)/7
                a2=(p0[0]+ux*tt+nx*26/sc, p0[1]+uy*tt+ny*26/sc)
                c2=(p0[0]+ux*tt-nx*26/sc, p0[1]+uy*tt-ny*26/sc)
                o.append(f'<line x1="{X(a2[0]):.1f}" y1="{Y(a2[1]):.1f}" x2="{X(c2[0]):.1f}" '
                         f'y2="{Y(c2[1]):.1f}" stroke="#8a6a42" stroke-width="2"/>')
            mE=(p0[0]+ux*L/2, p0[1]+uy*L/2)
            o.append(f'<text x="{X(mE[0]):.1f}" y="{Y(mE[1])+46:.1f}" font-size="13" font-weight="800" '
                     f'fill="#8a6a42" text-anchor="middle">ESCALERA (madera)</text>')
            continue
        if letra == "?":
            barra(0, L, "#fdf0e4", NAR, 2, 13)
        else:
            t = L - CORRIDA[letra][0]      # el hueco de las 2" va contra la pared
            for e in elems(letra):
                if e[0] == 'P':
                    cx, cy = p0[0]+ux*(t+1), p0[1]+uy*(t+1)
                    o.append(f'<rect x="{X(cx)-5:.1f}" y="{Y(cy)-5:.1f}" width="10" height="10" '
                             f'fill="{NEG}"/>')
                    t += 2.0
                else:
                    if e[0] == 'D': barra(t, t+e[1], NAR, "#a8531f", 1, 13)
                    else:           barra(t, t+e[1], "#fff", NEG, 1.6, 13)
                    t += e[1]

        # cota total del lateral, por fuera
        ox2, oy2 = perp(p0, p1, (24 if L < 60 else 40)/sc)   # corridas cortas, cota mas pegada
        a = (p0[0]+ox2, p0[1]+oy2); c = (p1[0]+ox2, p1[1]+oy2)
        o.append(f'<line x1="{X(a[0]):.1f}" y1="{Y(a[1]):.1f}" x2="{X(c[0]):.1f}" y2="{Y(c[1]):.1f}" '
                 f'stroke="{ROJO}" stroke-width="1.3" marker-start="url(#pa)" marker-end="url(#pa)"/>')
        mx, my = (a[0]+c[0])/2, (a[1]+c[1])/2
        rot = f' transform="rotate(-90 {X(mx):.1f} {Y(my):.1f})"' if vert else ''
        txt = "SIN MEDIR" if letra == "?" else f'{fr(L)}"   ({feet(L)})'
        o.append(f'<text x="{X(mx):.1f}" y="{Y(my)-8:.1f}" font-size="{13 if L < 60 else 17}" font-weight="800" '
                 f'fill="{ROJO}" text-anchor="middle"{rot}>{txt}</text>')
        if letra in MEDIDO:
            o.append(f'<text x="{X(mx):.1f}" y="{Y(my)+11:.1f}" font-size="11.5" font-weight="700" '
                     f'fill="{NAR}" text-anchor="middle"{rot}>se fabrica {fr(CORRIDA[letra][0])}"</text>')

    # remates y escalera
    for idx, (p, t) in enumerate(((tr[0][1], b['ini']), (tr[-1][2], b['fin']))):
        # la pared se corre hacia afuera: el poste del remate tiene que verse,
        # y entre poste y pared queda el hueco (ahi no hay anclaje)
        q0, q1 = (tr[0][1], tr[0][2]) if idx == 0 else (tr[-1][1], tr[-1][2])
        vx, vy = q1[0]-q0[0], q1[1]-q0[1]
        n = math.hypot(vx, vy) or 1
        sgn = -1 if idx == 0 else 1
        px = p[0] + sgn*vx/n*16/sc; py = p[1] + sgn*vy/n*16/sc
        o.append(f'<rect x="{X(px)-11:.1f}" y="{Y(py)-11:.1f}" width="22" height="22" fill="#8a6a42"/>')
        der = X(px) > VW/2
        o.append(f'<text x="{X(px) + (-15 if der else 15):.1f}" y="{Y(py)+4:.1f}" font-size="12" '
                 f'font-weight="800" fill="#8a6a42" text-anchor="{"end" if der else "start"}">{t}</text>')
    if b.get('esc'):
        p = tr[-1][2]
        o.append(f'<text x="{X(p[0]) + (-17 if X(p[0])>VW/2 else 17):.1f}" y="{Y(p[1])+19:.1f}" '
                 f'font-size="12" font-weight="800" fill="{ROJO}" '
                 f'text-anchor="{"end" if X(p[0])>VW/2 else "start"}">{b["esc"]}</text>')
    return f'<svg viewBox="0 0 {VW} {VH}" xmlns="http://www.w3.org/2000/svg">' + "".join(o) + '</svg>'

def tabla(b):
    f = []
    for letra, _, _, L in recorrido(b):
        if letra == "ESC":
            f.append('<tr><td><b>Escalera</b></td><td class="n"><i>hueco, sin baranda</i></td>'
                     '<td class="n">\u2014</td><td class="n">\u2014</td></tr>')
            continue
        if letra == "?":
            f.append(f'<tr><td><b>Lateral ?</b></td><td class="n"><i>sin medir</i></td>'
                     f'<td class="n">—</td><td class="n">—</td></tr>')
            continue
        el = elems(letra)
        d = sum(1 for e in el if e[0] == 'D')
        q = sum(1 for e in el if e[0] == 'L')
        extra = (f' <span style="color:{NAR};font-weight:700">\u2192 se fabrica '
                 f'{fr(CORRIDA[letra][0])}"</span>') if letra in MEDIDO else ''
        f.append(f'<tr><td><b>Lateral {letra}</b></td><td class="n">{fr(L)}" ({feet(L)}){extra}</td>'
                 f'<td class="n">{d}</td><td class="n">{q}</td></tr>')
    return "".join(f)

CSS = """
 *{margin:0;padding:0;box-sizing:border-box}
 body{font-family:'Segoe UI',-apple-system,Helvetica,Arial,sans-serif;color:#1b2a41;background:#fff;font-size:14px}
 .page{max-width:10.2in;margin:0 auto;padding:.3in .35in}
 @media print{@page{size:letter landscape;margin:.3in .35in}.page{padding:0;max-width:none}
              .pb{page-break-before:always}}
 .hd{display:flex;justify-content:space-between;align-items:center;border-bottom:4px solid #1b2a41;
     padding-bottom:6px;margin-bottom:10px}
 h1{font-size:23px;letter-spacing:.5px}
 .hd .m{font-size:13px;font-weight:700;text-align:right}
 .dw{border:2px solid #1b2a41;border-radius:5px;margin-bottom:10px}
 .dw svg{display:block;width:100%;height:auto;background:#fdfdfb}
 .key{display:flex;gap:14px;margin:10px 0;font-size:14px;align-items:center}
 .key span{display:flex;align-items:center;gap:7px}
 .sw{width:34px;height:13px;display:inline-block;border:1.6px solid #1b2a41}
 table{width:100%;border-collapse:collapse;margin:8px 0;font-size:15px}
 th{background:#1b2a41;color:#fff;padding:6px 10px;text-align:left}
 td{border:1px solid #c3ccd5;padding:5px 10px}
 td.n{text-align:right;white-space:nowrap;font-weight:700}
 tr.tot td{background:#eef2f6;font-size:16px}
 .nota{border-left:4px solid #c8571b;background:#fff8f2;padding:8px 12px;font-size:13px;margin:8px 0}
"""
LEY = ('<div class="key">'
       f'<span><i class="sw" style="background:{NAR};border-color:#a8531f"></i> <b>PAÑO CON DIBUJO</b></span>'
       '<span><i class="sw" style="background:#fff"></i> <b>PAÑO DE PIQUES RECTOS</b></span>'
       f'<span><i style="display:inline-block;width:13px;height:13px;background:{NEG}"></i> <b>POSTE</b></span>'
       '<span><i style="display:inline-block;width:15px;height:15px;background:#8a6a42"></i> <b>PARED</b> (la baranda NO se ancla a ella: muere en su poste)</span>'
       '</div>')

pag = ""
TD = TQ = 0
for i, b in enumerate(BAL):
    d, q = cuenta(b); TD += d; TQ += q
    tot = pies(b)
    pag += f"""
  {'<div class="pb"></div>' if i else ''}
  <div class="hd"><h1>{b['t']}</h1>
    <div class="m">{fr(tot)}" en total &#183; {tot/12:.1f} pies<br>{d} pa&#241;os con dibujo &#183; {q} de piques</div></div>
  <div class="dw"{' style="max-width:56%"' if b.get("girar") else ""}>{svg(b)}</div>
  {LEY}
  <table><tr><th style="width:20%">Lateral</th><th style="width:28%">Medida total</th>
    <th style="width:20%">Pa&#241;os con dibujo</th><th>Pa&#241;os de piques</th></tr>{tabla(b)}
    <tr class="tot"><td><b>TODO EL BALC&#211;N</b></td><td class="n">{fr(tot)}" ({tot/12:.1f} pies)</td>
      <td class="n">{d}</td><td class="n">{q}</td></tr></table>"""

html = f"""<!DOCTYPE html><html lang="es"><head><meta charset="UTF-8">
<title>Los cuatro balcones en planta</title><style>{CSS}</style></head><body><div class="page">
  <div class="hd"><h1>LOS CUATRO BALCONES EN PLANTA</h1>
    <div class="m">PARA REVISAR EL REPARTO<br>REV. 2 &#183; SEPT 20, 2026</div></div>
  {LEY}
  <table>
    <tr><th>Balc&#243;n</th><th style="width:22%">Total</th><th style="width:18%">Con dibujo</th><th style="width:18%">De piques</th></tr>
    {"".join(f'<tr><td><b>{b["t"]}</b></td><td class="n">{pies(b)/12:.1f} pies</td>'
             f'<td class="n">{cuenta(b)[0]}</td><td class="n">{cuenta(b)[1]}</td></tr>' for b in BAL)}
    <tr class="tot"><td><b>LOS CUATRO</b></td>
      <td class="n">{sum(pies(b) for b in BAL)/12:.1f} pies</td>
      <td class="n">{TD}</td><td class="n">{TQ}</td></tr>
  </table>
  <div class="nota"><b>Los dos del Pool House viran para el mismo lado</b> y los dos llevan la escalera
  al final del retorno largo, como en tus fotos. En las caballerizas el contorno de tu croquis no cierra,
  as&#237; que <b>revisa hacia d&#243;nde dobla cada lateral</b>. Si alguno est&#225; volteado, m&#225;rcalo:
  no cambia ni una medida ni una pieza.<br>
  <b>Las escaleras de las dos caballerizas se quedan de madera por ahora</b>, as&#237; que la baranda se para a cada lado del hueco y no baja. Las <b>&#250;nicas escaleras de aluminio son las 4 del Pool House</b>: 185-1/2 a 34&#176; dos veces y 198 a 33&#176; dos veces.<br>
  <b>Las 2" que pediste</b> salen de los cuatro pa&#241;os que mueren contra pared: <b>B</b> y <b>E</b> del
  Pool House y <b>G</b> y <b>P</b> de las caballerizas. Ah&#237; el poste queda suelto, separado de la
  pared, sin anclaje.
  El plano lleva <b>la medida que t&#250; tomaste</b> y debajo, en naranja, <b>lo que se fabrica</b>.</div>
{pag}
</div></body></html>"""

out = HERE / "railing-planta-balcones.html"
out.write_text(html, encoding="utf-8")
print("escrito:", out.name)
for b in BAL:
    d, q = cuenta(b); tot = pies(b)
    print(f"  {b['t']:34s} {tot/12:5.1f} pies · {d} dibujos · {q} de piques")
print(f"  {'LOS CUATRO':34s} {sum(pies(b) for b in BAL)/12:5.1f} pies "
      f"· {TD} dibujos · {TQ} de piques")
