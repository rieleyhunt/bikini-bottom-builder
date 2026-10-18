# Object type identification

These scripts identified every object type used by the editor (`editor/objinfo.js`). Set `BFBB_ROM` to a clean USA ROM and build `tools/libharness.so` first.

1. **`ident.py`** boots each type's home room in mGBA. It removes every other object, holds SpongeBob next to the target and screenshots it, diffed against a run without the object.
2. **`gen.js` + `place.py` + `batch.sh`** use the editor's own `exportRom` to add the object to 1-1, then boot it and diff the result. This is how the "works outside its home level" flag is decided.
3. **`touch.py`** and **`drop.py`** run behaviour checks: touching pickups, and dropping the player onto bounce pads and platforms.
4. **`mkicons.py`** cuts each object's sprite out of the screenshot diffs. It saves them with their offset from the object position, and the editor draws them on the map.
5. **`names.py`** holds the names and categories. Edit it, then regenerate `editor/objinfo.js`.
