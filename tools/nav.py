from emu import *
from PIL import Image
import sys
def sheet(e, name, n=8, step=30, keys=0):
    ims=[]
    for i in range(n):
        e.run(step, keys); ims.append(Image.frombuffer("RGBA",(240,160),bytes(e.lib.bf_vbuf().contents),"raw","RGBA",0,1).convert("RGB"))
    s=Image.new('RGB',(240*4,160*((n+3)//4)))
    for i,im in enumerate(ims): s.paste(im,((i%4)*240,(i//4)*160))
    s.save(f'shots/{name}.png')
