# -*- coding: utf-8 -*-
"""Zarovnani vsech 18 aut na spolecny zaklad podle VW T1 origsize (0x81)."""
import io, json, os, math
import numpy as np
from PIL import Image
BASE="/tmp/claude-0/-home-user-forclaude/a279456f-73fc-5ed8-ace3-5cf5b22fbe35/scratchpad"
os.chdir(BASE+"/auta/s1203modradodavka/sprites")
voz=json.load(io.open(BASE+"/auta_sprity.json"))
SM=["N","NE","E","SE","S","SW","W","NW"]; T=0.5; POMER=0.59   # rozchod/rozvor
AL=[math.radians(45*k) for k in range(8)]; CO=[math.cos(a) for a in AL]; SI=[math.sin(a) for a in AL]
cache={}
def sh(f):
    if f not in cache: cache[f]=np.array(Image.open(f).convert("RGBA"))
    return cache[f]
def mask(s):
    a=sh(s["file"])[s["y"]:s["y"]+s["h"], s["x"]:s["x"]+s["w"]]
    return a[:,:,3]>16
def reg(A,B,r=80):
    best=None; ha,wa=A.shape; hb,wb=B.shape
    A=A.astype(np.float32); B=B.astype(np.float32)
    minpx=0.35*min(A.sum(),B.sum())
    for dy in range(-r,r+1):
        for dx in range(-r,r+1):
            x0=max(0,-dx); x1=min(wa,wb-dx); y0=max(0,-dy); y1=min(ha,hb-dy)
            if x1<=x0 or y1<=y0: continue
            a=A[y0:y1,x0:x1]; b=B[y0+dy:y1+dy,x0+dx:x1+dx]
            sp=float((a*b).sum())
            if sp<minpx: continue
            sj=float(a.sum()+b.sum()-sp); v=sp/sj if sj else 0
            if best is None or v>best[0]: best=(v,dx,dy)
    return best
def pocatek(spr):
    M=[mask(s) for s in spr]
    dno=[int(np.where(m.any(axis=1))[0][-1]) for m in M]
    lev=[int(np.where(m.any(axis=0))[0][0]) for m in M]
    osa={}
    for k in (0,4):
        v,dx,dy=reg(M[k][:,::-1],M[k]); osa[k]=(spr[k]["w"]-1+dx)/2.0
    S={}
    for k in (1,2,3):
        v,dx,dy=reg(M[k][:,::-1],M[8-k]); S[k]=spr[k]["w"]-1+dx
    kol={}
    for k in (2,6):
        p=np.array([(np.where(M[k][:,x])[0][-1] if M[k][:,x].any() else -1) for x in range(spr[k]["w"])])
        u=np.where(p>=p.max()-1)[0]
        sk=[];cur=[u[0]]
        for q in u[1:]:
            if q-cur[-1]<=2: cur.append(q)
            else: sk.append(cur);cur=[q]
        sk.append(cur)
        st=[(c[0]+c[-1])/2.0 for c in sk]
        kol[k]=((min(st)+max(st))/2.0, max(st)-min(st))
    a=(kol[2][1]+kol[6][1])/4.0            # pulka rozvoru
    b=a*POMER
    pu=[0.0]*8
    pu[0]=osa[0]; pu[4]=osa[4]; pu[2]=kol[2][0]; pu[6]=kol[6][0]
    F=pu[2]-lev[2]; R=pu[6]-lev[6]; dif=0.7071*(F-R)
    pu[1]=(S[1]+dif)/2.0; pu[7]=(S[1]-dif)/2.0
    pu[3]=(S[3]+dif)/2.0; pu[5]=(S[3]-dif)/2.0
    pv=[dno[k]-T*(a*abs(CO[k])+b*abs(SI[k])) for k in range(8)]
    return np.array(pu),np.array(pv),2*a,dno
D={}
for vid,jm,spr in voz:
    pu,pv,rozvor,dno=pocatek(spr)
    D[vid]=dict(jm=jm,spr=spr,pu=pu,pv=pv,rozvor=rozvor,
                ax=np.array([-s["xo"] for s in spr],float),
                ay=np.array([-s["yo"] for s in spr],float))
    print("0x%02X %-32s rozvor %5.1f px" % (vid,jm,rozvor))
R=D[0x81]
du=R["ax"]-R["pu"]; dv=R["ay"]-R["pv"]
print("\nVW T1 origsize - kotva proti stredu rozvoru na vozovce:")
print("  %-4s %8s %8s" % ("dir","vodor.","svisle"))
for k in range(8): print("  %-4s %8.1f %8.1f" % (SM[k],du[k],dv[k]))
# jak moc to skace: prolozeni tuhym 3D bodem
Mu=np.array([[1.0,s,c] for c,s in zip(CO,SI)]); Mv=np.array([[1.0,c,s] for c,s in zip(CO,SI)])
cu,*_=np.linalg.lstsq(Mu,du,rcond=None); cv,*_=np.linalg.lstsq(Mv,dv,rcond=None)
print("  zbytky proti tuhemu bodu: vodor %s" % " ".join("%+.0f"%x for x in du-Mu.dot(cu)))
print("                            svisle %s" % " ".join("%+.0f"%x for x in dv-Mv.dot(cv)))
json.dump({str(k):dict(jm=v["jm"],pu=list(v["pu"]),pv=list(v["pv"]),rozvor=v["rozvor"],
                       ax=list(v["ax"]),ay=list(v["ay"])) for k,v in D.items()},
          io.open(BASE+"/vse.json","w"))
