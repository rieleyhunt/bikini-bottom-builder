# Original 16x16 pixel icons in the 16-colour Win9x style (drawn for this project).
from PIL import Image
import base64, io, json
P = {'.':None,'k':(0,0,0),'w':(255,255,255),'g':(192,192,192),'d':(128,128,128),'n':(0,0,128),'b':(0,0,255),
     'y':(255,255,0),'o':(128,128,0),'r':(255,0,0),'m':(128,0,0),'G':(0,128,0),'L':(0,255,0),'t':(0,128,128),'c':(0,255,255)}
I = {}
I['select'] = """
k...............
kk..............
kwk.............
kwwk............
kwwwk...........
kwwwwk..........
kwwwwwk.........
kwwwwwwk........
kwwwwwwwk.......
kwwwwwkkkk......
kwwkwwk.........
kwk.kwwk........
kk..kwwk........
k....kwwk.......
.....kwwk.......
......kk........"""
I['add'] = """
....kkkkk.......
..kkyyyyykk.....
.kyywwyyyyyk....
.kywwyyyyyyk....
kyywyyyyyyyok...
kyyyyyyyyyyok...
kyyyyyyyyyyok...
kyyyyyyyyyook...
.kyyyyyyyook....
.kyyyyyookkkk...
..kkooookkGGk...
....kkkkkkGGkkkk
.......kGGGGGGGk
.......kkkkGGkkk
..........kGGk..
..........kkkk.."""
I['tiles'] = """
kkkkkkkkkkkkkkkk
kbbbbbbkdgdgdgdk
kbcbbcbkgdgdgdgk
kbbbbbbkdgdgdgdk
kbbcbbckgdgdgdgk
kbbbbbbkdgdgdgdk
kbcbbbbkgdgdgdgk
kkkkkkkkkkkkkkkk
kGGLGGGkyyoyyyyk
kGLGGLGkyyyyoyyk
kGGGGGGkoyyyyyyk
kLGGLGGkyyyyyoyk
kGGGGLGkyoyyyyyk
kGLGGGGkyyyyoyyk
kGGGLGGkyyoyyyyk
kkkkkkkkkkkkkkkk"""
I['col'] = """
................
kkkkkkkkkkkkkkkk
krrrrrrkrrrrrrrk
kmmmmmmkmmmmmmmk
kkkkkkkkkkkkkkkk
krrrkrrrrrrkrrrk
kmmmkmmmmmmkmmmk
kkkkkkkkkkkkkkkk
krrrrrrkrrrrrrrk
kmmmmmmkmmmmmmmk
kkkkkkkkkkkkkkkk
krrrkrrrrrrkrrrk
kmmmkmmmmmmkmmmk
kkkkkkkkkkkkkkkk
................
................"""
I['copy'] = """
................
kwkwkwkwkwkwkwk.
w.............w.
k.............k.
w..ggggg......w.
k..gdddg......k.
w..ggggggggg..w.
k......gdddg..k.
w......ggggg..w.
k.............k.
w.............w.
kwkwkwkwkwkwkwk.
................
.............k..
............kwk.
.............k.."""
I['paste'] = """
......kkkk......
.....kmmmmk.....
.....kmmmmk.....
......kmmk......
......kmmk......
......kmmk......
...kkkkkkkkkk...
..kggggggggggk..
..kgwwwwwwwwdk..
..kddddddddddk..
..kkkkkkkkkkkk..
...krrrrrrrrk...
...kkkkkkkkkk...
................
..rr.rrr.rr.rr..
................"""
I['open'] = """
................
................
..kkkk..........
.kyyyyk.........
kyywwyykkkkkkk..
kywyyyyyyyyyyok.
kwyyyyyyyyyyyok.
kyykkkkkkkkkkkkk
kykyyyyyyyyyyyyk
kykyyyyyyyyyyok.
kkyyyyyyyyyyyok.
kkyyyyyyyyyyok..
kyyyyyyyyyyyok..
kkkkkkkkkkkkk...
................
................"""
I['undo'] = """
................
................
.....kk.........
....kbk.........
...kbbkkkkkk....
..kbbbbbbbbbkk..
.kbbbbbbbbbbbbk.
..kbbbbbkkkkbbbk
...kbbkk....kbbk
....kbk......kbk
.....kk......kbk
............kbbk
...........kbbk.
.........kkbbk..
.........kkkk...
................"""
I['save'] = """
kkkkkkkkkkkkkkk.
knnkggggggggknnk
knnkggggkdggknnk
knnkggggkdggknnk
knnkggggkdggknnk
knnkggggggggknnk
knnnkkkkkkkknnnk
knnnnnnnnnnnnnnk
knnkkkkkkkkkknnk
knkwwwwwwwwwwknk
knkwkkkkkkkkwknk
knkwwwwwwwwwwknk
knkwkkkkkkwwwknk
knkwwwwwwwwwwknk
kkkwwwwwwwwwwkkk
.kkkkkkkkkkkkkk."""
out = {}
sheet = Image.new('RGBA', (16*9*4, 16*4), (192,192,192,255))
for n,(name,s) in enumerate(I.items()):
    rows = [r for r in s.strip('\n').split('\n')]
    assert len(rows)==16, (name,len(rows))
    im = Image.new('RGBA',(16,16),(0,0,0,0))
    for y,r in enumerate(rows):
        r = r.ljust(16,'.')[:16]
        for x,ch in enumerate(r):
            c = P.get(ch)
            if c: im.putpixel((x,y), c+(255,))
    buf=io.BytesIO(); im.save(buf,'PNG'); out[name]='data:image/png;base64,'+base64.b64encode(buf.getvalue()).decode()
    sheet.alpha_composite(im.resize((64,64),Image.NEAREST),(n*64*1+ n*0, 0))
sheet.save('icons/icons.png')
json.dump(out, open('icons/icons.json','w'))
print({k:len(v) for k,v in out.items()})
