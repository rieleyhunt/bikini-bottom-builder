import sys, json
import os; HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,os.path.join(HERE,'..')); sys.path.insert(0,os.path.join(HERE,'..','objid'))
from emu import *
import run as RM, numpy as np
s32=lambda v: v-(1<<32) if v&0x80000000 else v
def boot_track(rom, room, hold=None, frames=600, step=10):
    e=Emu(rom); RM._e=e
    e.run(600); e.tap(START,5,60); e.tap(START,5,90)
    t=e.r32(0x200036c); l=e.r32(t+4); e.w32(l+8, 0x803c758+0x20*room)
    for i in range(6): e.tap(A,10,20)
    for i in range(40): e.tap(A,10,30)
    e.run(60); P=RM.find_player(e,room)
    ents=[]
    w=np.frombuffer(e.read(0x2000000,0x3f000),dtype=np.int32)
    xs=w>>8
    for o in RM.objs(room):
        _,ty,ox,oy,p=o
        if not (37<=ty<=59 or 66<=ty<=79): continue
        c=np.nonzero(np.abs(xs[:-1]-ox)<=2)[0]
        c=[i for i in c if abs(int(w[i+1]>>8)-oy)<=12]
        if c: ents.append((0x2000000+4*int(c[0]),ty,ox,oy,0))
    tr=[]
    for f in range(frames):
        if hold: e.w32(P,hold[0]<<8); e.w32(P+4,hold[1]<<8)
        e.run(1)
        if f%step==0: tr.append([(s32(e.r32(en+o))>>8, s32(e.r32(en+o+4))>>8) if o is not None else (0,0) for en,ty,ox,oy,o in ents])
    return ents, np.array(tr)
if __name__=='__main__':
    ents,tr=boot_track(sys.argv[1],int(sys.argv[2]),json.loads(sys.argv[4]) if len(sys.argv)>4 else None)
    np.savez(sys.argv[3],ents=np.array([[a,b,c,d,(o if o is not None else -1)] for a,b,c,d,o in ents]),tr=tr)
    for k,(en,ty,ox,oy,o) in enumerate(ents): print(ty,ox,oy,o, tr[0][k].tolist(), tr[-1][k].tolist(), 'xrange',tr[:,k,0].min(),tr[:,k,0].max())
