#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""VERIFICADOR DE TODA LA BARANDA.  Se corre solo:  python3 verificar-railings.py

   Una sola orden que revisa TODO contra las reglas que puso Rene y contra el
   codigo.  Si algo esta mal, sale en rojo y con el nombre de la seccion.
   Existe porque se me han ido errores que el tuvo que encontrar en obra."""
import importlib.util, pathlib, sys, io, contextlib

HERE = pathlib.Path("/home/user/yourparknow-website/proposals/jrg-welding-corp")

def load(n):
    s = importlib.util.spec_from_file_location(n.replace("-", "_").replace(".py", ""), HERE / n)
    m = importlib.util.module_from_spec(s)
    with contextlib.redirect_stdout(io.StringIO()):     # los generadores imprimen
        s.loader.exec_module(m)
    return m

FALLOS, AVISOS = [], []
def mal(msg):   FALLOS.append(msg)
def ojo(msg):   AVISOS.append(msg)

G = load("gen-railing-secciones.py")
P = load("gen-railing-planta.py")
E = load("gen-railing-escaleras.py")
fr = G.fr

SEC = {}
for cfg in G.EDIFICIOS:
    for _, gr in cfg['grupos']:
        for s in gr:
            s['largo'] = G.largo(s)
            SEC[s['name']] = s

# Corridas donde Rene PIDIO que hubiera dibujo pegado a la punta.  No son
# descuidos: cada una tiene su frase.  Si alguien quita una de aqui, el
# verificador vuelve a protestar, que es lo que se quiere.
DIBUJO_EN_LA_PUNTA_OK = {
 "B": 'pool 1: "arranca desde la pared... arranca con un dibujo de la pared"',
 "G": 'caballeriza 1: sale de la pared con dibujo',
 "P": 'caballeriza 2: sale de la pared con dibujo',
 "L": 'la pata de 47: "en el 47 pongo un dibujo para que no se vea esa L completa sin dibujo"',
}

def t1_cadenas():
    for nm, s in SEC.items():
        if abs(sum(G.POST if e[0] == 'P' else e[1] for e in s['elems']) - s['largo']) > 1e-9:
            mal(f"{nm}: la cadena de la seccion no suma")
    return f"{len(SEC)} secciones, todas cierran"

def t2_dibujos_pegados():
    """incluido cuando la union cae en el empate de dos secciones de la misma corrida"""
    n = 0
    for cfg in G.EDIFICIOS:
        for _, run, _, nms in cfg['corridas']:
            seq = [e[0] for nm in nms for e in SEC[nm]['elems'] if e[0] != 'P']
            n += 1
            for i, (a, b) in enumerate(zip(seq, seq[1:])):
                if a == 'D' and b == 'D':
                    mal(f"corrida {run}: DOS DIBUJOS PEGADOS (pano {i+1} y {i+2})")
            if seq and seq[0] == 'D' and run not in DIBUJO_EN_LA_PUNTA_OK:
                mal(f"corrida {run}: arranca en dibujo y no deberia")
            if seq and seq[-1] == 'D' and run not in DIBUJO_EN_LA_PUNTA_OK:
                mal(f"corrida {run}: termina en dibujo y no deberia")
    return f"{n} corridas ok ({len(DIBUJO_EN_LA_PUNTA_OK)} con dibujo en la punta, a pedido)"

def t3_postes_libres():
    for cfg in G.EDIFICIOS:
        cad, rev = cfg['cadena'], cfg.get('reverso', set())
        for _, run, _, nms in cfg['corridas']:
            i = cad.index(run)
            ini, fin = SEC[nms[0]]['elems'][0], SEC[nms[-1]]['elems'][-1]
            if run in rev: ini, fin = fin, ini
            for lado, ext, vec in (("arranque", ini, cad[i-1]), ("final", fin, cad[i+1])):
                if ext[0] != 'P' and vec is None:
                    mal(f"corrida {run}: el {lado} muere en pano y del otro lado la cadena "
                        f"esta rota. FALTA UN POSTE.")
    return "todos los extremos libres llevan su poste"

def t4_esfera():
    peor, peor_nm = 0.0, ""
    filo = []
    for nm, s in SEC.items():
        for e in s['elems']:
            if e[0] != 'L': continue
            n, g = G.piques_de(e[1]); luz = g + 0.25
            if luz >= 4.0:
                mal(f"{nm}: pano de {fr(e[1])}\" deja {fr(luz,32)}\" — PASA LA ESFERA DE 4\"")
            elif luz > 3.90:
                filo.append(f"{nm} ({fr(e[1])}\" -> {fr(luz,32)}\")")
            if luz > peor: peor, peor_nm = luz, nm
    if filo:
        ojo(f"{len(filo)} panos quedan a menos de 1/10\" de las 4\": " + ", ".join(filo)
            + ". En obra, con la tolerancia normal, esos se pasan.")
    return f"el peor es {peor_nm}: {fr(peor,32)}\" de luz libre (limite 4\")"

def t5_descuentos():
    for b in P.BAL:
        for letra, _, _, L in P.recorrido(b):
            if letra in ("ESC", "?"): continue
            med = P.MEDIDO.get(letra)
            if med is not None and abs((med - 2.0) - P.CORRIDA[letra][0]) > 1e-9:
                mal(f"corrida {letra}: medida {fr(med)}\", se fabrica "
                    f"{fr(P.CORRIDA[letra][0])}\" — no son las 2\"")
    return f"las 2\" se descuentan en {', '.join(sorted(P.MEDIDO))} y en ninguna otra"

def t6_remates():
    """Pool House: una pared y una escalera.  Caballerizas: pared en los dos lados."""
    esp = {"BALCÓN 1  ·  POOL HOUSE": ["PARED", "ESCALERA"],
           "BALCÓN 2  ·  POOL HOUSE": ["PARED", "ESCALERA"],
           "BALCÓN 3  ·  CABALLERIZA LADO 1": ["PARED", "PARED"],
           "BALCÓN 4  ·  CABALLERIZA LADO 2": ["PARED", "PARED"]}
    vis = {}
    for bal, tipo, _ in P.REMATES: vis.setdefault(bal, []).append(tipo)
    for bal, e in esp.items():
        if vis.get(bal) != e:
            mal(f"{bal}: remates {vis.get(bal)} cuando tenian que ser {e}")
    return "Pool House pared+escalera, caballerizas pared+pared"

def t7_escaleras():
    for e in E.ESCALERAS:
        g = E.geo(e)
        if abs(sum(E.POST_W if c[0] == 'P' else c[1] for c in g['cad']) - g['horiz']) > 1e-9:
            mal(f"{e['n']}: la cadena horizontal no cierra")
        if g['sep'] + E.GAP >= 4.0:
            mal(f"{e['n']}: pasa la esfera de 4\"")
        # el dibujo de escalera lleva 15 piezas, o 17 si la bahia necesita
        # pique de flanco. Se comprueba contra la composicion, no contra un numero.
        esperadas = 15 + 2 * g['n_fl']
        if g['n_piezas'] != esperadas:
            mal(f"{e['n']}: el dibujo lleva {g['n_piezas']} piezas y tenian que ser {esperadas}")
        if g['cc'] > E.CC_MAX + 1e-9:
            mal(f"{e['n']}: postes a {fr(g['cc'])}\" centro a centro, pasa de {E.CC_MAX:g}\"")
        seq = [c[0] for c in g['cad'] if c[0] != 'P']
        if seq[0] == 'D' or seq[-1] == 'D':
            mal(f"{e['n']}: arranca o termina en dibujo")
        if any(x == 'D' and y == 'D' for x, y in zip(seq, seq[1:])):
            mal(f"{e['n']}: dos dibujos pegados")
        # Rene los quiere ALTERNADOS, como en el balcon, no uno solo en el medio
        if seq != ['L' if i % 2 == 0 else 'D' for i in range(len(seq))]:
            mal(f"{e['n']}: el reparto no es pique-dibujo-pique-dibujo-pique: {' '.join(seq)}")
    nd = sum(E.geo(x)['n_dib'] * x['cant'] for x in E.ESCALERAS)
    return f"{sum(x['cant'] for x in E.ESCALERAS)} escaleras, alternadas, {nd} dibujos"

def t8_letras():
    todas = [s['name'] for s in SEC.values()]
    if len(todas) != len(set(todas)):
        mal("hay letras de seccion repetidas entre edificios")
    return f"{len(todas)} secciones, ninguna letra repetida"

def t9_caballeriza_madera():
    """Las escaleras de las caballerizas SE QUEDAN DE MADERA: no baja aluminio."""
    for e in E.ESCALERAS:
        if "CABALLERIZA" in e['n'].upper():
            mal("hay una escalera de aluminio en la caballeriza y no debe haberla")
    for b in P.BAL:
        if "CABALLERIZA" in b['t'] and b.get('esc'):
            mal(f"{b['t']}: tiene baranda de escalera y las de la caballeriza son de madera")
    return "en las caballerizas no baja aluminio: solo las 4 del Pool House"

def t10_huerfanos():
    """Ninguna hoja del set puede venir de un generador que ya no existe."""
    S = load("gen-railing-set.py")
    for n, _, _ in S.HOJAS:
        if n not in S.GENERADOR:
            mal(f"la hoja {n} entra al set sin generador declarado")
        elif not (HERE / S.GENERADOR[n]).exists():
            mal(f"la hoja {n} apunta a {S.GENERADOR[n]}, que no existe")
    return f"las {len(S.HOJAS)} hojas del set salen de un generador vivo"

def t11_mismo_ancho():
    """El taller dibujaba el dibujo de L-1 a 46 cuando su bahia es de 43: la misma
       pieza salia con dos anchos en dos hojas del mismo set. Que no vuelva."""
    import re
    for arch in ("gen-railing-taller.py", "gen-railing-fab-caballerizas.py"):
        txt = (HERE / arch).read_text()
        for m in re.finditer(r"G\.dibujito\(([^)]*)\)", txt):
            if "," not in m.group(1):
                mal(f"{arch}: llama a dibujito() sin pasarle la luz de la bahia — "
                    f"el dibujo de 43\" saldria de 46\"")
    anchos = {e[1] for s in SEC.values() for e in s['elems'] if e[0] == 'D'}
    return f"las bahias de dibujo son {', '.join(fr(a) for a in sorted(anchos))}\", y cada hoja usa la suya"

def t12_cuadro_unico():
    """Las piezas del CUADRO (las que flotan) se arman todas al mismo angulo
       para poder trabajar en serie. Solo la V y los piques cambian por escalera."""
    ref = None
    for e in E.ESCALERAS:
        g = E.geo(e)
        caja = {c: round(L, 6) for c, q, L, _ in g['piezas'] if c not in ("V", "B")}
        if ref is None:
            ref = caja
        elif caja != ref:
            dif = [c for c in caja if caja[c] != ref.get(c)]
            mal(f"{e['n']}: las piezas del cuadro no son iguales a las de la otra "
                f"escalera ({', '.join(dif)}). Se pierde el trabajo en serie.")
    nd = sum(E.geo(x)['n_dib'] * x['cant'] for x in E.ESCALERAS)
    return f"{nd} cuadros identicos, armados a {E.ANG_DIB:g}&#176;".replace("&#176;", "\u00b0")

PRUEBAS = [
 ("Cadenas de cada seccion",                t1_cadenas),
 ("Dos dibujos nunca van pegados",          t2_dibujos_pegados),
 ("Un poste en cada extremo libre",         t3_postes_libres),
 ("La esfera de 4 pulgadas",                t4_esfera),
 ("Los descuentos de 2 pulgadas",           t5_descuentos),
 ("Pared y escalera en su lado",            t6_remates),
 ("Las escaleras del Pool House",           t7_escaleras),
 ("Letras de seccion sin repetir",          t8_letras),
 ("Caballerizas: escaleras de madera",      t9_caballeriza_madera),
 ("Ninguna hoja huerfana en el set",        t10_huerfanos),
 ("El mismo dibujo, igual en toda hoja",    t11_mismo_ancho),
 ("Un solo cuadro para las 4 escaleras",    t12_cuadro_unico),
]

print("\n" + "=" * 68)
print("  VERIFICACION DE LA BARANDA DE RAUL")
print("=" * 68)
for i, (nom, fn) in enumerate(PRUEBAS, 1):
    antes = len(FALLOS)
    det = fn()
    estado = "MAL " if len(FALLOS) > antes else " OK "
    print(f"  [{estado}] {i:2d}. {nom:38s} {det}")

print("=" * 68)
if FALLOS:
    print(f"\n  {len(FALLOS)} FALLO(S) — NO IMPRIMIR NADA HASTA ARREGLARLOS:\n")
    for f in FALLOS: print("   ***", f)
else:
    print(f"\n  LAS {len(PRUEBAS)} VERIFICACIONES PASAN.")
if AVISOS:
    print(f"\n  {len(AVISOS)} AVISO(S) — no paran nada, pero mira esto:\n")
    for a in AVISOS: print("   ->", a)
print()
sys.exit(1 if FALLOS else 0)
