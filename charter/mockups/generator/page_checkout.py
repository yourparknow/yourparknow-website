# -*- coding: utf-8 -*-
from lib import *
from comp import *

c=C(2200)

# ---- header slim ----
brandmark(c,M,21,34)
c.glyph(M+CW-150,46,"⚓",14,OCEAN)
ic_lock(c,M+CW-126,40,8,OCEAN); c.text(M+CW-108,46,"Pago 100% seguro · cifrado SSL",size=13.5,weight="bold",fill=SLATE)
c.line(0,76,W,76,LINE,1.5)

# ---- título + pasos ----
c.text(M,128,"Confirma y paga",size=30,weight="bold",fill=INK)
# step bar
sy=158
steps=[("1","Detalles","done"),("2","Documentos","done"),("3","Pago","active")]
sxp=M
for i,(n,lab,st) in enumerate(steps):
    if st=="done":
        c.circle(sxp+15,sy+15,15,GREEN); c.glyph(sxp+15,sy+20,"✓",15,"#fff",anchor="middle")
        col=INK
    elif st=="active":
        c.circle(sxp+15,sy+15,15,TEAL); c.text(sxp+15,sy+20,n,size=14,weight="bold",fill="#04222f",anchor="middle")
        col=INK
    c.text(sxp+40,sy+20,lab,size=15,weight="bold",fill=col)
    sxp+=40+len(lab)*9+30
    if i<2: c.line(sxp-22,sy+15,sxp-2,sy+15,LINE,2)

# columnas
LX=M; LW=740; RX=M+LW+40; RW=CW-LW-40
y=210

def card(c,x,y,w,h,title,sub=None):
    c.rect(x,y,w,h,WHITE,rx=20,shadow=True); c.rect(x,y,w,h,"none",rx=20,stroke=LINE,sw=1.5)
    c.text(x+26,y+40,title,size=20,weight="bold",fill=INK)
    if sub: c.text(x+26,y+66,sub,size=14,fill=SLATE)

# ===== 1. DOCUMENTOS =====
dh=320
card(c,LX,y,LW,dh,"1 · Verifica tu identidad","Requisito de la ley SB-606 de Florida para alquiler de botes.")
docs=[("Identificación oficial","Licencia de conducir o pasaporte","ok",ic_card),
      ("Boater Safety ID (Florida)","Obligatorio si naciste después de 1988","ok",ic_doc),
      ("Selfie de verificación","Para confirmar que coincide con tu ID","pending",ic_users)]
dy=y+96
for nm,ds,st,ic in docs:
    rh=58
    bgc = "#eafaf2" if st=="ok" else CLOUD
    brc = GREEN if st=="ok" else LINE
    c.rect(LX+26,dy,LW-52,rh,bgc,rx=12,stroke=brc,sw=1.5)
    c.rect(LX+40,dy+13,32,32,"#fff",rx=9,stroke=LINE,sw=1.2)
    ic(c,LX+56,dy+29,9,(GREEN if st=="ok" else OCEAN))
    c.text(LX+88,dy+26,nm,size=15,weight="bold",fill=INK)
    c.text(LX+88,dy+46,ds,size=12.5,fill=SLATE)
    if st=="ok":
        c.glyph(LX+LW-150,dy+35,"✓",15,GREEN); c.text(LX+LW-128,dy+36,"Verificado",size=13,weight="bold",fill="#075e3a")
    else:
        c.rect(LX+LW-160,dy+13,120,32,c.grad([("0",AQUA),("1",TEAL)]),rx=16)
        c.text(LX+LW-100,dy+34,"Subir foto",size=13,weight="bold",fill="#04222f",anchor="middle")
    dy+=rh+12
y+=dh+28

