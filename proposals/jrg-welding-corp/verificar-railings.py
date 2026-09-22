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
 "Q": 'el retorno de la caballeriza 2: Rene lo mando en DOS panos, asi que con un '
      'dibujo y un liso el dibujo cae por fuerza en una punta. El liso va en la '
      'esquina de los platos. PENDIENTE de que Rene diga de que lado lo quiere.',
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
    # OJO: esto chequeaba SOLO los panos lisos. Los flancos del DIBUJO se
    # colaban, y el retorno de la caballeriza 2 los abre a 3-13/16 al pasar sus
    # panos a 47-1/2. Ahora se miran los dos.
    def flanco(luz):
        """luz libre a cada lado del cuadro del dibujito"""
        return (luz - 2*G.GAP_PANEL - 4*1.0 - G.LUZ_CUADRO if hasattr(G, 'LUZ_CUADRO')
                else luz - 2*G.GAP_PANEL - 4*1.0 - 28.25) / 4
    for nm, s in SEC.items():
        for e in s['elems']:
            if e[0] == 'D':
                lz = flanco(e[1]) + G.GAP_PANEL
                if lz >= 4.0:
                    mal(f"{nm}: el flanco del dibujo de {fr(e[1])}\" deja {fr(lz,32)}\" "
                        f"— PASA LA ESFERA DE 4\"")
                elif lz > 3.90:
                    filo.append(f"{nm} (flanco del dibujo de {fr(e[1])}\" -> {fr(lz,32)}\")")
                if lz > peor: peor, peor_nm = lz, nm + " (flanco)"
                continue
            if e[0] != 'L': continue
            n, g = G.piques_de(e[1]); luz = g + G.GAP_PANEL
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
            if letra not in P.MEDIDO: continue
            med, desc = P.MEDIDO[letra]
            if abs((med - desc) - P.CORRIDA[letra][0]) > 1e-9:
                mal(f"corrida {letra}: medida {fr(med)}\", descuento {fr(desc)}\", "
                    f"se fabrica {fr(P.CORRIDA[letra][0])}\" — no cuadra")
    con = sorted(k for k, v in P.MEDIDO.items() if v[1])
    sin = sorted(k for k, v in P.MEDIDO.items() if not v[1])
    return (f"2\" de descuento en {', '.join(con)}"
            + (f" ; {', '.join(sin)} sin descuento (la cinta llega al poste)" if sin else ""))

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
        if any(x == 'D' and y == 'D' for x, y in zip(seq, seq[1:])):
            mal(f"{e['n']}: dos dibujos pegados")
        # alternado, y el de ARRIBA tiene que ser dibujo para alternar con el
        # ultimo pano del balcon, que es de piques
        if seq != ['D' if i % 2 == 0 else 'L' for i in range(len(seq))]:
            mal(f"{e['n']}: el reparto no alterna: {' '.join(seq)}")
    nd = sum(E.geo(x)['n_dib'] * x['cant'] for x in E.ESCALERAS)
    return f"{sum(x['cant'] for x in E.ESCALERAS)} escaleras, alternadas, {nd} dibujos"

def t20_rotulos():
    """Cada pieza tiene que decir QUE ES, no solo su codigo. Rene no encontraba
       "el de 104" ni "la L" en la hoja de taller porque solo salia "J-1"."""
    faltan = [nm for nm in SEC if not G.ROTULOS.get(nm)]
    if faltan:
        mal("estas piezas salen sin nombre en la hoja de taller: " + ", ".join(sorted(faltan)))
    sobran = [k for k in G.ROTULOS if k not in SEC]
    if sobran:
        mal("hay rotulos de piezas que ya no existen: " + ", ".join(sorted(sobran)))
    return f"las {len(SEC)} piezas dicen que son, no solo su codigo"

