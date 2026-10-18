from lvl import *
import numpy as np
from PIL import Image
def decode_map(m):
    w,h=struct.unpack_from('<HH',R,m-0x8000000)
    offs=U(m+4,w); base=m+4+w*4
    grid=np.zeros((h,w),dtype=np.int32)
    for c in range(w):
        a=base+offs[c]*2-0x8000000; y=0
        while y<h:
            v=struct.unpack_from('<H',R,a)[0]; a+=2
            n=v&0x3fff
            if v&0x4000:   # literal block
                for k in range(n): grid[y,c]=struct.unpack_from('<H',R,a)[0]; a+=2; y+=1
            elif v&0x8000:  # run
                val=struct.unpack_from('<H',R,a)[0]; a+=2
                grid[y:y+n,c]=val; y+=n
            else:
                grid[y,c]=v; y+=1
    return grid
def tile_img(tiles, idx, pal, pb, hf, vf):
    t=tiles[idx*32:idx*32+32]
    im=np.zeros((8,8,3),dtype=np.uint8); a=np.zeros((8,8),dtype=bool)
    for py in range(8):
        for px in range(8):
            b=t[py*4+px//2]; v=(b>>4) if px&1 else (b&15)
            if v: im[py,px]=pal[pb*16+v]; a[py,px]=True
    if hf: im=im[:,::-1]; a=a[:,::-1]
    if vf: im=im[::-1]; a=a[::-1]
    return im,a
def render(grid, metatiles, tiles, pal, mtsize=16):
    h,w=grid.shape
    out=np.zeros((h*16,w*16,3),dtype=np.uint8); out[:]=(40,40,60)
    mt=np.frombuffer(metatiles,dtype=np.uint16).reshape(-1,4)
    cache={}
    for y in range(h):
        for x in range(w):
            m=grid[y,x]
            if m==0 or m>=len(mt): continue
            for k,(dx,dy) in enumerate(((0,0),(8,0),(0,8),(8,8))):
                e=int(mt[m,k]); key=e
                if key not in cache: cache[key]=tile_img(tiles,e&0xfff,pal,(e>>14)&3,(e>>12)&1,(e>>13)&1)
                im,a=cache[key]
                reg=out[y*16+dy:y*16+dy+8, x*16+dx:x*16+dx+8]; reg[a]=im[a]
    return Image.fromarray(out)

def tile8(bank, idx, pal, hf, vf):
    t=np.frombuffer(R[bank-0x8000000+idx*64: bank-0x8000000+idx*64+64],dtype=np.uint8).reshape(8,8)
    a=t!=0
    im=np.array(pal,dtype=np.uint8)[t]
    if hf: im=im[:,::-1]; a=a[:,::-1]
    if vf: im=im[::-1]; a=a[::-1]
    return im,a
def render8(grid, metatiles, bank, pal):
    h,w=grid.shape
    out=np.zeros((h*16,w*16,3),dtype=np.uint8); out[:]=(40,40,60)
    mt=np.frombuffer(metatiles,dtype=np.uint16).reshape(-1,4); cache={}
    for y in range(h):
        for x in range(w):
            m=grid[y,x]
            if m==0 or m>=len(mt): continue
            for k,(dx,dy) in enumerate(((0,0),(8,0),(0,8),(8,8))):
                e=int(mt[m,k])
                if e not in cache: cache[e]=tile8(bank,e&0xfff,pal,(e>>12)&1,(e>>13)&1)
                im,a=cache[e]
                reg=out[y*16+dy:y*16+dy+8, x*16+dx:x*16+dx+8]; reg[a]=im[a]
    return Image.fromarray(out)
def bgpal(addr):
    pr=np.frombuffer(R[addr-0x8000000:addr-0x8000000+512],dtype=np.uint16)
    return [((c&31)<<3|(c&31)>>2,((c>>5)&31)<<3|((c>>5)&31)>>2,((c>>10)&31)<<3|((c>>10)&31)>>2) for c in pr]
