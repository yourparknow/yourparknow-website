# JRG Welding Corp — Estado del trabajo de Raúl

**Cliente:** Raúl · 18398 131st Trail N, Jupiter, FL 33478
**Contratista:** JRG Welding Corp (Rene Garcia), Miami, FL
**Repo:** `yourparknow/yourparknow-website`
**Rama:** `claude/jrg-welding-proposal-xcc5jf` — se desarrolla y se empuja SOLO aquí
**Carpeta:** `proposals/jrg-welding-corp/`

Este archivo es el traspaso. Si llegas nuevo a este trabajo, léelo completo antes
de tocar un número.

---

## 1. Cómo hablarle a Rene

Habla por voz en español y el dictado le mete errores ("Hondipo" = Home Depot,
"Cloud"/"Clau" = Claude). Los documentos del cliente van en inglés.

**Lo que pidió expresamente:**

- **CERO ERRORES.** Los paños van a powder coating. Un paño mal fabricado hay que
  cortarlo o repintarlo y ahí se va la ganancia. Esta es la regla que manda sobre
  todas las demás.
- **Poco texto.** *"Dibujito de la baranda nada más con las cositas abajo, tantas
  piezas esto, tantas piezas esto. Sin tanto escrito y sin tanta mierda que eso no
  lo lee nadie."*
- **Que las piezas digan qué son**, no solo su código. Necesita encontrar "el de
  104" y "la L" sin descifrar nada.
- **Medidas en pulgadas Y en pies al lado**, chiquito. Él las anota en pies.
- No cambiar un número para tapar una explicación mala. Si el número está bien y la
  explicación está mal, se arregla la explicación.

---

## 2. La regla de oro del código

**`gen-railing-secciones.py` es la ÚNICA fuente de verdad.** Todos los demás
generadores lo cargan con `importlib`. Ninguna medida se teclea dos veces.

```
gen-railing-secciones.py      <- TODA la geometría vive aquí
   |
   +-- gen-railing-taller-simple.py   hojas de taller (las que usa el taller)
   +-- gen-railing-fab-caballerizas.py
   +-- gen-railing-escaleras.py
   +-- gen-railing-planta.py
   +-- gen-railing-detalle-anclaje.py
   +-- gen-railing-replanteo.py
   +-- gen-railing-taller.py
   +-- gen-railing-set.py
   +-- gen-railing-3d-data.py         inyecta los datos al 3D
   +-- gen-medidas-de-rene.py         lo que Rene DIJO, textual
   +-- verificar-railings.py          las 21 verificaciones
```

### Antes de publicar cualquier cosa

```bash
cd proposals/jrg-welding-corp
python3 verificar-railings.py       # tienen que pasar las 21
```

En la PC de Rene (Windows) se corre en modo UTF-8, si no se cae leyendo los HTML:

```bash
PYTHONUTF8=1 python verificar-railings.py
```

Ojo: la verificación 10 vuelve a imprimir los PDFs del set. Si no cambió ninguna
medida, no los subas (`git checkout -- '*.pdf'`).

Las 21 verificaciones incluyen: que cada cadena de cotas cierre, que no haya dos
dibujos pegados, la bola de 4 pulgadas (incluidos los flancos del dibujo), que
arriba mida igual que abajo, que cada junta del cap caiga donde toca, que cada
pieza diga qué es, y que **lo que dijo Rene sea igual a lo que se fabrica**.

Los asserts viven dentro del código de dibujo, así que una cadena mala no llega a
renderizar.

### Regenerar los PDFs

```bash
python3 gen-railing-taller-simple.py           # los 4 sets
python3 gen-railing-taller-simple.py S-1       # un paño solo
/opt/pw-browsers/chromium-1194/chrome-linux/chrome --headless --disable-gpu \
  --no-sandbox --no-pdf-header-footer --virtual-time-budget=9000 \
  --print-to-pdf=ARCHIVO.pdf ARCHIVO.html
```

---

## 3. Los números duros

| Constante | Valor | Por qué |
|---|---|---|
| `POST_LEN` | **51"** = 41 + `EMBED` 10 | Rene midió la fascia y **ya cortó los postes a 51** |
| `EMBED` | **10"** | Lo que entra en la fascia. Medido en obra, no supuesto |
| `GAP_PANEL` | **0.0** | El riel de abajo va **cara de poste a cara de poste**, soldado. Sin holgura |
| `LUZ_MAX` | **3.75"** | La regla es que no pase bola de 4". Se deja 1/4 de margen |
| Guard | 42" = 2 piso + 1 riel + 38 campo + 1 cap | 42 es decisión de Rene; el código de Florida pide 36 mínimo residencial |