def t21_contra_rene():
    """Lo que Rene DIJO contra lo que el generador esta fabricando. El registro
       vive en gen-medidas-de-rene.py, escrito a mano con sus palabras; los
       planos salen de gen-railing-secciones. Si los dos se separan, aqui se ve.
       Existe porque nos pasamos un dia discutiendo de memoria quien dijo que."""
    R = load("gen-medidas-de-rene.py")
    n = 0
    for bal, d in R.MEDIDAS.items():
        for que, dijo, pieza, secs, _ in d['filas']:
            falta = [x for x in secs if x not in SEC]
            if falta:
                mal(f"{bal} / {que}: el registro nombra secciones que no existen: {falta}")
                continue
            real = sum(G.largo(SEC[x]) for x in secs)
            n += 1
            if abs(real - pieza) > 1e-9:
                mal(f"{bal} / {que}: Rene dio {fr(pieza)}\" y el plano fabrica {fr(real)}\"")
    return f"las {n} medidas de Rene cuadran con lo que se fabrica"

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
        # ahora TODAS las piezas se cortan al mismo angulo, tambien la V y el pique
        caja = {c: round(L * 64) for c, q, L, _ in g['piezas']}   # al 1/64
        caja['pique'] = round(g['largo_pique'] * 64)
        caja['poste'] = round(g['post_cara_larga'] * 64)
        if ref is None:
            ref = caja
        elif caja != ref:
            dif = [c for c in caja if caja[c] != ref.get(c)]
            mal(f"{e['n']}: estas piezas no salen iguales a las de la otra escalera "
                f"({', '.join(dif)}). Se pierde el trabajo en serie.")
    nd = sum(E.geo(x)['n_dib'] * x['cant'] for x in E.ESCALERAS)
    return (f"{nd} cuadros, postes y piques identicos, todo a {E.ANG_CORTE:g}\u00b0")

def t13_no_se_acumula():
    """Lo que preocupaba a Rene: cortar a 33.5 una baranda de 190" y bajarse dos
       pulgadas abajo. No pasa, PERO SOLO si ninguna medida que corre POR LA
       PENDIENTE sale del angulo de corte. Las que corren por la pendiente son
       el cap y el riel de cada pano: esas tienen que salir del angulo REAL.
       Si alguien las cambia al de corte, se acumula y esta prueba lo caza."""
    import math
    for e in E.ESCALERAS:
        g = E.geo(e)
        ca_real = math.cos(math.radians(e['ang']))
        ca_corte = math.cos(math.radians(E.ANG_CORTE))
        riel_real  = (g['bay'] - 2*E.GAP) / ca_real
        riel_corte = (g['bay'] - 2*E.GAP) / ca_corte
        if abs(g['riel_pano'] - riel_real) > 1e-9:
            acum = g['n_bay'] * abs(riel_real - riel_corte)
            mal(f"{e['n']}: el riel del pano NO sale del angulo real. "
                f"Se acumulan {fr(acum,32)}\" en los {g['n_bay']} panos.")
        if abs(g['cap_largo'] - e['rake']) > 1e-9:
            mal(f"{e['n']}: el cap no sale del largo medido en obra")
    return "el cap y el riel salen del angulo real: no se acumula nada"

def t14_empalme_escalera():
    """Donde la escalera empata con el balcon, las lineas tienen que coincidir.
       Las dos caras que se ven de frente son el TOPE DEL CAP y la PANZA DEL
       RIEL: esas dos tienen que dar la misma altura en el balcon y en la
       escalera, o se ve un brinco desde el patio."""
    import math
    for e in E.ESCALERAS:
        g = E.geo(e)
        if abs(g['y_cap_t'] - G.GUARD) > 1e-9:
            mal(f"{e['n']}: el tope del cap queda a {fr(g['y_cap_t'],32)}\" y el del "
                f"balcon a {fr(G.GUARD)}\". Brinco en el empalme.")
        if abs(g['y_riel_b'] - (G.Y_DECK - G.Y_RAIL_B)) > 1e-9:
            mal(f"{e['n']}: la panza del riel queda a {fr(g['y_riel_b'],32)}\" y la del "
                f"balcon a {fr(G.Y_DECK - G.Y_RAIL_B)}\". Brinco en el empalme.")
    paso = 1/math.cos(math.radians(E.ANG_CORTE)) - 1
    return (f"tope del cap y panza del riel coinciden; por dentro queda el "
            f"nudillo de {fr(paso,64)}\", que se corta y se suelda")

def t15_poste_cuadra():
    """El poste de la tabla tiene que ser el que dibuja el plano. Decia 48 y el
       plano dibujaba 47: el cap corre POR ENCIMA de los postes, asi que la
       punta va a la panza del cap, no al tope. Un pulgada en 80 postes."""
    dibujado = (G.Y_DECK - G.Y_CAP_B) + 6.0          # de la panza del cap a la fascia
    if abs(G.POST_LEN - dibujado) > 1e-9:
        mal(f"el poste de la tabla dice {fr(G.POST_LEN)}\" y el plano dibuja "
            f"{fr(dibujado)}\". Se descuadra por el grueso del cap.")
    return f"poste {fr(G.POST_LEN)}\" = {fr(dibujado-6)} a la panza del cap + 6 a la fascia"

