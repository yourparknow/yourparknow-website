#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Juego de TALLER simplificado: un dibujo por seccion, sin cadenas de cotas.
   Solo: numero de pano, centro a centro de postes, y que lleva cada punta.
   Los datos salen del generador detallado, no se vuelven a teclear."""
import importlib.util, pathlib
from fractions import Fraction

HERE = pathlib.Path("/home/user/yourparknow-website/proposals/jrg-welding-corp")
spec = importlib.util.spec_from_file_location("gsec", HERE / "gen-railing-secciones.py")
G = importlib.util.module_from_spec(spec); spec.loader.exec_module(G)

fr, feet, piques_de = G.fr, G.feet, G.piques_de
POST, CAMPO, POST_LEN = G.POST, G.CAMPO, G.POST_LEN
Y_CAP_B, Y_RAIL_T, Y_DECK = G.Y_CAP_B, G.Y_RAIL_T, G.Y_DECK

# ------------------------------------------------ marco del dibujo
G.SC = 3.55
G.OX, G.OY = 52, 74
SC, OX, OY = G.SC, G.OX, G.OY
VW, VH = 792, 296
X, Y = G.X, G.Y
DIM, NEG = "#b91c1c", "#1b2a41"

def tipo_punta(txt):
    if "EMPATE" in txt or "ESCALERA" in txt: return "CONEXION"
    if "ESQUINA" in txt:                     return "ESQUINA"
    if "PARED" in txt or "CASA" in txt:      return "PARED"
    return "FINAL"

def vecino(txt):
    """seccion vecina (A-1) o numero de empate (③), si el texto lo menciona"""
    import re
    m = re.search(r"\b([A-M]-\d)\b", txt)
    if m: return m.group(1)
    m = re.search(r"[①-⑨]", txt)
    return m.group(0) if m else ""

def svg_simple(sec):
    o, T = [], sec['largo']
    elems = sec['elems']
    ti, td = tipo_punta(sec['izq']), tipo_punta(sec['der'])

    # ---- deck
    o.append(f'<rect x="{X(-8):.2f}" y="{Y(Y_DECK):.2f}" width="{(T+16)*SC:.2f}" '
             f'height="{2.2*SC:.2f}" fill="#e4ddd0" stroke="#b09a72" stroke-width="1"/>')

    # ---- recorrido
    x, bays, posts = 0.0, [], []
    for e in elems:
        if e[0] == 'P': posts.append(x); x += POST
        else:           bays.append((x, e[0], e[1])); x += e[1]

    for x0, kind, luz in bays:
        o.append(G.dibujito(x0) if kind == 'D' else G.pano_liso(x0, luz)[0])

    # ---- cap
    ext_i = 0.0 if elems[0][0] == 'P' else 2.0
    o.append(G.rect(-ext_i, 0, T + ext_i + (0 if elems[-1][0] == 'P' else 2), 1, "#8a97a2"))

    # ---- postes. El poste fantasma marca donde la OTRA seccion pone el suyo.
    for px in posts:
        o.append(G.rect(px, Y_CAP_B, POST, POST_LEN - 1, "#b9c4ce", "#1b2a41", 1.1))
    if elems[0][0] != 'P':
        o.append(f'<rect x="{X(-2):.2f}" y="{Y(Y_CAP_B):.2f}" width="{2*SC:.2f}" '
                 f'height="{(POST_LEN-1)*SC:.2f}" fill="none" stroke="{DIM}" '
                 f'stroke-width="1.1" stroke-dasharray="4 3"/>')

    # ---- numero de pano, grande y con una sola palabra debajo
    for i, (x0, kind, luz) in enumerate(bays, 1):
        cx = X(x0 + luz / 2)
        pal = "DIBUJO" if kind == 'D' else f"{piques_de(luz)[0]} PIQUES"
        o.append(f'<text x="{cx:.2f}" y="{OY-30}" font-size="11" font-weight="800" '
                 f'fill="{NEG}" text-anchor="middle">{pal}</text>')
        o.append(f'<circle cx="{cx:.2f}" cy="{OY-13}" r="12" fill="#1b2a41"/>')
        o.append(f'<text x="{cx:.2f}" y="{OY-8}" font-size="15" font-weight="800" '
                 f'fill="#fff" text-anchor="middle">{i}</text>')

    # ---- UNICA cota: centro de poste a centro de poste
    centros = [-1.0] if elems[0][0] != 'P' else []
    centros += [p + 1.0 for p in posts]
    if elems[-1][0] != 'P': centros.append(T + 1.0)
    yb = Y(POST_LEN) + 20
    for c in centros:
        o.append(f'<line x1="{X(c):.2f}" y1="{Y(Y_DECK):.2f}" x2="{X(c):.2f}" y2="{yb+7}" '
                 f'stroke="{DIM}" stroke-width="0.7" stroke-dasharray="3 3"/>')
    for a, b in zip(centros, centros[1:]):
        o.append(f'<line x1="{X(a):.2f}" y1="{yb}" x2="{X(b):.2f}" y2="{yb}" stroke="{DIM}" '
                 f'stroke-width="1.3" marker-start="url(#tm)" marker-end="url(#tm)"/>')
        o.append(f'<text x="{X((a+b)/2):.2f}" y="{yb-7}" font-size="13.5" font-weight="800" '
                 f'fill="{DIM}" text-anchor="middle">{fr(b-a)}</text>')
    o.append(f'<text x="{X(centros[0])-9:.2f}" y="{yb+4}" font-size="8" fill="{DIM}" '
             f'text-anchor="end">C–C</text>')

    # ---- que lleva cada punta
    def flag(xp, t, txt_orig, anchor):
        v = vecino(txt_orig)
        yy = OY - 58
        if t == "CONEXION":
            if "ESCALERA" in txt_orig:
                lab = "AQUÍ ARRANCA LA ESCALERA"
            else:
                lab = f"CONEXIÓN → {v}" if v else "CONEXIÓN"
            o.append(f'<text x="{xp:.2f}" y="{yy}" font-size="13" font-weight="800" fill="{DIM}" '
                     f'text-anchor="{anchor}" text-decoration="underline">{lab}</text>')
            o.append(f'<text x="{xp:.2f}" y="{yy+13}" font-size="8.5" fill="{DIM}" '
                     f'text-anchor="{anchor}">el poste lo lleva la otra sección</text>')
        elif t == "ESQUINA":
            lab = f"ESQUINA → {v}" if v else "ESQUINA"
            o.append(f'<text x="{xp:.2f}" y="{yy}" font-size="12" font-weight="700" fill="{NEG}" '
                     f'text-anchor="{anchor}">{lab}</text>')
        elif t == "PARED":
            o.append(f'<text x="{xp:.2f}" y="{yy}" font-size="12" font-weight="700" fill="{NEG}" '
                     f'text-anchor="{anchor}">CONTRA LA PARED</text>')
            o.append(f'<text x="{xp:.2f}" y="{yy+13}" font-size="8.5" fill="{NEG}" '
                     f'text-anchor="{anchor}">poste completo, no se toca</text>')
    flag(X(0), ti, sec['izq'], "start")
    flag(X(T), td, sec['der'], "end")

    o.append(f'<text x="{X(T/2):.2f}" y="{yb+30}" font-size="11" font-weight="700" fill="#555" '
             f'text-anchor="middle">LARGO TOTAL DE LA SECCIÓN &#160;{fr(T)}"&#160; ({feet(T)})</text>')
    return "".join(o)

MARKER = ('<defs><marker id="tm" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" '
          f'markerHeight="5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{DIM}"/>'
          '</marker></defs>')

def bloque(sec, edificio):
    nd = sum(1 for e in sec['elems'] if e[0] == 'D')
    nl = sum(1 for e in sec['elems'] if e[0] == 'L')
    return f"""
  <div class="dw">
    <div class="dt"><span class="sn">{sec['name']}</span>{edificio}
      <span class="r">{nd} dibujo{'s' if nd != 1 else ''} &#160;+&#160; {nl} de piques</span></div>
    <svg viewBox="0 0 {VW} {VH}" xmlns="http://www.w3.org/2000/svg">{MARKER}{svg_simple(sec)}</svg>
  </div>"""

CSS = """
  * { margin:0; padding:0; box-sizing:border-box; }
  body { font-family:'Segoe UI', -apple-system, Helvetica, Arial, sans-serif; color:#1b2a41; background:#fff; font-size:13px; }
  .page { max-width:10.2in; margin:0 auto; padding:0.3in 0.35in; }
  @media print { @page { size:letter landscape; margin:0.3in 0.35in; }
                 .page { padding:0; max-width:none; } .pb { page-break-before:always; }
                 .dw { page-break-inside:avoid; } }
  .hd { display:flex; justify-content:space-between; align-items:center;
        border-bottom:4px solid #1b2a41; padding-bottom:6px; margin-bottom:10px; }
  h1 { font-size:19px; letter-spacing:.5px; }
  .hd .m { font-size:12px; font-weight:700; }
  .dw { border:2px solid #1b2a41; border-radius:5px; margin:0 0 11px; }
  .dw .dt { background:#1b2a41; color:#fff; font-size:13px; padding:5px 10px; display:flex; align-items:center; }
  .dw .dt .sn { font-size:24px; font-weight:800; letter-spacing:1px; margin-right:14px; }
  .dw .dt .r { margin-left:auto; font-size:12px; }
  .dw svg { display:block; width:100%; height:auto; background:#fff; }
  table { width:100%; border-collapse:collapse; margin:6px 0 12px; font-size:14px; }
  th { background:#1b2a41; color:#fff; padding:6px 9px; text-align:left; }
  td { border:1px solid #c3ccd5; padding:5px 9px; }
  td.n { text-align:right; white-space:nowrap; font-weight:700; }
  td.mk { font-family:'Consolas','Courier New',monospace; font-size:12px; }
  h2 { font-size:14px; color:#fff; background:#1b2a41; padding:4px 10px; margin:12px 0 6px;
       text-transform:uppercase; letter-spacing:.7px; border-radius:2px; }
  .big { display:flex; gap:12px; margin:10px 0; }
  .big div { flex:1; border:3px solid #1b2a41; border-radius:6px; padding:10px; text-align:center; }
  .big b { display:block; font-size:38px; color:#b91c1c; line-height:1; }
  .big span { font-size:12px; text-transform:uppercase; letter-spacing:.8px; font-weight:700; }
  .key { display:flex; gap:12px; margin:8px 0 2px; font-size:13px; }
  .key div { flex:1; border:2px solid #c3ccd5; border-radius:5px; padding:8px 11px; }
  .key b { display:block; font-size:14px; margin-bottom:2px; }
  .rojo { color:#b91c1c; text-decoration:underline; }
"""

LEYENDA = """
  <h2>C&#243;mo leer este plano</h2>
  <div class="key">
    <div><b class="rojo">CONEXI&#211;N</b>Esa punta se une a otra secci&#243;n.
         El poste lo lleva la otra secci&#243;n &#8212; aqu&#237; va el riel solo, con su inset.
         En el dibujo se ve el poste en rayita roja.</div>
    <div><b>ESQUINA</b>Ah&#237; dobla. El poste s&#237; va en esta secci&#243;n, completo y soldado.</div>
    <div><b>CONTRA LA PARED</b>Muere contra la pared. Poste completo, no se toca.
         La placa se pone en obra.</div>
    <div><b>&#9312; &#9313; &#9314;</b>N&#250;mero de pa&#241;o dentro de la secci&#243;n.
         Debajo dice si es DIBUJO o cu&#225;ntos piques lleva.</div>
  </div>
  <p style="font-size:13px; margin:8px 0"><b>La &#250;nica medida del plano es de CENTRO DE POSTE A CENTRO DE POSTE.</b>
  Todo pa&#241;o de dibujo es <b>48"</b> centro a centro, siempre, en los dos edificios.</p>
"""

def doc(cfg):
    secs = [s for _, g in cfg['grupos'] for s in g]
    for s in secs:
        s['largo'] = G.largo(s)
    nd = sum(1 for s in secs for e in s['elems'] if e[0] == 'D')
    nl = sum(1 for s in secs for e in s['elems'] if e[0] == 'L')
    npq = sum(piques_de(e[1])[0] for s in secs for e in s['elems'] if e[0] == 'L')

    anchos = {}
    for s in secs:
        for e in s['elems']:
            if e[0] == 'L':
                n, g = piques_de(e[1])
                anchos.setdefault(e[1], [0, n, g]); anchos[e[1]][0] += 1
    filas = []
    for w in sorted(anchos, reverse=True):
        veces, n, g = anchos[w]
        marcas = [g + i * (1 + g) + 0.5 for i in range(n)]
        assert abs((marcas[-1] + 0.5 + g) - (w - 0.5)) < 1e-9
        ms = " &#160;<span style='color:#c8571b'>|</span>&#160; ".join(fr(m, 16) for m in marcas)
        filas.append(f"<tr><td class='n'>{fr(w+2)}\"</td><td class='n'>{fr(w-0.5)}\"</td>"
                     f"<td class='n'>{n}</td><td class='mk'>{ms}</td></tr>")

    cuerpo = ""
    for h1, grupo in cfg['grupos']:
        et = h1.split("—")[0].strip()
        cuerpo += (f'\n  <div class="pb"></div>\n  <div class="hd"><h1>{h1}</h1>'
                   f'<div class="m">VISTA DE FRENTE</div></div>\n')
        cuerpo += "\n".join(bloque(s, et) for s in grupo)

    html = f"""<!DOCTYPE html><html lang="es"><head><meta charset="UTF-8">
<title>{cfg['titulo']} &#8212; Taller</title><style>{CSS}</style></head><body><div class="page">
  <div class="hd"><h1>{cfg['titulo']}</h1><div class="m">HOJA DE TALLER &#183; SIMPLE<br>{cfg['meta']}</div></div>
  <div class="big">
    <div><b>{len(secs)}</b><span>secciones</span></div>
    <div><b>{nd}</b><span>pa&#241;os de dibujo</span></div>
    <div><b>{nl}</b><span>pa&#241;os de piques</span></div>
    <div><b>{npq}</b><span>piques de 38"</span></div>
  </div>
{LEYENDA}
  <h2>Corte recto de 38" de esta hoja</h2>
  <p style="font-size:14px; margin:4px 0 10px"><b>{npq}</b> piques de los pa&#241;os
  &#160;+&#160; <b>{nd*4}</b> de los dibujos (las 2 V y las 2 B de cada uno)
  &#160;=&#160; <b style="font-size:17px; color:#b91c1c">{npq + nd*4} piezas de 38" rectas</b>.
  Todas salen del mismo corte, se pican de corrido.</p>

  <h2>Marcas de los piques &#8212; medir desde la punta izquierda del riel</h2>
  <table>
    <tr><th style="width:13%">Pa&#241;o C&#8211;C</th><th style="width:13%">Riel</th>
        <th style="width:9%">Piques</th><th>Marca al centro de cada pique</th></tr>
    {"".join(filas)}
  </table>
  <p style="font-size:13px"><b>Cada marca se mide desde la misma punta del riel, no de pique en pique.</b>
  As&#237; no se corre el error.</p>
{cuerpo}
</div></body></html>"""
    out = HERE / f"railing-taller-{cfg['slug']}.html"
    out.write_text(html, encoding="utf-8")
    print(f"  {out.name}: {len(secs)} secciones · {nd} dibujos · {nl} lisos · {npq} piques")
    return nd, npq

if __name__ == "__main__":
    tot_d = tot_q = 0
    for c in G.EDIFICIOS:
        d, q = doc(c); tot_d += d; tot_q += q
    v_b = tot_d * 4                      # V y B del dibujito, tambien 38" rectos
    print(f"\nPIQUES RECTOS DE 38\": {tot_q} de paño + {v_b} de los dibujos (V y B) = {tot_q + v_b}")
    for tira, nom in ((240, "20'"), (288, "24'")):
        por = tira // 38; sob = tira - por * 38
        tiras = -(-(tot_q + v_b) // por)
        print(f"  tira de {nom}: {por} piques por tira, sobra {sob}\"  ->  {tiras} tiras, "
              f"{tiras} retazos de {sob}\"")