**Perfiles:** poste 2×2×.090 · cap y riel 2×1×.090 · piques y dibujo 1×1×1/16.

**Dibujo del balcón:** 17 piezas, cuadro de 30-1/4 exterior / 28-1/4 libre,
flotando 3-7/8 bajo el cap y sobre el riel. Los flancos absorben la diferencia de
ancho entre bahías.

### Reglas de geometría que Rene puso

- **Las medidas que él da son INTERIORES.** Los postes van por fuera de eso.
- **Paño entreverado**: uno con dibujo, uno liso, alternando.
- **Nunca dos paños con dibujo pegados.**
- **Esquinas y terminaciones van de piques**, lisas.
- **Paños de menos de 4 pies de luz libre** (la luz, no centro a centro).
- **Nada se ancla a la pared.**

### Las juntas del cap — `cap_tramo()`

Un solo sitio de donde salen el largo de corte y el dibujo:

- `EMPATE` → la junta va al **centro del poste**, −1 / +1
- `ESQUINA` y `PARED` → **a ras** con el paño
- `SOLDADA` → **inglete**, solo por el lado que arranca en paño

---

## 4. Estado de cada frente

### Railings de aluminio — EN PRODUCCIÓN

Cuatro balcones (dos Pool House, dos caballerizas) más cuatro barandas de escalera
del Pool House. 27 secciones en total.

- **Caballeriza 1** — 8 secciones, cerrada. `CABALLERIZA-1.pdf`
- **Caballeriza 2** — 7 secciones, cerrada (se agregó el paño S-1 de 105-1/4).
  `CABALLERIZA-2.pdf`
- **Balcón 1 y 2 Pool** — 6 secciones cada uno. `BALCON-1-POOL.pdf`, `BALCON-2-POOL.pdf`
- **Un paño solo:** `PANO-S-1.pdf` (para mandar al taller sin el set completo)
- **Lo que Rene dijo, textual:** `MEDIDAS-DE-RENE.pdf`

**Las escaleras:** las cuatro salen al mismo ángulo, **33.5°**. Un solo corte para
las cuatro. Funciona porque la baranda se arma a plomo y no se acumula nada
(verificación 13).

**Pool House Balcón 1 — RECTIFICADO el 2 de octubre.** Rene: *"en el primer dibujo
del balcón, esas son las medidas exactas"*. A = 383-5/8 interior + 2 postes = 387-5/8 ·
B = 161 − 2 de la pared = 159, sin poste en la esquina · C = 237-5/8 exacta, sin poste
en la esquina. Falta que confirme que el poste del empalme con la escalera lo lleva
el balcón (C-2), como está.

**Pool House Balcón 2 — RECTIFICADO el 2 de octubre.** D = 389-1/4 interior + 2 postes =
393-1/4 · E = 151-5/8 − 2 de la pared = 149-5/8, sin poste en la esquina, en 4 paños con
dibujo en la pared como la B (en 3 el liso pasaba de 4 pies) · F = 240-5/8 exacta (Rene
la corrigió; antes 239-3/4), sin poste en la esquina, con el poste del empalme.
**Escalera del Balcón 1: 185" a 34°** (Rene, 2 oct; antes 185-1/2). Rene pidió: *usar
las medidas que da AHORA, no recordarle las viejas.*

### Piso impermeable de los portalones del Pool House — EN INVESTIGACIÓN

El deck de 2×4 filtra agua al portal de abajo. Se arranca el 2×4 y se pone algo que
no deje pasar el agua, directo sobre las viguetas.

Cuatro opciones en la mesa. Hoja comparativa publicada:
**https://claude.ai/artifact/UVU69vVNDi5hfVMD6m5uAg**

| Opción | Sube | ¿La pone JRG? | Papeles |
|---|---|---|---|
| LockDry (aluminio, Nexan) | 1" | Sí | Intertek CCRR-0331 (carga, no agua) |
| Admiral SpaceMaker (PVC) | 1" | Sí | Nada verificado |
| Dec-K-ing (membrana PVC) | 0.78" | Sí | Nada encontrado |
| Dec-Tec CoolStep (membrana) | 0.78" | No, subcontrato | **FL 38019 + Intertek CCRR-0405** |

