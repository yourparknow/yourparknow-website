#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Arma el SET COMPLETO de planos en un solo PDF, con portada e indice.
   La portada se genera dos veces: la primera para saber cuantas paginas ocupa,
   la segunda ya con los numeros de pagina buenos."""
import sys, subprocess, pathlib, importlib.util, time
for _m in ("cryptography", "cryptography.exceptions", "cryptography.hazmat"):
    sys.modules[_m] = None                      # el paquete del sistema esta roto
from pypdf import PdfReader, PdfWriter

HERE = pathlib.Path("/home/user/yourparknow-website/proposals/jrg-welding-corp")
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
spec = importlib.util.spec_from_file_location("gsec", HERE / "gen-railing-secciones.py")
G = importlib.util.module_from_spec(spec); spec.loader.exec_module(G)

FECHA = "21 DE SEPTIEMBRE, 2026"
NEG, ROJO, NAR = "#1b2a41", "#b91c1c", "#c8571b"

# nombre de archivo, titulo en el indice, para que sirve
HOJAS = [
 ("railing-planta-balcones", "PLANOS DE INSTALACI&#211;N &#183; LOS 4 BALCONES",
  "D&#243;nde va cada corrida, con las medidas de obra y los pa&#241;os repartidos."),
 ("railing-escaleras", "FABRICACI&#211;N &#183; LAS 4 ESCALERAS",
  "Las dos de 34&#176; y las dos de 33&#176;, con el dibujo acostado y su despiece."),
 ("railing-detalle-anclaje", "DETALLE DE ANCLAJE",
  "Las orejas de los 9 postes de esquina. Bloqueo, tornillos y medidas de borde."),
 ("railing-secciones-pool-house", "SECCIONES &#183; POOL HOUSE",
  "Vista de frente de cada secci&#243;n soldada, corridas A a la F."),
 ("railing-secciones-caballeriza", "SECCIONES &#183; CABALLERIZA 1",
  "Corridas G a la M, con la ele soldada de la escalera."),
 ("railing-secciones-caballeriza-2", "SECCIONES &#183; CABALLERIZA 2",
  "Corridas N, P, Q y R."),
 ("railing-fabricacion-caballerizas", "FABRICACI&#211;N &#183; LAS DOS CABALLERIZAS",
  "Despiece hoja por hoja: poste, cap, riel y piques de cada secci&#243;n."),
 ("railing-taller-pool-house", "TALLER &#183; POOL HOUSE",
  "La versi&#243;n sin n&#250;meros, para cortar. Una cota por pa&#241;o."),
 ("railing-taller-caballeriza", "TALLER &#183; CABALLERIZA 1", "Idem."),
 ("railing-taller-caballeriza-2", "TALLER &#183; CABALLERIZA 2", "Idem."),
]

# ---------------------------------------------------------------------------
# CANDADO.  Una hoja vieja de un generador que ya no existe se colo en el set y
# salio impresa con errores que ya estaban corregidos.  Ahora cada hoja tiene
# que declarar su generador, se vuelven a correr todos, y se comprueba que el
# HTML y el PDF de cada hoja se acaban de rehacer en ESTA corrida.
GENERADOR = {
 "railing-planta-balcones":            "gen-railing-planta.py",
 "railing-escaleras":                  "gen-railing-escaleras.py",
 "railing-detalle-anclaje":            "gen-railing-detalle-anclaje.py",
 "railing-secciones-pool-house":       "gen-railing-secciones.py",
 "railing-secciones-caballeriza":      "gen-railing-secciones.py",
 "railing-secciones-caballeriza-2":    "gen-railing-secciones.py",
 "railing-fabricacion-caballerizas":   "gen-railing-fab-caballerizas.py",
 "railing-taller-pool-house":          "gen-railing-taller.py",
 "railing-taller-caballeriza":         "gen-railing-taller.py",
 "railing-taller-caballeriza-2":       "gen-railing-taller.py",
}
faltan = [n for n, _, _ in HOJAS if n not in GENERADOR]
assert not faltan, f"hojas sin generador declarado, no entran al set: {faltan}"

T0 = time.time() - 1
for g in dict.fromkeys(GENERADOR.values()):
    subprocess.run([sys.executable, str(HERE / g)], check=True, capture_output=True, cwd=HERE)

def render(html_path, pdf_path):
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-sandbox",
                    "--no-pdf-header-footer", "--virtual-time-budget=9000",
                    f"--print-to-pdf={pdf_path}", str(html_path)],
                   check=True, capture_output=True)

for n, _, _ in HOJAS:
    html, pdf = HERE / f"{n}.html", HERE / f"{n}.pdf"
    assert html.stat().st_mtime >= T0, (
        f"\n\n  *** {n}.html NO lo rehizo {GENERADOR[n]} en esta corrida.\n"
        f"      Es una hoja hu&#233;rfana o el generador no la escribe. NO entra al set.\n")
    render(html, pdf)
    assert pdf.stat().st_mtime >= T0, f"{n}.pdf no se volvio a imprimir"

paginas = {n: len(PdfReader(HERE / f"{n}.pdf").pages) for n, _, _ in HOJAS}

# --- totales, sacados del generador maestro (no se teclea ni un numero a mano)
tot = dict(dib=0, lis=0, piq=0, pos=0, sec=0)
for cfg in G.EDIFICIOS:
    for _, gr in cfg['grupos']:
        for s in gr:
            tot['sec'] += 1
            for e in s['elems']:
                if e[0] == 'P': tot['pos'] += 1
                elif e[0] == 'D': tot['dib'] += 1
                else:
                    tot['lis'] += 1
                    tot['piq'] += G.piques_de(e[1])[0]
PIQ_TOTAL = tot['piq'] + tot['dib'] * 4
spec_e = importlib.util.spec_from_file_location("gesc", HERE / "gen-railing-escaleras.py")
E = importlib.util.module_from_spec(spec_e); spec_e.loader.exec_module(E)
ESC_N   = sum(x['cant'] for x in E.ESCALERAS)
ESC_POS = sum((E.geo(x)['n_bay']) * x['cant'] for x in E.ESCALERAS)
ESC_DIB = sum(E.geo(x)['n_dib'] * x['cant'] for x in E.ESCALERAS)
ESC_PIQ = sum(((E.geo(x)['n_bay'] - E.geo(x)['n_dib']) * E.geo(x)['n_piq']
                + E.geo(x)['n_dib'] * (2 + 2*E.geo(x)['n_fl'])) * x['cant']
              for x in E.ESCALERAS)
ESC_SEC = ESC_N                                   # cada escalera sale como una pieza
spec_p = importlib.util.spec_from_file_location("gpl", HERE / "gen-railing-planta.py")
PL = importlib.util.module_from_spec(spec_p); spec_p.loader.exec_module(PL)
PIES_BAL = sum(PL.pies(b) for b in PL.BAL) / 12.0           # sin el panito sin medir
PIES_ESC = sum(x['rake'] * x['cant'] for x in E.ESCALERAS) / 12.0
PIES_TOT = PIES_BAL + PIES_ESC
SIN_MEDIR = PL.INCOGNITA / 12.0        # los 4 piques rectos de 38 de cada dibujo


def portada(offset):
    filas, p = [], 1 + offset
    for n, t, d in HOJAS:
        filas.append(f"<tr><td class='pg'>{p}</td><td><b>{t}</b></td><td>{d}</td>"
                     f"<td class='pg'>{paginas[n]}</td></tr>")
        p += paginas[n]
    total = p - 1
    return f"""<!DOCTYPE html><html lang="es"><head><meta charset="UTF-8">
