# -*- coding: utf-8 -*-
from lib import *
from comp import *

c=C(2600)
header(c,active="explorar")

# breadcrumb
c.text(M,110,"Inicio  ›  Miami, FL  ›  Yates  ›  Sea Breeze",size=13,fill=SLATE)
# título
c.text(M,150,"Sea Breeze — Yate de lujo de 52 ft",size=31,weight="bold",fill=INK)
c.glyph(M,182,"★",15,STAR); c.text(M+20,184,"4.97",size=14.5,weight="bold",fill=INK)
c.text(M+62,184,"· 128 reseñas  ·  ",size=14,fill=SLATE)
ic_pin(c,M+185,178,7,SLATE); c.text(M+198,184,"Miami Beach Marina, FL",size=14,fill=SLATE)
c.text(M+420,184,"·  Superhost ✓",size=14,weight="bold",fill=OCEAN)
# acciones
c.text(M+CW-200,150,"↗ Compartir",size=14,weight="bold",fill=INK)
c.glyph(M+CW-90,150,"♥",15,CORAL); c.text(M+CW-70,150,"Guardar",size=14,weight="bold",fill=INK)

# ---- galería ----
gy=206; gh=420; mainw=720; gap=12
cidm=c.clip_rect(M,gy,mainw,gh,18)
boat_scene(c,M,gy,mainw,gh,"yacht","sunset",clip=cidm)
rx=M+mainw+gap; rw=CW-mainw-gap; sw=(rw-gap)/2; shh=(gh-gap)/2
skies=["day","golden","dusk","blue"]
for i,sk in enumerate(skies):
    col=i%2; row=i//2
    xx=rx+col*(sw+gap); yy=gy+row*(shh+gap)
    cid=c.clip_rect(xx,yy,sw,shh,14)
    boat_scene(c,xx,yy,sw,shh,"yacht",sk,clip=cid)
# botón "ver fotos"
c.rect(M+mainw-180,gy+gh-50,164,36,"#ffffffEE",rx=18)
c.text(M+mainw-98,gy+gh-26,"⊞  Ver 24 fotos",size=13,weight="bold",fill=NAVY,anchor="middle")

# ================= CONTENIDO =================
LX=M; LW=800; RX=M+LW+40; RW=CW-LW-40
y=gy+gh+46

# encabezado del host
c.text(LX,y,"Yate entero alojado por Carlos M.",size=22,weight="bold",fill=INK)
c.text(LX,y+28,"12 invitados · 3 camarotes · 2 baños · capitán profesional incluido",size=15,fill=SLATE)
c.circle(LX+LW-32,y-4,28,c.grad([("0",PINK),("1",SUNSET)]))
c.text(LX+LW-32,y+4,"CM",size=18,weight="bold",fill="#fff",anchor="middle")
y+=58
# specs
specs=[("Eslora","52 ft",ic_ruler),("Capacidad","12 pers.",ic_users),("Año","2023",ic_cal),
       ("Motores","2× Volvo",ic_engine),("Camarotes","3",None),("Velocidad","28 kn",ic_bolt)]
sw2=(LW-5*12)/6
for i,(k,v,ic) in enumerate(specs):
    xx=LX+i*(sw2+12)
    c.rect(xx,y,sw2,84,CLOUD,rx=14); c.rect(xx,y,sw2,84,"none",rx=14,stroke=LINE,sw=1.2)
    if ic: ic(c,xx+sw2/2,y+26,9,OCEAN)
    c.text(xx+sw2/2,y+58,v,size=15,weight="bold",fill=INK,anchor="middle")
    c.text(xx+sw2/2,y+76,k,size=11,fill=SLATE,anchor="middle")
y+=84+34
c.line(LX,y,LX+LW,y,LINE,1.2); y+=34

# descripción
c.text(LX,y,"Sobre este bote",size=21,weight="bold",fill=INK); y+=34
desc=("Vive Miami desde el agua a bordo del Sea Breeze, un yate de 52 pies perfecto para celebrar, "
      "nadar en Sandbar o ver el atardecer en la bahía. Cuenta con amplia cubierta de sol, sistema "
      "de sonido JBL, nevera, baño interior y plataforma de baño. Capitán profesional y combustible "
      "para 4 horas incluidos. Snorkel y paddleboard disponibles sin costo.")