**Dec-Tec es la única con aprobación de Florida que la cubre como impermeabilización.**

**Cotizaciones pedidas por correo** (ya salieron, desde el Gmail de Rene):
- `sales@nexaninc.com` — LockDry
- `24hourhelp@admiral-spacemaker.com` — SpaceMaker

Se les pidió precio por pie cuadrado y lineal, flete a Jupiter, número FL, datos de
viento (160–170 mph), pendiente mínima, separación de viguetas, y la garantía por
escrito.

**Lo que va igual con cualquier opción:**
1. **Pendiente 1/8" por pie mínimo.** Ningún piso sellado funciona plano. Las cuñas
   van encima de las viguetas, antes del piso — gruesas contra la casa, finas en el
   borde. Después no se puede.
2. **El remate contra la pared** es donde filtran, no las tablas.
3. **Las viguetas tienen que estar secas.** Llevan años mojándose. Sellar sobre
   madera mojada levanta ampollas por vapor.
4. **Color claro**, no oscuro. El piso coge más de 160°F.
5. **El canal del agua choca con los postes de la baranda.** Los postes entran 10"
   en la fascia; en un 2×12 quedan 1-1/4" libres y no alcanza para colgar canal.
   Salida barata: tirar la pendiente hacia un costado con pocos postes.
6. **Orden:** arrancar el 2×4 → medir el rim y decidir para dónde bota el agua →
   cuñas y piso → canal → **y por último los postes a la fascia.**

### Puertas

