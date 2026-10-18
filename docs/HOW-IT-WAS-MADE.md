# How it was made

The project started with a ROM dump and a question: *"What's the first step?"* There's no public disassembly of the GBA *Battle for Bikini Bottom*, so everything here was worked out from the binary.

## 1. A scriptable emulator

The base of the work is a ~100-line C harness around **libmgba** ([`tools/harness.c`](../tools/harness.c)), loaded into Python with ctypes ([`tools/emu.py`](../tools/emu.py)). It can:

- run N frames with buttons held
- read and write any address
- save and load states
- grab the screen as a PNG
- set **write and read watchpoints** and **breakpoints** that log PC, LR and registers

Most discoveries came from the same loop: set a watchpoint, play a few frames, read the logged program counter, then disassemble it with capstone.

## 2. Levels

The level format was decoded piece by piece:

1. Found the **room table** at `0x0803C758`: 112 rooms × 32 bytes.
2. Decoded the **metatile maps**, which use column-RLE compression, and the **LZ77** compressed metatile and collision data.
3. Worked out the **object lists**: 8 bytes each, `{type, x, y, props}`, sorted right-to-left.
4. Rendered every room to PNG and compared it against emulator screenshots.

One early bug was that some rooms had "inverted" colours. The table actually starts 8 bytes earlier than first thought, so every room was using its neighbour's palette.

The editor reuses the same codecs in JavaScript. The exporter expands the ROM to 16 MB, appends re-encoded data and repoints the room table.

## 3. Identifying every object

The object spawner is a 116-case `switch` on the type (`0x0800A764`, jump table `0x0800A7C0`), so the valid types are known exactly. The ROM doesn't contain names, so each type was tested in three ways:

1. **In its home level.** Every other object is removed from the room, SpongeBob is held next to the target and the frame is diffed against a run without it. Whatever changed is the object.
2. **Placed with the editor.** The editor's own export code adds each type to 1-1, the emulator boots that ROM, and the object either shows up or doesn't. This decides the "works outside its home level" flag.
3. **By behaviour.** Touch tests showed lives going 3 → 4 for the Extra life and the spatula counter going 0 → 1 for the Golden spatula. Drop tests showed the player bouncing on the bounce pad and umbrellas. Touching type 60 moves the player into the next area.

The screenshot diffs also gave each object's sprite, cut out with transparency, and its exact offset from the object position. The camera position was found at `0x02003D24` by searching memory for a value that moved 300 px when the player was moved 300 px. That's how the editor draws real sprites on the map.

<img src="images/objects.png" width="760" alt="All identified objects">

## 4. Identifying collision

The collision grid uses 16 values, but only 0 and 8 were understood at first. Code and experiments were used together.

**Code.**
1. A read watchpoint on the decompressed collision under SpongeBob's feet led to the cell reader `0x08018B5C`.
2. The cell reader led to a lookup that turns each value into a flag word using a 16-entry table at `0x08031F0C`.
3. Searching the code for those flag bits showed:
   - Enemy movement code treats bits `0x40`/`0x80`/`0x100`/`0x200` as floor, ceiling and walls.
   - The player update calls the hurt routine when it touches bit `0x8000`.

**Experiments.** Every value was painted into 1-1 with the editor's own exporter ([`tools/colid`](../tools/colid)), and SpongeBob was put through four tests per value:

| Test | Setup | What it shows |
|---|---|---|
| Floor | Dropped onto a strip of the value | Does he land? |
| Ceiling | Jumps up into a strip | Does it stop him? |
| Wall | Walks into a column from each side | Does it block him? |
| Overlap | Stands inside a block, then presses Up, Down and A | Hurt? Climbing? |

That separated Solid (8), One-way (5: floor only), Climbable (4: Up makes him climb) and Hazard (1: the health bar drops). Values 10, 11, 13 and 14 did nothing to SpongeBob.

So the next step was removing every 11, 13, 10 or 14 from 1-1 and tracking enemies:

| Removed | What changed |
|---|---|
| 13 | A walking robot that normally turns at x=1039 walked off the right end of its ledge and fell |
| 11 | The same robot went further left |
| 10 | Flying robots dropped lower than before |
| 14 | Flying robots flew up to the top of the screen |