words=desc.split(); line="";
for wd in words:
    if len(line)+len(wd)>92:
        c.text(LX,y,line,size=15,fill="#33414e"); y+=25; line=wd
    else: line=(line+" "+wd).strip()
c.text(LX,y,line,size=15,fill="#33414e"); y+=25
y+=24; c.line(LX,y,LX+LW,y,LINE,1.2); y+=34

# qué incluye
c.text(LX,y,"Qué incluye",size=21,weight="bold",fill=INK); y+=34
amen=["Capitán profesional","Combustible (4 h)","Sistema de sonido JBL","Nevera y hielera",
      "Equipo de snorkel","Paddleboard","Baño interior","Plataforma de baño",
      "Toallas y cojines","Wifi a bordo","Sombra / bimini","Hielera con bebidas"]
colw=LW/2
for i,a in enumerate(amen):
    col=i%2; row=i//2
    xx=LX+col*colw; yy=y+row*34
    c.glyph(xx,yy+4,"✓",15,GREEN); c.text(xx+24,yy+5,a,size=14.5,fill="#33414e")
y+=6*34+22; c.line(LX,y,LX+LW,y,LINE,1.2); y+=34

# capitán
c.text(LX,y,"Tu capitán",size=21,weight="bold",fill=INK); y+=20
c.rect(LX,y,LW,108,CLOUD,rx=16); c.rect(LX,y,LW,108,"none",rx=16,stroke=LINE,sw=1.2)
c.circle(LX+50,y+54,32,c.grad([("0",OCEAN),("1",TEAL)])); c.text(LX+50,y+62,"AR",size=22,weight="bold",fill="#fff",anchor="middle")
c.text(LX+100,y+40,"Capitán Andrés R.",size=17,weight="bold",fill=INK)
c.glyph(LX+100,y+66,"★",13,STAR); c.text(LX+118,y+67,"4.98 · 240 viajes · USCG licenciado",size=14,fill=SLATE)
c.text(LX+100,y+90,"Bilingüe (ES/EN) · 9 años navegando la bahía de Biscayne",size=13.5,fill=SLATE)
c.rect(LX+LW-150,y+38,130,36,"#fff",rx=18,stroke=TEAL,sw=1.6); c.text(LX+LW-85,y+62,"Ver perfil",size=13.5,weight="bold",fill=OCEAN,anchor="middle")
y+=108+34; c.line(LX,y,LX+LW,y,LINE,1.2); y+=34

# reseñas
c.glyph(LX,y,"★",20,STAR); c.text(LX+28,y+2,"4.97 · 128 reseñas",size=21,weight="bold",fill=INK); y+=30
revs=[("Jessica P.","Mayo 2026","Día perfecto. El capitán Andrés conoce los mejores spots y el yate impecable. ¡Reservaremos otra vez!","JP"),
      ("Michael T.","Abril 2026","Celebré mi cumpleaños aquí. Sonido increíble, súper limpio y el proceso de reserva facilísimo.","MT"),
      ("Laura G.","Abril 2026","Mejor precio que encontré en Miami y sin cargos ocultos. El depósito se devolvió en 2 días.","LG"),
      ("David R.","Marzo 2026","Snorkel en el sandbar espectacular. Todo incluido tal cual la descripción. 10/10.","DR")]
rcw=(LW-24)/2
for i,(nm,dt,tx,ini) in enumerate(revs):
    col=i%2; row=i//2
    xx=LX+col*(rcw+24); yy=y+row*150
    c.rect(xx,yy,rcw,134,"#fff",rx=16,stroke=LINE,sw=1.4)
    c.circle(xx+28,yy+34,18,c.grad([("0",AQUA),("1",TEAL)])); c.text(xx+28,yy+40,ini,size=14,weight="bold",fill="#04222f",anchor="middle")
    c.text(xx+56,yy+30,nm,size=14.5,weight="bold",fill=INK)
    c.text(xx+56,yy+50,dt,size=12.5,fill=SLATE)
    c.glyph(xx+rcw-90,yy+30,"★★★★★",12,STAR)
    # wrap review
    ww=tx.split(); ln=""; ly=yy+78
    for wd in ww:
        if len(ln)+len(wd)>46: c.text(xx+20,ly,ln,size=13,fill="#33414e"); ly+=20; ln=wd
        else: ln=(ln+" "+wd).strip()
    c.text(xx+20,ly,ln,size=13,fill="#33414e")
