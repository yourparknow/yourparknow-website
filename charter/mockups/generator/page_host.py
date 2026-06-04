# -*- coding: utf-8 -*-
from lib import *
from comp import *

c=C(2900)

# ---------- HERO ----------
hh=560
hg=c.grad([("0",PINK),("0.5",SUNSET),("1",GOLD)])
c.rect(0,0,W,hh,hg)
c.circle(W*0.9,-30,240,"#fff",op=0.12); c.circle(80,hh+30,240,NAVY,op=0.12)
header(c,dark=True,active="host")
LX=M
c.text(LX,180,"Tu bote trabaja para ti.",size=56,weight="bold",fill="#fff")
c.text(LX,250,"Quédate con el 90%.",size=56,weight="bold",fill="#fff")
c.text(LX,300,"La comisión más baja de Miami: solo 10%. Tú pones el precio,",size=19,fill="#fff",op=0.95)
c.text(LX,328,"las fechas y las reglas. Nosotros traemos clientes, pagos y seguro.",size=19,fill="#fff",op=0.95)
c.rect(LX,366,230,54,"#fff",rx=27); c.text(LX+115,366+34,"Publicar mi bote",size=16,weight="bold",fill=CORAL,anchor="middle")
c.rect(LX+250,366,210,54,"none",rx=27,stroke="#fff",sw=2); c.text(LX+250+105,366+34,"Cómo funciona",size=15.5,weight="bold",fill="#fff",anchor="middle")
# stat chips
stx=LX
for v,k in [("$0","para publicar"),("24–48 h","para cobrar"),("10%","comisión")]:
    c.text(stx,470,v,size=30,weight="bold",fill="#fff")
    c.text(stx,498,k,size=14,fill="#fff",op=0.9)
    stx+=200
# earnings card (right)
ecx=W-M-360; ecy=150
c.rect(ecx,ecy,360,300,"#fff",rx=22,shadow=True)
c.text(ecx+28,ecy+44,"Tus ganancias estimadas",size=14,weight="bold",fill=SLATE)
c.text(ecx+28,ecy+96,"$39,600",size=46,weight="bold",fill=INK)
c.text(ecx+28,ecy+124,"al mes  ·  yate 50 ft · 20 días",size=13.5,fill=SLATE)
c.line(ecx+28,ecy+146,ecx+332,ecy+146,LINE,1.2)
rows=[("Ingresos brutos","$44,000"),("Comisión MAREA (10%)","–$4,400"),("Recibes tú","$39,600")]
yy=ecy+180
for i,(k,v) in enumerate(rows):
    bold = i==2
    c.text(ecx+28,yy,k,size=14,weight=("bold" if bold else "normal"),fill=(INK if bold else SLATE))
    c.text(ecx+332,yy,v,size=15 if bold else 14,weight="bold",fill=(GREEN if bold else INK),anchor="end")
    yy+=34
c.rect(ecx+28,yy+2,304,40,AQUASOFT,rx=10)
c.text(ecx+28+152,yy+27,"+$7,920/mes vs. Boatsetter",size=13.5,weight="bold",fill="#075e6b",anchor="middle")

# ---------- CALCULADORA / COMPARATIVA ----------
y=hh+70
section_head(c,y,"Compara tu pago","Con MAREA recibes mucho más por el mismo viaje",
             "Mismo bote, mismas 20 noches al mes. Mira cuánto te queda con cada plataforma.")
by=y+150
plats=[("MAREA","10%",39600,0.90,True),("GetMyBoat","20%",35200,0.80,False),
       ("Boatsetter","28%",31680,0.72,False),("Sailo","35%",28600,0.65,False)]
barx=M+260; barmax=CW-260-160
for i,(nm,com,amt,frac,ours) in enumerate(plats):
    ry=by+i*72
    c.text(M,ry+22,nm,size=17,weight="bold",fill=(OCEAN if ours else INK))
    c.text(M,ry+44,f"comisión {com}",size=12.5,fill=SLATE)
    c.rect(barx,ry+6,barmax,40,CLOUD,rx=12)
    bw=barmax*frac
    fill = c.grad([("0",AQUA),("1",TEAL)]) if ours else c.grad([("0","#9fb6c4"),("1","#7d97a8")])
    c.rect(barx,ry+6,bw,40,fill,rx=12)
    c.text(barx+bw-16,ry+32,f"${amt:,}",size=16,weight="bold",fill=("#04222f" if ours else "#fff"),anchor="end")
    if ours:
        c.rect(barx+bw+12,ry+10,118,32,NAVY,rx=16); c.text(barx+bw+12+59,ry+31,"+$7,920 ▲",size=12.5,weight="bold",fill=AQUA,anchor="middle")
after_bars=by+4*72+10

