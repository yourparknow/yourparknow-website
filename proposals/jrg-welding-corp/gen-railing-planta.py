#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Planos EN PLANTA de los cuatro balcones, para instalacion.
   Vista desde arriba, cada corrida con su medida y cada seccion con su letra.
   Los largos salen del generador de secciones: no se teclea ningun numero dos veces."""
import importlib.util, pathlib, math

HERE = pathlib.Path("/home/user/yourparknow-website/proposals/jrg-welding-corp")
spec = importlib.util.spec_from_file_location("gsec", HERE / "gen-railing-secciones.py")
G = importlib.util.module_from_spec(spec); spec.loader.exec_module(G)
fr, feet = G.fr, G.feet

# ---------------------------------------------------------------- recorridos
# rumbo: N S E O  ·  cada corrida = (letra, rumbo, secciones que la componen)
# el largo de cada corrida lo saca del propio generador, no se repite aqui.
BAL = [
 dict(slug="pool-house-1", titulo="POOL HOUSE — BALCÓN 1",
      nota="El croquis no dice hacia qué lado dobla cada corrida: los rumbos son mi lectura. "
           "Los <b>largos y las letras sí son los tuyos</b>.",
      ini="PARED DE LA CASA",
      pasos=[("B","N",["B-1"]), ("A","O",["A-2","A-1"]), ("C","S",["C-1","C-2"])],
      fin="ARRANQUE DE LA ESCALERA  (185\" a 34°)"),
 dict(slug="pool-house-2", titulo="POOL HOUSE — BALCÓN 2",
      nota="Las dos puntas mueren contra la casa. <b>¿Dónde arranca la escalera de 198\" a 33°?</b> "
           "No lo tengo marcado en ninguna punta.",
      ini="PARED DE LA CASA",
      pasos=[("F","N",["F-2","F-1"]), ("D","O",["D-1","D-2","D-3"]), ("E","S",["E-1"])],
      fin="PARED DE LA CASA"),
 dict(slug="caballeriza-1", titulo="CABALLERIZA — LADO 1",
      nota="Del croquis de 195 · 36'-10\" · 104 · 98-3/4 · 47 · 29. "
           "El contorno de tu croquis no cierra, así que <b>los rumbos son mi lectura</b>.",
      ini="PARED DE LA CABALLERIZA", girar=True,
      pasos=[("G","E",["G-1"]), ("H","N",["H-1","H-2","H-3"]), ("J","O",["J-1"]),
             ("K","S",["K-1"]), ("L","O",["L-1"]), ("M","N",["M-1"])],
      fin="PARED DE LA CABALLERIZA"),
 dict(slug="caballeriza-2", titulo="CABALLERIZA — LADO 2",
      nota="Del croquis del signo de interrogación. <b>El paño del ¿ sigue sin medir</b> "
           "(calculas 8 a 9 pies). Los rumbos son mi lectura.",
      ini="PARED DE LA CABALLERIZA", girar=True,
      pasos=[("P","O",["P-1"]), ("N","S",["N-1","N-2","N-3"]),
             ("?","E",None), ("Q","N",["Q-1"]), ("R","E",["R-1"])],
      fin="PARED DE LA CABALLERIZA"),
]
INCOGNITA = 108.0          # el pano sin medir, dibujado a 9 pies

SEC = {}
LARGO_CORRIDA = {}
for cfg in G.EDIFICIOS:
    for _, grupo in cfg['grupos']:
        for s in grupo:
            s['largo'] = G.largo(s); SEC[s['name']] = s
    for _, run, total, nombres in cfg['corridas']:
        LARGO_CORRIDA[run] = (total, nombres)

DX = {"N":(0,1), "S":(0,-1), "E":(1,0), "O":(-1,0)}
GIRO = {"N":"E", "E":"S", "S":"O", "O":"N"}      # 90 grados, para que quepa a lo ancho

def recorrido(b):
    """devuelve [(letra, p0, p1, largo, secciones)] en coordenadas de planta"""
    x = y = 0.0; out = []
    for letra, rumbo, secs in b['pasos']:
        L = INCOGNITA if letra == "?" else LARGO_CORRIDA[letra][0]
        dx, dy = DX[GIRO[rumbo] if b.get('girar') else rumbo]
        p0 = (x, y); x += dx*L; y += dy*L
        out.append((letra, p0, (x, y), L, secs))
    return out

# ---------------------------------------------------------------- dibujo
def svg(b):
    tr = recorrido(b)
    xs = [p for _,a,c,_,_ in tr for p in (a[0], c[0])]
    ys = [p for _,a,c,_,_ in tr for p in (a[1], c[1])]
    w, h = max(xs)-min(xs), max(ys)-min(ys)
    M = 118                                    # margen para cotas y letras
    VW, VH = 940, 620
    sc = min((VW-2*M)/max(w,1), (VH-2*M)/max(h,1))
    ox = M + (VW-2*M - w*sc)/2 - min(xs)*sc
    oy = VH - M - (VH-2*M - h*sc)/2 + min(ys)*sc
    X = lambda v: ox + v*sc
    Y = lambda v: oy - v*sc
    o = ['<defs><marker id="pa" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" '
         'markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#b91c1c"/>'
         '</marker></defs>']

    def perp(p0, p1, d):
        vx, vy = p1[0]-p0[0], p1[1]-p0[1]
        n = math.hypot(vx, vy) or 1
        return (-vy/n*d, vx/n*d)                # normal a la izquierda del avance

    for letra, p0, p1, L, secs in tr:
        inc = letra == "?"
        col = "#c8571b" if inc else "#1b2a41"
        o.append(f'<line x1="{X(p0[0]):.1f}" y1="{Y(p0[1]):.1f}" x2="{X(p1[0]):.1f}" '
                 f'y2="{Y(p1[1]):.1f}" stroke="{col}" stroke-width="9" stroke-linecap="butt"'
                 + (' stroke-dasharray="10 7"' if inc else '') + '/>')
        # cota de la corrida, por fuera
        ux, uy = perp(p0, p1, 34/sc)
        a = (p0[0]+ux, p0[1]+uy); c = (p1[0]+ux, p1[1]+uy)
        o.append(f'<line x1="{X(a[0]):.1f}" y1="{Y(a[1]):.1f}" x2="{X(c[0]):.1f}" y2="{Y(c[1]):.1f}" '
                 f'stroke="#b91c1c" stroke-width="1.2" marker-start="url(#pa)" marker-end="url(#pa)"/>')
        mx, my = (a[0]+c[0])/2, (a[1]+c[1])/2
        vert = abs(p1[0]-p0[0]) < 1e-6
        rot = f' transform="rotate(-90 {X(mx):.1f} {Y(my):.1f})"' if vert else ''
        txt = "SIN MEDIR" if inc else f'{fr(L)}"  ({feet(L)})'
        o.append(f'<text x="{X(mx):.1f}" y="{Y(my)-7:.1f}" font-size="15" font-weight="800" '
                 f'fill="#b91c1c" text-anchor="middle"{rot}>{txt}</text>')
        # letra de la corrida, encima de la linea
        o.append(f'<circle cx="{X((p0[0]+p1[0])/2):.1f}" cy="{Y((p0[1]+p1[1])/2):.1f}" r="15" '
                 f'fill="#fff" stroke="{col}" stroke-width="2.5"/>')
        o.append(f'<text x="{X((p0[0]+p1[0])/2):.1f}" y="{Y((p0[1]+p1[1])/2)+6:.1f}" font-size="17" '
                 f'font-weight="800" fill="{col}" text-anchor="middle">{letra}</text>')
        # secciones: corchete por dentro
        if secs:
            ix, iy = perp(p0, p1, -20/sc)
            t = 0.0
            for nm in secs:
                Ls = SEC[nm]['largo']
                if SEC[nm]['elems'][0][0] != 'P': Ls += 2      # arranca en pano: cuenta el poste vecino
                f0 = t/L; f1 = min((t+Ls)/L, 1.0); t += Ls
                q0 = (p0[0]+(p1[0]-p0[0])*f0+ix, p0[1]+(p1[1]-p0[1])*f0+iy)
                q1 = (p0[0]+(p1[0]-p0[0])*f1+ix, p0[1]+(p1[1]-p0[1])*f1+iy)
                o.append(f'<line x1="{X(q0[0]):.1f}" y1="{Y(q0[1]):.1f}" x2="{X(q1[0]):.1f}" '
                         f'y2="{Y(q1[1]):.1f}" stroke="#0f766e" stroke-width="3.5"/>')
                for q in (q0, q1):
                    px, py = perp(p0, p1, 6/sc)
                    o.append(f'<line x1="{X(q[0]-px):.1f}" y1="{Y(q[1]-py):.1f}" '
                             f'x2="{X(q[0]+px):.1f}" y2="{Y(q[1]+py):.1f}" stroke="#0f766e" stroke-width="2"/>')
                mx2, my2 = (q0[0]+q1[0])/2, (q0[1]+q1[1])/2
                rot2 = f' transform="rotate(-90 {X(mx2):.1f} {Y(my2):.1f})"' if vert else ''
                o.append(f'<rect x="{X(mx2)-21:.1f}" y="{Y(my2)-9:.1f}" width="42" height="18" rx="3" '
                         f'fill="#0f766e"{rot2}/>')
                o.append(f'<text x="{X(mx2):.1f}" y="{Y(my2)+5:.1f}" font-size="12.5" font-weight="800" '
                         f'fill="#fff" text-anchor="middle"{rot2}>{nm}</text>')

    # esquinas
    for i in range(len(tr)-1):
        p = tr[i][2]
        o.append(f'<rect x="{X(p[0])-7:.1f}" y="{Y(p[1])-7:.1f}" width="14" height="14" '
                 f'fill="#fff" stroke="#1b2a41" stroke-width="2.5"/>')
        o.append(f'<text x="{X(p[0])+13:.1f}" y="{Y(p[1])-11:.1f}" font-size="10" '
                 f'fill="#1b2a41" font-weight="700">esquina</text>')
    # remates
    for p, t in ((tr[0][1], b['ini']), (tr[-1][2], b['fin'])):
        o.append(f'<rect x="{X(p[0])-11:.1f}" y="{Y(p[1])-11:.1f}" width="22" height="22" '
                 f'fill="#8a6a42"/>')
        # el texto se va hacia adentro del marco para que no se corte
        derecha = X(p[0]) > VW/2
        anc = "end" if derecha else "start"
        tx = X(p[0]) + (-16 if derecha else 16)
        o.append(f'<text x="{tx:.1f}" y="{Y(p[1])+4:.1f}" '
                 f'font-size="11.5" font-weight="800" fill="#8a6a42" text-anchor="{anc}">{t}</text>')
    if b.get('girar'):
        o.append(f'<text x="14" y="24" font-size="12" font-weight="800" fill="#c8571b">'
                 f'PLANO GIRADO 90\u00b0 PARA QUE QUEPA EN LA HOJA</text>')
    o.append(f'<text x="{VW-14}" y="{VH-12}" font-size="11" fill="#888" text-anchor="end">'
             f'VISTA EN PLANTA · escala aprox. 1:{12/sc:.0f}</text>')
    return f'<svg viewBox="0 0 {VW} {VH}" xmlns="http://www.w3.org/2000/svg">' + "".join(o) + '</svg>'

# ---------------------------------------------------------------- HTML
CSS = """
 *{margin:0;padding:0;box-sizing:border-box}
 body{font-family:'Segoe UI',-apple-system,Helvetica,Arial,sans-serif;color:#1b2a41;background:#fff;font-size:13px}
 .page{max-width:10.2in;margin:0 auto;padding:.3in .35in}
 @media print{@page{size:letter landscape;margin:.3in .35in}.page{padding:0;max-width:none}
              .pb{page-break-before:always}.dw{page-break-inside:avoid}}
 .hd{display:flex;justify-content:space-between;align-items:center;border-bottom:4px solid #1b2a41;
     padding-bottom:6px;margin-bottom:8px}
 h1{font-size:20px;letter-spacing:.5px}
 .hd .m{font-size:12px;font-weight:700;text-align:right}
 .dw{border:2px solid #1b2a41;border-radius:5px;margin-bottom:10px}
 .dw svg{display:block;width:100%;height:auto;background:#fdfdfb}
 .nota{border-left:4px solid #c8571b;background:#fff8f2;padding:7px 11px;font-size:12px;margin:8px 0}
 .key{display:flex;gap:10px;margin:8px 0;font-size:12px}
 .key div{flex:1;border:2px solid #c3ccd5;border-radius:5px;padding:7px 10px}
 .key b{display:block;margin-bottom:2px}
 table{width:100%;border-collapse:collapse;margin:6px 0;font-size:13px}
 th{background:#1b2a41;color:#fff;padding:5px 9px;text-align:left}
 td{border:1px solid #c3ccd5;padding:4px 9px}
 td.n{text-align:right;white-space:nowrap;font-weight:700}
"""

def tabla(b):
    f = []
    for letra, _, _, L, secs in recorrido(b):
        s = "<i>falta medir</i>" if not secs else " &#183; ".join(secs)
        lg = "<i>sin medir</i>" if letra == "?" else f'{fr(L)}" ({feet(L)})'
        f.append(f"<tr><td><b>Corrida {letra}</b></td><td class='n'>{lg}</td><td>{s}</td></tr>")
    return "".join(f)

paginas = ""
for i, b in enumerate(BAL):
    paginas += f"""
  {'<div class="pb"></div>' if i else ''}
  <div class="hd"><h1>{b['titulo']}</h1><div class="m">PLANO DE INSTALACI&#211;N &#183; EN PLANTA<br>REV. 1 &#183; SEPT 20, 2026</div></div>
  <div class="dw">{svg(b)}</div>
  <table><tr><th style="width:18%">Corrida</th><th style="width:22%">Largo</th><th>Secciones soldadas</th></tr>{tabla(b)}</table>
  <div class="nota"><b>REVISA ESTO:</b> {b['nota']}</div>"""

html = f"""<!DOCTYPE html><html lang="es"><head><meta charset="UTF-8">
<title>Planos en planta &#8212; instalaci&#243;n</title><style>{CSS}</style></head><body><div class="page">
  <div class="hd"><h1>BARANDA &#8212; LOS CUATRO BALCONES EN PLANTA</h1>
    <div class="m">PLANOS DE INSTALACI&#211;N<br>REV. 1 &#183; SEPT 20, 2026</div></div>
  <div class="key">
    <div><b style="color:#1b2a41">&#9312; Letra en c&#237;rculo</b>La corrida. Su medida va en rojo por fuera.</div>
    <div><b style="color:#0f766e">Barra verde</b>Cada secci&#243;n soldada, con su letra. As&#237; se reparten en el trailer.</div>
    <div><b style="color:#1b2a41">Cuadrito blanco</b>Esquina.</div>
    <div><b style="color:#8a6a42">Bloque marr&#243;n</b>Donde muere contra la pared.</div>
  </div>
  <div class="nota"><b>Para qu&#233; es esta hoja:</b> revisar el recorrido contra el edificio antes de instalar.
  Los <b>largos y las letras</b> salen del mismo archivo que los planos de taller, as&#237; que no pueden discrepar.
  Lo que s&#237; tienes que revisar es <b>hacia qu&#233; lado dobla cada corrida</b>: eso lo le&#237; de tus croquis y
  puede estar volteado. Si una queda al rev&#233;s, <b>no cambia ni un largo ni una pieza</b> &#8212; solo cu&#225;l
  secci&#243;n se lleva cada poste de esquina.</div>
{paginas}
</div></body></html>"""

out = HERE / "railing-planta-instalacion.html"
out.write_text(html, encoding="utf-8")
print("escrito:", out.name)
for b in BAL:
    tr = recorrido(b)
    tot = sum(L for _,_,_,L,_ in tr)
    print(f"  {b['titulo']:28s} {len(tr)} corridas · {fr(tot)}\" = {tot/12:.1f} LF")
print(f"  TOTAL 4 balcones: {sum(sum(L for _,_,_,L,_ in recorrido(b)) for b in BAL)/12:.1f} LF (sin escaleras)")
