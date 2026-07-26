# -*- coding: utf-8 -*-
from lib import *
from comp import *
from data import BOATS as ALLBOATS
BOATS=ALLBOATS[:6]

c=C(2980)

# ---------- HERO ----------
hero_h=600
hg=c.grad([("0",NAVY),("0.55",OCEAN),("1",TEAL)])
c.rect(0,0,W,hero_h,hg)
# brillos
c.circle(W*0.85,-40,260,AQUA,op=0.18)
c.circle(120,hero_h+40,260,SUNSET,op=0.16)
header(c,dark=True,active="explorar")
c.text(W/2,170,"Renta el bote perfecto en Miami.",size=58,weight="bold",fill="#fff",anchor="middle")
c.text(W/2,238,"Reserva yates, lanchas y pontones con o sin capitán.",size=21,fill="#e6f7fb",anchor="middle",op=0.95)
c.text(W/2,270,"Pagos seguros, depósito protegido y la comisión más baja del mercado.",size=21,fill="#e6f7fb",anchor="middle",op=0.95)
# chips
chips=[("★","4.9 promedio"),(None,"2,400+ botes en Miami"),(None,"Solo 10% de comisión"),(None,"Depósito 100% protegido")]
def chipw(ic,t): return len(t)*8.2+44+(20 if ic else 0)
cx=W/2 - sum(chipw(ic,t) for ic,t in chips)/2 - 6*3
for ic,t in chips:
    wc=chipw(ic,t)
    c.rect(cx,300,wc,38,"#ffffff",rx=19,op=0.16)
    tx=cx+wc/2 - (10 if ic else 0)
    if ic: c.glyph(tx-len(t)*4.1-8,325,ic,15,GOLD)
    c.text(cx+wc/2+(10 if ic else 0),324,t,size=13.5,weight="bold",fill="#fff",anchor="middle")
    cx+=wc+12
# search bar
sb_w=940; sb_x=(W-sb_w)/2; sb_y=384; sb_h=82
c.rect(sb_x,sb_y,sb_w,sb_h,"#ffffff",rx=22,shadow=True)
fields=[("UBICACIÓN","Miami Beach, FL",ic_pin),("FECHA","Sáb, 14 jun",ic_cal),("PERSONAS","8 invitados",ic_users),("TIPO","Yate · con capitán",None)]
fx=sb_x+18; fw=(sb_w-150-18)/4
for i,(lbl,val,ic) in enumerate(fields):
    if ic: ic(c,fx+12,sb_y+sb_h/2,9,OCEAN)
    ox=fx+(30 if ic else 6)
    c.text(ox,sb_y+34,lbl,size=10.5,weight="bold",fill=SLATE,ls="0.6")
    c.text(ox,sb_y+57,val,size=15,weight="bold",fill=INK)
    if i<3: c.line(fx+fw,sb_y+16,fx+fw,sb_y+sb_h-16,LINE,1.2)
    fx+=fw
bg=c.grad([("0",AQUA),("1",TEAL)])
c.rect(sb_x+sb_w-132,sb_y+12,120,sb_h-24,bg,rx=18)
# lupa dibujada
mcx=sb_x+sb_w-108; mcy=sb_y+sb_h/2
c.circle(mcx,mcy-2,8,"none",stroke="#04222f",sw=3)
c.line(mcx+6,mcy+4,mcx+12,mcy+10,"#04222f",3)
c.text(sb_x+sb_w-54,sb_y+sb_h/2+6,"Buscar",size=15,weight="bold",fill="#04222f",anchor="middle")

