import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); TOOLS = os.path.dirname(HERE); ROM = os.environ.get("BFBB_ROM", "baserom.gba")
import sys, json
sys.path.insert(0,TOOLS); sys.path.insert(0,HERE)
from emu import *
import run as RM, numpy as np
rom,room,out=sys.argv[1],int(sys.argv[2]),sys.argv[3]
px,py=int(sys.argv[4]),int(sys.argv[5])
e=Emu(rom); RM._e=e
e.run(600); e.tap(START,5,60); e.tap(START,5,90)
t=e.r32(0x200036c); l=e.r32(t+4); e.w32(l+8, 0x803c758+0x20*room)
for i in range(6): e.tap(A,10,20)
for i in range(40): e.tap(A,10,30)
e.run(60)
st=e.save(); 
P=RM.find_player(e,room) if True else None
ims=[]
for f in range(1,121):
    if P: e.w32(P,px<<8); e.w32(P+4,py<<8); e.w32(P+0x274,0)
    e.run(1)
    if f in (20,60,120): ims.append(np.array(RM.grab(e)))
np.save(out,np.stack(ims)); print("CAM",e.r16(0x2003d24),e.r16(0x2003d26),e.r16(0x2003d28),e.r16(0x2003d2a))
