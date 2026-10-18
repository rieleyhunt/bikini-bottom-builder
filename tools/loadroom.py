from nav import *
import sys
def boot_room(rom, room, frames=120):
    e=Emu(rom)
    e.run(600); e.tap(START,5,60); e.tap(START,5,90)
    t=e.r32(0x200036c); lst=e.r32(t+4)
    e.w32(lst+8, 0x803c760+0x20*room-8)
    for i in range(6): e.tap(A,10,20)
    for i in range(40): e.tap(A,10,30)
    e.run(frames)
    return e
if __name__=='__main__':
    e=boot_room(sys.argv[1],int(sys.argv[2])); e.shot(sys.argv[3])
