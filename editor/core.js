// ---- BFBB GBA level data core (no DOM) ----
const BB = (() => {
  // Room record (8 words): palette, far background layer, mid layer, front layer, main layer,
  // collision (LZ77), object list header, tile banks [8bpp, 4bpp].
  const ROOM_TABLE = 0x0803C758, ROOM_COUNT = 112, ROOM_SIZE = 0x20;
  // [room index, chapter, level name, part, parts] in game order (from the chapter tables)
  const LEVELS = [[0, 1, "1-1 When Robots Attack", 1, 3], [1, 1, "1-1 When Robots Attack", 2, 3], [2, 1, "1-1 When Robots Attack", 3, 3], [5, 1, "1-2 Hi Ho Mystery, Away!", 1, 3], [6, 1, "1-2 Hi Ho Mystery, Away!", 2, 3], [7, 1, "1-2 Hi Ho Mystery, Away!", 3, 3], [10, 1, "1-3 Robot from the Goo Lagoon", 1, 4], [11, 1, "1-3 Robot from the Goo Lagoon", 2, 4], [37, 1, "1-3 Robot from the Goo Lagoon", 3, 4], [12, 1, "1-3 Robot from the Goo Lagoon", 4, 4], [13, 1, "1-4 Please Please Kelp Me", 1, 4], [19, 1, "1-4 Please Please Kelp Me", 2, 4], [20, 1, "1-4 Please Please Kelp Me", 3, 4], [21, 1, "1-4 Please Please Kelp Me", 4, 4], [8, 1, "1-5 There Goes the Neighborhood", 1, 4], [9, 1, "1-5 There Goes the Neighborhood", 2, 4], [28, 1, "1-5 There Goes the Neighborhood", 3, 4], [29, 1, "1-5 There Goes the Neighborhood", 4, 4], [15, 1, "1-6 Nuts and Bolts", 1, 4], [16, 1, "1-6 Nuts and Bolts", 2, 4], [17, 1, "1-6 Nuts and Bolts", 3, 4], [36, 1, "1-6 Nuts and Bolts", 4, 4], [18, 1, "Attack of the Steel Squirrel", 1, 1], [27, 1, "B-1 One Wheel Madness", 1, 1], [79, 1, "B-2 Sponge Bath", 1, 1], [3, 2, "2-1 Bring it Around Downtown", 1, 3], [4, 2, "2-1 Bring it Around Downtown", 2, 3], [35, 2, "2-1 Bring it Around Downtown", 3, 3], [22, 2, "2-2 Gone Jellyfishing", 1, 5], [23, 2, "2-2 Gone Jellyfishing", 2, 5], [25, 2, "2-2 Gone Jellyfishing", 3, 5], [24, 2, "2-2 Gone Jellyfishing", 4, 5], [34, 2, "2-2 Gone Jellyfishing", 5, 5], [14, 2, "2-3 Short Circuit", 1, 4], [30, 2, "2-3 Short Circuit", 2, 4], [31, 2, "2-3 Short Circuit", 3, 4], [32, 2, "2-3 Short Circuit", 4, 4], [26, 2, "2-4 No Horsing Around", 1, 4], [33, 2, "2-4 No Horsing Around", 2, 4], [54, 2, "2-4 No Horsing Around", 3, 4], [57, 2, "2-4 No Horsing Around", 4, 4], [58, 2, "2-5 New Robotropolis", 1, 3], [59, 2, "2-5 New Robotropolis", 2, 3], [60, 2, "2-5 New Robotropolis", 3, 3], [38, 2, "2-6 To the Mermalair!", 1, 6], [39, 2, "2-6 To the Mermalair!", 2, 6], [40, 2, "2-6 To the Mermalair!", 3, 6], [61, 2, "2-6 To the Mermalair!", 4, 6], [62, 2, "2-6 To the Mermalair!", 5, 6], [63, 2, "2-6 To the Mermalair!", 6, 6], [49, 2, "Star Power", 1, 1], [80, 2, "B-3 The Uni-Speedster 5800", 1, 1], [81, 2, "B-4 Where Did I Leave my Car?", 1, 1], [41, 3, "3-1 Around the Way Sponge", 1, 5], [44, 3, "3-1 Around the Way Sponge", 2, 5], [45, 3, "3-1 Around the Way Sponge", 3, 5], [46, 3, "3-1 Around the Way Sponge", 4, 5], [47, 3, "3-1 Around the Way Sponge", 5, 5], [42, 3, "3-2 Seanutbutter and Jellyfish", 1, 4], [43, 3, "3-2 Seanutbutter and Jellyfish", 2, 4], [48, 3, "3-2 Seanutbutter and Jellyfish", 3, 4], [51, 3, "3-2 Seanutbutter and Jellyfish", 4, 4], [52, 3, "3-3 Mystery Loves Company", 1, 4], [53, 3, "3-3 Mystery Loves Company", 2, 4], [67, 3, "3-3 Mystery Loves Company", 3, 4], [68, 3, "3-3 Mystery Loves Company", 4, 4], [73, 3, "3-4 Hitting the Slopes", 1, 5], [74, 3, "3-4 Hitting the Slopes", 2, 5], [75, 3, "3-4 Hitting the Slopes", 3, 5], [76, 3, "3-4 Hitting the Slopes", 4, 5], [77, 3, "3-4 Hitting the Slopes", 5, 5], [69, 3, "3-5 In-Cog-Neato!", 1, 3], [70, 3, "3-5 In-Cog-Neato!", 2, 3], [71, 3, "3-5 In-Cog-Neato!", 3, 3], [50, 3, "3-6 Robots in the Skies", 1, 4], [55, 3, "3-6 Robots in the Skies", 2, 4], [72, 3, "3-6 Robots in the Skies", 3, 4], [89, 3, "3-6 Robots in the Skies", 4, 4], [56, 3, "Squid Vicious", 1, 1], [82, 3, "B-5 Not Just Another Day at the Beach", 1, 1], [85, 3, "B-6 To the Invisible Boatmobile!", 1, 1], [64, 4, "4-1 It Came from Rock Bottom", 1, 4], [65, 4, "4-1 It Came from Rock Bottom", 2, 4], [66, 4, "4-1 It Came from Rock Bottom", 3, 4], [78, 4, "4-1 It Came from Rock Bottom", 4, 4], [94, 4, "4-2 Deep Trouble", 1, 5], [95, 4, "4-2 Deep Trouble", 2, 5], [96, 4, "4-2 Deep Trouble", 3, 5], [97, 4, "4-2 Deep Trouble", 4, 5], [98, 4, "4-2 Deep Trouble", 5, 5], [99, 4, "4-3 Escape from Sand Mountain", 1, 5], [100, 4, "4-3 Escape from Sand Mountain", 2, 5], [101, 4, "4-3 Escape from Sand Mountain", 3, 5], [102, 4, "4-3 Escape from Sand Mountain", 4, 5], [104, 4, "4-3 Escape from Sand Mountain", 5, 5], [86, 4, "4-4 Back to the Seacave", 1, 4], [87, 4, "4-4 Back to the Seacave", 2, 4], [88, 4, "4-4 Back to the Seacave", 3, 4], [90, 4, "4-4 Back to the Seacave", 4, 4], [109, 4, "4-5 Industrial Robolution", 1, 4], [110, 4, "4-5 Industrial Robolution", 2, 4], [92, 4, "4-5 Industrial Robolution", 3, 4], [93, 4, "4-5 Industrial Robolution", 4, 4], [103, 4, "4-6 Plankton's Inner Sanctum", 1, 5], [105, 4, "4-6 Plankton's Inner Sanctum", 2, 5], [106, 4, "4-6 Plankton's Inner Sanctum", 3, 5], [107, 4, "4-6 Plankton's Inner Sanctum", 4, 5], [108, 4, "4-6 Plankton's Inner Sanctum", 5, 5], [91, 4, "SpongeBot SteelPants", 1, 2], [111, 4, "SpongeBot SteelPants", 2, 2], [83, 4, "B-7 Tour de Sponge", 1, 1], [84, 4, "B-8 Mountain of Dune", 1, 1]];
  const OBJ_NAMES = {"0": "Start / door", "9": "Seaweed", "10": "Bubbles", "11": "Blue coral", "12": "Little red fish", "13": "Pink kelp curl", "14": "Small pink kelp curl", "15": "Red tube coral", "16": "Orange tube coral", "17": "Red branch coral", "18": "Pink crystal", "19": "Bubble puff", "20": "Bubble puff (B)", "21": "Bubble puff (C)", "22": "Green kelp curl", "23": "Tall pink kelp curl", "24": "Golden dome", "25": "Monitor screen", "26": "Orange coral", "27": "Red coral", "28": "Finish line", "29": "Monitor screen (small)", "30": "Gold key", "31": "Extra life", "32": "Underwear (health)", "33": "Krabby Patty", "34": "Golden spatula", "35": "Silver key", "36": "Water fountain", "37": "Robot (walker)", "38": "Robot (walker B)", "39": "Robot (flyer)", "40": "Robot (walker C)", "41": "Umbrella robot", "42": "Blue octopus", "43": "Spiky red crab", "44": "Spiky red puffer", "45": "Spiky red puffer (B)", "46": "Pink jellyfish", "47": "Pink jellyfish (B)", "48": "Red clam", "49": "Red clam (B)", "50": "Red clam (C)", "51": "Diver robot", "52": "Cone-head robot", "53": "Diver robot (B)", "54": "Electric spark (small)", "55": "Cannon robot", "56": "Cannon robot (B)", "57": "Cone-head robot (B)", "58": "Purple bubble", "59": "Bounce pad", "60": "Level exit (invisible)", "61": "Doorway (invisible)", "62": "Finish trigger (invisible)", "63": "Purple block", "64": "Flower block", "65": "Purple block (small)", "66": "Orange mini-sub", "67": "Green mini-sub", "68": "Bouncy umbrella (red)", "69": "Bouncy umbrella (green)", "70": "Propeller robot", "71": "Propeller robot (B)", "72": "Ceiling claw", "73": "Ceiling claw (B)", "74": "Ceiling claw (C)", "75": "Ceiling claw (D)", "76": "Flying fish", "77": "Flame arm", "78": "Flying fish (B)", "79": "Purple hover-boat", "80": "Arrow block", "81": "Arrow block (small)", "82": "Sandy", "83": "Squidward", "84": "Mr. Krabs", "85": "Patrick", "86": "Gary", "87": "Green fish citizen", "88": "Pink fish citizen", "89": "Mermaid Man", "90": "Fish citizen (red shirt)", "91": "Mystery the seahorse", "92": "Vehicle start (unicycle levels)", "93": "Vehicle start (bath/boat levels)", "94": "Boss: Star Power", "95": "Boss: Robo-Sandy", "96": "Boss: Robo-Squidward", "97": "Boss: SpongeBot SteelPants", "98": "SpongeBot boss: press", "99": "Spiked pillar", "100": "Spatula gate", "101": "Jelly block (outline)", "102": "Jelly block (solid)", "103": "Screw platform", "104": "Electric beam", "105": "Light pole", "106": "Floor button", "107": "Floor button (B)", "108": "Jelly switch", "109": "Lever", "110": "Electric spark", "111": "Little yellow fish", "112": "Glowing orb", "113": "Piston crusher", "114": "Ceiling eye", "115": "Conveyor platform"};

  class Rom {
    constructor(bytes) { this.b = bytes; }
    o(a) { const o = a - 0x08000000; if (o < 0 || o >= this.b.length) throw new Error("Bad ROM address 0x" + a.toString(16)); return o; }
    u8(a) { return this.b[this.o(a)]; }
    u16(a) { const o = this.o(a); return this.b[o] | (this.b[o + 1] << 8); }
    u32(a) { const o = this.o(a); return (this.b[o] | (this.b[o + 1] << 8) | (this.b[o + 2] << 16) | (this.b[o + 3] << 24)) >>> 0; }
    w16(a, v) { const o = this.o(a); this.b[o] = v & 255; this.b[o + 1] = (v >> 8) & 255; }
    w32(a, v) { const o = this.o(a); this.b[o] = v & 255; this.b[o + 1] = (v >>> 8) & 255; this.b[o + 2] = (v >>> 16) & 255; this.b[o + 3] = (v >>> 24) & 255; }
    gameCode() { return String.fromCharCode(...this.b.slice(0xAC, 0xB0)); }
  }

  function lzDecompress(rom, a) {
    let o = rom.o(a);
    const B = rom.b;
    if (B[o] !== 0x10) throw new Error("Not LZ77 data at 0x" + a.toString(16));
    const size = B[o + 1] | (B[o + 2] << 8) | (B[o + 3] << 16); o += 4;
    const out = new Uint8Array(size); let n = 0;
    while (n < size) {
      const flags = B[o++];
      for (let bit = 0; bit < 8 && n < size; bit++) {
        if (flags & (0x80 >> bit)) {
          const x = (B[o] << 8) | B[o + 1]; o += 2;
          const len = (x >> 12) + 3, disp = (x & 0xFFF) + 1;
          for (let k = 0; k < len && n < size; k++) { out[n] = out[n - disp]; n++; }
        } else out[n++] = B[o++];
      }
    }
    return out;
  }

  // GBA LZ77 (type 0x10) compressor. Greedy, window 4096, min match 3,
  // displacement >= 2 so the data is also safe for VRAM-style decoders.
  function lzCompress(data) {
    const out = [0x10, data.length & 255, (data.length >> 8) & 255, (data.length >> 16) & 255];
    const head = new Map();
    let i = 0;
    const key = (p) => data[p] | (data[p + 1] << 8) | (data[p + 2] << 16);
    const addPos = (p) => { if (p + 2 < data.length) { const k = key(p); let l = head.get(k); if (!l) head.set(k, l = []); l.push(p); } };
    while (i < data.length) {
      const flagPos = out.length; out.push(0); let flags = 0;
      for (let bit = 0; bit < 8 && i < data.length; bit++) {
        let bestLen = 0, bestDisp = 0;
        if (i + 2 < data.length) {
          const l = head.get(key(i));
          if (l) {
            for (let j = l.length - 1; j >= 0; j--) {
              const p = l[j], disp = i - p;
              if (disp > 4096) break;
              if (disp < 2) continue;
              let len = 0;
              while (len < 18 && i + len < data.length && data[p + len] === data[i + len]) len++;
              if (len > bestLen) { bestLen = len; bestDisp = disp; if (len === 18) break; }
            }
          }
        }
        if (bestLen >= 3) {
          flags |= 0x80 >> bit;
          const x = ((bestLen - 3) << 12) | (bestDisp - 1);
          out.push(x >> 8, x & 255);
          for (let k = 0; k < bestLen; k++) addPos(i + k);
          i += bestLen;
        } else { out.push(data[i]); addPos(i); i++; }
      }
      out[flagPos] = flags;
    }
    while (out.length % 4) out.push(0);
    return new Uint8Array(out);
  }

  // Column-RLE tile map: u16 w, u16 h, u32 colOffset[w] (in halfwords), then u16 streams.
  // Stream codes: 11nnnnnnnnnnnnnn = n literal values follow; 10nn.. = run of n, value follows.
  function decodeMap(rom, a) {
    const w = rom.u16(a), h = rom.u16(a + 2);
    const base = a + 4 + w * 4;
    const grid = new Uint16Array(w * h);
    for (let c = 0; c < w; c++) {
      let p = base + rom.u32(a + 4 + c * 4) * 2, y = 0;
      while (y < h) {
        const v = rom.u16(p); p += 2;
        const n = v & 0x3FFF, top = v >> 14;
        if (top === 3) { for (let k = 0; k < n; k++) { if (y < h) grid[y * w + c] = rom.u16(p); y++; p += 2; } }
        else if (top === 2) { const val = rom.u16(p); p += 2; for (let k = 0; k < n; k++) { if (y < h) grid[y * w + c] = val; y++; } }
        else { grid[y * w + c] = v; y++; }
      }
    }
    return { w, h, grid };
  }

  function encodeMap(w, h, grid) {
    const streams = [];
    for (let c = 0; c < w; c++) {
      const col = []; for (let y = 0; y < h; y++) col.push(grid[y * w + c]);
      const s = []; let y = 0, lit = [];
      const flush = () => { if (lit.length) { s.push(0xC000 | lit.length, ...lit); lit = []; } };
      while (y < h) {
        let r = 1; while (y + r < h && col[y + r] === col[y]) r++;
        if (r >= 3) { flush(); s.push(0x8000 | r, col[y]); y += r; }
        else { lit.push(col[y]); y++; }
      }
      flush();
      streams.push(s);
    }
    let total = 0; const offs = streams.map(s => { const o = total; total += s.length; return o; });
    const out = new Uint8Array(4 + w * 4 + total * 2);
    const dv = new DataView(out.buffer);
    dv.setUint16(0, w, true); dv.setUint16(2, h, true);
    offs.forEach((o, c) => dv.setUint32(4 + c * 4, o, true));
    let p = 4 + w * 4;
    for (const s of streams) for (const v of s) { dv.setUint16(p, v, true); p += 2; }
    return out;
  }

  function palette256(rom, a) {
    const pal = new Uint8Array(256 * 3);
    for (let i = 0; i < 256; i++) {
      const c = rom.u16(a + i * 2);
      const r = c & 31, g = (c >> 5) & 31, b = (c >> 10) & 31;
      pal[i * 3] = (r << 3) | (r >> 2); pal[i * 3 + 1] = (g << 3) | (g >> 2); pal[i * 3 + 2] = (b << 3) | (b >> 2);
    }
    return pal;
  }

  function roomRecord(rom, i) {
    const a = ROOM_TABLE + i * ROOM_SIZE, r = [];
    for (let k = 0; k < 8; k++) r.push(rom.u32(a + k * 4));
    return { addr: a, r };
  }

  function loadRoom(rom, i) {
    const { addr, r } = roomRecord(rom, i);
    const main = r[4];
    const mtPtr = rom.u32(main), mapPtr = rom.u32(main + 4);
    const metatiles = new Uint16Array(lzDecompress(rom, mtPtr).buffer.slice(0));
    const map = decodeMap(rom, mapPtr);
    // Background layers: far sky (r[1]) then mid (r[2]); 4bpp, scrolled at fx/fy of the camera.
    const bgs = [];
    for (const k of [1, 2]) {
      if (!r[k]) continue;
      try {
        const metas = new Uint16Array(lzDecompress(rom, rom.u32(r[k])).buffer.slice(0));
        bgs.push({ metas, map: decodeMap(rom, rom.u32(r[k] + 4)), fx: rom.u32(r[k] + 12) / 256, fy: rom.u32(r[k] + 16) / 256 });
      } catch (e) { /* skip unreadable layer */ }
    }
    let overlay = null;
    if (r[3]) {
      const omt = new Uint16Array(lzDecompress(rom, rom.u32(r[3])).buffer.slice(0));
      const om = decodeMap(rom, rom.u32(r[3] + 4));
      if (om.w === map.w && om.h === map.h) overlay = { metatiles: omt, ...om };
    }
    const bank8 = rom.u32(r[7]) + 4, bank4 = rom.u32(r[7] + 4) + 4;
    const pal = palette256(rom, r[0]);
    const colRaw = lzDecompress(rom, r[5]);
    const cw = colRaw[0] | (colRaw[1] << 8), ch = colRaw[2] | (colRaw[3] << 8);
    const col = new Uint8Array(cw * ch);
    for (let k = 0; k < cw * ch; k++) { const b = colRaw[4 + (k >> 1)]; col[k] = (k & 1) ? (b >> 4) : (b & 15); }
    const oh = r[6], count = rom.u32(oh), listPtr = rom.u32(oh + 4);
    const objects = [];
    for (let k = 0; k < count; k++) {
      const p = listPtr + k * 8;
      objects.push({ type: rom.u16(p), x: rom.u16(p + 2), y: rom.u16(p + 4), prop: rom.u16(p + 6) });
    }
    let maxProp = 0; objects.forEach(o => maxProp = Math.max(maxProp, o.prop));
    return { index: i, recAddr: addr, rec: r, mainLayer: main, metatiles, map, overlay, bgs, bank8, bank4, pal,
             col: { w: cw, h: ch, cells: col }, objects, maxProp, objHeader: oh };
  }

  function tile8(rom, bank, t) { const o = rom.o(bank + t * 64); return rom.b.subarray(o, o + 64); }
  function tile4(rom, bank, t) { const o = rom.o(bank + t * 32); return rom.b.subarray(o, o + 32); }

  // Draw one 16x16 metatile into RGBA buffer (stride in pixels).
  function drawMetatile(rom, room, mt, rgba, stride, ox, oy, fourbpp, metas) {
    const pal = room.pal;
    const m = metas || room.metatiles;
    if (mt * 4 + 3 >= m.length) return;
    for (let k = 0; k < 4; k++) {
      const e = m[mt * 4 + k];
      const t = e & 0xFFF, hf = (e >> 12) & 1, vf = (e >> 13) & 1, pb = (e >> 14) & 3;
      const dx = (k & 1) * 8, dy = (k >> 1) * 8;
      let td;
      try { td = fourbpp ? tile4(rom, room.bank4, t) : tile8(rom, room.bank8, t); } catch (err) { continue; }
      for (let py = 0; py < 8; py++) for (let px = 0; px < 8; px++) {
        const sx = hf ? 7 - px : px, sy = vf ? 7 - py : py;
        let ci;
        if (fourbpp) { const b = td[sy * 4 + (sx >> 1)]; const v = (sx & 1) ? (b >> 4) : (b & 15); if (!v) continue; ci = pb * 16 + v; }
        else { ci = td[sy * 8 + sx]; if (!ci) continue; }
        const q = ((oy + dy + py) * stride + (ox + dx + px)) * 4;
        rgba[q] = pal[ci * 3]; rgba[q + 1] = pal[ci * 3 + 1]; rgba[q + 2] = pal[ci * 3 + 2]; rgba[q + 3] = 255;
      }
    }
  }

  // ---- Export ----
  const EXT_START = 0x08800000;
  function allocator(rom) {
    // first free (0xFF) byte after any data already placed above 8 MB
    let end = rom.b.length - 1;
    while (end >= 0x800000 && rom.b[end] === 0xFF) end--;
    let p = Math.max(EXT_START, 0x08000000 + end + 1);
    p = (p + 15) & ~15;
    return {
      put(bytes) {
        const a = p;
        if (rom.o(a) + bytes.length > rom.b.length) throw new Error("ROM full");
        rom.b.set(bytes, rom.o(a));
        p = (a + bytes.length + 15) & ~15;
        return a;
      }
    };
  }

  function expand(bytes) {
    if (bytes.length >= 0x1000000) return bytes;
    const nb = new Uint8Array(0x1000000); nb.fill(0xFF); nb.set(bytes); return nb;
  }

  // rooms: array of edited room objects (with .dirty flags). Returns new ROM bytes.
  function exportRom(srcBytes, rooms) {
    const rom = new Rom(expand(new Uint8Array(srcBytes)));
    const alloc = allocator(rom);
    for (const room of rooms) {
      if (!room || !room.dirty) continue;
      if (room.dirty.map) {
        const enc = encodeMap(room.map.w, room.map.h, room.map.grid);
        rom.w32(room.mainLayer + 4, alloc.put(enc));
      }
      if (room.dirty.col) {
        const { w, h, cells } = room.col;
        const raw = new Uint8Array(4 + Math.ceil(w * h / 2));
        raw[0] = w & 255; raw[1] = w >> 8; raw[2] = h & 255; raw[3] = h >> 8;
        for (let k = 0; k < w * h; k++) raw[4 + (k >> 1)] |= (k & 1) ? (cells[k] << 4) : cells[k];
        rom.w32(room.recAddr + 20, alloc.put(lzCompress(raw)));
      }
      if (room.dirty.objects) {
        const objs = [...room.objects].sort((a, b) => b.x - a.x);
        const buf = new Uint8Array(objs.length * 8 + 8);
        const dv = new DataView(buf.buffer);
        objs.forEach((o, k) => { dv.setUint16(k * 8, o.type, true); dv.setUint16(k * 8 + 2, o.x, true); dv.setUint16(k * 8 + 4, o.y, true); dv.setUint16(k * 8 + 6, o.prop, true); });
        const p = alloc.put(buf);
        rom.w32(room.objHeader, objs.length);
        rom.w32(room.objHeader + 4, p);
      }
    }
    return rom.b;
  }

  // Collision values, identified by testing each one in mGBA: [name, description, used by the game]
  const COL_INFO = [["Empty", "Nothing here.", 1], ["Hazard", "Hurts SpongeBob on contact (spikes, goo). Not solid, so use it inside pits.", 1], ["Solid (variant A)?", "Solid like 8. Unused by the game; the code also nudges objects stuck inside it upward.", 0], ["Solid (variant B)?", "Solid like 8. Unused by the game; the code also nudges objects stuck inside it downward.", 0], ["Climbable", "Ladders and climbable walls. Press Up to climb.", 1], ["One-way platform", "Stand on it from above; jump up through it and walk through it sideways.", 1], ["No effect (6)", "Unused. Nothing in the game reacts to it.", 0], ["No effect (7)", "Used once (an 8 px gap in a floor in 2-3). Nothing reacts to it.", 1], ["Solid", "Ordinary ground, walls and ceilings. Solid from every side.", 1], ["No effect (9)", "Unused. Nothing in the game reacts to it.", 0], ["Enemy floor", "Invisible to SpongeBob. Flying enemies won't go below it.", 1], ["Enemy wall (left)", "Invisible to SpongeBob. Enemies can't walk or fly left past it. Put it at the left end of a ledge.", 1], ["No effect (12)", "Unused. Nothing in the game reacts to it.", 0], ["Enemy wall (right)", "Invisible to SpongeBob. Enemies can't walk or fly right past it. Put it at the right end of a ledge.", 1], ["Enemy ceiling", "Invisible to SpongeBob. Flying enemies won't go above it.", 1], ["No effect (15)", "Unused. Nothing in the game reacts to it.", 0]];
  const COL_COLORS = ["#0000", "#ff3b30", "#c9a227", "#a88a1f", "#34c759", "#ff9f0a", "#8e8e93", "#8e8e93", "#ffd60a", "#8e8e93", "#bf5af2", "#0a84ff", "#8e8e93", "#64d2ff", "#ff6ad5", "#8e8e93"];
  return { Rom, ROOM_COUNT, LEVELS, OBJ_NAMES, COL_INFO, COL_COLORS, lzDecompress, lzCompress, decodeMap, encodeMap, loadRoom, drawMetatile, exportRom };
})();
if (typeof module !== "undefined") module.exports = BB;
