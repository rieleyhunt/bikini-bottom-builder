// usage: node gen_col.js room '[[x,y,v],...]' out.gba   — uses the editor's own exporter
const BB=require(__dirname+'/../../editor/core.js');const fs=require('fs');
const [room,edits,out]=process.argv.slice(2);
const src=new Uint8Array(fs.readFileSync(process.env.BFBB_ROM||'baserom.gba'));
const r=BB.loadRoom(new BB.Rom(src),+room);
for(const [x,y,v] of JSON.parse(edits)) r.col.cells[y*r.col.w+x]=v;
r.dirty={col:true};const rooms=[];rooms[+room]=r;
fs.writeFileSync(out,BB.exportRom(src,rooms));
