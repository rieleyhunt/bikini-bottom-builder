import ctypes, os
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
A, B, SEL, START, RIGHT, LEFT, UP, DOWN, R, L = [1 << i for i in range(10)]


class Hit(ctypes.Structure):
    _fields_ = [("addr", ctypes.c_uint32), ("oldv", ctypes.c_uint32), ("newv", ctypes.c_uint32),
                ("pc", ctypes.c_uint32), ("lr", ctypes.c_uint32), ("r", ctypes.c_uint32 * 13),
                ("kind", ctypes.c_uint32), ("frame", ctypes.c_uint32)]


class Emu:
    def __init__(self, rom):
        self.lib = lib = ctypes.CDLL(os.path.join(HERE, "libharness.so"))
        for n in ["bf_r8", "bf_r16", "bf_r32", "bf_reg", "bf_frame"]:
            getattr(lib, n).restype = ctypes.c_uint32
        lib.bf_reg.argtypes = [ctypes.c_char_p]
        lib.bf_vbuf.restype = ctypes.POINTER(ctypes.c_uint32 * (240 * 160))
        lib.bf_hits.restype = ctypes.POINTER(Hit * 65536)
        assert lib.bf_init(rom.encode()) == 0
        self.ss = lib.bf_statesize()

    def run(self, n=1, keys=0):
        self.lib.bf_run(n, keys)

    def tap(self, keys, hold=3, after=20):
        self.run(hold, keys); self.run(after, 0)

    def r8(self, a): return self.lib.bf_r8(a)
    def r16(self, a): return self.lib.bf_r16(a)
    def r32(self, a): return self.lib.bf_r32(a)
    def w8(self, a, v): self.lib.bf_w8(a, v)
    def w16(self, a, v): self.lib.bf_w16(a, v)
    def w32(self, a, v): self.lib.bf_w32(a, v)

    def read(self, a, n):
        b = ctypes.create_string_buffer(n)
        self.lib.bf_readblk(a, n, b)
        return b.raw

    def save(self):
        b = ctypes.create_string_buffer(self.ss)
        self.lib.bf_save(b)
        return b

    def load(self, b): self.lib.bf_load(b)

    def shot(self, path):
        buf = bytes(self.lib.bf_vbuf().contents)
        im = Image.frombuffer("RGBA", (240, 160), buf, "raw", "RGBA", 0, 1).convert("RGB")
        im.save(path)
        return im

    def reg(self, n): return self.lib.bf_reg(n.encode())
    def frame(self): return self.lib.bf_frame()
    def watch(self, a, t=1): return self.lib.bf_watch(a, t)  # 1 write, 2 read, 3 rw
    def brk(self, a): return self.lib.bf_break(a)
    def clear(self, i): return self.lib.bf_clearpoint(i)
    def stoponhit(self, s): self.lib.bf_stoponhit(s)

    def hits(self):
        n = self.lib.bf_nhits()
        h = self.lib.bf_hits().contents
        out = [h[i] for i in range(n)]
        self.lib.bf_clearhits()
        return out
