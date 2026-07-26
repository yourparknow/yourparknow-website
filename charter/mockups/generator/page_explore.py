# -*- coding: utf-8 -*-
from lib import *
from comp import *
from data import BOATS

c=C(2000)
header(c,active="explorar")

# ---- barra de búsqueda condensada ----
sy=98; sh=60; sx=M; sw=CW
c.rect(sx,sy,sw,sh,"#ffffff",rx=18,shadow=True)
c.rect(sx,sy,sw,sh,"none",rx=18,stroke=LINE,sw=1.2)
segs=[("Miami Beach, FL",ic_pin),("Sáb, 14 jun – Dom, 15",ic_cal),("8 invitados",ic_users),("Yate · con capitán",None)]
fx=sx+24; fw=(sw-150)/4
for i,(val,ic) in enumerate(segs):
    if ic: ic(c,fx,sy+sh/2,8,OCEAN)
    c.text(fx+(22 if ic else 0),sy+sh/2+5,val,size=14.5,weight="bold",fill=INK)
    if i<3: c.line(fx+fw-20,sy+14,fx+fw-20,sy+sh-14,LINE,1.2)
    fx+=fw
bg=c.grad([("0",AQUA),("1",TEAL)])
c.rect(sx+sw-128,sy+10,116,sh-20,bg,rx=14)
c.text(sx+sw-70,sy+sh/2+5,"Buscar",size=14.5,weight="bold",fill="#04222f",anchor="middle")

# ---- título + orden ----
ty=210
c.text(M,ty,"Botes en alquiler en Miami, FL",size=30,weight="bold",fill=INK)
c.text(M,ty+30,"318 botes disponibles · cancelación flexible · comisión 10%",size=14.5,fill=SLATE)
# ordenar
c.rect(M+CW-470,ty-26,210,40,"#fff",rx=12,stroke=LINE,sw=1.5)
c.text(M+CW-454,ty-1,"Ordenar:",size=13.5,fill=SLATE)
c.text(M+CW-388,ty-1,"Recomendados",size=13.5,weight="bold",fill=INK)
c.glyph(M+CW-282,ty-1,"▾",13,SLATE)
# toggle mapa
c.rect(M+CW-240,ty-26,110,40,"#fff",rx=12,stroke=LINE,sw=1.5)
ic_pin(c,M+CW-218,ty-7,7,OCEAN); c.text(M+CW-200,ty-1,"Mapa",size=13.5,weight="bold",fill=INK)
c.rect(M+CW-118,ty-26,118,40,NAVY,rx=12)
c.text(M+CW-59,ty-1,"Guardar búsqueda",size=12.5,weight="bold",fill="#fff",anchor="middle")

# ================= FILTROS =================
fx0=M; fw0=280; fy0=260
def checkbox(c,x,y,checked,label,count):
    if checked:
        c.rect(x,y-13,18,18,c.grad([("0",AQUA),("1",TEAL)]),rx=5)
        c.glyph(x+9,y+2,"✓",13,"#04222f",anchor="middle")
    else:
        c.rect(x,y-13,18,18,"#fff",rx=5,stroke=LINE,sw=1.6)
    c.text(x+28,y+2,label,size=14,fill=INK,weight=("bold" if checked else "normal"))
    c.text(fx0+fw0-20,y+2,f"({count})",size=12.5,fill=SLATE,anchor="end")

# alto de la tarjeta de filtros
fh=940
c.rect(fx0,fy0,fw0,fh,"#fff",rx=20,shadow=True)
c.rect(fx0,fy0,fw0,fh,"none",rx=20,stroke=LINE,sw=1.5)
px=fx0+22; py=fy0+40
c.text(px,py,"Filtros",size=18,weight="bold",fill=INK)
c.text(fx0+fw0-22,py,"Limpiar",size=13,weight="bold",fill=OCEAN,anchor="end")
py+=30; c.line(fx0+16,py,fx0+fw0-16,py,LINE,1.2); py+=26

c.text(px,py,"Tipo de bote",size=14.5,weight="bold",fill=INK); py+=30
for lab,cnt,ch in [("Yate de lujo",124,True),("Center console",88,True),("Pontón",62,False),("Velero",40,False),("Catamarán",31,False),("Sport cruiser",54,True)]:
    checkbox(c,px,py,ch,lab,cnt); py+=34
py+=6; c.line(fx0+16,py,fx0+fw0-16,py,LINE,1.2); py+=26

