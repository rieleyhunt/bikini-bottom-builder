# BFBB (GBA, USA `BSQE`) ROM notes

All addresses are GBA bus addresses (ROM at `0x08000000`).

## Levels
- The room table is at `0x0803C758`: 112 rooms × 0x20 bytes.
  - `[0]` palette (256 colours)
  - `[1]` far background layer
  - `[2]` mid layer
  - `[3]` front overlay (4bpp)
  - `[4]` main layer (8bpp)
  - `[5]` collision (LZ77)
  - `[6]` object header
  - `[7]` tile banks `[8bpp hdr, 4bpp hdr]`
- A layer is `[metatiles (LZ77), map, prio, scrollX/256, scrollY/256, flags]`.
- Maps use column RLE:
  - Header: `u16 w, u16 h, u32 offsets[w]` (offsets in halfwords), followed by the streams.
  - `0xC000|n` means n literal values follow; `0x8000|n` means a run, with the value following.
- A metatile entry: bits 0–11 tile, bit 12 horizontal flip, bit 13 vertical flip, bits 14–15 palette.
- Collision is a 4-bit grid at 8×8 px resolution, packed two cells per byte with the low nibble first, and decompressed to EWRAM at room load.
  - `0x08018B5C` reads one cell.
  - `0x08018638(world, pos)` returns the flag word for the cell at a 24.8 fixed-point position, using the table at `0x08031F0C` (16 × u32).
  - Flag word bits:
    - `0x1`, `0x2`, `0x4`, `0x8`: solid from each side. Solid (8) has all four; One-way (5) has only `0x8`, the "landed on top" bit.
    - `0x10`: not solid.
    - `0x20`: platform or climbable top.
    - `0x40`, `0x80`, `0x100`, `0x200`: enemy-only floor, ceiling, right wall and left wall (values 10, 14, 13, 11). Enemy movement code merges them with the solid bits (`0x08000D64`).
    - `0x8000`: hazard. The player update calls the hurt routine `0x080277A4` when its body overlaps it.
    - `0x10000` and `0x20000`: push certain objects up or down.
  - Values: 0 empty, 1 hazard, 4 climbable, 5 one-way, 8 solid, 10/11/13/14 enemy-only bounds, 2/3 solid variants. 6, 7, 9, 12 and 15 have no effect.
- An object header is `{count, list ptr, ...}`. An object is 8 bytes `{type, x, y, prop}`, sorted by x descending.
- Objects are spawned by `0x0800A764(world, type, &pos, params)`, which switches on `type` through a jump table at `0x0800A7C0` (116 cases).
  - Types 1–8 and anything above 115 spawn nothing.
  - `prop` indexes a per-room parameter table: offsets are u16 values at `objHeader+8`, added to the base pointer at `objHeader+12`.
  - Names for every type are in `editor/objinfo.js`.
- The camera's top-left world position (x, y) is the u16 pair at `0x02003D24`.
- Level names are at `0x0804A588` (36 levels). Chapter level lists are in RAM at `0x0200036C`.
- Parallax centre is `120 + (camX-120)*fx`, `80 + (camY-80)*fy`.
- The editor exports by expanding the ROM to 16 MB, appending new data from `0x08800000` and repointing.
