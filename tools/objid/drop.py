import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); TOOLS = os.path.dirname(HERE); ROM = os.environ.get("BFBB_ROM", "baserom.gba")
import sys,json
sys.path.insert(0,HERE)
import ident as I, run as RM
res=json.load(open(os.path.join(HERE,'out','all.json')))
for t in sys.argv[1:]:
    r=res[t]
    for keep in (r['idx'],-1):
        e=I._get(); O=I.objs(r['room'])
        I.set_types(e,r['room'],[o[1] if (o[1]==0 or o[0]==keep) else 1 for o in O])
        e.load(RM._cache['base']); tt=e.r32(0x200036c); l=e.r32(tt+4); e.w32(l+8,0x803c758+0x20*r['room'])
        for i in range(6): e.tap(I.A,10,20)
        for i in range(40): e.tap(I.A,10,30)
        e.run(60); P=RM.find_player(e,r['room'])
        ys=[]
        for f in range(150):
            if f<3: e.w32(P,r['x']<<8); e.w32(P+4,(r['y']-48)<<8); e.w32(P+0x274,0)
            e.run(1); ys.append(I.s32(e.r32(P+4))>>8)
        I.set_types(e,r['room'],[o[1] for o in O])
        print(t,'with' if keep>=0 else 'w/o ', 'y0',r['y'],'min',min(ys),'final',ys[-1], ys[::15])
