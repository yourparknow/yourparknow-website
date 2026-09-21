#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Hoja de DECISION: el dibujo de la escalera acostado (A) contra derecho (B),
   en el mismo pano y a la misma escala, para que Rene escoja.
   NO es del set de planos: es para decidir. Cuando escoja, se rehace la hoja
   de escaleras con esa forma y esta se borra."""
import math, pathlib, importlib.util
H=pathlib.Path("/home/user/yourparknow-website/proposals/jrg-welding-corp")
s=importlib.util.spec_from_file_location("g",H/"gen-railing-secciones.py")
G=importlib.util.module_from_spec(s); s.loader.exec_module(G)
fr=G.fr
NEG,ROJO,ALU,ALU2,PIQ="#1b2a41","#b91c1c","#9fb0c0","#7b8d9e","#e5e7eb"
ANG=34.0; a=math.radians(ANG); ca,ta=math.cos(a),math.tan(a)
CAMPO=40-2/ca; BAY=35.9375; PANEL=BAY-0.5
ACOST, DERECHO = 26.0, 20.0

def bay(op, VW=390, VH=330):
    mx,my=28,30
    sc=min((VW-2*mx)/BAY,(VH-2*my)/(BAY*ta+42))
    OX=mx; OY=VH-my
    def S(x,y): return OX+x*sc, OY-(x*ta+y)*sc
    def band(x0,x1,y0,y1,f,st=NEG,w=1.0):
        p=[S(x0,y0),S(x1,y0),S(x1,y1),S(x0,y1)]
        return '<polygon points="%s" fill="%s" stroke="%s" stroke-width="%s"/>'%(
            " ".join("%.1f,%.1f"%q for q in p),f,st,w)
    yrt=2+1/ca; ycb=42-1/ca
    o=['<svg viewBox="0 0 %d %d" xmlns="http://www.w3.org/2000/svg">'%(VW,VH)]
    o.append(band(0,BAY,2,yrt,ALU2)); o.append(band(0,BAY,ycb,42,ALU2))
    for px in (-2.0,BAY):
        o.append(band(px,px+2,-3,ycb,ALU,NEG,1.3))
    cx=BAY/2; cy=(yrt+ycb)/2
    if op=="A":
        half=ACOST/2
        v1,v2=cx-half,cx+half-1
        for xx in (v1,v2): o.append(band(xx,xx+1,yrt,ycb,ALU,NEG,0.9))
        yb,yt=cy-half,cy+half
        for yy in (yb,yt-1): o.append(band(v1+1,v2,yy,yy+1,ALU,NEG,0.9))
        ia,ib=v1+1,v2
        for p,q in (((ia,yb+1),(ib,yt-1)),((ia,yt-1),(ib,yb+1))):
            A,B=S(*p),S(*q)
            o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%.1f"/>'%(A[0],A[1],B[0],B[1],NEG,sc))
        for od in (20.5*ACOST/30.25,10.75*ACOST/30.25):
            r=(od-1)/2
            p=[S(cx-r,cy-r),S(cx+r,cy-r),S(cx+r,cy+r),S(cx-r,cy+r)]
            o.append('<polygon points="%s" fill="none" stroke="%s" stroke-width="%.1f"/>'%(
                " ".join("%.1f,%.1f"%q for q in p),NEG,sc))
        # flancos
        hueco=(PANEL-ACOST)/2; g=(hueco-1)/2
        for xx in (0.25+g, BAY-0.25-g-1):
            o.append(band(xx,xx+1,yrt,ycb,PIQ,ALU2,0.7))
    else:
        h=DERECHO/2
        # cuadro DERECHO: se dibuja en coordenadas de pantalla, sin cizalla
        P0=S(cx,cy)
        def R(dx,dy,w,hh):
            return '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s" stroke="%s" stroke-width="0.9"/>'%(
                P0[0]+dx*sc,P0[1]-dy*sc-hh*sc,w*sc,hh*sc,ALU,NEG)
        o.append(R(-h,-h,1,DERECHO)); o.append(R(h-1,-h,1,DERECHO))
        o.append(R(-h+1,h-1,DERECHO-2,1)); o.append(R(-h+1,-h,DERECHO-2,1))
        for p,q in (((-h+1,-h+1),(h-1,h-1)),((-h+1,h-1),(h-1,-h+1))):
            o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%.1f"/>'%(
                P0[0]+p[0]*sc,P0[1]-p[1]*sc,P0[0]+q[0]*sc,P0[1]-q[1]*sc,NEG,sc))
        for od in (20.5*DERECHO/30.25,10.75*DERECHO/30.25):
            r=(od-1)/2
            o.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="none" stroke="%s" stroke-width="%.1f"/>'%(
                P0[0]-r*sc,P0[1]-r*sc,2*r*sc,2*r*sc,NEG,sc))
        hueco=(PANEL-DERECHO)/2; n=2; g=(hueco-n)/(n+1)
        for side in (0,1):
            for i in range(n):
                xx=(0.25+g+i*(1+g)) if side==0 else (BAY-0.25-g-1-i*(1+g))
                o.append(band(xx,xx+1,yrt,ycb,PIQ,ALU2,0.7))
    o.append('</svg>')
    return "".join(o)

html="""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Segoe UI',Helvetica,Arial,sans-serif;color:#1b2a41;font-size:13px}
.page{max-width:10.2in;margin:0 auto;padding:.3in}
@media print{@page{size:letter landscape;margin:.3in}.page{padding:0;max-width:none}}
h1{font-size:19px;border-bottom:4px solid #1b2a41;padding-bottom:7px;margin-bottom:12px}
.row{display:flex;gap:16px}
.col{flex:1;border:2px solid #1b2a41;border-radius:6px}
.col h2{background:#1b2a41;color:#fff;font-size:14px;padding:6px 11px}
.col.b h2{background:#b91c1c}
.col svg{display:block;width:100%;height:auto}
ul{margin:9px 14px 11px 28px;font-size:12.5px}li{margin:3px 0}
b.big{color:#b91c1c}
</style></head><body><div class="page">
<h1>EL DIBUJO DE LA ESCALERA &#8212; LAS DOS FORMAS, PARA QUE ESCOJAS</h1>
<div class="row">
 <div class="col"><h2>A &#183; ACOSTADO &#8212; lo que te mand&#233;</h2>"""+bay("A")+"""
  <ul><li>Cuadro de <b>26&#215;26</b>, inclinado con la escalera</li>
      <li><b>15 o 17 piezas</b>, con <b class="big">8 &#225;ngulos distintos</b> de corte</li>
      <li>Los 4 dibujos son <b class="big">DISTINTOS entre s&#237;</b>: 2 de 34&#176; y 2 de 33&#176;</li>
      <li>Si el segundo &#225;ngulo no es 33, <b>hay que rehacer dos</b></li></ul></div>
 <div class="col b"><h2>B &#183; DERECHO &#8212; como el del balc&#243;n, m&#225;s chico</h2>"""+bay("B")+"""
  <ul><li>Cuadro de <b>20&#215;20</b>, parado, flotando bajo el cap inclinado</li>
      <li><b>13 piezas</b>, <b class="big">corte recto y a 45&#176;</b> nada m&#225;s</li>
      <li>Los 4 dibujos son <b class="big">IGUALES</b></li>
      <li><b class="big">No dependen del &#225;ngulo:</b> da igual si el segundo es 33 o 34</li></ul></div>
</div>
<p style="margin-top:12px;font-size:13px"><b>Los dos caben y los dos pasan c&#243;digo.</b>
Solo cambia c&#243;mo se ve y cu&#225;nto trabajo da. Dime <b>A</b> o <b>B</b> y lo dejo listo.</p>
</div></body></html>"""
(H/"railing-escalera-opciones.html").write_text(html,encoding="utf-8")
print("escrito")
