#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Planos de FABRICACION de las dos caballerizas.
   Dibujo simple + despiece.  NO lleva el despiece del dibujito: esos ya estan hechos.
   Lo que lleva: poste, cap, riel de cada pano, piques, y donde va el dibujo."""
import importlib.util, pathlib
from fractions import Fraction

HERE = pathlib.Path("/home/user/yourparknow-website/proposals/jrg-welding-corp")
spec = importlib.util.spec_from_file_location("gsec", HERE / "gen-railing-secciones.py")
G = importlib.util.module_from_spec(spec); spec.loader.exec_module(G)
# la medida de la oreja se saca de su propia hoja: antes estaba tecleada aqui
# a mano y las dos hojas del mismo set daban medidas distintas.
_sa = importlib.util.spec_from_file_location("ganc", HERE / "gen-railing-detalle-anclaje.py")
import io, contextlib
ANC = importlib.util.module_from_spec(_sa)
with contextlib.redirect_stdout(io.StringIO()): _sa.loader.exec_module(ANC)
fr, feet, piques_de = G.fr, G.feet, G.piques_de
POST, POST_LEN, Y_CAP_B, Y_RAIL_T, Y_DECK = G.POST, G.POST_LEN, G.Y_CAP_B, G.Y_RAIL_T, G.Y_DECK

G.SC = 3.35
G.OX, G.OY = 92, 62
SC, OX, OY = G.SC, G.OX, G.OY
VW, VH = 792, 326
X, Y = G.X, G.Y
NEG, ROJO, VERDE, NAR = "#1b2a41", "#b91c1c", "#0f766e", "#c8571b"
AIRE, CUADRO = 3.875, 30.25            # el dibujito flota 3-7/8 bajo el cap y sobre el riel

def punta(txt):
    if "EMPATE" in txt:  return ("CONEXIÓN", ROJO, True)
    if "ESCALERA" in txt or "HUECO" in txt: return ("MUERE EN LA ESCALERA", NEG, False)
    if "PARED" in txt or "CASA" in txt: return ("MUERE CONTRA LA PARED", NEG, False)
    if "ESQUINA" in txt: return ("ESQUINA", NEG, False)
    return ("TERMINA", NEG, False)

def vecino(txt):
    import re
    m = re.search(r"\b([A-R]-\d)\b", txt)
    return m.group(1) if m else ""

cap_largo = G.cap_largo          # una sola definicion, en gen-railing-secciones

def svg(s):
    o, T = [], s['largo']
    el = s['elems']
    o.append(f'<rect x="{X(-7):.1f}" y="{Y(Y_DECK):.1f}" width="{(T+14)*SC:.1f}" '
             f'height="{2.2*SC:.1f}" fill="#e4ddd0" stroke="#b09a72" stroke-width="1"/>')

    x, bays, posts = 0.0, [], []
    for e in el:
        if e[0] == 'P': posts.append(x); x += POST
        else:           bays.append((x, e[0], e[1])); x += e[1]
    for x0, k, luz in bays:
        o.append(G.dibujito(x0, luz) if k == 'D' else G.pano_liso(x0, luz)[0])

    ca, cb = G.cap_tramo(s)          # el cap se dibuja donde se corta, ni mas ni menos
    o.append(G.rect(ca, 0, cb - ca, 1, "#8a97a2"))
    for px in posts:
        o.append(G.rect(px, Y_CAP_B, POST, POST_LEN, "#b9c4ce", NEG, 1.1))
    if el[0][0] != 'P':
        o.append(f'<rect x="{X(-2):.1f}" y="{Y(Y_CAP_B):.1f}" width="{2*SC:.1f}" '
                 f'height="{(POST_LEN)*SC:.1f}" fill="none" stroke="{ROJO}" '
                 f'stroke-width="1.1" stroke-dasharray="4 3"/>')

    # que es cada pano
    for x0, k, luz in bays:
        cx = X(x0 + luz/2)
        pal = "DIBUJO" if k == 'D' else f"{piques_de(luz)[0]} PIQUES"
        o.append(f'<text x="{cx:.1f}" y="{OY-(14 if T < 90 else 26)}" font-size="10.5" font-weight="800" '
                 f'fill="{NEG}" text-anchor="middle">{pal}</text>')

    # ---- cota de centro a centro de poste
    cen = ([-1.0] if el[0][0] != 'P' else []) + [p+1 for p in posts] + \
          ([T+1.0] if el[-1][0] != 'P' else [])
    yb = Y(POST_LEN) + 22
    for c in cen:
        o.append(f'<line x1="{X(c):.1f}" y1="{Y(Y_DECK):.1f}" x2="{X(c):.1f}" y2="{yb+6}" '
                 f'stroke="{ROJO}" stroke-width="0.7" stroke-dasharray="3 3"/>')
    for a, b in zip(cen, cen[1:]):
        o.append(f'<line x1="{X(a):.1f}" y1="{yb}" x2="{X(b):.1f}" y2="{yb}" stroke="{ROJO}" '
                 f'stroke-width="1.2" marker-start="url(#fm)" marker-end="url(#fm)"/>')
        o.append(f'<text x="{X((a+b)/2):.1f}" y="{yb-6}" font-size="12.5" font-weight="800" '
                 f'fill="{ROJO}" text-anchor="middle">{fr(b-a)}</text>')
    o.append(f'<text x="{X(cen[0])-10:.1f}" y="{yb+4}" font-size="8" fill="{ROJO}" '
             f'text-anchor="end">C–C</text>')

    # ---- largo de cada riel (lo que se corta)
    yr = yb + 30
    xx = 0.0
    for e in el:
        if e[0] == 'P': xx += POST; continue
        a, b = xx + G.GAP_PANEL, xx + e[1] - G.GAP_PANEL
        o.append(f'<line x1="{X(a):.1f}" y1="{yr}" x2="{X(b):.1f}" y2="{yr}" stroke="{VERDE}" '
                 f'stroke-width="2.6"/>')
        for q in (a, b):
            o.append(f'<line x1="{X(q):.1f}" y1="{yr-5}" x2="{X(q):.1f}" y2="{yr+5}" '
                     f'stroke="{VERDE}" stroke-width="1.6"/>')
        o.append(f'<text x="{X((a+b)/2):.1f}" y="{yr+16}" font-size="11" font-weight="800" '
                 f'fill="{VERDE}" text-anchor="middle">{fr(e[1] - 2 * G.GAP_PANEL)}</text>')
        xx += e[1]
    o.append(f'<text x="{X(cen[0])-10:.1f}" y="{yr+4}" font-size="8" fill="{VERDE}" '
             f'text-anchor="end">RIEL</text>')

    # ---- cotas verticales
    xl = X(0) - 16
    for a, b, t in ((0,1,"1"), (1,1+AIRE,fr(AIRE)), (1+AIRE,1+AIRE+CUADRO,fr(CUADRO)),
                    (1+AIRE+CUADRO,39,fr(AIRE)), (39,40,"1"), (40,42,"2"), (42,48,"6")):
        o.append(f'<line x1="{xl}" y1="{Y(a):.1f}" x2="{xl}" y2="{Y(b):.1f}" stroke="{ROJO}" stroke-width="0.7"/>')
        for q in (a, b):
            o.append(f'<line x1="{xl-3}" y1="{Y(q):.1f}" x2="{xl+3}" y2="{Y(q):.1f}" stroke="{ROJO}" stroke-width="0.6"/>')
        o.append(f'<text x="{xl-5}" y="{Y((a+b)/2)+3:.1f}" font-size="8" font-weight="700" '
                 f'fill="{ROJO}" text-anchor="end">{t}</text>')
    xg = X(0) - 48
    o.append(f'<line x1="{xg}" y1="{Y(0):.1f}" x2="{xg}" y2="{Y(Y_DECK):.1f}" stroke="{ROJO}" '
             f'stroke-width="1" marker-start="url(#fm)" marker-end="url(#fm)"/>')
    o.append(f'<text x="{xg-5}" y="{Y(21):.1f}" font-size="11" font-weight="800" fill="{ROJO}" '
             f'transform="rotate(-90 {xg-5} {Y(21):.1f})" text-anchor="middle">42 GUARD</text>')

    # ---- puntas
    corta = T < 90          # no cabe una punta a cada lado: van escalonadas
    for xp, txt, anc, dy in ((X(0), s['izq'], "start", 44),
                             (X(T), s['der'], "end", 30 if corta else 44)):
        lab, col, con = punta(txt)
        v = vecino(txt)
        full = f"{lab} → {v}" if (con and v) else lab
        o.append(f'<text x="{xp:.1f}" y="{OY-dy}" font-size="12.5" font-weight="800" fill="{col}" '
                 f'text-anchor="{anc}"' + (' text-decoration="underline"' if con else '') + f'>{full}</text>')
    o.append(f'<text x="{X(T/2):.1f}" y="{yr+34}" font-size="11.5" font-weight="800" fill="#555" '
             f'text-anchor="middle">LARGO DE LA SECCIÓN &#160;{fr(T)}"&#160; ({feet(T)})</text>')
    return ('<svg viewBox="0 0 %d %d" xmlns="http://www.w3.org/2000/svg">' % (VW, VH)
            + '<defs><marker id="fm" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" '
              f'markerHeight="5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{ROJO}"/>'
              '</marker></defs>' + "".join(o) + '</svg>')

def despiece(s):
    el = s['elems']
    np_ = sum(1 for e in el if e[0] == 'P')
    rieles, piques, nd = {}, {}, 0
    for e in el:
        if e[0] == 'P': continue
        L = e[1] - 2 * G.GAP_PANEL
        rieles[L] = rieles.get(L, 0) + 1
        if e[0] == 'D': nd += 1
        else:
            n = piques_de(e[1])[0]
            piques[n] = piques.get(n, 0) + 1
    f = [f"<tr><td><b>POSTE</b></td><td>2×2×.090</td><td class='n'>{fr(POST_LEN)}\"</td>"
         f"<td class='n'><b>{np_}</b></td><td>{fr(POST_LEN-6)} a la panza del cap + 6 a la fascia &#183; el cap corre por encima</td></tr>",
         f"<tr><td><b>CAP</b></td><td>2×1×.090 de plano</td><td class='n'>{fr(cap_largo(s))}\"</td>"
         f"<td class='n'><b>1</b></td><td>corrido, de punta a punta de la sección</td></tr>"]
    for L in sorted(rieles, reverse=True):
        f.append(f"<tr><td><b>RIEL</b></td><td>2×1×.090 acostado</td><td class='n'>{fr(L)}\"</td>"
                 f"<td class='n'><b>{rieles[L]}</b></td><td>uno por paño</td></tr>")
    tot_q = sum(n*v for n, v in piques.items())
    if tot_q:
        det = " + ".join(f"{v} paño{'s' if v!=1 else ''} de {n}" for n, v in sorted(piques.items()))
        f.append(f"<tr><td><b>PIQUE</b></td><td>1×1×1/16</td><td class='n'>38\"</td>"
                 f"<td class='n'><b>{tot_q}</b></td><td>{det}</td></tr>")
    if nd:
        f.append(f"<tr class='ya'><td><b>DIBUJO</b></td><td>ya armado</td><td class='n'>—</td>"
                 f"<td class='n'><b>{nd}</b></td><td>no se corta nada: entra montado en el paño</td></tr>")
    return "".join(f)

CSS = """
 *{margin:0;padding:0;box-sizing:border-box}
 body{font-family:'Segoe UI',-apple-system,Helvetica,Arial,sans-serif;color:#1b2a41;background:#fff;font-size:13px}
 .page{max-width:10.2in;margin:0 auto;padding:.3in .35in}
 @media print{@page{size:letter landscape;margin:.3in .35in}.page{padding:0;max-width:none}
              .pb{page-break-before:always}
              .dw{page-break-before:always;page-break-inside:avoid}
              .hd+.dw{page-break-before:avoid}}
 .hd{display:flex;justify-content:space-between;align-items:center;border-bottom:4px solid #1b2a41;
     padding-bottom:6px;margin-bottom:9px}
 h1{font-size:20px;letter-spacing:.5px}
 .hd .m{font-size:12px;font-weight:700;text-align:right}
 .dw{border:2px solid #1b2a41;border-radius:5px;margin-bottom:11px}
 .dw .dt{background:#1b2a41;color:#fff;font-size:12.5px;padding:5px 10px;display:flex;align-items:center}
 .dw .dt .sn{font-size:22px;font-weight:800;letter-spacing:1px;margin-right:13px}
 .dw .dt .r{margin-left:auto;font-size:11.5px}
 .dw svg{display:block;width:100%;height:auto;background:#fff;border-bottom:1px solid #dfe4ea}
 table{width:100%;border-collapse:collapse;font-size:12.5px}
 th{background:#41505f;color:#fff;padding:4px 9px;text-align:left;font-size:11px}
 td{border:1px solid #d3dae1;padding:4px 9px}
 td.n{text-align:right;white-space:nowrap;font-weight:700}
 tr.ya td{background:#fdf0e4;color:#8a4a17}
 .key{display:flex;gap:12px;margin:9px 0;font-size:12.5px}
 .key div{flex:1;border:2px solid #c3ccd5;border-radius:5px;padding:7px 10px}
 .key b{display:block;margin-bottom:2px}
 .rj{color:#b91c1c} .vd{color:#0f766e}
"""
LEY = f"""
 <div class="key">
  <div><b class="rj">COTA ROJA</b>Centro de poste a centro de poste, y la vertical del lado.</div>
  <div><b class="vd">COTA VERDE</b>Largo del riel de cada pa&#241;o. Eso es lo que se corta.</div>
  <div><b class="rj" style="text-decoration:underline">CONEXI&#211;N</b>Se une a otra secci&#243;n.
       El poste lo lleva la otra (rayita roja).</div>
  <div><b>MUERE / ESQUINA</b>Ah&#237; termina. El poste va completo en esta secci&#243;n.</div>
  <div><b class="rj">POSTE DE ESQUINA</b>Lleva <b>2 orejas de 1/4"&#215;{G.fr(ANC.OREJA_L)}"&#215;{G.fr(ANC.OREJA_H)}"</b> soldadas.
       Ver la hoja <i>Detalle de anclaje</i>.</div>
 </div>
 <p style="font-size:12.5px;margin:6px 0"><b>El dibujito ya est&#225; armado</b> y flota
 <b>3-7/8" bajo el cap y 3-7/8" sobre el riel</b>; el cuadro es de <b>30-1/4"</b>. Esos tres n&#250;meros
 est&#225;n en la cota vertical de la izquierda. Del dibujo no hay nada que cortar.</p>
"""

def nota_de(s):
    n = s.get('nota') or ""
    if not n: return ""
    return (f'<p style="font-size:12px;padding:6px 10px;background:#fff5f5;'
            f'border-top:2px solid {ROJO};color:#7f1d1d"><b>OJO:</b> {n}</p>')

def ele_soldada():
    """La L de la escalera: M-1 (29) + L-1 (47) SALEN SOLDADAS EN UNA SOLA PIEZA.
       Los dos extremos son libres -- escalera de un lado, pared del otro -- asi que
       la pieza carga sus TRES postes. Se dibuja en planta para que no haya duda."""
    k = 6.2
    ox, oy = 215, 250                      # poste de la pared
    a, b = 47.0, 29.0
    xc, yc = ox + a * k, oy                # poste de esquina
    xf, yf = xc, oy - b * k                # poste de la escalera
    p = 2.0 * k                            # poste 2x2 en planta
    def poste(x, y, txt, sub):
        return (f'<rect x="{x-p/2:.1f}" y="{y-p/2:.1f}" width="{p:.1f}" height="{p:.1f}" '
                f'fill="{ROJO}" stroke="{NEG}" stroke-width="1.4"/>'
                f'<text x="{x:.1f}" y="{y-p/2-19:.1f}" font-size="12.5" font-weight="800" '
                f'text-anchor="middle" fill="{ROJO}">{txt}</text>'
                f'<text x="{x:.1f}" y="{y-p/2-7:.1f}" font-size="10.5" text-anchor="middle" '
                f'fill="{NEG}">{sub}</text>')
    s = [f'<svg viewBox="0 0 792 348" xmlns="http://www.w3.org/2000/svg">',
         # pared de la caballeriza (NO se ancla)
         f'<line x1="{ox-34:.0f}" y1="{oy-120:.0f}" x2="{ox-34:.0f}" y2="{oy+44:.0f}" '
         f'stroke="{NEG}" stroke-width="3.5"/>',
         f'<text x="{ox-48:.0f}" y="{oy-2:.0f}" font-size="11" text-anchor="end" fill="{NEG}">'
         f'PARED DE LA CABALLERIZA</text>',
         f'<text x="{ox-48:.0f}" y="{oy+14:.0f}" font-size="11.5" font-weight="800" text-anchor="end" '
         f'fill="{ROJO}">NO SE ANCLA</text>',
         # las dos patas
         f'<line x1="{ox:.1f}" y1="{oy:.1f}" x2="{xc:.1f}" y2="{yc:.1f}" stroke="{NEG}" stroke-width="7"/>',
         f'<line x1="{xc:.1f}" y1="{yc:.1f}" x2="{xf:.1f}" y2="{yf:.1f}" stroke="{NEG}" stroke-width="7"/>',
         # el dibujito de la pata de 47
         f'<rect x="{ox+(a/2-9)*k:.1f}" y="{oy-11:.1f}" width="{18*k:.1f}" height="22" '
         f'fill="#fdf0e4" stroke="{NAR}" stroke-width="1.8"/>',
         f'<text x="{ox+a/2*k:.1f}" y="{oy+4:.1f}" font-size="11" font-weight="800" '
         f'text-anchor="middle" fill="{NAR}">DIBUJO</text>',
         # cotas
         f'<line x1="{ox:.1f}" y1="{oy+30:.1f}" x2="{xc:.1f}" y2="{oy+30:.1f}" stroke="{ROJO}" stroke-width="1.4"/>',
         f'<text x="{ox+a/2*k:.1f}" y="{oy+25:.1f}" font-size="15" font-weight="800" '
         f'text-anchor="middle" fill="{ROJO}">47"</text>',
         f'<line x1="{xc+30:.1f}" y1="{yc:.1f}" x2="{xc+30:.1f}" y2="{yf:.1f}" stroke="{ROJO}" stroke-width="1.4"/>',
         f'<text x="{xc+38:.1f}" y="{(yc+yf)/2+5:.1f}" font-size="15" font-weight="800" fill="{ROJO}">29"</text>',
         # hueco de la escalera
         f'<text x="{xf:.1f}" y="{yf-46:.0f}" font-size="11" text-anchor="middle" fill="{NEG}">'
         f'HUECO DE LA ESCALERA (27")</text>',
         poste(ox, oy, "POSTE 1", "suelto"),
         poste(xc, yc, "POSTE 2", "esquina soldada"),
         poste(xf, yf, "POSTE 3", "suelto"),
         f'<text x="396" y="336" font-size="14" font-weight="800" text-anchor="middle" '
         f'fill="{ROJO}">UNA SOLA PIEZA SOLDADA · 3 POSTES · NO SE EMPATA CON NADA</text>',
         '</svg>']
    return "".join(s)

ELE_HTML = f"""
  <div class="dw" style="border-color:{ROJO};border-width:3px">
    <div class="dt" style="background:{ROJO}"><span class="sn">L</span>
      LA ELE DE LA ESCALERA &#8212; M-1 + L-1 SALEN SOLDADAS EN UNA SOLA PIEZA
      <span class="r">47" &#215; 29" &#160;&#183;&#160; 3 postes &#160;&#183;&#160; 1 dibujo</span></div>
    {ele_soldada()}
    <table><tr><th style="width:24%">Extremo</th><th>Qu&#233; lleva</th></tr>
      <tr><td><b>Contra la pared</b></td><td>Poste completo de 48", <b>suelto</b>. No se ancla a la
          pared de la caballeriza: se para solo en el deck.</td></tr>
      <tr><td><b>Esquina</b></td><td>Poste completo de 48". <b>La esquina se suelda en el taller</b>,
          cap y riel corridos doblando de una pata a la otra.</td></tr>
      <tr><td><b>En la escalera</b></td><td>Poste completo de 48", <b>suelto</b>. Ah&#237; muere:
          empieza el hueco de 27" y sigue la baranda de madera.</td></tr>
    </table>
  </div>"""

# SOLO LA CABALLERIZA 1. La 2 sale cuando Rene cierre sus medidas: el frente ya
# esta (441-3/8 interior) pero el pano de la izquierda sigue sin medir y el
# retorno y el panito suelto cambiaron de largo. Sacarla ahora seria imprimir
# numeros viejos, que es justo lo que le costo el material la vez pasada.
EDIF = [("CABALLERIZA 1", "caballeriza")]
pag, tot = "", {}
for i, (titulo, slug) in enumerate(EDIF):
    cfg = next(c for c in G.EDIFICIOS if c['slug'] == slug)
    secs = [s for _, g in cfg['grupos'] for s in g]
    for s in secs: s['largo'] = G.largo(s)
    np_ = sum(1 for s in secs for e in s['elems'] if e[0] == 'P')
    nd = sum(1 for s in secs for e in s['elems'] if e[0] == 'D')
    nq = sum(piques_de(e[1])[0] for s in secs for e in s['elems'] if e[0] == 'L')
    tot[titulo] = (len(secs), np_, nd, nq)
    salto = '<div class="pb"></div>' if i else ''
    pag += ("\n  " + salto + "\n"
            '  <div class="hd"><h1>' + titulo + '</h1><div class="m">PLANO DE FABRICACI&#211;N'
            f'<br>{len(secs)} secciones &#183; {np_} postes &#183; {nd} dibujos &#183; {nq} piques'
            '</div></div>\n')
    # la leyenda ya va una vez arriba del documento: no la repitas por edificio
    for s in secs:
        if s['name'] == 'M-1':
            pag += ELE_HTML          # la ele va ANTES de sus dos patas
        ndb = sum(1 for e in s['elems'] if e[0] == 'D')
        nqb = sum(piques_de(e[1])[0] for e in s['elems'] if e[0] == 'L')
        pag += f"""
  <div class="dw">
    <div class="dt"><span class="sn">{s['name']}</span>{titulo}
      <span class="r">{fr(s['largo'])}" ({feet(s['largo'])}) &#160;&#183;&#160; {ndb} dibujo{'s' if ndb!=1 else ''}
      &#160;&#183;&#160; {nqb} piques</span></div>
    {svg(s)}
    <table><tr><th style="width:11%">Pieza</th><th style="width:20%">Perfil</th>
      <th style="width:12%">Largo de corte</th><th style="width:8%">Cant.</th><th>Nota</th></tr>
      {despiece(s)}</table>{nota_de(s)}
  </div>"""

html = f"""<!DOCTYPE html><html lang="es"><head><meta charset="UTF-8">
<title>Caballeriza 1 &#8212; plano de fabricaci&#243;n</title><style>{CSS}</style></head><body><div class="page">
  <div class="hd"><h1>CABALLERIZA 1 &#8212; PLANO DE FABRICACI&#211;N</h1>
    <div class="m">CABALLERIZA 1 &#183; REV. 2 &#183; SEPT 21, 2026 &#183; MEDIDAS INTERIORES<br>TODAS LAS SECCIONES A LA MISMA ESCALA</div></div>
  <table><tr><th>Lado</th><th style="width:14%">Secciones</th><th style="width:14%">Postes de {fr(POST_LEN)}"</th>
    <th style="width:14%">Dibujos</th><th style="width:14%">Piques de 38"</th></tr>
    {"".join(f'<tr><td><b>{k}</b></td><td class="n">{v[0]}</td><td class="n">{v[1]}</td>'
             f'<td class="n">{v[2]}</td><td class="n">{v[3]}</td></tr>' for k, v in tot.items())}
  </table>
{pag}
</div></body></html>"""

out = HERE / "railing-fabricacion-caballerizas.html"
out.write_text(html, encoding="utf-8")
print("escrito:", out.name)
for k, v in tot.items():
    print(f"  {k}: {v[0]} secciones · {v[1]} postes · {v[2]} dibujos · {v[3]} piques")