<title>Set de planos</title><style>
 *{{margin:0;padding:0;box-sizing:border-box}}
 body{{font-family:'Segoe UI',-apple-system,Helvetica,Arial,sans-serif;color:{NEG};font-size:13px}}
 .page{{max-width:10.2in;margin:0 auto;padding:.3in .35in}}
 @media print{{@page{{size:letter landscape;margin:.3in .35in}}.page{{padding:0;max-width:none}}}}
 .hd{{border-bottom:5px solid {NEG};padding-bottom:9px;margin-bottom:11px;
     display:flex;justify-content:space-between;align-items:flex-end}}
 h1{{font-size:27px;letter-spacing:.5px;line-height:1.1}}
 .hd .s{{font-size:14px;color:#55606c;margin-top:3px}}
 .hd .m{{text-align:right;font-size:12px;font-weight:700;line-height:1.5}}
 .big{{display:flex;gap:9px;margin:11px 0}}
 .big div{{flex:1;border:2px solid {NEG};border-radius:5px;padding:7px 9px;text-align:center}}
 .big b{{display:block;font-size:27px;color:{ROJO};line-height:1.1}}
 .big span{{font-size:9.5px;text-transform:uppercase;letter-spacing:.6px;font-weight:700}}
 table{{width:100%;border-collapse:collapse;font-size:12.5px}}
 th{{background:{NEG};color:#fff;padding:5px 9px;text-align:left;font-size:11px}}
 td{{border:1px solid #d3dae1;padding:4.5px 9px}}
 td.pg{{text-align:center;font-weight:800;width:8%}}
 .warn{{border-left:5px solid {ROJO};background:#fff5f5;padding:9px 13px;font-size:12.5px;margin-top:11px}}
 h2{{font-size:12px;background:{NEG};color:#fff;padding:4px 10px;margin:12px 0 6px;
    text-transform:uppercase;letter-spacing:.6px}}
</style></head><body><div class="page">

 <div class="hd">
   <div><h1>BARANDA DE ALUMINIO &#183; SET COMPLETO DE PLANOS</h1>
        <div class="s">Raúl &#183; 18398 131st Trail N, Jupiter, FL 33478 &#183; los cuatro balcones</div></div>
   <div class="m">JRG WELDING CORP<br>{FECHA}<br>{total} P&#193;GINAS</div>
 </div>

 <div class="big">
   <div><b>4+4</b><span>balcones y escaleras</span></div>
   <div><b>{PIES_TOT:.0f}</b><span>pies de baranda</span></div>
   <div><b>{tot['dib']+ESC_DIB}</b><span>dibujos</span></div>
   <div><b>{PIQ_TOTAL+ESC_PIQ}</b><span>piques</span></div>
   <div><b>{tot['pos'] + ESC_POS}</b><span>postes</span></div>
   <div><b>{tot['sec']+ESC_SEC}</b><span>secciones soldadas</span></div>
 </div>

 <h2>Qu&#233; hay en este set</h2>
 <table>
  <tr><th class="pg">P&#225;g.</th><th style="width:27%">Hoja</th><th>Para qu&#233; sirve</th>
      <th class="pg">Hojas</th></tr>
  {''.join(filas)}
 </table>

 <div class="warn"><b>LAS 4 ESCALERAS YA EST&#193;N EN EL SET</b>, con el dibujo acostado
 y su despiece. <b>Est&#225;n hechas tomando que las 185-1/2" y las 198" las mediste POR LA
 PENDIENTE</b>, pegada la cinta al stringer: as&#237; la del balc&#243;n 1 sube 8'-7-23/32" y la del
 balc&#243;n 2 sube 8'-11-27/32". <b>Mide del piso de abajo al deck antes de cortar.</b> Y ojo:
 los {ESC_DIB} dibujos de las escaleras <b>NO son los del balc&#243;n</b>, son piezas nuevas, 2 de
 34&#176; y 2 de 33&#176;.</div>

 <div class="warn"><b>LO QUE FALTA MEDIR:</b> el pa&#241;ito del signo de interrogaci&#243;n en
 la caballeriza lado 2, como <b>{SIN_MEDIR:.0f} pies</b>. <b>No est&#225; dibujado y NO est&#225;
 contado arriba</b> &#8212; los {PIES_TOT:.0f} pies son solo lo que est&#225; dibujado y se puede
 cortar. Cuando me des esa medida te digo si lleva un dibujo o dos y actualizo los totales.</div>

 <div class="warn"><b>Dos cosas para el carpintero, antes de montar:</b>
 <b>bloqueo s&#243;lido 2&#215; en las 9 esquinas</b>, en las dos direcciones, y el
 <b>rim de 2&#215;8 como m&#237;nimo</b> para que quepan las 6" que baja el poste con la
 oreja adentro. Sin eso el anclaje de esquina no sirve. Si el trabajo lleva permiso,
 la hoja del anclaje hay que pasarla por el ingeniero.</div>

</div></body></html>"""


# --- dos pasadas: la primera para saber cuanto ocupa la portada
ph, pp = HERE / "railing-set-portada.html", HERE / "railing-set-portada.pdf"
ph.write_text(portada(1), encoding="utf-8"); render(ph, pp)
n_port = len(PdfReader(pp).pages)
ph.write_text(portada(n_port), encoding="utf-8"); render(ph, pp)
assert len(PdfReader(pp).pages) == n_port, "la portada cambio de tamano en la segunda pasada"

w = PdfWriter()
for pg in PdfReader(pp).pages: w.add_page(pg)
for n, _, _ in HOJAS:
    for pg in PdfReader(HERE / f"{n}.pdf").pages: w.add_page(pg)
out = HERE / "RAILING-SET-COMPLETO.pdf"
with open(out, "wb") as f: w.write(f)

total = n_port + sum(paginas.values())
assert len(PdfReader(out).pages) == total, "el merge no cuadra"
print(f"escrito: {out.name}  ({total} paginas, portada de {n_port})")
p = 1 + n_port
for n, t, _ in HOJAS:
    print(f"   pag {p:3d}   {t.replace('&#183;','·').replace('&#211;','Ó').replace('&#241;','ñ')}")
    p += paginas[n]
print(f"\n   {tot['dib']+1} dibujos · {PIQ_TOTAL} piques · {tot['pos']} postes · {tot['sec']} secciones")
