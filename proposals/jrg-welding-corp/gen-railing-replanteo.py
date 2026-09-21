#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PLANO DE REPLANTEO: en planta, DONDE VA CADA POSTE y DONDE CAE CADA EMPATE.

   Con las medidas reales de fabricacion -- o sea las que ya llevan descontadas
   las 2" de los panos que mueren contra la pared -- y con la posicion de cada
   poste acumulada desde el arranque de su corrida, para que en obra se marque
   con la cinta de un tiron y no de poste en poste.

   Todo sale del generador de secciones y del de planta: aqui no se teclea
   ninguna medida."""
import math, pathlib, importlib.util, io, contextlib

HERE = pathlib.Path("/home/user/yourparknow-website/proposals/jrg-welding-corp")
def load(n):
    s = importlib.util.spec_from_file_location(n.replace("-", "_").replace(".py", ""), HERE / n)
    m = importlib.util.module_from_spec(s)
    with contextlib.redirect_stdout(io.StringIO()): s.loader.exec_module(m)
    return m
G = load("gen-railing-secciones.py")
P = load("gen-railing-planta.py")
fr, feet = G.fr, G.feet

NEG, ROJO, VERDE, NAR = "#1b2a41", "#b91c1c", "#0f766e", "#c8571b"
MAD = "#8a6a42"


def con_seccion(run):
    """la corrida entera, cada elemento con la seccion de la que viene.

       El poste prestado solo se pone si el total de la tabla LO INCLUYE. En la
       caballeriza 1 (medidas interiores) el frente carga sus dos postes de
       esquina y el total de los laterales es su material propio: ahi no hay
       nada que prestar. Ver la nota larga en gen-railing-planta.elems()."""
    total, nombres = P.CORRIDA[run]
    el = []
    for nm in nombres:
        for x in P.SEC[nm]['elems']:
            el.append((x[0], None if x[0] == 'P' else x[1], nm, False))
    suma = sum(G.POST if x[0] == 'P' else x[1] for x in el)
    if el[0][0] != 'P' and abs(suma + G.POST - total) < 1e-9:
        el.insert(0, ('P', None, nombres[0], True))      # poste prestado de la corrida vecina
    if run in P.REVERSO: el = el[::-1]
    return el


def postes_de(run):
    """(distancia al EJE del poste desde el arranque de la corrida, tipo, seccion)"""
    el = con_seccion(run)
    out, x = [], 0.0
    for i, (k, w, nm, prest) in enumerate(el):
        if k != 'P':
            x += w; continue
        antes = el[i-1][2] if i > 0 else None
        desp  = el[i+1][2] if i < len(el)-1 else None
        empate = (antes is not None and desp is not None and antes != desp)
        out.append(dict(x=x + G.POST/2, empate=empate, prest=prest, nm=nm,
                        primero=(i == 0), ultimo=(i == len(el)-1)))
        x += G.POST
    assert abs(x - P.CORRIDA[run][0]) < 1e-9, f"la corrida {run} no cierra en el replanteo"
    return out


def afuera(p0, p1, d, centro):
    """la normal que apunta LEJOS del centro del balcon, para que los rotulos
       no caigan encima del dibujo"""
    vx, vy = p1[0]-p0[0], p1[1]-p0[1]
    n = math.hypot(vx, vy) or 1
    nx, ny = -vy/n, vx/n
    mx_, my_ = (p0[0]+p1[0])/2, (p0[1]+p1[1])/2
    if (mx_ - centro[0])*nx + (my_ - centro[1])*ny < 0: nx, ny = -nx, -ny
    return nx*d, ny*d


def balcon(b, VW=792, VH=430):
    tr = P.recorrido(b)
    xs = [p[0] for _, p, q, _ in tr for p in (p, q)]
    ys = [p[1] for _, p, q, _ in tr for p in (p, q)]
    w, h = max(xs)-min(xs), max(ys)-min(ys)
    mx, my = 96, 62
    sc = min((VW-2*mx)/max(w, 1), (VH-2*my)/max(h, 1))
    OX = mx + (VW-2*mx - w*sc)/2 - min(xs)*sc
    OY = VH - my - (VH-2*my - h*sc)/2 + min(ys)*sc
    def S(p): return OX + p[0]*sc, OY - p[1]*sc
    cen = ((min(xs)+max(xs))/2, (min(ys)+max(ys))/2)

    o = ['<svg viewBox="0 0 %d %d" xmlns="http://www.w3.org/2000/svg">' % (VW, VH),
         '<defs><marker id="r" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" '
         f'markerHeight="5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{ROJO}"/>'
         '</marker></defs>']
    n = 0
    filas = []
    for letra, p0, p1, L in tr:
        d = (p1[0]-p0[0], p1[1]-p0[1]); nn = math.hypot(*d) or 1
        u = (d[0]/nn, d[1]/nn); perp = (-u[1], u[0])
        A, B = S(p0), S(p1)
        if letra in ("ESC", "?"):
            o.append(f'<line x1="{A[0]:.1f}" y1="{A[1]:.1f}" x2="{B[0]:.1f}" y2="{B[1]:.1f}" '
                     f'stroke="{MAD}" stroke-width="3" stroke-dasharray="7 5"/>')
            m = ((A[0]+B[0])/2, (A[1]+B[1])/2)
            o.append(f'<text x="{m[0]:.1f}" y="{m[1]-7:.1f}" font-size="10" font-weight="700" '
                     f'fill="{MAD}" text-anchor="middle">'
                     f'{"HUECO ESCALERA" if letra=="ESC" else "SIN MEDIR"}</text>')
            continue
        # Las corridas de MEDIDO llevan 2" menos: la baranda arranca separada de
        # la pared. Se dibuja el largo DE FABRICACION y se marca el hueco.
        hueco = L - P.CORRIDA[letra][0]
        q0 = (p0[0] + u[0]*hueco, p0[1] + u[1]*hueco)
        Aq = S(q0)
        o.append(f'<line x1="{Aq[0]:.1f}" y1="{Aq[1]:.1f}" x2="{B[0]:.1f}" y2="{B[1]:.1f}" '
                 f'stroke="{NEG}" stroke-width="4" opacity=".25"/>')
        if hueco > 1e-9:
            o.append(f'<line x1="{A[0]:.1f}" y1="{A[1]:.1f}" x2="{Aq[0]:.1f}" y2="{Aq[1]:.1f}" '
                     f'stroke="{ROJO}" stroke-width="2.5"/>')
            hx, hy = afuera(p0, q0, 15/sc, cen)
            HM = S(((p0[0]+q0[0])/2 + hx, (p0[1]+q0[1])/2 + hy))
            o.append(f'<text x="{HM[0]:.1f}" y="{HM[1]+3:.1f}" font-size="9.5" font-weight="800" '
                     f'fill="{ROJO}" text-anchor="middle">{fr(hueco)}"</text>')
        # letra de la corrida, al lado de afuera
        lx, ly = afuera(p0, p1, 26/sc, cen)
        m = S(((p0[0]+p1[0])/2 + lx, (p0[1]+p1[1])/2 + ly))
        o.append(f'<text x="{m[0]:.1f}" y="{m[1]+4:.1f}" font-size="15" font-weight="800" '
                 f'fill="{NEG}" text-anchor="middle">{letra}</text>')
        fab = P.CORRIDA[letra][0]
        o.append(f'<text x="{m[0]:.1f}" y="{m[1]+17:.1f}" font-size="11" font-weight="800" '
                 f'fill="{NEG}" text-anchor="middle">{fr(fab)}"</text>')
        if hueco > 1e-9:
            o.append(f'<text x="{m[0]:.1f}" y="{m[1]+29:.1f}" font-size="9.5" '
                     f'fill="{ROJO}" text-anchor="middle">(mediste {fr(L)}")</text>')
        for pt in postes_de(letra):
            # el poste de esquina es UNO SOLO: ya lo numero la corrida anterior.
            # Aqui se dibuja igual pero no se vuelve a numerar ni a contar.
            if pt['prest']:
                c = (q0[0] + u[0]*pt['x'], q0[1] + u[1]*pt['x']); C = S(c)
                o.append(f'<rect x="{C[0]-4.2:.1f}" y="{C[1]-4.2:.1f}" width="8.4" height="8.4" '
                         f'fill="{NEG}" stroke="{NEG}" stroke-width="1.2"/>')
                continue
            n += 1
            c = (q0[0] + u[0]*pt['x'], q0[1] + u[1]*pt['x'])
            C = S(c)
            col = ROJO if pt['empate'] else NEG
            r = 5.5 if pt['empate'] else 4.2
            o.append(f'<rect x="{C[0]-r:.1f}" y="{C[1]-r:.1f}" width="{2*r:.1f}" '
                     f'height="{2*r:.1f}" fill="{"#fff" if pt["empate"] else col}" '
                     f'stroke="{col}" stroke-width="{2.2 if pt["empate"] else 1.2}"/>')
            tx, ty = afuera(p0, p1, -13/sc, cen)
            T = S((c[0]+tx, c[1]+ty))
            o.append(f'<text x="{T[0]:.1f}" y="{T[1]+3:.1f}" font-size="8.5" font-weight="700" '
                     f'fill="{col}" text-anchor="middle">{n}</text>')
            filas.append((n, letra, pt, L))
    o.append('</svg>')
    return "".join(o), filas


CSS = f"""
 *{{margin:0;padding:0;box-sizing:border-box}}
 body{{font-family:'Segoe UI',-apple-system,Helvetica,Arial,sans-serif;color:{NEG};font-size:13px}}
 .page{{max-width:10.2in;margin:0 auto;padding:.3in .35in}}
 @media print{{@page{{size:letter landscape;margin:.3in .35in}}.page{{padding:0;max-width:none}}
              .pb{{page-break-before:always}}.dw{{page-break-inside:avoid}}}}
 .hd{{display:flex;justify-content:space-between;align-items:center;border-bottom:4px solid {NEG};
     padding-bottom:6px;margin-bottom:9px}}
 h1{{font-size:19px;letter-spacing:.4px}} .hd .m{{font-size:11.5px;font-weight:700;text-align:right}}
 .dw{{border:2px solid {NEG};border-radius:5px;margin-bottom:10px}}
 .dw .dt{{background:{NEG};color:#fff;font-size:12px;padding:5px 10px;display:flex}}
 .dw .dt .r{{margin-left:auto;font-weight:400}}
 .dw svg{{display:block;width:100%;height:auto;background:#fff}}
 table{{width:100%;border-collapse:collapse;font-size:11.5px;margin-bottom:9px}}
 th{{background:#41505f;color:#fff;padding:4px 8px;text-align:left;font-size:10.5px}}
 td{{border:1px solid #d3dae1;padding:3.5px 8px}}
 td.n{{text-align:right;white-space:nowrap;font-weight:700}}
 tr.emp td{{background:#fff5f5}}
 .key{{display:flex;gap:11px;margin:8px 0}}
 .key div{{flex:1;border:2px solid #c3ccd5;border-radius:5px;padding:6px 9px;font-size:11.5px}}
 .key b:first-child{{display:block;margin-bottom:2px}}
 .warn{{border-left:5px solid {ROJO};background:#fff5f5;padding:8px 12px;font-size:12px;margin:8px 0}}
"""

cuerpo, tot_p, tot_e = "", 0, 0
for i, b in enumerate(P.BAL):
    svg, filas = balcon(b)
    tot_p += len(filas)
    tot_e += sum(1 for _, _, pt, _ in filas if pt['empate'])
    tb, run_ant = [], None
    for n, letra, pt, L in filas:
        nuevo = letra != run_ant; run_ant = letra
        tipo = ("EMPATE de secciones" if pt['empate'] else
                "arranque de la corrida" if pt['primero'] else
                "final de la corrida" if pt['ultimo'] else "intermedio")
        cls = "emp" if pt['empate'] else ""
        col_run = ("<b>%s</b>  (%s\")" % (letra, fr(P.CORRIDA[letra][0]))) if nuevo else ""
        extra = " &#183; poste de la corrida vecina" if pt['prest'] else ""
        tb.append("<tr class='%s'><td class='n'>%d</td><td>%s</td>"
                  "<td class='n'>%s\"</td><td class='n'>%s</td>"
                  "<td>%s</td><td>%s%s</td></tr>"
                  % (cls, n, col_run, fr(pt['x'],16), feet(pt['x']), tipo, pt['nm'], extra))
    cuerpo += f"""
  {'<div class="pb"></div>' if i else ''}
  <div class="hd"><h1>REPLANTEO &#183; {b['t']}</h1>
    <div class="m">D&#211;NDE VA CADA POSTE Y CADA EMPATE<br>
    {len(filas)} postes &#183; {sum(1 for _,_,p,_ in filas if p['empate'])} empates</div></div>
  <div class="dw"><div class="dt">EN PLANTA
      <span class="r">cuadro relleno = poste &#183; cuadro hueco rojo = EMPATE de dos secciones</span></div>
    {svg}</div>
  <table>
    <tr><th style="width:7%">Poste</th><th style="width:17%">Corrida</th>
        <th style="width:15%">Al eje, desde el arranque</th><th style="width:13%">En pies</th>
        <th style="width:22%">Qu&#233; es</th><th>Secci&#243;n</th></tr>
    {''.join(tb)}
  </table>
"""

HTML = f"""<!DOCTYPE html><html lang="es"><head><meta charset="UTF-8">
<title>Replanteo de postes y empates</title><style>{CSS}</style></head><body><div class="page">

  <div class="hd"><h1>REPLANTEO DE POSTES Y EMPATES &#183; LOS 4 BALCONES</h1>
    <div class="m">EN PLANTA, CON LAS MEDIDAS DE FABRICACI&#211;N<br>
    {tot_p} postes &#183; {tot_e} empates de secciones</div></div>

  <div class="key">
    <div><b style="color:{NEG}">&#9632; POSTE</b>Cuadro relleno. Va soldado dentro de su secci&#243;n.</div>
    <div><b style="color:{ROJO}">&#9633; EMPATE</b>Cuadro hueco rojo. Ah&#237; se juntan dos
         secciones soldadas: el poste lo trae una y la otra llega en pa&#241;o.</div>
    <div><b>LA MEDIDA</b>Al <b>eje del poste</b>, acumulada <b>desde el arranque de su
         corrida</b>. No se encadena de poste en poste.</div>
  </div>

  <div class="warn"><b>Las medidas son las de FABRICACI&#211;N, no las de la cinta.</b>
  En las corridas <b>B, E, G y P</b> ya est&#225;n descontadas las 2" de los pa&#241;os que mueren
  contra la pared: B se fabrica {fr(P.CORRIDA['B'][0])}" (mediste 161), E {fr(P.CORRIDA['E'][0])}"
  (mediste 151-5/8), G {fr(P.CORRIDA['G'][0])}" (mediste 195) y P {fr(P.CORRIDA['P'][0])}"
  (mediste 193-3/8). Al replantear en obra, <b>la baranda arranca separada de la pared</b>:
  el &#250;ltimo poste queda suelto, sin anclaje.</div>

  <div class="warn"><b>C&#243;mo se marca en obra.</b> Se estira la cinta <b>desde el arranque de
  cada corrida</b> y se marcan todos los ejes de un tir&#243;n, con los n&#250;meros de la tabla.
  Marcando de poste en poste el error se acumula y al llegar al final no cuadra el &#250;ltimo pa&#241;o.</div>
{cuerpo}
</div></body></html>"""

out = HERE / "railing-replanteo.html"
out.write_text(HTML, encoding="utf-8")
print("escrito:", out.name)
print(f"  {tot_p} postes · {tot_e} empates de secciones")
for b in P.BAL:
    _, f = balcon(b)
    print(f"    {b['t']:34s} {len(f):2d} postes, "
          f"{sum(1 for _,_,p,_ in f if p['empate'])} empates")
