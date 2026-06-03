"""
Arbol de levas - Motor diesel 6 cilindros en linea
Dibujo esquematico + simulacion de cargas AXIALES

Fuentes de carga axial sobre el arbol de levas:
  1) Empuje del engranaje helicoidal de accionamiento  -> Fa_gear = Ft * tan(beta)
  2) Componente axial por friccion leva-seguidor        -> oscila con el angulo
  3) Empuje de la excentrica de la bomba de inyeccion
  4) Dilatacion termica restringida (carga sobre cojinete de empuje)

Salida: PNG con 4 sub-figuras.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, FancyArrow

# ----------------------------------------------------------------------
# 1. PARAMETROS DEL MOTOR / ARBOL
# ----------------------------------------------------------------------
N_CYL        = 6
FIRING_ORDER = [1, 5, 3, 6, 2, 4]
rpm_engine   = 2200.0                 # rpm ciguenal
rpm_cam      = rpm_engine / 2.0       # arbol gira a la mitad
omega_cam    = rpm_cam * 2*np.pi/60   # rad/s

# Engranaje helicoidal de mando
m_n     = 3.0                         # modulo normal [mm]
z_gear  = 38                          # n. dientes
beta    = np.deg2rad(20.0)            # angulo de helice
phi_n   = np.deg2rad(20.0)            # angulo de presion normal
d_pitch = m_n * z_gear / np.cos(beta) # diametro primitivo [mm]
P_kW    = 7.5                         # potencia absorbida por la distribucion [kW]

# Par y fuerzas en el engranaje
T_cam   = P_kW*1000 / omega_cam       # par [N.m]
Ft      = 2.0 * T_cam / (d_pitch/1000)        # fuerza tangencial [N]
Fa_gear = Ft * np.tan(beta)                    # EMPUJE AXIAL del helicoidal [N]
Fr_gear = Ft * np.tan(phi_n)/np.cos(beta)      # fuerza radial [N]

# Leva / seguidor
lift      = 8.5e-3                     # alzada [m]
F_valve   = 950.0                      # fuerza max muelle+gas sobre la valvula [N]
mu        = 0.08                       # coef. friccion leva-seguidor
ramp_ang  = np.deg2rad(7.0)            # angulo de rampa (genera comp. axial)

# Excentrica bomba inyeccion
F_pump    = 1800.0                     # fuerza radial pico de la bomba [N]
mu_pump   = 0.06

# Dilatacion termica
L         = 0.850                      # longitud entre apoyos de empuje [m]
alpha     = 12e-6                      # acero [1/K]
dT        = 70.0                       # incremento temperatura [K]
E         = 210e9                      # modulo elastico [Pa]
A_sec     = np.pi/4*(0.040**2)         # seccion del cuerpo Ø40 [m2]
k_axial   = 0.001                      # fraccion de dilatacion realmente restringida
                                       # (un extremo del arbol flota -> casi libre)

# ----------------------------------------------------------------------
# 2. SIMULACION vs ANGULO DEL ARBOL (0..360 grados arbol = ciclo completo)
# ----------------------------------------------------------------------
theta = np.linspace(0, 360, 1441)          # grados arbol de levas
thr   = np.deg2rad(theta)

# --- Perfil de alzada por leva (admision+escape de los 6 cilindros) ---
def lobe_profile(th, center_deg, dur_deg=120.0):
    """Alzada normalizada 0..1 tipo coseno levantado, centrada en 'center_deg'."""
    c   = np.deg2rad(center_deg)
    half= np.deg2rad(dur_deg/2.0)
    d   = (th - c + np.pi) % (2*np.pi) - np.pi
    out = np.where(np.abs(d) < half, 0.5*(1+np.cos(np.pi*d/half)), 0.0)
    return out

# Centros de leva segun orden de encendido (sep. 60 grados arbol)
centers = {cyl: 60.0*i for i, cyl in enumerate(FIRING_ORDER)}

# Carga normal total leva-seguidor (suma de los cilindros activos)
F_normal = np.zeros_like(theta)
for cyl, c0 in centers.items():
    s = lobe_profile(thr, c0)
    F_normal += F_valve * s            # cada leva aporta su fuerza cuando esta activa

# Componente AXIAL por rampa + friccion en flanco
# (la rampa tangencial induce una pequena componente a lo largo del eje)
Fa_cam = mu * F_normal * np.cos(ramp_ang) + F_normal * np.sin(ramp_ang)*0.04

# Excentrica bomba (un evento por vuelta de arbol)
s_pump = lobe_profile(thr, 30.0, dur_deg=80.0)
Fa_pump = mu_pump * F_pump * s_pump

# Empuje del engranaje (constante mientras transmite par)
Fa_gear_arr = np.full_like(theta, Fa_gear)

# Dilatacion termica (constante en regimen) - reaccion en cojinete de empuje
F_thermal = k_axial * E * A_sec * alpha * dT
F_thermal_arr = np.full_like(theta, F_thermal)

# CARGA AXIAL TOTAL sobre el cojinete de empuje
Fa_total = Fa_gear_arr + Fa_cam + Fa_pump + F_thermal_arr

# ----------------------------------------------------------------------
# 3. DISTRIBUCION DE CARGA AXIAL ACUMULADA A LO LARGO DEL EJE (estatica)
# ----------------------------------------------------------------------
# Posiciones axiales (mm) de cada elemento a lo largo del arbol
x_axis   = np.array([0, 120, 240, 360, 480, 600, 720, 850])  # apoyos
# Fuerza axial pico de cada leva (admision/escape) actuando en su posicion
lobe_x   = np.linspace(60, 790, N_CYL)                        # centros de cilindro
lobe_Fa  = np.full(N_CYL, mu*F_valve)                         # comp axial pico/leva
# Diagrama de fuerza axial interna acumulada (de cola -> engranaje frontal)
xs = np.concatenate(([0], lobe_x, [850]))
internal = [Fa_gear]            # arranca con el empuje del engranaje frontal
acc = Fa_gear
for fx in lobe_Fa:
    acc += fx
    internal.append(acc)
internal.append(acc + F_thermal + mu_pump*F_pump)
internal = np.array(internal)

# ----------------------------------------------------------------------
# 4. FIGURA
# ----------------------------------------------------------------------
fig = plt.figure(figsize=(15, 11))
fig.suptitle("Arbol de levas L6 Diesel  -  Dibujo y simulacion de CARGAS AXIALES",
             fontsize=15, fontweight="bold")

# ---- (A) DIBUJO ESQUEMATICO DEL ARBOL ----
axA = plt.subplot2grid((3, 2), (0, 0), colspan=2)
axA.set_title("(A) Dibujo esquematico  -  arbol, levas, apoyos y cojinete de empuje")
# cuerpo del eje
axA.add_patch(Rectangle((0, -0.5), 850, 1.0, color="#9aa7b5", ec="k"))
# apoyos (7)
for i, xp in enumerate(x_axis[:-1] if False else [0,120,240,360,480,600,720]):
    axA.add_patch(Rectangle((xp-8, -1.4), 16, 2.8, color="#5b6b7b", ec="k"))
    axA.text(xp, 1.8, f"A{i+1}", ha="center", fontsize=8)
# levas (par por cilindro)
for i, xc in enumerate(lobe_x):
    cyl = [c for c,v in centers.items()][i]
    for dx, col in [(-22, "#e07b39"), (22, "#3a7d44")]:   # adm / esc
        axA.add_patch(Circle((xc+dx, 0), 9, color=col, ec="k"))
    axA.text(xc, -2.4, f"Cil {i+1}", ha="center", fontsize=8)
# engranaje helicoidal frontal
axA.add_patch(Circle((850+25, 0), 22, color="#c0392b", ec="k"))
axA.text(875, 2.6, "Engr.\nhelic.", ha="center", fontsize=8)
# cojinete de empuje (thrust) en cola
axA.add_patch(Rectangle((-18, -2.0), 10, 4.0, color="#2c3e50", ec="k"))
axA.text(-13, 3.0, "Cojinete\nempuje", ha="center", fontsize=8)
# flecha de carga axial
axA.add_patch(FancyArrow(820, 0, 60, 0, width=0.5, head_width=2.5,
                         head_length=18, color="red", length_includes_head=True))
axA.text(720, -3.6, "Fa (empuje axial del engranaje helicoidal) -->",
         color="red", fontsize=9)
axA.add_patch(FancyArrow(20, 0, -50, 0, width=0.5, head_width=2.5,
                         head_length=15, color="darkred", length_includes_head=True))
axA.set_xlim(-60, 920); axA.set_ylim(-5, 5)
axA.set_xlabel("Posicion axial [mm]"); axA.set_yticks([])
axA.legend(handles=[
    plt.Line2D([0],[0], marker='o', color='w', markerfacecolor='#e07b39', label='Leva admision', markersize=9),
    plt.Line2D([0],[0], marker='o', color='w', markerfacecolor='#3a7d44', label='Leva escape', markersize=9),
    plt.Line2D([0],[0], marker='s', color='w', markerfacecolor='#5b6b7b', label='Apoyo', markersize=9),
], loc="upper center", ncol=3, fontsize=8)

# ---- (B) CARGA AXIAL vs ANGULO DEL ARBOL ----
axB = plt.subplot2grid((3, 2), (1, 0))
axB.set_title("(B) Carga axial en cojinete de empuje vs angulo")
axB.plot(theta, Fa_total, "b-", lw=1.8, label="Fa total")
axB.plot(theta, Fa_gear_arr, "r--", lw=1, label="Engranaje helicoidal")
axB.plot(theta, F_thermal_arr, "g--", lw=1, label="Termica")
axB.plot(theta, Fa_cam, "m-", lw=0.8, label="Leva+friccion")
axB.axhline(Fa_total.mean(), color="k", ls=":", lw=0.8)
axB.set_xlabel("Angulo arbol [grados]"); axB.set_ylabel("Fuerza axial [N]")
axB.set_xlim(0, 360); axB.grid(alpha=0.3); axB.legend(fontsize=7, ncol=2)

# ---- (C) DIAGRAMA DE FUERZA AXIAL INTERNA A LO LARGO DEL EJE ----
axC = plt.subplot2grid((3, 2), (1, 1))
axC.set_title("(C) Fuerza axial interna acumulada a lo largo del eje")
axC.step(xs, internal, where="post", color="#c0392b", lw=2)
axC.fill_between(xs, internal, step="post", alpha=0.2, color="#c0392b")
for i, xc in enumerate(lobe_x):
    axC.axvline(xc, color="gray", ls=":", lw=0.6)
axC.set_xlabel("Posicion axial [mm]"); axC.set_ylabel("N(x) axial [N]")
axC.grid(alpha=0.3)

# ---- (D) DISTRIBUCION POR CONTRIBUCION + ESFUERZO ----
axD = plt.subplot2grid((3, 2), (2, 0))
axD.set_title("(D) Contribucion de cada fuente al empuje axial (pico)")
labels = ["Engranaje\nhelic.", "Levas+\nfriccion", "Bomba\nineccion", "Termica"]
vals   = [Fa_gear, Fa_cam.max(), (mu_pump*F_pump), F_thermal]
bars = axD.bar(labels, vals, color=["#c0392b", "#8e44ad", "#e07b39", "#27ae60"])
axD.bar_label(bars, fmt="%.0f N", fontsize=8)
axD.set_ylabel("Fuerza axial [N]"); axD.grid(alpha=0.3, axis="y")

# ---- (E) ESFUERZO AXIAL Y FACTOR DE SEGURIDAD ----
axE = plt.subplot2grid((3, 2), (2, 1))
axE.set_title("(E) Esfuerzo axial y verificacion del cojinete")
sigma = Fa_total / A_sec / 1e6                 # MPa
axE.plot(theta, sigma, "navy", lw=1.5)
axE.set_xlabel("Angulo arbol [grados]"); axE.set_ylabel("Esfuerzo axial [MPa]")
axE.set_xlim(0, 360); axE.grid(alpha=0.3)
Sy = 420.0                                      # limite elastico [MPa]
axE.text(0.02, 0.92, f"sigma_max = {sigma.max():.2f} MPa\nSy = {Sy:.0f} MPa\n"
         f"FS = {Sy/sigma.max():.0f}",
         transform=axE.transAxes, fontsize=8, va="top",
         bbox=dict(boxstyle="round", fc="lightyellow"))

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig("camshaft_axial_loads.png", dpi=140, bbox_inches="tight")
print("Figura guardada: camshaft_axial_loads.png")

# ----------------------------------------------------------------------
# 5. RESUMEN NUMERICO
# ----------------------------------------------------------------------
print("\n===== RESULTADOS SIMULACION CARGAS AXIALES =====")
print(f"Par en arbol de levas ........ T  = {T_cam:7.2f} N.m")
print(f"Diametro primitivo engranaje . d  = {d_pitch:7.2f} mm")
print(f"Fuerza tangencial ............ Ft = {Ft:7.1f} N")
print(f"EMPUJE AXIAL engranaje ....... Fa = {Fa_gear:7.1f} N")
print(f"Comp. axial leva (pico) ...... Fa = {Fa_cam.max():7.1f} N")
print(f"Empuje bomba inyeccion ....... Fa = {mu_pump*F_pump:7.1f} N")
print(f"Carga axial termica .......... Fa = {F_thermal:7.1f} N")
print(f"---------------------------------------------")
print(f"CARGA AXIAL TOTAL (pico) ..... Fa = {Fa_total.max():7.1f} N")
print(f"CARGA AXIAL TOTAL (media) .... Fa = {Fa_total.mean():7.1f} N")
print(f"Esfuerzo axial maximo ........ s  = {sigma.max():7.2f} MPa")
print(f"Factor de seguridad cojinete . FS = {Sy/sigma.max():7.1f}")
