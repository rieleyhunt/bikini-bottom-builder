import capstone, sys, struct
import os
ROM=open(os.environ.get('BFBB_ROM', 'baserom.gba'),'rb').read()
def dis(addr, n=40, thumb=True):
    md=capstone.Cs(capstone.CS_ARCH_ARM, capstone.CS_MODE_THUMB if thumb else capstone.CS_MODE_ARM)
    off=addr-0x08000000
    out=[]
    for i in md.disasm(ROM[off:off+n*4], addr):
        extra=''
        if 'pc' in i.op_str and i.mnemonic.startswith('ldr'):
            try:
                imm=int(i.op_str.split('#')[-1].rstrip(']'),16)
                la=((i.address+4)&~3)+imm
                extra=' ; =0x%08x'%struct.unpack('<I',ROM[la-0x08000000:la-0x08000000+4])[0]
            except Exception: pass
        out.append('%08x: %-8s %s%s'%(i.address,i.mnemonic,i.op_str,extra))
        if len(out)>=n: break
    return '\n'.join(out)
if __name__=='__main__':
    a=int(sys.argv[1],16); n=int(sys.argv[2]) if len(sys.argv)>2 else 40
    print(dis(a,n, not (len(sys.argv)>3 and sys.argv[3]=='arm')))