# ---------- POR QUÉ MAREA ----------
y=after_bars+70
section_head(c,y,"Ventajas para dueños","Todo lo que necesitas para rentar sin estrés")
fy=y+130
feats=[("Comisión de solo 10%","La más baja del mercado. Más ganancia en cada salida.",ic_card),
       ("Pagos en 24–48 h","Cobra rápido y directo a tu banco vía Stripe.",ic_bolt),
       ("Seguro y depósito","Cobertura de daños y depósito retenido en cada viaje.",ic_shield),
       ("Tú tienes el control","Tu precio, tu calendario, tus reglas. Apruebas cada reserva.",ic_lock)]
fw=(CW-3*24)/4
for i,(t,d,ic) in enumerate(feats):
    x=M+i*(fw+24)
    c.rect(x,fy,fw,210,"#fff",rx=20,shadow=True); c.rect(x,fy,fw,210,"none",rx=20,stroke=LINE,sw=1.4)
    c.rect(x+24,fy+24,52,52,AQUASOFT,rx=14); ic(c,x+24+26,fy+24+26,11,OCEAN)
    c.text(x+24,fy+106,t,size=16.5,weight="bold",fill=INK)
    ww=d.split(); ln=""; ly=fy+134
    for wd in ww:
        if len(ln)+len(wd)>26: c.text(x+24,ly,ln,size=13,fill=SLATE); ly+=20; ln=wd
        else: ln=(ln+" "+wd).strip()
    c.text(x+24,ly,ln,size=13,fill=SLATE)
after_feats=fy+210

# ---------- PUBLICA EN 4 PASOS ----------
y=after_feats+70
section_head(c,y,"Empieza hoy","Publica tu bote en 4 pasos")
sy=y+130
steps=[("1","Crea tu anuncio","Sube fotos, describe tu bote y fija tu precio. Gratis."),
       ("2","Verifícate","Subimos tu documentación y registro del bote una sola vez."),
       ("3","Recibe reservas","Apruebas solicitudes y chateas con los clientes en la app."),
       ("4","Cobra","El pago llega a tu banco 24–48 h después de cada viaje.")]
sw_=(CW-3*24)/4
for i,(n,t,d) in enumerate(steps):
    x=M+i*(sw_+24)
    c.rect(x,sy,sw_,176,CLOUD,rx=18); c.rect(x,sy,sw_,176,"none",rx=18,stroke=LINE,sw=1.2)
    c.rect(x+24,sy+22,46,46,c.grad([("0",AQUA),("1",TEAL)]),rx=13); c.text(x+24+23,sy+53,n,size=22,weight="bold",fill="#04222f",anchor="middle")
    c.text(x+24,sy+98,t,size=16,weight="bold",fill=INK)
    ww=d.split(); ln=""; ly=sy+124
    for wd in ww:
        if len(ln)+len(wd)>27: c.text(x+24,ly,ln,size=12.5,fill=SLATE); ly+=19; ln=wd
        else: ln=(ln+" "+wd).strip()
    c.text(x+24,ly,ln,size=12.5,fill=SLATE)
after_steps=sy+176

# ---------- TESTIMONIO ----------
y=after_steps+60
c.rect(M,y,CW,180,NAVY,rx=24)
c.circle(M+90,y+90,44,c.grad([("0",PINK),("1",SUNSET)])); c.text(M+90,y+99,"RG",size=26,weight="bold",fill="#fff",anchor="middle")
c.glyph(M+170,y+58,"★★★★★",18,GOLD)
c.text(M+170,y+98,"“Cambié de Boatsetter a MAREA y gano casi $8 mil más al mes por el mismo",size=18,fill="#eaf4f9")
c.text(M+170,y+126,"bote. Los pagos llegan rapidísimo y el soporte es local.”",size=18,fill="#eaf4f9")
c.text(M+170,y+158,"— Roberto G., dueño de yate · Miami Beach",size=13.5,weight="bold",fill=AQUA)
after_test=y+180

# ---------- CTA FINAL ----------
y=after_test+60
c.rect(M,y,CW,200,c.grad([("0",AQUA),("1",TEAL)]),rx=24)
c.text(W/2,y+78,"Convierte tu bote en ingresos.",size=34,weight="bold",fill="#04222f",anchor="middle")
c.text(W/2,y+114,"Publicar es gratis y toma menos de 10 minutos.",size=17,fill="#063a44",anchor="middle")
c.rect(W/2-130,y+138,260,52,NAVY,rx=26); c.text(W/2,y+170,"Publicar mi bote ahora",size=16,weight="bold",fill="#fff",anchor="middle")
after_cta=y+200

footer(c,after_cta+70)
c.h=after_cta+70+300
c.render("/tmp/render/out/05-host.png",scale=2)
print("host OK",c.h)