def t16_alterna_empalme():
    """En el poste del empalme, el ultimo pano del balcon y el primero de la
       escalera tienen que ser distintos. Rene: "si termina en dibujo la
       escalera tiene que empezar con los piques y si termina en los piques
       la escalera tiene que empezar con el dibujo"."""
    par = {"ESCALERA DEL BALC\u00d3N 1": ("C", ["C-1", "C-2"]),
           "ESCALERA DEL BALC\u00d3N 2": ("F", ["F-1", "F-2"])}
    txt = []
    for e in E.ESCALERAS:
        run, nms = par[e['n']]
        bal = [x[0] for n in nms for x in SEC[n]['elems'] if x[0] != 'P'][-1]
        esc = [c[0] for c in E.geo(e)['cad'] if c[0] != 'P'][-1]
        if bal == esc:
            mal(f"{e['n']}: la corrida {run} termina en "
                f"{'dibujo' if bal=='D' else 'piques'} y la escalera arranca igual. "
                f"Tienen que alternar en el poste del empalme.")
        txt.append(f"{run} termina en {'dibujo' if bal=='D' else 'piques'} -> "
                   f"escalera arranca en {'dibujo' if esc=='D' else 'piques'}")
    return " ; ".join(txt)

def t17_entreverado():
    """PANO ENTREVERADO: uno si, uno no, por toda la corrida y CRUZANDO los
       empates rectos. Regla de Rene desde el principio.
       La excepcion son las ESQUINAS de 90: ahi el pidio piques a los dos lados
       ("que en las esquinas quedaran los piques, para ajustar en las esquinas"),
       asi que dos panos de pique tocandose en una esquina es lo correcto --
       ademas van en dos planos distintos y no se leen como dos seguidos.
       Lo que NO puede pasar es que se rompa en una linea recta, que es
       justo lo que paso en el empalme de la escalera."""
    import math
    for b in P.BAL:
        tr = P.recorrido(b)
        for (l1, p0, p1, _), (l2, q0, q1, _) in zip(tr, tr[1:]):
            if l1 in ("ESC", "?") or l2 in ("ESC", "?"): continue
            v1 = (p1[0]-p0[0], p1[1]-p0[1]); v2 = (q1[0]-q0[0], q1[1]-q0[1])
            n1 = math.hypot(*v1) or 1; n2 = math.hypot(*v2) or 1
            ang = math.degrees(math.acos(max(-1, min(1,
                  (v1[0]*v2[0]+v1[1]*v2[1])/(n1*n2)))))
            if ang > 45: continue                      # esquina: exenta
            a = [e[0] for e in P.elems(l1) if e[0] != 'P']
            c = [e[0] for e in P.elems(l2) if e[0] != 'P']
            if l1 in P.REVERSO: a = a[::-1]
            if l2 in P.REVERSO: c = c[::-1]
            if a and c and a[-1] == c[0]:
                mal(f"{b['t']}: {l1} termina en "
                    f"{'dibujo' if a[-1]=='D' else 'piques'} y {l2} arranca igual, "
                    f"y siguen RECTO. Se rompe el entreverado.")
        # dentro de cada corrida
        for letra, _, _, _ in tr:
            if letra in ("ESC", "?"): continue
            q = [e[0] for e in P.elems(letra) if e[0] != 'P']
            for i, (x, y) in enumerate(zip(q, q[1:])):
                if x == y:
                    mal(f"{b['t']}: corrida {letra}, panos {i+1} y {i+2} los dos "
                        f"{'dibujo' if x=='D' else 'piques'}. No esta entreverado.")
    return "uno si, uno no, en toda corrida y en todo empate recto (las esquinas van de piques, a pedido)"