3 slabs de acero 36×80 + astragal. Rene compró en Home Depot Jupiter (tienda #0274)
una **Masonite 6-Panel Impact Steel, 36×80, Left Hand Outswing**, SKU 1002357645,
rough opening 38-1/4 × 81-1/8, jamb 4-9/16, sin brickmold, HVHZ Impact, DP +50/−70,
aprobación FL22513.6. La etiqueta de aprobación viene **rasgada justo en el número
FL** — si el trabajo va permisado hay que bajar la aprobación de floridabuilding.org
e imprimirla.

### Carports

Tres techos: 24'×25' ($17,500), 16'×20' ($9,500), manure bin ($3,000) = $30,000.
Depósito de $12,000 cobrado. Ver `carports-invoice-deposit.html`.

### Siding de fibrocemento de la casita

Herramientas: Rene tiene taladros de batería y un multiuso, no tiene sierra ni
pulidora. La vía es tijera de fibrocemento para taladro (Malco TSF2 o PacTool SS724)
+ hoja de grano de carburo para el multiuso + cuchilla de rayar. **El polvo de
fibrocemento es sílice** — siempre afuera, N95 puesta, nunca con disco de
mampostería en seco.

---

## 5. Facturación

- **Contrato de railings: $40,000.** Depósito recibido $20,000. Se facturaron
  $7,000 más (`railing-invoice-progress.html`, JRG-2026-007-P1). Saldo $13,000.
- **⚠️ Hay un descuadre sin resolver:** el proposal JRG-2026-007 en el repo dice
  **$26,125**, pero el invoice factura contra un contrato de **$40,000**. Hay que
  preguntarle a Rene cuál manda y arreglar el proposal.

**Nunca poner costos de proveedor ni márgenes internos en documentos del cliente.**

---

## 6. Lo que está abierto

1. **¿Las 105-1/4 del paño S-1 incluyen los dos postes?** Se fabricó pelado (sin
   postes propios). Si el número ya los incluía, la pieza baja a **101-1/4**.
2. **Pool House:** los dos balcones ya están rectificados (2 oct).
3. **De qué lado del retorno Q-1 va el dibujo.** Se puso el paño liso contra la
   esquina de los platos de la fascia. Nunca lo confirmó.
4. **El hueco de escalera de 42" en caballeriza 1** salió del croquis, no de una
   cinta. Falta confirmarlo.
5. **Medidas del deck del Pool House:** pendiente actual (hueco de nivel de 4 pies
   en 3 sitios), alto del rim/fascia, largo y fondo de cada portalón, separación de
   viguetas (16" o 24"), y del piso al umbral de la puerta.
6. **El descuadre del proposal vs el invoice** (ver arriba).
7. **Placeholders amarillos** en los documentos del cliente: `[Last Name]`,
   `[Email]`, `[License #]`, `[Client Contact]`.
8. **Color de pintura:** Benjamin Moore publica #515D51 para el que escogió. No
   existe tabla oficial pintura→powder coating. El RAL más cercano es 7009 a dE 6.0
   (se ve distinto). La vía buena es el color-match gratis de Prismatic Powders con
   muestra gratis; si no, $49.95 de librería o $300 formulación nueva, mínimo 6 lb.

---

## 7. Links y contactos

**Artefactos publicados:**
- 3D para el cliente: https://claude.ai/artifact/NEpYwjiEQJ3nrC7WbJFT6T
- Piso impermeable: https://claude.ai/artifact/UVU69vVNDi5hfVMD6m5uAg

**Teléfonos:**
- Home Depot Jupiter #0274 — (561) 748-1412 — 1694 W Indiantown Rd
- Palm Beach County PZB, Building Division — (561) 233-5100
  (la propiedad es **condado no incorporado**, NO el pueblo de Jupiter)
- Nexan / LockDry — 888-739-6172
- Admiral SpaceMaker — 844-772-2362
- Florida Coast Contracting (Dec-Tec certificado, Palm Beach) — (561) 260-3126
- Acrylux Paint (distribuidor Gaco) — (954) 772-0300
- Pli-Dek — 800-364-0287
- Duradek US — 800-338-3568

---

## 8. Errores que ya se cometieron — no repetirlos

Esto es lo más útil de este archivo.

1. **La convención de interior/exterior.** Las medidas de Rene son interiores. Se
   asumió lo contrario y los dos frentes salieron 4" cortos. Él ya había impreso los
   planos. Hubo que rehacer las dos caballerizas.
2. **Flanco del dibujo a exactamente 4.000".** Se propusieron bahías de 47-3/4, él
   aprobó, y después se descubrió que el flanco caía en 4" justo — la bola pasa.
   **Verificar los flancos del dibujo, no solo los paños lisos.**
3. **`GAP_PANEL` a 1/4 por lado.** Dejaba el riel de abajo 1/2" corto en cada paño
   de todo el trabajo. Rene lo cachó midiendo: *"arriba está bien, abajo me faltan
   dos pulgadas."* Estaba escrito a mano en 6 sitios.
4. **Cap dibujado con un `+1` fijo.** Él lo circuló en rojo. De ahí salió
   `cap_tramo()` como fuente única.
5. **Después se pusieron TODOS los caps a ras.** También mal. Los empates van al
   centro del poste; el único a ras es el que choca por el lado.
6. **Postes a 47 en vez de 51.** El empotre de 6" era una suposición. Él lo midió:
   10". Estaba escrito a mano en 4 sitios.
7. **Se quitaron los rótulos de las piezas** cuando pidió menos texto, y entonces no
   encontraba "el de 104" ni "la L". De ahí salió el dict `ROTULOS` y la
   verificación 20.
8. **Cadenas de cotas que no cerraban**, y el "arreglo" inventó números sin
   significado. Él: *"pero las medidas están mal."*
9. **`:first-of-type` nunca hacía match** (cuenta el primer DIV hermano, y un
   `div.pb` va antes), dejando páginas de título huérfanas. Se cambió a hermano
   adyacente `.doc-header + .drawing`.
10. **Se le dio ida y vuelta a un número** (190-3/4 → 192-3/4 → 193) cuando el
    número estaba bien desde el principio y lo que estaba mal era la explicación.
    Él: *"tienes un para atrás y para adelante de tres pares repinga."*

**El patrón:** se generaban planos más rápido de lo que se verificaban. Verificar
primero, generar después.

---

## 9. Limitación del entorno

El contenedor tiene política de red que **bloquea** homedepot.com, floridabuilding.org,
los sitios de fabricantes, foros y prensa del oficio. Las búsquedas web sí funcionan
(devuelven el índice), pero **no se puede abrir una página directa**. Toda
información de esos sitios en este trabajo salió del índice de búsqueda, no de leer
el documento. Si el chat nuevo tiene control remoto a la computadora de Rene, **esa
es la vía para abrir esos PDFs y cerrar los huecos** marcados arriba.

El correo (Gmail) sí funciona y ya se usó para pedir las dos cotizaciones.
