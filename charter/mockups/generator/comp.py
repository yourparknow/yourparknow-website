# -*- coding: utf-8 -*-
from lib import *

M=100; CW=W-2*M   # margen y ancho de contenido (100..1340, 1240)

def brandmark(c,x,y,s=34,dark=False):
    g=c.grad([("0",TEAL),("1",AQUA)])
    c.rect(x,y,s,s,g,rx=10,shadow=False)
    # dos olas dentro del cuadro
    c.path(f"M{x+s*0.16} {y+s*0.42} q{s*0.17} {-s*0.20} {s*0.34} 0 q{s*0.17} {s*0.20} {s*0.34} 0",stroke="#ffffff",sw=2.6,fill="none")
    c.path(f"M{x+s*0.16} {y+s*0.66} q{s*0.17} {-s*0.20} {s*0.34} 0 q{s*0.17} {s*0.20} {s*0.34} 0",stroke="#ffffff",sw=2.6,fill="none",op=0.7)
    c.text(x+s+12,y+s*0.72,"MAREA",size=24,weight="bold",fill=(WHITE if dark else NAVY))

def header(c,dark=False,active=None):
    txt= WHITE if dark else INK
    brandmark(c,M,21,34,dark=dark)
    links=[("Explorar","explorar"),("Cómo funciona","como"),("Pon tu bote","host"),("Ayuda","ayuda")]
    x=360
    for label,key in links:
        col = (AQUA if dark else OCEAN) if active==key else (txt)
        op = 1 if active==key else (0.92 if dark else 0.8)
        c.text(x,46,label,size=15,weight=("bold" if active==key else "normal"),fill=col,op=op)
        x+=len(label)*9.0+46
    # derecha
    c.text(1130,46,"ES / EN",size=14,weight="bold",fill=(WHITE if dark else SLATE),op=0.9)
    c.text(1210,46,"Entrar",size=15,weight="bold",fill=txt,op=0.9)
    bg = c.grad([("0",AQUA),("1",TEAL)])
    c.rect(1262,24,78,40,(WHITE if not dark else None) or "#ffffff",rx=20) if False else None
    c.rect(1248,24,92,40,bg,rx=20,shadow=False)
    c.text(1294,49,"Únete",size=14.5,weight="bold",fill="#04222f",anchor="middle")
    if not dark:
        c.line(0,76,W,76,LINE,1.5)

def chip(c,x,y,w,h,text,bg,fg,icon=None,bold=True,size=12.5):
    c.rect(x,y,w,h,bg,rx=h/2)
    tx=x+w/2
    c.text(tx,y+h/2+size*0.36,text,size=size,weight=("bold" if bold else "normal"),fill=fg,anchor="middle")

