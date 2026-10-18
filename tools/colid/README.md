# Collision identification

These scripts identified the 16 collision values. Set `BFBB_ROM` to a clean USA ROM; the scripts write their output to `work/`.

- **`gen_col.js`** paints collision cells into a room with the editor's exporter.
- **`scen.py`** boots a room, runs a scripted input sequence with optional teleports, and records SpongeBob's position every frame.
- **`tests.py`** runs the floor, ceiling, wall and overlap tests for every value.
- **`ents.py`** and **`enemy_test.py`** remove one value from a room and compare enemy movement against the original.
