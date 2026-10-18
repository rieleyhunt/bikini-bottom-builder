import sys, json, struct
import os; HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,os.path.join(HERE,'..')); sys.path.insert(0,os.path.join(HERE,'..','objid'))
from emu import *
import run as RM, numpy as np
s32=lambda v: v-(1<<32) if v&0x80000000 else v
def run(rom, room, script, shots=()):
    """script: list of (frames, keys, teleport(x,y) or None)"""
    e=Emu(rom); RM._e=e
    e.run(600); e.tap(START,5,60); e.tap(START,5,90)
    t=e.r32(0x200036c); l=e.r32(t+4); e.w32(l+8, 0x803c758+0x20*room)
    for i in range(6): e.tap(A,10,20)
    for i in range(40): e.tap(A,10,30)
    e.run(60)
    P=RM.find_player(e,room)
    tr=[]; ims={}; f=0
    for n,keys,tp in script:
        for i in range(n):
            if tp and i<3: e.w32(P,tp[0]<<8); e.w32(P+4,tp[1]<<8); e.w32(P+0x274,0)
            e.run(1,keys); f+=1
            tr.append((s32(e.r32(P))>>8, s32(e.r32(P+4))>>8))
            if f in shots: ims[f]=np.array(RM.grab(e))
    return tr, ims, np.array(RM.grab(e))
if __name__=='__main__':
    rom,room,out=sys.argv[1],int(sys.argv[2]),sys.argv[3]
    script=json.loads(sys.argv[4]); shots=json.loads(sys.argv[5]) if len(sys.argv)>5 else []
    tr,ims,last=run(rom,room,[(a,b,c) for a,b,c in script],set(shots))
    np.savez_compressed(out, tr=np.array(tr), last=last, **{f's{k}':v for k,v in ims.items()})