def t18_arriba_igual_abajo():
    """La linea de ARRIBA (el cap) y la linea de ABAJO (los rieles con los postes
       metidos en el medio) tienen que medir LO MISMO. Rene lo cogio en obra:
       "arriba esta bien, abajo me faltan dos pulgadas". Eran 1/4 de holgura por
       lado en cada pano -- 1/2 por pano -- que se comian la linea de abajo. En
       la G eran 4 panos = 2 pulgadas. Estaba en las 26 secciones de la obra."""
    peor, peor_nm = 0.0, ""
    for nm, s in SEC.items():
        arriba = sum(G.POST if e[0] == 'P' else e[1] for e in s['elems'])
        abajo  = sum(G.POST if e[0] == 'P' else e[1] - 2 * G.GAP_PANEL for e in s['elems'])
        d = abs(arriba - abajo)
        if d > 1e-9:
            mal(f"{nm}: arriba mide {fr(arriba)}\" y abajo {fr(abajo)}\" — "
                f"{fr(d)}\" de diferencia. El riel tiene que ir de cara de poste a cara de poste.")
        if d > peor: peor, peor_nm = d, nm
    return (f"las {len(SEC)} secciones miden igual arriba que abajo "
            f"(holgura de panel = {fr(G.GAP_PANEL)}\": el riel va completo y soldado)")

def t19_cap_no_sobresale():
    """DONDE MUERE EL CAP, SEGUN EL TIPO DE JUNTA:
         EMPATE  -> al CENTRO del poste (-1 / +1), para que las dos puntas de
                    cap se encuentren encima del poste. Rene: "corrigeme todos
                    los empates que queden en el centro".
         ESQUINA y PARED -> A RAS con el pano. Rene lo cogio en obra con el cap
                    saliendose 2" por la esquina de la G.
         SOLDADA -> inglete de la L, cortado en el taller antes de pintar.
       Y los caps de una corrida tienen que cubrir su material propio."""
    for nm, s in SEC.items():
        L = G.largo(s)
        a, b = G.cap_tramo(s)
        if abs((b - a) - G.cap_largo(s)) > 1e-9:
            mal(f"{nm}: el cap dibujado mide {fr(b-a)}\" y la tabla dice {fr(G.cap_largo(s))}\"")
        for lado, txt, pos, esp in (("izq", s['izq'], a, 0.0), ("der", s['der'], b, L)):
            if "EMPATE" in txt:
                ok = abs(pos - (esp + (-1.0 if lado == "izq" else -1.0))) < 1e-9
                if not ok:
                    mal(f"{nm} ({lado}): es un EMPATE y el cap no cae en el centro del poste")
            elif "SOLDADA" in txt and lado == "izq":
                # el inglete solo lo lleva la pata que ARRANCA EN PANO sobre el
                # poste compartido. La otra pata LLEVA ese poste, y por ese lado
                # su cap muere a ras, como cualquier esquina.
                if abs(pos - (esp - G.POST)) > 1e-9:
                    mal(f"{nm} ({lado}): es la L soldada y el inglete no llega a la punta")
            else:
                if abs(pos - esp) > 1e-9:
                    mal(f"{nm} ({lado}): esquina o pared, el cap tiene que morir A RAS "
                        f"y se pasa {fr(abs(pos-esp))}\"")
    for cfg in G.EDIFICIOS:
        for _, run, total, nms in cfg['corridas']:
            suma = sum(G.cap_largo(SEC[n]) for n in nms)
            propio = sum(G.largo(SEC[n]) for n in nms)
            propio += G.POST * sum(1 for n in nms if "SOLDADA" in SEC[n]['izq'])
            if abs(suma - propio) > 1e-9:
                mal(f"corrida {run}: los caps suman {fr(suma)}\" y su material es {fr(propio)}\"")
    return "empates al centro del poste, esquinas y paredes a ras, la L a inglete"

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
 ("Un solo corte para las 4 escaleras",     t12_cuadro_unico),
 ("El medio grado no se acumula",           t13_no_se_acumula),
 ("El empalme escalera-balcon cuadra",      t14_empalme_escalera),
 ("El poste de la tabla = el dibujado",     t15_poste_cuadra),
 ("Alterna en el poste del empalme",        t16_alterna_empalme),
 ("Pa\u00f1o entreverado en linea recta",      t17_entreverado),
 ("Arriba mide igual que abajo",            t18_arriba_igual_abajo),
 ("Cada junta del cap donde toca",          t19_cap_no_sobresale),
 ("Cada pieza dice qu\u00e9 es",                t20_rotulos),
 ("Lo que dijo Rene = lo que se fabrica",   t21_contra_rene),
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
