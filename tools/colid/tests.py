import json, subprocess, sys, os
from concurrent.futures import ThreadPoolExecutor
D='work'; os.makedirs(D,exist_ok=True)
def edits(kind,v):
    if kind=='F': return [[x,31,v] for x in range(13,21)]
    if kind=='C': return [[x,24,v] for x in range(13,21)]
    if kind=='W': return [[17,y,v] for y in range(25,31)]
    if kind=='O': return [[x,y,v] for x in range(14,20) for y in range(25,31)]
SCRIPTS={
 'F':  ('F',[[60,0,[136,200]],[60,0,None]],[]),
 'C':  ('C',[[30,0,[136,230]],[25,1,None],[45,0,None]],[]),
 'WR': ('W',[[10,0,[110,230]],[60,16,None]],[]),
 'WL': ('W',[[10,0,[160,230]],[60,32,None]],[]),
 'O':  ('O',[[120,0,[136,230]],[60,64,None],[40,128,None],[25,1,None],[45,0,None]],[30,90,150,200,260]),
}
def job(v,name):
    kind,script,shots=SCRIPTS[name]
    rom=f'{D}/{kind}{v}.gba'
    if not os.path.exists(rom):
        subprocess.run(['node','gen_col.js','0',json.dumps(edits(kind,v) if v>=0 else []),rom],check=True)
    subprocess.run(['python3','scen.py',rom,'0',f'{D}/{name}_{v}',json.dumps(script),json.dumps(shots)],check=True,capture_output=True)
    return v,name
vals=[int(a) for a in sys.argv[1:]] or list(range(-1,16))
# build ROMs first serially per kind to avoid races
for v in vals:
    for kind in 'FCWO':
        rom=f'{D}/{kind}{v}.gba'
        if not os.path.exists(rom): subprocess.run(['node','gen_col.js','0',json.dumps(edits(kind,v) if v>=0 else []),rom],check=True)
with ThreadPoolExecutor(6) as ex:
    for r in ex.map(lambda a: job(*a), [(v,n) for v in vals for n in SCRIPTS]): pass
print('done')
