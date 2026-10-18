// usage: node gen.js room type x y prop out.gba   (type -1 = baseline, no object added)
const BB=require(__dirname+'/../../editor/core.js');const fs=require('fs');
const [room,type,x,y,prop,out]=process.argv.slice(2);
const src=new Uint8Array(fs.readFileSync(process.env.BFBB_ROM||'baserom.gba'));
const r=BB.loadRoom(new BB.Rom(src),+room);
if(+type>=0) r.objects.push({type:+type,x:+x,y:+y,prop:+prop});
r.dirty={objects:true};
const rooms=[];rooms[+room]=r;
fs.writeFileSync(out,BB.exportRom(src,rooms));
