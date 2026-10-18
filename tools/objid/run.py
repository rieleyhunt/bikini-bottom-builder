import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); TOOLS = os.path.dirname(HERE); ROM = os.environ.get("BFBB_ROM", "baserom.gba")
import sys, os, json, struct
sys.path.insert(0,TOOLS)
from emu import *
from PIL import Image, ImageDraw
s32=lambda v: v-(1<<32) if v&0x80000000 else v
R=open(ROM,'rb').read()
U=lambda a:struct.unpack_from('<I',R,a-0x8000000)[0]
H=lambda a:struct.unpack_from('<H',R,a-0x8000000)[0]
def objs(room):
    oh=U(0x803c758+0x20*room+24); n=U(oh); l=U(oh+4)
    return [(i,H(l+8*i),H(l+8*i+2),H(l+8*i+4),H(l+8*i+6)) for i in range(n)]
_e=None; _cache={}
def boot(room, rom=ROM):
    global _e
    if _e is None: _e=Emu(rom)
    e=_e
    if room in _cache: e.load(_cache[room]); return e
    e.lib.bf_init(rom.encode()) if False else None
    if 'base' not in _cache:
        e.run(600); e.tap(START,5,60); e.tap(START,5,90); _cache['base']=e.save()
    e.load(_cache['base'])
    t=e.r32(0x200036c); l=e.r32(t+4); e.w32(l+8, 0x803c758+0x20*room)
    for i in range(6): e.tap(A,10,20)
    for i in range(40): e.tap(A,10,30)
    e.run(60)
    _cache[room]=e.save(); return e
def grab(e): return Image.frombuffer("RGBA",(240,160),bytes(e.lib.bf_vbuf().contents),"raw","RGBA",0,1).convert("RGB")
def view(room, x, y, dx=-56, frames=(20,50,80), hold=True):
    e=boot(room)
    ims=[]; f=0
    for target in frames:
        while f<target:
            if hold: e.w32(0x201d154,(x+dx)<<8); e.w32(0x201d158,y<<8)
            e.run(1); f+=1
        ims.append(grab(e))
    return ims
if __name__=='__main__':
    room=int(sys.argv[1]); 
    e=boot(room); print('player',s32(e.r32(0x201d154))>>8,s32(e.r32(0x201d158))>>8)
    for o in objs(room)[:40]: print(o)
import numpy as _np
def find_player(e, room):
    st=[o for o in objs(room) if o[1]==0]
    w=_np.frombuffer(e.read(0x2000000,0x3f000),dtype=_np.int32)
    cands=[]
    for i in range(len(w)-1):
        x,y=int(w[i]),int(w[i+1])
        if x<=0 or y<=0 or x&0xff and False: continue
        for o in st:
            if abs((x>>8)-o[2])<8 and abs((y>>8)-o[3])<40: cands.append(0x2000000+4*i); break
    # test: hold RIGHT and see which moves right
    s=e.save(); before={a:e.r32(a) for a in cands}
    e.run(20,RIGHT); good=[a for a in cands if (e.r32(a)-before[a])>0x200 and (e.r32(a)-before[a])<0x8000]
    e.load(s)
    return good[0] if good else None
