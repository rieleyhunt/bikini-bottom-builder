import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); TOOLS = os.path.dirname(HERE); ROM = os.environ.get("BFBB_ROM", "baserom.gba")
import sys, json, base64, io
sys.path.insert(0,HERE)
import numpy as np
from PIL import Image
P=json.load(open(os.path.join(HERE,'work')+'/place.json'))
base=np.load(os.path.join(HERE,'work')+'/base.npy')
OUT={}
def icon_from(a,b,ax,ay,t,src):
    d=np.abs(a.astype(int)-b.astype(int)).sum(2)>30; d[138:]=False
    ys,xs=np.nonzero(d)
    if not len(xs): return None
    # keep pixels within 72px of anchor to drop far-away side effects
    keep=(np.abs(xs-ax)<72)&(np.abs(ys-ay)<72)
    xs,ys=xs[keep],ys[keep]
    if not len(xs): return None
    x0,x1,y0,y1=xs.min(),xs.max()+1,ys.min(),ys.max()+1
    rgba=np.zeros((y1-y0,x1-x0,4),np.uint8)
    rgba[ys-y0,xs-x0,:3]=a[ys,xs]; rgba[ys-y0,xs-x0,3]=255
    im=Image.fromarray(rgba); im.save(os.path.join(HERE,'icons',f'{t}.png'))
    buf=io.BytesIO(); im.save(buf,'PNG',optimize=True)
    return {'src':src,'dx':int(x0-ax),'dy':int(y0-ay),'w':int(x1-x0),'h':int(y1-y0),'png':base64.b64encode(buf.getvalue()).decode()}
native=[]
for t,v in P.items():
    t=int(t)
    if v['box'] and v['frac']<0.15:
        a=np.load(fos.path.join(HERE,'work')+'/t{t}.npy')[0]
        r=icon_from(a,base[0],200-10,200-152,t,'room0')
        if r: OUT[t]=r; continue
    native.append(t)
print('native needed',native)
import ident as I
res=json.load(open(os.path.join(HERE,'out','all.json')))
for t in native:
    r=res.get(str(t))
    if not r: continue
    a=I.run_case(r['room'],r['idx'],r['x'],r['y'],-72,(20,)); cam=I.CAMS[0]
    b=I.run_case(r['room'],-1,r['x'],r['y'],-72,(20,))
    ic=icon_from(a[0],b[0],r['x']-cam[0],r['y']-cam[1],t,'room%d'%r['room'])
    if ic: OUT[t]=ic
    print(t, 'ok' if ic else 'none', cam)
json.dump(OUT,open(os.path.join(HERE,'icons.json'),'w'))
print(len(OUT), sum(len(v['png']) for v in OUT.values()))
