# -*- coding: utf-8 -*-
"""Motor de dibujo SVG -> PNG para las maquetas de MAREA."""
import cairosvg

W = 1440
FONT = "Liberation Sans, DejaVu Sans, sans-serif"
ICON = "DejaVu Sans"

# Paleta
NAVY="#06243B"; NAVY2="#0A2F4E"; OCEAN="#0E7C9B"; TEAL="#13B6C9"; AQUA="#3FE0D0"
AQUASOFT="#D6F7F4"; CORAL="#FF6B6B"; SUNSET="#FF8A5B"; GOLD="#FFC15E"; PINK="#FF5C8A"
INK="#0B1B2B"; SLATE="#5A6B7B"; LINE="#E6ECF1"; CLOUD="#F4F8FB"; SAND="#FFFBF6"; WHITE="#fff"
GREEN="#0a8f5b"; RED="#c0392b"; STAR="#FFB400"

def esc(s):
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

class C:
    def __init__(self, h, bg=WHITE, w=W):
        self.w=w; self.h=h; self.bg=bg; self.defs=[]; self.b=[]; self._i=0
    def uid(self,p="x"): self._i+=1; return f"{p}{self._i}"
    def add(self,*s): self.b.extend(s)
    def grad(self, stops, vertical=True, x1=0,y1=0,x2=0,y2=1):
        i=self.uid("g")
        if vertical: x1,y1,x2,y2=0,0,0,1
        st="".join(f'<stop offset="{o}" stop-color="{c}"/>' for o,c in stops)
        self.defs.append(f'<linearGradient id="{i}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}">{st}</linearGradient>')
        return f"url(#{i})"
    def gradd(self, stops, x1,y1,x2,y2):
        return self.grad(stops, vertical=False, x1=x1,y1=y1,x2=x2,y2=y2)
    # ---- primitivas ----
    def rect(self,x,y,w,h,fill,rx=0,op=1,stroke=None,sw=1.5,sop=1,shadow=False):
        if shadow: self.shadow(x,y,w,h,rx)
        s=f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}"'
        if op!=1: s+=f' opacity="{op}"'
        if stroke: s+=f' stroke="{stroke}" stroke-width="{sw}" stroke-opacity="{sop}"'
        self.b.append(s+"/>")
    def shadow(self,x,y,w,h,rx,dy=14,blur=22,op=0.16):
        fid=self.uid("sh")
        self.defs.append(f'<filter id="{fid}" x="-40%" y="-40%" width="180%" height="180%"><feDropShadow dx="0" dy="{dy}" stdDeviation="{blur}" flood-color="{NAVY}" flood-opacity="{op}"/></filter>')
        self.b.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="#ffffff" filter="url(#{fid})"/>')
    def line(self,x1,y1,x2,y2,stroke=LINE,sw=1.5,op=1):
        self.b.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{sw}" opacity="{op}"/>')
    def circle(self,cx,cy,r,fill,op=1,stroke=None,sw=1.5):
        s=f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" opacity="{op}"'
        if stroke: s+=f' stroke="{stroke}" stroke-width="{sw}"'
        self.b.append(s+"/>")
    def path(self,d,fill="none",op=1,stroke=None,sw=1.5,cap="round",join="round"):
        s=f'<path d="{d}" fill="{fill}" opacity="{op}"'
        if stroke: s+=f' stroke="{stroke}" stroke-width="{sw}" stroke-linecap="{cap}" stroke-linejoin="{join}"'
        self.b.append(s+"/>")
    def text(self,x,y,s,size=15,fill=INK,weight="normal",anchor="start",font=FONT,ls=None,op=1):
        a=f' text-anchor="{anchor}"' if anchor!="start" else ""
        l=f' letter-spacing="{ls}"' if ls else ""
        o=f' opacity="{op}"' if op!=1 else ""
        self.b.append(f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" font-weight="{weight}" fill="{fill}"{a}{l}{o}>{esc(s)}</text>')
    def glyph(self,x,y,s,size,fill,anchor="start",op=1):
        self.text(x,y,s,size=size,fill=fill,anchor=anchor,font=ICON,op=op)
    def stars(self,x,y,size=15,n=5,fill=STAR):
        self.glyph(x,y,"★"*n,size,fill)
    # ---- clip helper ----
    def clip_rect(self,x,y,w,h,rx):
        cid=self.uid("cp")
        self.defs.append(f'<clipPath id="{cid}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}"/></clipPath>')
        return cid
    def clip_top(self,x,y,w,h,r):
        cid=self.uid("cp")
        d=f"M{x} {y+r} Q{x} {y} {x+r} {y} L{x+w-r} {y} Q{x+w} {y} {x+w} {y+r} L{x+w} {y+h} L{x} {y+h} Z"
        self.defs.append(f'<clipPath id="{cid}"><path d="{d}"/></clipPath>')
        return cid
    def gopen(self, clip=None):
        self.b.append(f'<g clip-path="url(#{clip})">' if clip else "<g>")
    def gclose(self): self.b.append("</g>")
    def render(self, path, scale=2):
        svg=(f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" '
             f'viewBox="0 0 {self.w} {self.h}"><rect width="{self.w}" height="{self.h}" fill="{self.bg}"/>'
             f'<defs>{"".join(self.defs)}</defs>{"".join(self.b)}</svg>')
        cairosvg.svg2png(bytestring=svg.encode(), write_to=path, scale=scale)
        return path

# ============ Iconos vectoriales (line style) ============
def ic_pin(c,cx,cy,s,col):
    c.path(f"M{cx} {cy-s} C{cx-s*0.8} {cy-s} {cx-s*0.8} {cy+s*0.2} {cx} {cy+s} C{cx+s*0.8} {cy+s*0.2} {cx+s*0.8} {cy-s} {cx} {cy-s} Z", fill=col)
    c.circle(cx,cy-s*0.25,s*0.28,"#ffffff")
def ic_cal(c,cx,cy,s,col):
    x=cx-s; y=cy-s
    c.rect(x,y+s*0.25,2*s,1.7*s,"none",rx=s*0.25,stroke=col,sw=s*0.18)
    c.line(x,y+s*0.8,x+2*s,y+s*0.8,col,s*0.18)
    c.line(x+s*0.55,y,x+s*0.55,y+s*0.45,col,s*0.18)
    c.line(x+2*s-s*0.55,y,x+2*s-s*0.55,y+s*0.45,col,s*0.18)
def ic_users(c,cx,cy,s,col):
    c.circle(cx-s*0.45,cy-s*0.3,s*0.42,col)
    c.path(f"M{cx-s*1.15} {cy+s} a{s*0.7} {s*0.7} 0 0 1 {s*1.4} 0 Z",fill=col)
    c.circle(cx+s*0.6,cy-s*0.15,s*0.34,col,op=0.7)
    c.path(f"M{cx+s*0.05} {cy+s} a{s*0.6} {s*0.6} 0 0 1 {s*1.1} 0 Z",fill=col,op=0.7)
def ic_ruler(c,cx,cy,s,col):
    c.rect(cx-s,cy-s*0.45,2*s,s*0.9,"none",rx=s*0.18,stroke=col,sw=s*0.18)
    for k in (-0.6,-0.2,0.2,0.6):
        c.line(cx+k*s,cy-s*0.45,cx+k*s,cy-s*0.05,col,s*0.16)
def ic_engine(c,cx,cy,s,col):
    c.rect(cx-s*0.5,cy-s,s*1.0,s*1.4,"none",rx=s*0.2,stroke=col,sw=s*0.18)
    c.line(cx,cy+s*0.4,cx,cy+s,col,s*0.18)
    c.path(f"M{cx-s*0.5} {cy+s} L{cx+s*0.5} {cy+s}",stroke=col,sw=s*0.18)
def ic_shield(c,cx,cy,s,col):
    c.path(f"M{cx} {cy-s} L{cx+s*0.85} {cy-s*0.6} L{cx+s*0.85} {cy+s*0.2} C{cx+s*0.85} {cy+s*0.8} {cx+s*0.4} {cy+s} {cx} {cy+s*1.15} C{cx-s*0.4} {cy+s} {cx-s*0.85} {cy+s*0.8} {cx-s*0.85} {cy+s*0.2} L{cx-s*0.85} {cy-s*0.6} Z",fill=col)
    c.glyph(cx,cy+s*0.45,"✓",s*1.1,"#ffffff",anchor="middle")
def ic_lock(c,cx,cy,s,col):
    c.rect(cx-s*0.7,cy-s*0.15,s*1.4,s*1.1,col,rx=s*0.2)
    c.path(f"M{cx-s*0.45} {cy-s*0.15} L{cx-s*0.45} {cy-s*0.55} a{s*0.45} {s*0.55} 0 0 1 {s*0.9} 0 L{cx+s*0.45} {cy-s*0.15}",stroke=col,sw=s*0.2)
    c.circle(cx,cy+s*0.35,s*0.18,"#ffffff")
def ic_bolt(c,cx,cy,s,col):
    c.path(f"M{cx+s*0.2} {cy-s} L{cx-s*0.5} {cy+s*0.15} L{cx} {cy+s*0.15} L{cx-s*0.2} {cy+s} L{cx+s*0.55} {cy-s*0.2} L{cx} {cy-s*0.2} Z",fill=col)
def ic_headset(c,cx,cy,s,col):
    c.path(f"M{cx-s*0.85} {cy+s*0.1} a{s*0.85} {s*0.85} 0 0 1 {s*1.7} 0",stroke=col,sw=s*0.2)
    c.rect(cx-s*0.95,cy+s*0.05,s*0.45,s*0.75,col,rx=s*0.12)
    c.rect(cx+s*0.5,cy+s*0.05,s*0.45,s*0.75,col,rx=s*0.12)
    c.path(f"M{cx+s*0.72} {cy+s*0.8} a{s*0.9} {s*0.6} 0 0 1 {-s*0.9} {s*0.55}",stroke=col,sw=s*0.18)
def ic_card(c,cx,cy,s,col):
    c.rect(cx-s,cy-s*0.7,2*s,1.4*s,"none",rx=s*0.2,stroke=col,sw=s*0.18)
    c.line(cx-s,cy-s*0.2,cx+s,cy-s*0.2,col,s*0.22)
    c.line(cx-s*0.7,cy+s*0.35,cx-s*0.1,cy+s*0.35,col,s*0.16)
def ic_doc(c,cx,cy,s,col):
    c.path(f"M{cx-s*0.7} {cy-s} L{cx+s*0.35} {cy-s} L{cx+s*0.7} {cy-s*0.6} L{cx+s*0.7} {cy+s} L{cx-s*0.7} {cy+s} Z",fill="none",stroke=col,sw=s*0.18)
    for k in (-0.35,0,0.35):
        c.line(cx-s*0.4,cy+k*s,cx+s*0.4,cy+k*s,col,s*0.14)

# ============ Escena de bote (la "foto") ============
PALETTES={
 "sunset":[("0","#FFD27D"),("0.55","#FF9E6B"),("1","#FF7E9D")],
 "day":   [("0","#8FD8F2"),("1","#D6F0FB")],
 "golden":[("0","#FFE08A"),("1","#FF9E6B")],
 "teal":  [("0","#62D8CC"),("1","#2BA9C9")],
 "dusk":  [("0","#9AA8E0"),("0.5","#FF9CB0"),("1","#FFC98A")],
 "blue":  [("0","#6FC6EE"),("1","#2C8FC0")],
}
SEAS={
 "sunset":[("0","#1BB3CC"),("1","#0B6C8A")],
 "day":   [("0","#1FBBD0"),("1","#0E7C9B")],
 "golden":[("0","#16A9C2"),("1","#0A6A86")],
 "teal":  [("0","#19C3CE"),("1","#0C7C92")],
 "dusk":  [("0","#1C9BC0"),("1","#0A5A78")],
 "blue":  [("0","#23A6D6"),("1","#0E6A92")],
}

def boat_scene(c,x,y,w,h,kind="yacht",sky="sunset",clip=None):
    cid=clip if clip else c.clip_rect(x,y,w,h,18)
    c.gopen(cid)
    wl=y+h*0.62
    skyg=c.grad(PALETTES.get(sky,PALETTES["sunset"]))
    seag=c.grad(SEAS.get(sky,SEAS["sunset"]))
    c.rect(x,y,w,wl-y,skyg)
    # sol
    c.circle(x+w*0.80,y+h*0.26,h*0.13,"#FFF6DD",op=0.9)
    c.circle(x+w*0.80,y+h*0.26,h*0.20,"#FFF6DD",op=0.18)
    c.rect(x,wl,w,y+h-wl,seag)
    # brillo del sol en agua
    c.rect(x+w*0.72,wl,w*0.16,y+h-wl,"#FFF1C9",op=0.16)
    cx=x+w*0.5
    _silhouette(c,kind,x,y,w,h,wl,cx)
    # reflejo
    c.rect(x+w*0.30,wl,w*0.40,3,"#ffffff",op=0.35)
    c.gclose()

def _silhouette(c,kind,x,y,w,h,wl,cx):
    white="#FFFFFF"; dark="#16384B"; glass="#9FD6E6"
    if kind=="yacht":
        bw=w*0.62; bx=cx-bw/2
        # casco
        c.path(f"M{bx} {wl-h*0.02} L{bx+bw} {wl-h*0.02} L{bx+bw-w*0.05} {wl+h*0.10} L{bx+w*0.04} {wl+h*0.10} Z",fill=white)
        c.path(f"M{bx} {wl-h*0.02} L{bx+bw} {wl-h*0.02} L{bx+bw} {wl+h*0.0} L{bx} {wl+h*0.0} Z",fill=NAVY)
        # cubierta 1
        c.rect(bx+bw*0.10,wl-h*0.16,bw*0.74,h*0.15,white,rx=4)
        for i in range(6):
            c.rect(bx+bw*0.16+i*bw*0.105,wl-h*0.125,bw*0.07,h*0.07,glass,rx=2)
        # cubierta 2 (puente)
        c.rect(bx+bw*0.22,wl-h*0.27,bw*0.42,h*0.12,white,rx=4)
        for i in range(4):
            c.rect(bx+bw*0.26+i*bw*0.095,wl-h*0.24,bw*0.06,h*0.06,glass,rx=2)
        # antena/radar
        c.line(cx,wl-h*0.27,cx,wl-h*0.36,dark,2)
        c.circle(cx,wl-h*0.37,h*0.012,dark)
    elif kind=="console":
        bw=w*0.60; bx=cx-bw/2
        c.path(f"M{bx} {wl-h*0.05} L{bx+bw} {wl-h*0.05} L{bx+bw-w*0.04} {wl+h*0.08} L{bx+w*0.06} {wl+h*0.08} Z",fill=white)
        c.rect(bx,wl-h*0.05,bw,h*0.02,NAVY)
        # consola central + T-top
        c.rect(cx-bw*0.10,wl-h*0.20,bw*0.20,h*0.16,"#E9EEF1",rx=3)
        c.rect(cx-bw*0.04,wl-h*0.16,bw*0.08,h*0.07,glass,rx=2)
        c.line(cx-bw*0.13,wl-h*0.20,cx-bw*0.13,wl-h*0.31,dark,3)
        c.line(cx+bw*0.13,wl-h*0.20,cx+bw*0.13,wl-h*0.31,dark,3)
        c.rect(cx-bw*0.17,wl-h*0.33,bw*0.34,h*0.025,"#1f4d63",rx=3)
        # motores fuera de borda
        c.rect(bx+bw-bw*0.02,wl-h*0.06,bw*0.05,h*0.14,dark,rx=2)
    elif kind=="pontoon":
        bw=w*0.60; bx=cx-bw/2
        c.rect(bx,wl-h*0.02,bw,h*0.06,white)            # cubierta
        c.circle(bx+bw*0.10,wl+h*0.06,h*0.04,"#33586b")  # tubos
        c.circle(bx+bw*0.90,wl+h*0.06,h*0.04,"#33586b")
        c.rect(bx,wl+h*0.04,bw,h*0.03,"#33586b")
        # barandas
        c.rect(bx,wl-h*0.07,bw,h*0.05,"none",rx=2,stroke="#7fa6b6",sw=2)
        # bimini
        c.rect(bx+bw*0.18,wl-h*0.20,bw*0.5,h*0.04,c.grad([("0",TEAL),("1",OCEAN)]),rx=4)
        c.line(bx+bw*0.20,wl-h*0.16,bx+bw*0.20,wl-h*0.04,"#7fa6b6",2.5)
        c.line(bx+bw*0.64,wl-h*0.16,bx+bw*0.64,wl-h*0.04,"#7fa6b6",2.5)
    elif kind=="sail":
        bw=w*0.46; bx=cx-bw/2
        c.path(f"M{bx} {wl-h*0.02} L{bx+bw} {wl-h*0.02} L{bx+bw-w*0.03} {wl+h*0.07} L{bx+w*0.03} {wl+h*0.07} Z",fill=white)
        c.rect(bx,wl-h*0.02,bw,h*0.015,NAVY)
        mx=cx; top=wl-h*0.46
        c.line(mx,wl-h*0.02,mx,top,dark,3)
        c.path(f"M{mx-3} {top+6} L{mx-3} {wl-h*0.05} L{mx-bw*0.42} {wl-h*0.05} Z",fill=white)      # mayor
        c.path(f"M{mx+3} {top+18} L{mx+3} {wl-h*0.05} L{mx+bw*0.34} {wl-h*0.05} Z",fill="#FFD7E2")  # foque
    elif kind=="cat":
        bw=w*0.58; bx=cx-bw/2
        c.path(f"M{bx} {wl-h*0.0} L{bx+bw*0.34} {wl-h*0.0} L{bx+bw*0.30} {wl+h*0.09} L{bx+bw*0.04} {wl+h*0.09} Z",fill=white)
        c.path(f"M{bx+bw*0.66} {wl-h*0.0} L{bx+bw} {wl-h*0.0} L{bx+bw*0.96} {wl+h*0.09} L{bx+bw*0.70} {wl+h*0.09} Z",fill=white)
        c.rect(bx+bw*0.06,wl-h*0.14,bw*0.88,h*0.14,white,rx=6)
        for i in range(6):
            c.rect(bx+bw*0.12+i*bw*0.13,wl-h*0.11,bw*0.08,h*0.07,glass,rx=2)
        c.line(cx,wl-h*0.14,cx,wl-h*0.42,dark,3)
        c.path(f"M{cx-3} {wl-h*0.42} L{cx-3} {wl-h*0.16} L{cx-bw*0.30} {wl-h*0.16} Z",fill=white)
    elif kind=="sport":
        bw=w*0.60; bx=cx-bw/2
        c.path(f"M{bx} {wl-h*0.04} L{bx+bw} {wl-h*0.10} L{bx+bw-w*0.04} {wl+h*0.07} L{bx+w*0.05} {wl+h*0.07} Z",fill=white)
        c.path(f"M{bx} {wl-h*0.04} L{bx+bw} {wl-h*0.10} L{bx+bw} {wl-h*0.05} L{bx} {wl+h*0.0} Z",fill=c.grad([("0",PINK),("1",CORAL)],vertical=False,x1=0,y1=0,x2=1,y2=0))
        # parabrisas
        c.path(f"M{cx-bw*0.06} {wl-h*0.05} L{cx+bw*0.18} {wl-h*0.05} L{cx+bw*0.12} {wl-h*0.18} L{cx-bw*0.02} {wl-h*0.18} Z",fill=glass)
