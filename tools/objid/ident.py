import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); TOOLS = os.path.dirname(HERE); ROM = os.environ.get("BFBB_ROM", "baserom.gba")
import sys, os, json, struct
sys.path.insert(0,TOOLS); sys.path.insert(0,HERE)
from run import *
import numpy as np
from collections import defaultdict
OUT=os.path.join(HERE,'out'); os.makedirs(OUT,exist_ok=True)
def objlist(room):
    oh=U(0x803c758+0x20*room+24); return U(oh+4)
def set_types(e, room, types):
    l=objlist(room)
    for i,t in enumerate(types):
        e.lib.bf_romw8(l+8*i, t&255); e.lib.bf_romw8(l+8*i+1, t>>8)
def run_case(room, keep_idx, x, y, dx, frames, holdn=10**9, dy=0):
    e=boot(-1) if False else None
    e=_get()
    O=objs(room)
    types=[o[1] if (o[1]==0 or o[0]==keep_idx) else 1 for o in O]
    set_types(e, room, types)
    e.load(_cache['base'])
    t=e.r32(0x200036c); l=e.r32(t+4); e.w32(l+8, 0x803c758+0x20*room)
    for i in range(6): e.tap(A,10,20)
    for i in range(40): e.tap(A,10,30)
    e.run(60)
    import run as RM
    P=RM.find_player(e, room)
    if P is None: raise Exception('no player')
    ims=[]; f=0; CAMS.clear()
    for target in frames:
        while f<target:
            if f<holdn: e.w32(P,(x+dx)<<8); e.w32(P+4,(y+dy)<<8); e.w32(P+0x274,0)
            e.run(1); f+=1
        ims.append(np.array(grab(e))); CAMS.append((e.r16(0x2003d24),e.r16(0x2003d26)))
    set_types(e, room, [o[1] for o in O])
    return ims
def _get():
    global _e
    import run as RM
    if RM._e is None:
        RM._e=Emu(ROM); e=RM._e
        e.run(600); e.tap(START,5,60); e.tap(START,5,90); RM._cache['base']=e.save()
    return RM._e
from run import _cache
FR=(15,45,90)
CAMS=[]
def ident(ty, room, idx, x, y, dx=-72):
    a=run_case(room, idx, x, y, dx, FR)
    b=run_case(room, -1, x, y, dx, FR)
    out=[]
    for A_,B_ in zip(a,b):
        d=np.abs(A_.astype(int)-B_.astype(int)).sum(2)>30
        d[138:]=False
        im=Image.fromarray(A_); dr=ImageDraw.Draw(im)
        ys,xs=np.nonzero(d)
        box=None
        if len(xs): box=(int(xs.min()),int(ys.min()),int(xs.max()),int(ys.max())); dr.rectangle(box,outline=(255,0,0))
        out.append((im,box))
    return out
if __name__=='__main__':
    import run as RM
    RM._e=None
    # pick examples
    ex=defaultdict(list)
    for room in range(112):
        try: O=objs(room)
        except Exception: continue
        for o in O: ex[o[1]].append((room,)+o)
    todo=[int(a) for a in sys.argv[1:]] or sorted(ex)
    res={}
    for ty in todo:
        if ty==0 or not ex[ty]: continue
        out=None
        for cand in ex[ty][:6]:
            room,idx,_,x,y,prop=cand
            try: out=ident(ty,room,idx,x,y)
            except Exception as err: print(ty,room,'ERR',err); continue
            if any(b for _,b in out) or cand==ex[ty][:6][-1]: break
        if out is None: continue
        row=Image.new('RGB',(720,160))
        for j,(im,box) in enumerate(out): row.paste(im,(j*240,0))
        ImageDraw.Draw(row).text((3,3),f'type {ty} room {room} prop {prop}',fill=(255,0,0))
        row.save(f'{OUT}/{ty:03d}.png'); res[ty]={'room':room,'idx':idx,'x':x,'y':y,'prop':prop,'boxes':[b for _,b in out]}
        print(ty,room,res[ty]['boxes'],flush=True)
    json.dump(res,open(f'{OUT}/res_{todo[0]}.json','w'))
