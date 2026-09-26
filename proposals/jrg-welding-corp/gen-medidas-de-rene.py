#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EL REGISTRO DE LAS MEDIDAS DE RENE.  Una sola hoja, todo lo que dijo,
   repartido por balcon, con sus propias palabras al lado.

   Existe porque nos pasamos el dia dando vueltas sobre quien dijo que:
   "hijo, pero si ayer las medidas que me estabas dando... anota bien las cosas
    ahi a las una sola vez. Pon un puto archivo con las medidas que te di,
    divididas las de un lado para el otro."

   ESTO NO SE CALCULA: es lo que Rene DIJO.  Los planos salen de
   gen-railing-secciones; esta hoja es contra lo que se comprueban.  Si una
   medida de aqui no cuadra con la del generador, la verificacion 21 lo canta.
"""
import importlib.util, pathlib, io, contextlib

HERE = pathlib.Path("/home/user/yourparknow-website/proposals/jrg-welding-corp")
_s = importlib.util.spec_from_file_location("gsec", HERE / "gen-railing-secciones.py")
G = importlib.util.module_from_spec(_s)
with contextlib.redirect_stdout(io.StringIO()): _s.loader.exec_module(G)
fr, feet = G.fr, G.feet

# (que es, lo que dijo, como queda la PIEZA, que seccion lo lleva, sus palabras)
# "pieza" = el largo que sale del taller. None = todavia no hay pieza.
MEDIDAS = {
"CABALLERIZA 1": dict(
  cuando="21 de septiembre — «pon ahí caballeriza número uno»",
  filas=[
   ("EL FRENTE", "36'-10\" = 442 interior",  446.0, ["H-1","H-2","H-3"],
    "«36 pies 10 pulgadas el frente, más los dos postes de los lados»"),
   ("LATERAL DERECHO", "193 con su poste de la pared", 193.0, ["G-1"],
    "«va a ir a 193 con un solo poste, el que va pegado a la pared, porque se va a amarrar al poste del paño del frente»"),
   ("LATERAL IZQUIERDO", "104 pelado, sin poste propio", 104.0, ["J-1"],
    "«el paño de 104 va a ir de 104 nada más, porque se va a amarrar al poste este y se va a amarrar al poste del frente»"),
   ("LA 4ta, PARALELA AL FRENTE", "98-3/4 de paño + 2 del poste", 100.75, ["K-1"],
    "«98-3/4 con un solo poste, el del final, el que conecta al paño de 104... van a ser 100-3/4 con el poste»"),
   # 47 + 29 = 76 contaria DOS VECES el poste de la esquina, que las dos patas
   # comparten. El material que sale del taller son 74. La verificacion 21 lo
   # cogio en su primera corrida, con el 76 que habia puesto yo aqui.
   ("LA L SOLDADA", "47 x 29-3/4 afuera a afuera (comparten el poste de la esquina)",
    74.75, ["M-1","L-1"],
    "«esa L de 47 por 29. Va a ser 29, 3 cuartos exacto» — del croquis del 22 sept"),
  ],
  abierto=["<b>LA VUELTA YA CIERRA</b>, con el croquis del 22 de septiembre: el lateral "
           "derecho baja 193, el izquierdo 104 y la pata de la L son 47, así que "
           "<b>el hueco de la escalera son 42\"</b> (193 − 104 − 47). Yo lo tenía en 27. "
           "<b>Confírmame ese 42</b> — sale del croquis, no de una cinta.",
           "El lateral derecho quedó en <b>193 de material</b>, confirmado por Rene el 22: "
           "su poste va en la punta de la pared y por la esquina muere en paño contra el "
           "poste del frente."]),

"CABALLERIZA 2": dict(
  cuando="21 de septiembre — «esta es la otra, la caballeriza nueva, la número 2»",
  filas=[
   ("EL FRENTE", "37'-1-3/8\" de poste a poste", 445.375, ["N-1","N-2","N-3"],
    "del croquis del 22: «37-1 3/8 DE POSTE A POSTE» — clavado con lo que ya estaba"),
   ("PAÑO DERECHO", "191-3/8, 1 solo poste", 191.375, ["P-1"],
    "del croquis del 22 sept: «191-3/8, 1 SOLO POSTE», el de la pared"),
   ("EL RETORNO", "101 afuera a afuera, 2 postes", 101.0, ["Q-1"],
    "del croquis del 22: «101\", 2 POSTES». Y antes: «no vamos a poner tres paños, tiene que irse en dos»"),
   ("PAÑO DE LA IZQUIERDA", "105-1/4 pelado, sin poste propio", 105.25, ["S-1"],
    "«el pañito que nos faltaba en la caballeriza número 2 es de 105 un cuarto» — 26 sept"),
   ("PAÑITO SUELTO", "46-3/4 afuera a afuera, 2 postes", 46.75, ["R-1"],
    "del croquis del 22: «46-3/4, 2 POSTES». Antes lo había dado en 47"),
  ],
  abierto=["<b>EL PAÑO DE LA IZQUIERDA YA ESTÁ</b>: 105-1/4, dado el 26 de septiembre. "
           "Va <b>sin poste propio en ninguna punta</b> — se amarra al poste de esquina del "
           "frente por un lado y al poste de los platos por el otro, igual que el de 104 en "
           "la caballeriza 1. <b>Rene no dijo si esas 105-1/4 llevan los postes adentro: "
           "si los llevan, la pieza baja a 101-1/4.</b>",
           "<b>Falta decir de qué lado va el dibujo del retorno.</b> Con dos paños, el "
           "dibujo cae por fuerza en una punta. Lo puse con el paño liso en la esquina de "
           "los platos, que es la regla de las esquinas.",
           "Con las <b>101\"</b> del croquis, los dos paños del retorno salen a <b>47-1/2</b>: "
           "si el dibujo se quedara en 46, el liso se iría a 49, por encima de tus 4 pies. "
           "El flanco de ese dibujo abre a <b>3-13/16</b> (el límite es 4)."]),

"BALCÓN 1 · POOL HOUSE": dict(
  cuando="de las medidas anteriores — no se han vuelto a revisar con Rene",
  filas=[
   ("EL FRENTE LARGO", "383-5/8", 383.625, ["A-1","A-2","A-3"], ""),
   ("LATERAL CONTRA LA CASA", "161 medidas − 2 de la pared", 157.0, ["B-1"], ""),
   ("LATERAL DE LA ESCALERA", "237-5/8", 235.625, ["C-1","C-2"], ""),
  ],
  abierto=["Estas medidas son de <b>antes</b> de que Rene aclarara lo de las medidas "
           "interiores y los postes de esquina. <b>Los largos no se han vuelto a confirmar "
           "con él.</b> Los arreglos de fabricación (riel completo, cap a ras, poste de 47) "
           "sí están aplicados aquí."]),

"BALCÓN 2 · POOL HOUSE": dict(
  cuando="de las medidas anteriores — no se han vuelto a revisar con Rene",
  filas=[
   ("EL FRENTE LARGO", "389-1/4", 389.25, ["D-1","D-2","D-3"], ""),
   ("LATERAL CONTRA LA CASA", "151-5/8 medidas − 2 de la pared", 147.625, ["E-1"], ""),
   ("LATERAL DE LA ESCALERA", "239-3/4", 237.75, ["F-1","F-2"], ""),
  ],
  abierto=["Igual que el balcón 1: los largos vienen de las medidas anteriores y "
           "<b>no se han vuelto a confirmar</b>."]),
}

CSS = """
 *{margin:0;padding:0;box-sizing:border-box}
 body{font-family:'Segoe UI',-apple-system,Helvetica,Arial,sans-serif;color:#1b2a41;font-size:12.5px}
 .page{max-width:10.4in;margin:0 auto;padding:.3in .35in}
 @media print{@page{size:letter landscape;margin:.35in}.page{padding:0;max-width:none}
              .bal{page-break-inside:avoid}}
 h1{font-size:26px;letter-spacing:.5px;border-bottom:5px solid #1b2a41;padding-bottom:6px}
 .sub{font-size:12px;color:#555;margin:6px 0 14px}
 .bal{border:2px solid #1b2a41;border-radius:6px;margin-bottom:13px;overflow:hidden}
 .bal h2{background:#1b2a41;color:#fff;font-size:17px;padding:6px 12px;letter-spacing:1px;
         display:flex;justify-content:space-between;align-items:baseline}
 .bal h2 em{font-style:normal;font-size:11px;color:#a9bacd;font-weight:500;letter-spacing:0}
 table{width:100%;border-collapse:collapse}
 th{background:#eef2f6;font-size:10.5px;text-transform:uppercase;letter-spacing:.6px;
    padding:5px 10px;text-align:left;border-bottom:1px solid #cfd6dd}
 td{padding:6px 10px;border-bottom:1px solid #e6ebf0;vertical-align:top}
 td.q{color:#555;font-style:italic;font-size:11.5px}
 td.n{white-space:nowrap;font-weight:800;text-align:right}
 td.ok{white-space:nowrap;text-align:center;font-weight:800;color:#0f766e}
 td.mal{white-space:nowrap;text-align:center;font-weight:800;color:#b91c1c}
 .ab{background:#fff5f5;border-top:2px solid #b91c1c;padding:8px 12px;font-size:12px;color:#7f1d1d}
 .ab p{margin:3px 0}
"""

def hoja():
    cuerpo = ""
    for bal, d in MEDIDAS.items():
        filas = ""
        for que, dijo, pieza, secs, palabras in d['filas']:
            real = sum(G.largo(s) for c in G.EDIFICIOS for _, gr in c['grupos']
                       for s in gr if s['name'] in secs)
            ok = abs(real - pieza) < 1e-9
            filas += (f"<tr><td><b>{que}</b></td><td>{dijo}</td>"
                      f"<td class='n'>{fr(pieza)}\"</td>"
                      f"<td class='{'ok' if ok else 'mal'}'>{'✔' if ok else '✘ ' + fr(real)}</td>"
                      f"<td>{', '.join(secs)}</td><td class='q'>{palabras}</td></tr>")
        ab = "".join(f"<p>{x}</p>" for x in d['abierto'])
        cuerpo += (f"<div class='bal'><h2>{bal}<em>{d['cuando']}</em></h2>"
                   f"<table><tr><th style='width:17%'>Qué es</th><th style='width:17%'>Lo que dijo</th>"
                   f"<th style='width:8%'>La pieza</th><th style='width:6%'>Cuadra</th>"
                   f"<th style='width:10%'>Secciones</th><th>Sus palabras</th></tr>"
                   f"{filas}</table><div class='ab'>{ab}</div></div>")
    return (f"<!DOCTYPE html><html lang='es'><head><meta charset='UTF-8'>"
            f"<title>Las medidas de Rene</title><style>{CSS}</style></head><body><div class='page'>"
            f"<h1>LAS MEDIDAS DE RENE — TODAS, POR BALCÓN</h1>"
            f"<p class='sub'>Lo que Rene dio, dónde va cada una, y qué falta todavía. "
            f"La columna <b>«Cuadra»</b> compara la medida contra lo que el generador está "
            f"fabricando de verdad: si alguna sale en rojo, el plano no dice lo que él dijo.</p>"
            f"{cuerpo}</div></body></html>")

if __name__ == "__main__":
    out = HERE / "MEDIDAS-DE-RENE.html"
    out.write_text(hoja(), encoding="utf-8")
    print("escrito:", out.name)
    for bal, d in MEDIDAS.items():
        print(f"  {bal:26s} {len(d['filas'])} medidas, {len(d['abierto'])} cosa(s) abierta(s)")