# ---------- FEE BAND ----------
fy=hero_h+56
c.rect(M,fy,CW,236,NAVY,rx=28,shadow=True)
c.circle(M+CW-90,fy-10,150,SUNSET,op=0.22)
c.text(M+44,fy+66,"Cobramos 10%. Ellos hasta 35%.",size=30,weight="bold",fill="#fff")
c.text(M+44,fy+104,"Más dinero para los dueños. Mejores precios para",size=16,fill="#cfe6f0")
c.text(M+44,fy+128,"los clientes. Así de simple.",size=16,fill="#cfe6f0")
c.rect(M+44,fy+158,210,44,c.grad([("0",AQUA),("1",TEAL)]),rx=22)
c.text(M+44+105,fy+186,"Ver comparación  →",size=14.5,weight="bold",fill="#04222f",anchor="middle")
# fee cards
fee=[("MAREA","10%",True),("GetMyBoat","~20%",False),("Boatsetter","~28%",False),("Sailo","~35%",False)]
fcw=220; gap=18; fgx=M+CW-(fcw*4+gap*3)-44; fcy=fy+44
for i,(nm,pct,ours) in enumerate(fee):
    xx=fgx+i*(fcw+gap)
    if ours:
        c.rect(xx,fcy,fcw,148,c.grad([("0",AQUA),("1",TEAL)]),rx=18)
        pc="#04222f"; nc="#04222f"
    else:
        c.rect(xx,fcy,fcw,148,"#ffffff",rx=18,op=0.08)
        c.rect(xx,fcy,fcw,148,"none",rx=18,stroke="#ffffff",sw=1,sop=0.18)
        pc="#fff"; nc="#bcd6e4"
    c.text(xx+fcw/2,fcy+74,pct,size=42,weight="bold",fill=pc,anchor="middle")
    c.text(xx+fcw/2,fcy+108,nm,size=14,weight="bold",fill=nc,anchor="middle")
    if ours: c.text(xx+fcw/2,fcy+130,"tu comisión",size=11.5,fill="#0a4a52",anchor="middle")

# ---------- FEATURED ----------
fty=fy+236+90
section_head(c,fty,"Botes destacados","Los favoritos de Miami esta semana","Capacidad real, capitanes verificados y cancelación flexible.")
gy=fty+130
cw=(CW-2*28)/3
for i,d in enumerate(BOATS):
    col=i%3; row=i//3
    x=M+col*(cw+28); y=gy+row*(384+28)
    boat_card(c,x,y,cw,d)
after_boats=gy+2*384+28

# ---------- HOW IT WORKS ----------
hw=after_boats+70
section_head(c,hw,"Cómo funciona","Reserva en 3 pasos","De la búsqueda al muelle en minutos, todo desde la app.")
steps=[("1","Busca y compara","Filtra por tipo, fecha, capacidad y precio. Fotos reales, reseñas verificadas y precio final sin sorpresas."),
       ("2","Reserva y paga seguro","Sube tus documentos, paga con tarjeta o Apple Pay. El depósito queda retenido, no cobrado."),
       ("3","Sube a bordo","Te conectamos con el dueño o capitán. Disfruta. El depósito se libera 48 h después si todo está bien.")]
sy=hw+130; scw=(CW-2*28)/3
for i,(n,t,desc) in enumerate(steps):
    x=M+i*(scw+28)
    c.rect(x,sy,scw,210,CLOUD,rx=22)
    c.rect(x,sy,scw,210,"none",rx=22,stroke=LINE,sw=1.5)
    c.rect(x+28,sy+28,52,52,c.grad([("0",AQUA),("1",TEAL)]),rx=15)
    c.text(x+28+26,sy+63,n,size=26,weight="bold",fill="#04222f",anchor="middle")
    c.text(x+28,sy+118,t,size=20,weight="bold",fill=INK)
    # wrap desc
    words=desc.split(); line=""; ly=sy+148
    for wd in words:
        if len(line)+len(wd)>42:
            c.text(x+28,ly,line,size=13.5,fill=SLATE); ly+=21; line=wd
        else: line=(line+" "+wd).strip()
    c.text(x+28,ly,line,size=13.5,fill=SLATE)
after_steps=sy+210