y+=2*150+10
c.rect(LX,y,200,44,"#fff",rx=22,stroke=LINE,sw=1.6); c.text(LX+100,y+28,"Ver 128 reseñas",size=14,weight="bold",fill=INK,anchor="middle")
left_bottom=y+44

# ================= BOOKING WIDGET =================
bx=RX; bw=RW; byy=gy+gh+46
c.rect(bx,byy,bw,560,WHITE,rx=20,shadow=True)
c.rect(bx,byy,bw,560,"none",rx=20,stroke=LINE,sw=1.5)
ipx=bx+24; iw=bw-48
c.text(ipx,byy+44,"$2,200",size=30,weight="bold",fill=INK)
c.text(ipx+118,byy+44,"/ día",size=15,fill=SLATE)
c.glyph(bx+bw-96,byy+44,"★",14,STAR); c.text(bx+bw-78,byy+44,"4.97",size=14,weight="bold",fill=INK)
c.text(bx+bw-24,byy+44,"(128)",size=12.5,fill=SLATE,anchor="end")
# date/guests box
fb=byy+66
c.rect(ipx,fb,iw,108,"#fff",rx=14,stroke=LINE,sw=1.6)
c.line(ipx+iw/2,fb,ipx+iw/2,fb+54,LINE,1.4); c.line(ipx,fb+54,ipx+iw,fb+54,LINE,1.4)
c.text(ipx+14,fb+22,"LLEGADA",size=10,weight="bold",fill=SLATE,ls="0.5"); c.text(ipx+14,fb+44,"sáb 14 jun · 9:00",size=13.5,weight="bold",fill=INK)
c.text(ipx+iw/2+14,fb+22,"REGRESO",size=10,weight="bold",fill=SLATE,ls="0.5"); c.text(ipx+iw/2+14,fb+44,"sáb 14 jun · 17:00",size=13.5,weight="bold",fill=INK)
c.text(ipx+14,fb+76,"INVITADOS",size=10,weight="bold",fill=SLATE,ls="0.5"); c.text(ipx+14,fb+98,"8 invitados",size=13.5,weight="bold",fill=INK)
c.glyph(ipx+iw-24,fb+96,"▾",13,SLATE)
# breakdown
brk=fb+128
items=[("$2,200 × 1 día","$2,200"),("Limpieza","$150"),("Tarifa de servicio (10%)","$220")]
yy=brk
for k,v in items:
    c.text(ipx,yy,k,size=14,fill="#33414e"); c.text(ipx+iw,yy,v,size=14,fill="#33414e",anchor="end"); yy+=30
c.line(ipx,yy-4,ipx+iw,yy-4,LINE,1.2); yy+=18
c.text(ipx,yy,"Total",size=17,weight="bold",fill=INK); c.text(ipx+iw,yy,"$2,570",size=17,weight="bold",fill=INK,anchor="end")
yy+=26
# ahorro
c.rect(ipx,yy,iw,38,AQUASOFT,rx=10)
c.glyph(ipx+14,yy+25,"✓",14,GREEN); c.text(ipx+34,yy+25,"Ahorras $390 vs. la misma reserva en Boatsetter",size=12.5,weight="bold",fill="#075e6b")
yy+=54
# botón
c.rect(ipx,yy,iw,52,c.grad([("0",AQUA),("1",TEAL)]),rx=14)
c.text(ipx+iw/2,yy+33,"Reservar ahora",size=16,weight="bold",fill="#04222f",anchor="middle")
yy+=64
c.text(bx+bw/2,yy,"No se te cobrará todavía",size=13,fill=SLATE,anchor="middle"); yy+=24
c.glyph(ipx,yy,"⚓",13,OCEAN); c.text(ipx+22,yy+1,"Depósito $1,000 reembolsable — retenido, no cobrado.",size=12.5,fill=SLATE)
yy+=22
c.glyph(ipx,yy,"✓",13,GREEN); c.text(ipx+22,yy+1,"Cancelación gratis hasta 48 h antes.",size=12.5,fill=SLATE)

bottom=max(left_bottom,byy+560)+60
footer(c,bottom)
c.h=bottom+300
c.render("/tmp/render/out/03-boat.png",scale=2)
print("boat OK",c.h)
