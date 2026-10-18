import struct
import os
R=open(os.environ.get('BFBB_ROM', 'baserom.gba'),'rb').read()
def U(a,n): return struct.unpack_from('<%dI'%n,R,a-0x8000000)
def lz77(a):
    o=a-0x8000000
    assert R[o]==0x10
    size=int.from_bytes(R[o+1:o+4],'little'); o+=4
    out=bytearray()
    while len(out)<size:
        flags=R[o]; o+=1
        for b in range(8):
            if len(out)>=size: break
            if flags&(0x80>>b):
                x=R[o]<<8|R[o+1]; o+=2
                ln=(x>>12)+3; disp=(x&0xfff)+1
                for k in range(ln): out.append(out[-disp])
            else:
                out.append(R[o]); o+=1
    return bytes(out), o-(a-0x8000000)  # data, compressed length consumed
LEVELS=0x803c760
def level(i): return U(LEVELS+0x20*i,8)
