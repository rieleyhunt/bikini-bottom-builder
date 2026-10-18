import struct,sys
import os
R=open(os.environ.get('BFBB_ROM', 'baserom.gba'),'rb').read()
def bl_xrefs(target, lo=0, hi=0x100000):
    out=[]
    for o in range(lo,hi,2):
        h1,h2=struct.unpack_from('<HH',R,o)
        if (h1&0xf800)==0xf000 and (h2&0xf800)==0xf800:
            off=((h1&0x7ff)<<12)|((h2&0x7ff)<<1)
            if off&0x400000: off-=0x800000
            if 0x8000000+o+4+off==target: out.append(0x8000000+o)
    return out
if __name__=='__main__':
    for t in sys.argv[1:]:
        r=bl_xrefs(int(t,16)); print(t,len(r),[hex(x) for x in r[:40]])
