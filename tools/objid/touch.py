import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); TOOLS = os.path.dirname(HERE); ROM = os.environ.get("BFBB_ROM", "baserom.gba")
import sys,json
sys.path.insert(0,HERE)
import ident as I
from PIL import Image, ImageDraw
res=json.load(open(os.path.join(HERE,'out','all.json')))
from collections import defaultdict
ex=defaultdict(list)
for room in range(112):
    try: O=I.objs(room)
    except Exception: continue
    for o in O: ex[o[1]].append((room,)+o)
out=Image.new('RGB',(720,160*len(sys.argv[1:])))
for n,t in enumerate(sys.argv[1:]):
    r=res.get(t)
    cands=[(r['room'],r['idx'],r['x'],r['y'])] if r else [(c[0],c[1],c[3],c[4]) for c in ex[int(t)]]
    for room,idx,x,y in cands:
        try: ims=I.run_case(room,idx,x,y,0,(6,45,140),holdn=int(__import__("os").environ.get("HOLD","4")),dy=int(__import__("os").environ.get("DY","-6"))); break
        except Exception as e: ims=None
    if not ims: continue
    for j,im in enumerate(ims): out.paste(Image.fromarray(im),(240*j,160*n))
    ImageDraw.Draw(out).text((3,160*n+3),f'touch {t} r{room}',fill=(255,0,0))
out.save('/tmp/touch.png')