c.text(px,py,"Precio por día",size=14.5,weight="bold",fill=INK); py+=30
c.rect(px,py-14,84,32,"#fff",rx=8,stroke=LINE,sw=1.5); c.text(px+12,py+6,"$200",size=13,weight="bold",fill=INK)
c.text(px+98,py+6,"—",size=14,fill=SLATE)
c.rect(px+116,py-14,fw0-44-116,32,"#fff",rx=8,stroke=LINE,sw=1.5); c.text(px+128,py+6,"$3,000",size=13,weight="bold",fill=INK)
py+=34
# slider
c.rect(px,py,fw0-44,5,LINE,rx=3)
c.rect(px+40,py,140,5,c.grad([("0",AQUA),("1",TEAL)],vertical=False,x1=0,y1=0,x2=1,y2=0),rx=3)
c.circle(px+40,py+2.5,9,"#fff",stroke=TEAL,sw=3); c.circle(px+180,py+2.5,9,"#fff",stroke=TEAL,sw=3)
py+=34; c.line(fx0+16,py,fx0+fw0-16,py,LINE,1.2); py+=26

c.text(px,py,"Capacidad",size=14.5,weight="bold",fill=INK); py+=28
caps=[("1–6",False),("7–12",True),("13–20",False),("20+",False)]
cxp=px
for lab,on in caps:
    w_=len(lab)*9+26
    c.rect(cxp,py-6,w_,32,(NAVY if on else "#fff"),rx=16,stroke=(None if on else LINE),sw=1.5)
    c.text(cxp+w_/2,py+15,lab,size=13,weight="bold",fill=("#fff" if on else SLATE),anchor="middle")
    cxp+=w_+8
py+=44; c.line(fx0+16,py,fx0+fw0-16,py,LINE,1.2); py+=26

c.text(px,py,"Capitán",size=14.5,weight="bold",fill=INK); py+=30
# toggle on
c.rect(px,py-14,44,26,c.grad([("0",AQUA),("1",TEAL)]),rx=13); c.circle(px+31,py-1,10,"#fff")
c.text(px+56,py+4,"Con capitán incluido",size=14,fill=INK,weight="bold"); py+=36
c.rect(px,py-14,44,26,LINE,rx=13); c.circle(px+13,py-1,10,"#fff")
c.text(px+56,py+4,"Solo sin capitán",size=14,fill=SLATE); py+=40
c.line(fx0+16,py,fx0+fw0-16,py,LINE,1.2); py+=26

c.text(px,py,"Comodidades",size=14.5,weight="bold",fill=INK); py+=28
am=[("Wifi",True),("Nevera",True),("Snorkel",False),("Sonido JBL",True),("Baño",False),("Tobogán",False),("Paddleboard",True)]
cxp=px; ry=py
for lab,on in am:
    w_=len(lab)*8.2+24
    if cxp+w_>fx0+fw0-22: cxp=px; ry+=38
    c.rect(cxp,ry-6,w_,30,(AQUASOFT if on else "#fff"),rx=15,stroke=(TEAL if on else LINE),sw=1.4)
    c.text(cxp+w_/2,ry+14,lab,size=12.5,weight=("bold" if on else "normal"),fill=("#075e6b" if on else SLATE),anchor="middle")
    cxp+=w_+8
py=ry+44
c.rect(px,py,fw0-44,46,c.grad([("0",AQUA),("1",TEAL)]),rx=14)
c.text(px+(fw0-44)/2,py+29,"Aplicar filtros",size=14.5,weight="bold",fill="#04222f",anchor="middle")

# ================= RESULTADOS =================
gx=fx0+fw0+30; gw=W-M-gx
cols=3; gap=24; cw=(gw-(cols-1)*gap)/cols
gy=260
sky_cycle=["sunset","day","golden","dusk","teal","blue","golden","dusk","day"]
for i,d in enumerate(BOATS[:9]):
    col=i%cols; row=i//cols
    x=gx+col*(cw+gap); y=gy+row*(384+gap)
    dd=dict(d); dd["sky"]=sky_cycle[i]
    boat_card(c,x,y,cw,dd)
grid_bottom=gy+3*384+2*gap

# botón cargar más
ly=grid_bottom+10
c.rect(gx+gw/2-130,ly,260,48,"#fff",rx=24,stroke=TEAL,sw=2)
c.text(gx+gw/2,ly+30,"Mostrar más botes",size=15,weight="bold",fill=OCEAN,anchor="middle")

bottom=max(fy0+fh, ly+48)+70
footer(c,bottom)
c.h=bottom+300
c.render("/tmp/render/out/02-explore.png",scale=2)
print("explore OK",c.h)
