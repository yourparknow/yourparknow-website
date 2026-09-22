#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""HOJA DE TALLER, UNA POR SET.  Lo que Rene pidio: el dibujito de la baranda y
   debajo las piezas que se cortan.  Nada mas.

   "no me pongas toda la bola de numeros esa... dibujito de la baranda nada mas
    con las cositas abajo, tantas piezas esto, tantas piezas esto. Sin tanto
    escrito, que eso no lo lee nadie."

   Cada set sale en su propio archivo para mandarlo por WhatsApp:
     CABALLERIZA-1 · CABALLERIZA-2 · BALCON-1-POOL · BALCON-2-POOL
   Todo sale de gen-railing-secciones: ni una medida tecleada aqui.
"""
import importlib.util, pathlib, io, contextlib

HERE = pathlib.Path("/home/user/yourparknow-website/proposals/jrg-welding-corp")
_s = importlib.util.spec_from_file_location("gsec", HERE / "gen-railing-secciones.py")
G = importlib.util.module_from_spec(_s)
with contextlib.redirect_stdout(io.StringIO()): _s.loader.exec_module(G)
fr, feet, piques_de = G.fr, G.feet, G.piques_de
POST, POST_LEN = G.POST, G.POST_LEN

G.SC = 3.05
G.OX, G.OY = 40, 56
SC, OX, OY = G.SC, G.OX, G.OY
VW, VH = 790, 252   # el alto tiene que dar para la cadena de cotas de abajo
X, Y = G.X, G.Y
NEG, ROJO = "#1b2a41", "#b91c1c"

# que set sale en cada archivo, y como se llama en la hoja
SETS = [
    ("CABALLERIZA-1",  "CABALLERIZA 1",   "caballeriza"),
    ("CABALLERIZA-2",  "CABALLERIZA 2",   "caballeriza-2"),
    ("BALCON-1-POOL",  "BALCÓN 1 · POOL", "pool-house"),
    ("BALCON-2-POOL",  "BALCÓN 2 · POOL", "pool-house"),
]
# los dos balcones del Pool House viven en la misma hoja del generador, asi que
# se separan por sus letras.
LETRAS_POOL = {"BALCON-1-POOL": "ABC", "BALCON-2-POOL": "DEF"}


def dibujo(s):
    """la baranda de frente: postes, panos y el ancho de cada pano. Ya esta."""
    o, T = [], G.largo(s)
    el = s['elems']
    x, bays, posts = 0.0, [], []
    for e in el:
        if e[0] == 'P': posts.append(x); x += POST
        else:           bays.append((x, e[0], e[1])); x += e[1]
    for x0, k, luz in bays:
        o.append(G.dibujito(x0, luz) if k == 'D' else G.pano_liso(x0, luz)[0])
    ca, cb = G.cap_tramo(s)
    o.append(G.rect(ca, 0, cb - ca, 1, "#8a97a2"))
    for px in posts:
        o.append(G.rect(px, G.Y_CAP_B, POST, POST_LEN, "#b9c4ce", NEG, 1.1))

    # la cadena: poste, pano, poste, pano... y cierra en el largo de la seccion
    yb = Y(POST_LEN) + 20
    xx, suma = 0.0, []
    for e in el:
        w = POST if e[0] == 'P' else e[1]
        a, b = xx, xx + w
        poste = e[0] == 'P'
        col = "#8a97a2" if poste else ROJO
        o.append(f'<line x1="{X(a):.1f}" y1="{Y(G.Y_DECK):.1f}" x2="{X(a):.1f}" y2="{yb+5}" '
                 f'stroke="{col}" stroke-width="0.6" stroke-dasharray="3 3"/>')
        o.append(f'<line x1="{X(a):.1f}" y1="{yb}" x2="{X(b):.1f}" y2="{yb}" stroke="{col}" '
                 f'stroke-width="{1.3 if poste else 2}"'
                 + ('' if poste else ' marker-start="url(#fm)" marker-end="url(#fm)"') + '/>')
        o.append(f'<text x="{X((a+b)/2):.1f}" y="{yb + (13 if poste else -6)}" '
                 f'font-size="{7.5 if poste else 12.5}" font-weight="800" '
                 f'fill="{col}" text-anchor="middle">{fr(w)}</text>')
        suma.append(w); xx = b
    o.append(f'<line x1="{X(T):.1f}" y1="{Y(G.Y_DECK):.1f}" x2="{X(T):.1f}" y2="{yb+5}" '
             f'stroke="{ROJO}" stroke-width="0.6" stroke-dasharray="3 3"/>')
    assert abs(sum(suma) - T) < 1e-9, ("la cadena no cierra", s['name'])
    assert yb + 16 < VH, ("la cadena de cotas se sale del dibujo", s['name'], yb, VH)
    o.append(f'<text x="{X(T)+7:.1f}" y="{yb+4}" font-size="10" font-weight="800" '
             f'fill="{ROJO}" text-anchor="start">= {fr(T)}"</text>')
    return ('<svg viewBox="0 0 %d %d" xmlns="http://www.w3.org/2000/svg">' % (VW, VH)
            + '<defs><marker id="fm" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="5" '
              f'markerHeight="5" orient="auto"><path d="M2,2 L8,5 L2,8" fill="none" '
              f'stroke="{ROJO}" stroke-width="1.4"/></marker></defs>'
            + "".join(o) + '</svg>')


def piezas(s):
    """las cositas de abajo: cuantas de cada una y de que largo."""
    el = s['elems']
    np_ = sum(1 for e in el if e[0] == 'P')
    rieles, piq, nd = {}, 0, 0
    for e in el:
        if e[0] == 'P': continue
        rieles[e[1]] = rieles.get(e[1], 0) + 1
        if e[0] == 'D': nd += 1
        else:           piq += piques_de(e[1])[0]
    f = [(np_, f'POSTE 2×2', f'{fr(POST_LEN)}"'),
         (1,   f'CAP 2×1',   f'{fr(G.cap_largo(s))}"')]
    for w in sorted(rieles, reverse=True):
        f.append((rieles[w], 'RIEL 2×1', f'{fr(w)}"'))
    if piq: f.append((piq, 'PIQUE 1×1', '38"'))
    if nd:  f.append((nd,  'DIBUJO',    'ya armado'))
    return "".join(f'<div><b>{n}</b><span>{q}</span><i>{L}</i></div>' for n, q, L in f)


CSS = """
 *{margin:0;padding:0;box-sizing:border-box}
 body{font-family:'Segoe UI',-apple-system,Helvetica,Arial,sans-serif;color:#1b2a41;background:#fff}
 .page{max-width:10.2in;margin:0 auto;padding:.3in .35in}
 @media print{@page{size:letter landscape;margin:.35in}.page{padding:0;max-width:none}
              .sec{page-break-inside:avoid}}
 .top{display:flex;justify-content:space-between;align-items:baseline;
      border-bottom:5px solid #1b2a41;padding-bottom:7px;margin-bottom:14px}
 .top h1{font-size:30px;letter-spacing:1px}
 .top span{font-size:14px;font-weight:700;color:#b91c1c}
 .sec{border:2px solid #1b2a41;border-radius:6px;margin-bottom:14px;overflow:hidden}
 .sec .t{background:#1b2a41;color:#fff;padding:6px 12px;font-size:19px;font-weight:800;
         letter-spacing:.5px;display:flex;justify-content:space-between;align-items:baseline}
 .sec .t em{font-style:normal;font-size:15px;color:#8fa2b8;letter-spacing:2px}
 .sec svg{display:block;width:100%;height:auto;background:#fdfdfb}
 .pz{display:flex;flex-wrap:wrap;gap:0;border-top:2px solid #1b2a41}
 .pz div{flex:1 1 0;min-width:96px;padding:7px 4px;text-align:center;border-right:1px solid #cfd6dd}
 .pz div:last-child{border-right:0}
 .pz b{display:block;font-size:26px;color:#b91c1c;line-height:1}
 .pz span{display:block;font-size:10.5px;font-weight:700;letter-spacing:.5px;margin-top:2px}
 .pz i{display:block;font-size:13px;font-style:normal;font-weight:800;margin-top:1px}
"""


def hoja(titulo, secs):
    cuerpo = ""
    for s in secs:
        cuerpo += (f'<div class="sec"><div class="t">{G.ROTULOS[s["name"]]}'
                   f'<em>{s["name"]}</em></div>'
                   f'{dibujo(s)}<div class="pz">{piezas(s)}</div></div>')
    tot_p = sum(1 for s in secs for e in s['elems'] if e[0] == 'P')
    tot_d = sum(1 for s in secs for e in s['elems'] if e[0] == 'D')
    tot_q = sum(piques_de(e[1])[0] for s in secs for e in s['elems'] if e[0] == 'L')
    return (f'<!DOCTYPE html><html lang="es"><head><meta charset="UTF-8">'
            f'<title>{titulo}</title><style>{CSS}</style></head><body><div class="page">'
            f'<div class="top"><h1>{titulo}</h1>'
            f'<span>{len(secs)} piezas &#183; {tot_p} postes &#183; {tot_d} dibujos '
            f'&#183; {tot_q} piques</span></div>{cuerpo}</div></body></html>')


if __name__ == "__main__":
    porslug = {c['slug']: [s for _, gr in c['grupos'] for s in gr] for c in G.EDIFICIOS}
    for arch, titulo, slug in SETS:
        secs = porslug[slug]
        if arch in LETRAS_POOL:
            secs = [s for s in secs if s['name'][0] in LETRAS_POOL[arch]]
        out = HERE / f"{arch}.html"
        out.write_text(hoja(titulo, secs), encoding="utf-8")
        print(f"  {arch:16s} {len(secs)} secciones")
