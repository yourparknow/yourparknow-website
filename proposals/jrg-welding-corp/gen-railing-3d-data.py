#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Exporta la geometria de los cuatro balcones a JSON para el visor 3D.
   Sale del mismo generador de secciones: ni una medida se teclea dos veces."""
import importlib.util, pathlib, json

HERE = pathlib.Path("/home/user/yourparknow-website/proposals/jrg-welding-corp")
spec = importlib.util.spec_from_file_location("gsec", HERE / "gen-railing-secciones.py")
G = importlib.util.module_from_spec(spec); spec.loader.exec_module(G)

spec2 = importlib.util.spec_from_file_location("gpl", HERE / "gen-railing-planta.py")
# el generador de planta escribe su HTML al importarlo; lo dejamos correr, solo
# queremos sus recorridos y su tabla de descuentos.
P = importlib.util.module_from_spec(spec2); spec2.loader.exec_module(P)

SALIDA = []
for b in P.BAL:
    runs = []
    for letra, p0, p1, L in P.recorrido(b):
        if letra == "ESC":
            runs.append(dict(letra="ESC", p0=list(p0), p1=list(p1), largo=L, elems=[]))
            continue
        if letra == "?":
            runs.append(dict(letra="?", p0=list(p0), p1=list(p1), largo=L, elems=[]))
            continue
        el = [[e[0]] if e[0] == 'P' else [e[0], e[1], P.piques_de(e[1])[0] if e[0] == 'L' else 0]
              for e in P.elems(letra)]
        hueco = L - P.CORRIDA[letra][0]          # las 2" contra la pared
        runs.append(dict(letra=letra, p0=list(p0), p1=list(p1), largo=L, hueco=hueco, elems=el))
    esc = None
    if b.get('esc'):
        import re
        m = re.search(r"(\d+)(?:-(\d+)/(\d+))?\"\s*a\s*(\d+)", b['esc'])
        largo = float(m.group(1)) + (float(m.group(2))/float(m.group(3)) if m.group(2) else 0)
        esc = dict(largo=largo, grados=float(m.group(4)),
                   p=list(P.recorrido(b)[-1][2]),
                   dir=[P.recorrido(b)[-1][2][0]-P.recorrido(b)[-1][1][0],
                        P.recorrido(b)[-1][2][1]-P.recorrido(b)[-1][1][1]])
    d, q = P.cuenta(b)
    # postes de verdad: los que lleva cada SECCION. Si se cuentan por corrida,
    # cada poste de esquina sale dos veces.
    letras = {r['letra'] for r in runs}
    postes = 0
    for cfg in G.EDIFICIOS:
        for _, run, _, nombres in cfg['corridas']:
            if run in letras:
                postes += sum(1 for nm in nombres
                                for e in P.SEC[nm]['elems'] if e[0] == 'P')
    SALIDA.append(dict(nombre=b['t'], runs=runs, escalera=esc, postes=postes,
                       pies=round(P.pies(b)/12, 1), dibujos=d, panos=q))

out = HERE / "railing-3d-data.json"
out.write_text(json.dumps(SALIDA, separators=(",", ":")), encoding="utf-8")
print("escrito:", out.name, out.stat().st_size, "bytes")
for s in SALIDA:
    e = f" + escalera {s['escalera']['largo']}\" a {s['escalera']['grados']}°" if s['escalera'] else ""
    print(f"  {s['nombre']:32s} {len(s['runs'])} corridas · {s['dibujos']} dibujos{e}")