# ===== 2. PAGO =====
ph=560
card(c,LX,y,LW,ph,"2 · Método de pago","Tus datos viajan cifrados. Procesado por Stripe.")
py=y+92
# wallets
c.rect(LX+26,py,(LW-52-14)/2,52,"#000",rx=12); c.text(LX+26+(LW-52-14)/4,py+33,"Apple Pay",size=16,weight="bold",fill="#fff",anchor="middle")
gx=LX+26+(LW-52-14)/2+14
c.rect(gx,py,(LW-52-14)/2,52,"#fff",rx=12,stroke=LINE,sw=1.6); c.text(gx+(LW-52-14)/4,py+33,"G  Pay",size=16,weight="bold",fill=INK,anchor="middle")
py+=72
# divisor
c.line(LX+26,py,LX+LW/2-70,py,LINE,1.4); c.text(LX+LW/2,py+5,"o paga con tarjeta",size=13,fill=SLATE,anchor="middle"); c.line(LX+LW/2+70,py,LX+LW-26,py,LINE,1.4)
py+=30
def inp(x,y,w,label,val,ph=False,focus=False):
    c.text(x,y,label,size=13,weight="bold",fill=INK)
    c.rect(x,y+10,w,48,"#fff",rx=12,stroke=(TEAL if focus else LINE),sw=(2 if focus else 1.6))
    if focus: c.rect(x,y+10,w,48,"none",rx=12,stroke=TEAL,sw=4,sop=0.15)
    c.text(x+16,y+40,val,size=15,weight="bold" if not ph else "normal",fill=(INK if not ph else "#9fb0bd"))
# número
inp(LX+26,py+18,LW-52,"Número de tarjeta","4242  4242  4242  4242",focus=True)
# brand icons
bx=LX+LW-52-150
c.rect(bx,py+30,40,26,"#1A1F71",rx=5); c.text(bx+20,py+47,"VISA",size=11,weight="bold",fill="#fff",anchor="middle")
c.circle(bx+58,py+43,11,"#EB001B"); c.circle(bx+72,py+43,11,"#F79E1B",op=0.9)
c.rect(bx+92,py+30,46,26,"#2E77BC",rx=5); c.text(bx+115,py+47,"AMEX",size=10,weight="bold",fill="#fff",anchor="middle")
py+=82
half=(LW-52-16)/2
inp(LX+26,py+18,half,"Vencimiento","09 / 28")
inp(LX+26+half+16,py+18,half,"CVC","•••  123",)
py+=82
inp(LX+26,py+18,LW-52,"Nombre en la tarjeta","José R. González")
py+=82
inp(LX+26,py+18,half,"País","Estados Unidos")
inp(LX+26+half+16,py+18,half,"Código postal","33139")
y+=ph+28

# ===== 3. DEPÓSITO =====
sh2=210
card(c,LX,y,LW,sh2,"3 · Depósito de seguridad","Se retiene, no se cobra. Vuelve a tu tarjeta si no hay daños.")
ddy=y+104
# timeline
tl=[("48 h antes","Se retiene $1,000 en tu tarjeta (hold)"),("Durante el viaje","El hold permanece sin cobrarse"),("48–72 h después","Se libera el 100% si no hay daños")]
seg=(LW-52)/3
for i,(t,d) in enumerate(tl):
    xx=LX+26+i*seg
    c.circle(xx+12,ddy,9,c.grad([("0",AQUA),("1",TEAL)]))
    if i<2: c.line(xx+24,ddy,xx+seg,ddy,LINE,2.5)
    c.text(xx,ddy+34,t,size=13.5,weight="bold",fill=INK)
    # wrap d
    ww=d.split(); ln=""; ly=ddy+56
    for wd in ww:
        if len(ln)+len(wd)>26: c.text(xx,ly,ln,size=12,fill=SLATE); ly+=17; ln=wd
        else: ln=(ln+" "+wd).strip()
    c.text(xx,ly,ln,size=12,fill=SLATE)
y+=sh2+28

# checkbox términos
c.rect(LX+2,y,20,20,c.grad([("0",AQUA),("1",TEAL)]),rx=6); c.glyph(LX+12,y+15,"✓",14,"#04222f",anchor="middle")
c.text(LX+32,y+15,"Acepto los Términos, la Política de cancelación y el contrato de alquiler.",size=13.5,fill="#33414e")
left_bottom=y+30