# ---------- COMPARISON TABLE ----------
ct=after_steps+80
section_head(c,ct,"Por qué MAREA","La diferencia se nota en tu bolsillo")
ty=ct+110
cols=["","MAREA","Boatsetter","GetMyBoat","Sailo"]
rows=[
 ("Comisión total","10%","~28%","~20%","~35%"),
 ("El dueño recibe","90%","~72%","~80%","~65%"),
 ("Depósito de seguridad","Retenido, no cobrado","Cobrado 48 h antes","Variable","Retenido"),
 ("Pago al dueño","24–48 h","Hasta 5 días","Variable","Hasta 7 días"),
 ("Soporte local Miami","Sí","Parcial","No","No"),
 ("Documentos digitales","Sí","Parcial","Manual","Parcial"),
]
tw=CW; tx=M
colw=[tw*0.30,tw*0.19,tw*0.17,tw*0.17,tw*0.17]
rh=58; theadh=58
c.rect(tx,ty,tw,theadh+rh*len(rows),"#ffffff",rx=20,shadow=True)
# header row
cxs=[tx];
for w_ in colw[:-1]: cxs.append(cxs[-1]+w_)
c.rect(tx,ty,tw,theadh,NAVY,rx=20)
c.rect(tx,ty+theadh-20,tw,20,NAVY)   # cuadrar parte baja del header
# resaltar columna MAREA
mx=cxs[1]
c.rect(mx,ty,colw[1],theadh+rh*len(rows),AQUASOFT,rx=0,op=1)
c.rect(mx,ty,colw[1],theadh,c.grad([("0",AQUA),("1",TEAL)]))
for i,h in enumerate(cols):
    if i==0: continue
    cxx=cxs[i]+colw[i]/2
    col="#04222f" if i==1 else "#fff"
    c.text(cxx,ty+36,h,size=15,weight="bold",fill=col,anchor="middle")
# rows
for r,row in enumerate(rows):
    yy=ty+theadh+r*rh
    if r>0: c.line(tx+20,yy,tx+tw-20,yy,LINE,1.2)
    c.text(tx+24,yy+36,row[0],size=14.5,weight="bold",fill=INK)
    for i in range(1,5):
        cxx=cxs[i]+colw[i]/2
        val=row[i]
        if i==1:
            c.glyph(cxx-len(val)*4.2-12,yy+37,"✓",14,GREEN)
            c.text(cxx+6,yy+36,val,size=14,weight="bold",fill="#075e3a",anchor="middle")
        else:
            c.text(cxx,yy+36,val,size=13.5,fill=SLATE,anchor="middle")
c.rect(mx,ty,colw[1],theadh+rh*len(rows),"none",rx=12,stroke=TEAL,sw=2)
after_table=ty+theadh+rh*len(rows)

# ---------- OWNER CTA ----------
oy=after_table+80
c.rect(M,oy,CW,260,c.grad([("0",PINK),("0.5",SUNSET),("1",GOLD)]),rx=28,shadow=True)
c.text(M+50,oy+86,"¿Tienes un bote? Gana el 90%.",size=36,weight="bold",fill="#fff")
c.text(M+50,oy+126,"Publica gratis en minutos. Tú pones el precio y las reglas.",size=17,fill="#fff",op=0.95)
c.text(M+50,oy+152,"Nosotros traemos los clientes, los pagos y el seguro.",size=17,fill="#fff",op=0.95)
c.rect(M+50,oy+182,210,48,"#ffffff",rx=24)
c.text(M+50+105,oy+212,"Publicar mi bote",size=15,weight="bold",fill=CORAL,anchor="middle")
c.rect(M+274,oy+182,196,48,"none",rx=24,stroke="#ffffff",sw=2)
c.text(M+274+98,oy+212,"Calcular ganancias",size=14.5,weight="bold",fill="#fff",anchor="middle")
# tarjeta ganancia
ox=M+CW-360;
c.rect(ox,oy+40,310,180,"#ffffff",rx=20,op=0.16)
c.rect(ox,oy+40,310,180,"none",rx=20,stroke="#ffffff",sw=1.5,sop=0.4)
c.text(ox+28,oy+78,"Yate de 50 ft · 20 días/mes",size=13.5,fill="#fff",op=0.95)
c.text(ox+28,oy+128,"$39,600",size=42,weight="bold",fill="#fff")
c.text(ox+28,oy+156,"para ti / mes  (vs $31,680 en Boatsetter)",size=13,fill="#fff",op=0.95)
c.text(ox+28,oy+190,"+$7,920 más al mes con MAREA",size=14.5,weight="bold",fill="#fff")
after_owner=oy+260

# ---------- FOOTER ----------
fly=after_owner+70
footer(c,fly)
c.h=fly+300
c.render("/tmp/render/out/01-home.png",scale=2)
print("home OK", c.h)
