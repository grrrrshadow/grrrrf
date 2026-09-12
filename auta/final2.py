# -*- coding: utf-8 -*-
"""Tuhe (3D konzistentni) zarovnani spritu: VW T1 a Skoda 1203."""
import io, json, os, math
import numpy as np
from PIL import Image
BASE = "/tmp/claude-0/-home-user-forclaude/a279456f-73fc-5ed8-ace3-5cf5b22fbe35/scratchpad"
os.chdir(BASE + "/auta/s1203modradodavka/sprites")
voz = json.load(io.open(BASE + "/auta_sprity.json"))
SM = ["N","NE","E","SE","S","SW","W","NW"]
AL = [math.radians(45*k) for k in range(8)]
CO = [math.cos(a) for a in AL]; SI = [math.sin(a) for a in AL]
cache={}
def sh(f):
    if f not in cache: cache[f]=np.array(Image.open(f).convert("RGBA"))
    return cache[f]
def mask(s):
    a=sh(s["file"])[s["y"]:s["y"]+s["h"], s["x"]:s["x"]+s["w"]]
    return a[:,:,3]>16
def reg(Af,Bf,r=80):
    """posun (dx,dy) s nejvetsim IoU; vyzaduje slusny prekryv"""
    best=None; ha,wa=Af.shape; hb,wb=Bf.shape
    Af=Af.astype(np.float32); Bf=Bf.astype(np.float32)
    minpx=0.35*min(Af.sum(),Bf.sum())
    for dy in range(-r,r+1):
        for dx in range(-r,r+1):
            x0=max(0,-dx); x1=min(wa,wb-dx); y0=max(0,-dy); y1=min(ha,hb-dy)
            if x1<=x0 or y1<=y0: continue
            a=Af[y0:y1,x0:x1]; b=Bf[y0+dy:y1+dy,x0+dx:x1+dx]
            sp=float((a*b).sum())
            if sp<minpx: continue
            sj=float(a.sum()+b.sum()-sp)
            v=sp/sj if sj else 0
            if best is None or v>best[0]: best=(v,dx,dy)
    return best

def pocatky(spr):
    M=[mask(s) for s in spr]
    dno=[int(np.where(m.any(axis=1))[0][-1]) for m in M]
    lev=[int(np.where(m.any(axis=0))[0][0]) for m in M]
    osa={}
    for k in (0,4):
        v,dx,dy=reg(M[k][:,::-1], M[k]); osa[k]=(spr[k]["w"]-1+dx)/2.0
    S={}
    for k in (1,2,3):
        v,dx,dy=reg(M[k][:,::-1], M[8-k]); S[k]=spr[k]["w"]-1+dx
    kol={}
    for k in (2,6):
        s=spr[k]; m=M[k]
        prof=np.array([(np.where(m[:,x])[0][-1] if m[:,x].any() else -1) for x in range(s["w"])])
        u=np.where(prof>=prof.max()-1)[0]
        sk=[]; cur=[u[0]]
        for p in u[1:]:
            if p-cur[-1]<=2: cur.append(p)
            else: sk.append(cur); cur=[p]
        sk.append(cur)
        st=[(c[0]+c[-1])/2.0 for c in sk]
        kol[k]=((min(st)+max(st))/2.0, max(st)-min(st))
    po=[0.0]*8
    po[0]=osa[0]; po[4]=osa[4]; po[2]=kol[2][0]; po[6]=kol[6][0]
    F=po[2]-lev[2]; R=po[6]-lev[6]; dif=0.7071*(F-R)
    po[1]=(S[1]+dif)/2.0; po[7]=(S[1]-dif)/2.0
    po[3]=(S[3]+dif)/2.0; po[5]=(S[3]-dif)/2.0
    return M,dno,po,kol[2][1]

Bm=np.array([[1.0,s,c] for c,s in zip(CO,SI)])
Am=np.array([[max(c,0),max(-c,0),abs(s)] for c,s in zip(CO,SI)])
vys={}
for cil,nm in ((0x80,"VW T1"),(0x82,"Skoda 1203")):
    for vid,jm,spr in voz:
        if vid!=cil: continue
        M,dno,po,rozvor=pocatky(spr)
        ax=[-s["xo"] for s in spr]; ay=[-s["yo"] for s in spr]
        du=np.array([ax[k]-po[k] for k in range(8)])
        bu,*_=np.linalg.lstsq(Bm,du,rcond=None)
        d=np.array([dno[k]-ay[k] for k in range(8)],float)
        par,*_=np.linalg.lstsq(Am,d,rcond=None)
        vys[cil]=dict(spr=spr,M=M,dno=dno,po=po,ax=ax,ay=ay,bu=bu,par=par,rozvor=rozvor,d=d,du=du)

T=vys[0x80]; S=vys[0x82]
lam = S["rozvor"]/T["rozvor"]
print("Merítko: rozvor VW T1 %.1f px, Skoda %.1f px -> Skoda je %.0f %% vetsi"
      % (T["rozvor"], S["rozvor"], (lam-1)*100))
print()
for cil,nm in ((0x80,"VW T1"),(0x82,"Skoda 1203")):
    v=vys[cil]
    if cil==0x80:
        bu, par = v["bu"], v["par"]
    else:
        bu, par = T["bu"]*lam, T["par"]*lam     # konvence VW T1, preskalovana
    novx=[v["po"][k]+Bm[k].dot(bu) for k in range(8)]
    novy=[v["dno"][k]-Am[k].dot(par) for k in range(8)]
    v["novx"]=novx; v["novy"]=novy; v["bu2"]=list(bu); v["par2"]=list(par)
    print("=== %s ===" % nm)
    print("  posun kotvy proti pocatku: C=%.1f podel=%.1f napric=%.1f | svisle A+=%.1f A-=%.1f Q=%.1f"
          % (bu[0],bu[1],bu[2],par[0],par[1],par[2]))
    print("  %-3s | %5s %5s | %7s %7s | %7s %7s | %s" %
          ("dir","w","h","xoffs","novy","yoffs","novy","posun"))
    for k in range(8):
        nx=-int(round(novx[k])); ny=-int(round(novy[k]))
        print("  %-3s | %5d %5d | %7d %7d | %7d %7d | %+d,%+d" %
              (SM[k], v["spr"][k]["w"], v["spr"][k]["h"],
               v["spr"][k]["xo"], nx, v["spr"][k]["yo"], ny,
               nx-v["spr"][k]["xo"], ny-v["spr"][k]["yo"]))
    print()
json.dump({str(c):dict(po=vys[c]["po"],novx=vys[c]["novx"],novy=vys[c]["novy"],
                       ax=vys[c]["ax"],ay=vys[c]["ay"],dno=vys[c]["dno"],
                       rozvor=vys[c]["rozvor"]) for c in vys}, io.open(BASE+"/oprava.json","w"))