def boat_card(c,x,y,w,d):
    h=384; ph=230
    c.rect(x,y,w,h,WHITE,rx=20,shadow=True)
    c.rect(x,y,w,h,"none",rx=20,stroke=LINE,sw=1.5)
    cid=c.clip_top(x,y,w,ph,20)
    boat_scene(c,x,y,w,ph,d.get("kind","yacht"),d.get("sky","sunset"),clip=cid)
    # tag tipo
    t=d["type"]; tw=len(t)*7.6+26
    c.rect(x+14,y+14,tw,28,"#ffffffEE",rx=14)
    c.text(x+14+tw/2,y+14+19,t,size=12.5,weight="bold",fill=NAVY,anchor="middle")
    # capitan
    if d.get("captain"):
        cw=118; c.rect(x+w-14-cw,y+14,cw,28,NAVY,rx=14)
        c.glyph(x+w-14-cw+16,y+14+20,"⚓",13,AQUA)
        c.text(x+w-14-cw+34,y+14+19,"Con capitán",size=12,weight="bold",fill="#fff")
    # corazon
    c.circle(x+w-32,y+ph-30,18,"#ffffffEE")
    c.glyph(x+w-32,y+ph-24,"♥",17,CORAL,anchor="middle")
    # cuerpo
    by=y+ph
    c.text(x+18,by+34,d["name"],size=19,weight="bold",fill=INK)
    ic_pin(c,x+22,by+58,6,SLATE)
    c.text(x+34,by+62,d["loc"],size=13.5,fill=SLATE)
    # rating (alineado a la derecha, sin solaparse)
    rate=f'{d["rating"]}'; rev=f'({d["rev"]})'
    rev_w=len(rev)*7.0; rate_w=len(rate)*8.4
    c.text(x+w-18,by+34,rev,size=12.5,fill=SLATE,anchor="end")
    c.text(x+w-18-rev_w-6,by+34,rate,size=14,weight="bold",fill=INK,anchor="end")
    c.glyph(x+w-18-rev_w-6-rate_w-18,by+34,"★",14,STAR)
    # specs chips (icono + texto, sin duplicar)
    sy=by+82
    specs=[("↔",f'{d["len"]} ft'),("⚓",f'{d["cap"]} pers'),(None,d.get("year","2023"))]
    sx=x+18
    for icon,label in specs:
        tw=len(label)*7.2
        sw=tw+(24 if icon else 0)+22
        c.rect(sx,sy,sw,26,CLOUD,rx=8)
        ix=sx+13
        if icon:
            c.glyph(ix,sy+18,icon,13,OCEAN); ix+=18
        c.text(ix,sy+18,label,size=11.5,weight="bold",fill=SLATE)
        sx+=sw+8
    # precio
    c.line(x+18,by+120,x+w-18,by+120,LINE,1.2)
    c.text(x+18,by+150,f'${d["price"]:,}',size=23,weight="bold",fill=INK)
    px=x+18+len(f'${d["price"]:,}')*14+8
    c.text(px,by+150,"/día",size=13,fill=SLATE)
    bg=c.grad([("0",AQUA),("1",TEAL)])
    c.rect(x+w-118,by+128,100,34,bg,rx=17)
    c.text(x+w-68,by+150,"Reservar",size=13.5,weight="bold",fill="#04222f",anchor="middle")

def footer(c,y):
    h=300
    c.rect(0,y,W,h,NAVY)
    brandmark(c,M,y+44,32,dark=True)
    c.text(M,y+108,"El marketplace de charters de Miami",size=14,fill="#9fc0d4")
    c.text(M,y+132,"que te deja quedarte con lo que ganas.",size=14,fill="#9fc0d4")
    c.glyph(M,y+172,"⚓",16,AQUA); c.text(M+26,y+176,"Miami · Fort Lauderdale · Key Biscayne",size=13,fill="#7fa6bd")
    cols=[("Explorar",["Yates","Center console","Pontones","Veleros","Catamaranes"]),
          ("Compañía",["Cómo funciona","Pon tu bote","Precios y comisión","Seguridad","Blog"]),
          ("Legal",["Términos","Privacidad","Reembolsos","Seguro","Contacto"])]
    cx=760
    for title,items in cols:
        c.text(cx,y+50,title.upper(),size=13,weight="bold",fill="#ffffff",ls="0.5")
        yy=y+82
        for it in items:
            c.text(cx,yy,it,size=13.5,fill="#a9c6d8"); yy+=27
        cx+=200
    c.line(M,y+h-56,W-M,y+h-56,"#ffffff",1,op=0.12)
    c.text(M,y+h-28,"© 2026 MAREA Charters · Miami, FL — Maqueta de presentación",size=12.5,fill="#7fa6bd")
    c.text(W-M,y+h-28,"Comisión 10% · Pagos seguros con Stripe",size=12.5,fill="#7fa6bd",anchor="end")

def section_head(c,y,eyebrow,title,sub=None,center=True):
    ax=W/2 if center else M
    an="middle" if center else "start"
    c.text(ax,y,eyebrow.upper(),size=13,weight="bold",fill=OCEAN,anchor=an,ls="1.2")
    c.text(ax,y+44,title,size=38,weight="bold",fill=INK,anchor=an)
    if sub:
        c.text(ax,y+80,sub,size=17,fill=SLATE,anchor=an)