# ================= RESUMEN (derecha) =================
ry=210
c.rect(RX,ry,RW,640,WHITE,rx=20,shadow=True); c.rect(RX,ry,RW,640,"none",rx=20,stroke=LINE,sw=1.5)
# header boat
cid=c.clip_rect(RX+22,ry+22,96,72,12); boat_scene(c,RX+22,ry+22,96,72,"yacht","sunset",clip=cid)
c.text(RX+132,ry+44,"Sea Breeze",size=17,weight="bold",fill=INK)
c.text(RX+132,ry+66,"Yate de lujo · 52 ft",size=13,fill=SLATE)
c.glyph(RX+132,ry+88,"★",12,STAR); c.text(RX+148,ry+89,"4.97 (128) · Miami Beach",size=12.5,fill=SLATE)
c.line(RX+22,ry+116,RX+RW-22,ry+116,LINE,1.2)
# trip rows
iy=ry+146
for k,v in [("Fecha","Sáb 14 jun · 9:00–17:00"),("Invitados","8 personas"),("Capitán","Andrés R. (incluido)")]:
    c.text(RX+22,iy,k,size=13.5,fill=SLATE); c.text(RX+RW-22,iy,v,size=13.5,weight="bold",fill=INK,anchor="end"); iy+=30
c.line(RX+22,iy+2,RX+RW-22,iy+2,LINE,1.2); iy+=28
# breakdown
for k,v in [("$2,200 × 1 día","$2,200"),("Limpieza","$150"),("Tarifa de servicio (10%)","$220")]:
    c.text(RX+22,iy,k,size=14,fill="#33414e"); c.text(RX+RW-22,iy,v,size=14,fill="#33414e",anchor="end"); iy+=30
c.line(RX+22,iy+2,RX+RW-22,iy+2,LINE,1.2); iy+=30
c.text(RX+22,iy,"Pagas hoy",size=18,weight="bold",fill=INK); c.text(RX+RW-22,iy,"$2,570",size=20,weight="bold",fill=INK,anchor="end"); iy+=34
# deposit hold
c.rect(RX+22,iy,RW-44,52,CLOUD,rx=12)
c.glyph(RX+38,iy+33,"⚓",14,OCEAN); c.text(RX+60,iy+26,"Depósito (hold)",size=13,weight="bold",fill=INK)
c.text(RX+60,iy+44,"Retenido, no cobrado ahora",size=11.5,fill=SLATE)
c.text(RX+RW-38,iy+35,"$1,000",size=16,weight="bold",fill=INK,anchor="end")
iy+=70
# botón pagar
c.rect(RX+22,iy,RW-44,54,c.grad([("0",AQUA),("1",TEAL)]),rx=14)
ic_lock(c,RX+22+60,iy+27,8,"#04222f")
c.text(RX+RW/2+12,iy+34,"Pagar $2,570",size=16.5,weight="bold",fill="#04222f",anchor="middle")
iy+=68
# ahorro
c.glyph(RX+22,iy,"✓",13,GREEN); c.text(RX+42,iy+1,"Ahorras $390 vs. Boatsetter en este viaje",size=12.5,weight="bold",fill="#075e6b")
iy+=30
# badges
bxs=RX+22
for t in ["🔒 Stripe","PCI-DSS","SSL 256-bit"]:
    t=t.replace("🔒 ","")
    w_=len(t)*7.2+22
    c.rect(bxs,iy,w_,28,"#fff",rx=8,stroke=LINE,sw=1.3); c.text(bxs+w_/2,iy+19,t,size=12,weight="bold",fill=SLATE,anchor="middle")
    bxs+=w_+8

# Marea promise
my=ry+640+24
c.rect(RX,my,RW,120,AQUASOFT,rx=18)
ic_shield(c,RX+44,my+50,16,TEAL)
c.text(RX+80,my+42,"Garantía MAREA",size=16,weight="bold",fill="#075e6b")
c.text(RX+80,my+66,"Seguro de responsabilidad y daños incluido",size=12.5,fill="#0a6273")
c.text(RX+80,my+86,"en cada viaje. Soporte 24/7 en Miami.",size=12.5,fill="#0a6273")

bottom=max(left_bottom,my+120)+60
footer(c,bottom)
c.h=bottom+300
c.render("/tmp/render/out/04-checkout.png",scale=2)
print("checkout OK",c.h)
