import sys, os, json, subprocess, numpy as np
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from ents import boot_track
import importlib
room=int(sys.argv[1]); vals=[int(v) for v in sys.argv[2].split(',')]
os.makedirs('work',exist_ok=True)
CORE=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','editor','core.js').replace(os.sep,'/')
BB_JS="""const BB=require('CORE_PATH');const fs=require('fs');
const [room,vals,out]=process.argv.slice(2);const V=JSON.parse(vals);
const src=new Uint8Array(fs.readFileSync((process.env.BFBB_ROM||'baserom.gba')));const r=BB.loadRoom(new BB.Rom(src),+room);
for(let k=0;k<r.col.cells.length;k++) if(V.includes(r.col.cells[k])) r.col.cells[k]=0;
r.dirty={col:true};const rooms=[];rooms[+room]=r;fs.writeFileSync(out,BB.exportRom(src,rooms));"""
open('work/strip.js','w').write(BB_JS.replace('CORE_PATH',CORE))
roms={'base':f'work/r{room}_base.gba'}
subprocess.run(['node','work/strip.js',str(room),'[]',roms['base']],check=True)
for v in vals:
    roms[v]=f'work/r{room}_no{v}.gba'; subprocess.run(['node','work/strip.js',str(room),json.dumps([v]),roms[v]],check=True)
# enemy list from base
import run as RM
O=[o for o in RM.objs(room) if 37<=o[1]<=59 or 66<=o[1]<=79]
res={}
for o in O[:int(sys.argv[3]) if len(sys.argv)>3 else 8]:
    _,ty,x,y,p=o; hold=[x-80,y-30]
    row=[]
    for k,rom in roms.items():
        ents,tr=boot_track(rom,room,hold,frames=500,step=5)
        idx=[i for i,(en,t,ox,oy,of) in enumerate(ents) if t==ty and ox==x and oy==y]
        if not idx: row.append((k,None)); continue
        t=tr[:,idx[0]]; row.append((k,(int(t[:,0].min()),int(t[:,0].max()),int(t[:,1].min()),int(t[:,1].max()))))
    print(ty,x,y,row,flush=True)
