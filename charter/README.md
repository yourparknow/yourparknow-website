# MAREA — Marketplace de charters de botes en Miami 🛥️

> Maqueta de presentación (concepto). El nombre **MAREA** es un placeholder y se puede cambiar.

Plataforma para rentar botes en Miami (estilo Boatsetter / GetMyBoat) pero con la
**comisión más baja del mercado: 10%**, frente al 20–35% que cobran los demás.

---

## 1. Estudio del mercado actual

Investigación de las plataformas que existen hoy:

| Plataforma | Comisión total | Notas |
|---|---|---|
| **Sailo** | **~35%** | Enfoque premium / yates de lujo. La más cara. |
| **Boatsetter** | **~28%** | Líder en EE. UU. Incluye seguro. Depósito **cobrado** 48 h antes. |
| **GetMyBoat** | **~20%** | ~7% al dueño + 5–15% al cliente. 130k+ botes, 184 países. NO da seguro. |
| **Click&Boat** | variable | Fuerte en Europa / Mediterráneo. |
| **MAREA (nosotros)** | **10%** | El dueño recibe 90%. Mejores precios para el cliente. |

**Cómo cobran y operan (lo que copiamos bien y mejoramos):**
- **Depósito de seguridad:** Boatsetter retiene un mínimo de **$500** en la tarjeta del
  cliente, lo toma 48 h antes y lo libera 48–72 h después si no hay daños. → Nosotros lo
  hacemos **retenido (hold), no cobrado**, y lo liberamos en 48–72 h. Más confianza.
- **Documentos / Ley SB-606 (Florida):** ID con foto, tarjeta de **Boater Safety**
  (obligatoria para nacidos después de 1988), y seguro de alquiler. → Lo hacemos
  **100% digital** dentro del checkout.
- **Precios reales en Miami:** pontones desde ~$65/h; lanchas $200–$1,200/día; yates
  con capitán $1,700 (4 h) a $4,500 (día completo).

**Fuentes:** Boatsetter (fees, security deposit), GetMyBoat (commission, Miami regs),
Sailo (pricing 2026), boat-alert / sharetribe comparativas, Florida SB-606.

---

## 2. Nuestra propuesta de valor

1. **10% de comisión** — la mitad o menos que la competencia.
2. **El dueño se queda con el 90%** y cobra en **24–48 h** (Stripe).
3. **Depósito protegido** (retenido, no cobrado).
4. **Documentos digitales** y verificación de identidad integrada.
5. **Soporte local de Miami** y seguro de daños/responsabilidad incluido.

---

## 3. Las maquetas (carpeta `mockups/`)

| # | Pantalla | Qué muestra |
|---|---|---|
| 1 | `01-home.png` | Portada: buscador, "10% vs 35%", botes destacados, cómo funciona, tabla comparativa, CTA para dueños. |
| 2 | `02-explore.png` | Resultados con filtros (tipo, precio, capacidad, capitán, comodidades) y rejilla de botes. |
| 3 | `03-boat.png` | Detalle del bote: galería, specs, qué incluye, capitán, reseñas y **widget de reserva**. |
| 4 | `04-checkout.png` | **Pago**: documentos requeridos, Apple Pay / tarjeta, **depósito** y resumen. |
| 5 | `05-host.png` | "Pon tu bote, gana 90%": calculadora de ganancias y comparativa de pagos. |

Las imágenes son ilustrativas (botes, fotos y datos imaginarios) para presentación.
Se generan con los scripts de `mockups/generator/` (Python + cairosvg).

---

## 4. Cómo se construiría (siguiente fase)

- **Frontend:** Next.js / React + el sistema de diseño de `styles.css`.
- **Pagos:** **Stripe Connect** (destination charges) → cobro al cliente, comisión 10%
  automática (`application_fee`), pago directo al dueño, y **depósito como pre-autorización**
  (hold) que se libera o captura según haya daños.
- **Verificación:** Stripe Identity para ID + carga de Boater Safety card.
- **Cumplimiento:** Florida SB-606 (seguro de alquiler, licencia).

> `styles.css` incluye el sistema de diseño base (paleta océano + atardecer de Miami)
> listo para empezar el desarrollo real.
