# Bikini Bottom Builder: editor guide

<img src="images/editor-world3.png" width="860" alt="Editing 3-2 Seanutbutter and Jellyfish">

## Getting started

| Version | How to run |
|---|---|
| **Windows app** | Download `BikiniBottomBuilder.exe` from the [Releases page](../../../releases/latest) and run it. It opens in its own Edge or Chrome window, works offline and saves exports through a normal Save dialog. |
| **Offline page** | Download `BikiniBottomBuilder.html` from the [Releases page](../../../releases/latest) and open it in Chrome or Edge. Firefox works too, but saves exports as a download. |

Click **Choose .gba file** and pick your *Battle for Bikini Bottom (USA)* ROM. The editor checks for game code `BSQE`. It also accepts a ROM you exported earlier.

Nothing is uploaded anywhere. The ROM is read and written in your browser.

## The screen

- **Level picker** (top bar): all 112 rooms, named by level and part, e.g. *1-1 When Robots Attack (part 1 of 3)*. Bonus stages and boss rooms are in the list too.
- **Tool rail** (left).
- **Stage** (centre): the room at 1×–4× zoom, with the parallax background behind it.
- **Side panel** (right): view toggles, the current tool's options and room info. Drag the dotted splitter to resize it; the arrow keys also work while it has focus.

### View toggles

| Toggle | Shows |
|---|---|
| Front layer | The foreground overlay drawn in front of the player |
| Collision | Collision cells as coloured squares (yellow = solid) |
| Objects | Object markers |
| Object sprites | Each object's in-game sprite at its real position |
| Object names | A name label next to every object |
| Background | The parallax sky and far layers |
| Grid | The 16×16 metatile grid |

## Tools

| Tool | Key | What it does |
|---|---|---|
| **Objects** | `V` | Click an object, or its sprite, to select it, then drag to move. `Delete` removes it. The panel shows its type, position and props. |
| **Add** | `A` | Pick a type from the picture grid, then click the level to place it. Add stays on, so you can keep clicking. |
| **Tiles** | `T` | Paint 16×16 metatiles from the palette. **Right-click** the level to pick up the tile under the cursor. |
| **Collision** | `C` | Paint the 8×8 collision grid. Right-click erases. |
| **Copy** | `R` | Drag a box over part of the level. Its tiles and collision are copied together. |
| **Stamp** | `P` | Click to paste what you copied. |

| Shortcut | Action |
|---|---|
| `Ctrl+Z` | Undo |
| `Ctrl+Shift+Z` or `Ctrl+Y` | Redo |
| `Delete` / `Backspace` | Delete the selected object |

## Building platforms you can stand on

Tiles are only graphics. What the player can stand on is set by the **collision** grid, which is separate. The walkable line usually sits a little below the visual top of a ground tile, so painting collision by hand to match the art is fiddly.

The easy way is to use **Copy** and **Stamp**:

1. Press `R` and drag a box over an existing platform, including a row or two of collision under its surface.
2. Press `P` and click wherever you want new platforms.

Each copy brings its collision with it, so SpongeBob lands on it exactly as he does on the original. This was tested in the emulator: a stamped platform in 1-1 catches the player at the same height as the real one.

### Collision values

All 16 values were identified by testing each one in mGBA. The tests painted each value into 1-1 with the editor's exporter, then dropped, walked and jumped SpongeBob into it and watched enemies around it. See [How it was made](HOW-IT-WAS-MADE.md#4-identifying-collision).

| Value | Name | What it does | Used in levels |
|---|---|---|---|
| 0 | Empty | Nothing | everywhere |
| **8** | **Solid** | Ground, walls and ceilings, solid from every side | all 112 rooms |
| **5** | **One-way platform** | Stand on it from above. Jump up through it and walk through it sideways. Used for the floating shells. | 75 rooms |
| **4** | **Climbable** | Ladders and climbable walls. Hold Up to climb. | 47 rooms |
| **1** | **Hazard** | Hurts SpongeBob on contact. It isn't solid, so line the bottom of pits with it. | 30 rooms |
| 11 | Enemy wall (left) | Invisible to SpongeBob. Enemies can't move left past it. Put it at the left end of a ledge. | 102 rooms |
| 13 | Enemy wall (right) | Invisible to SpongeBob. Enemies can't move right past it. Put it at the right end of a ledge. | 100 rooms |
| 10 | Enemy floor | Invisible to SpongeBob. Flying enemies won't go below it. | 88 rooms |
| 14 | Enemy ceiling | Invisible to SpongeBob. Flying enemies won't go above it. | 92 rooms |
| 2, 3 | Solid (variants)? | Solid like 8. The code also nudges a few object types inside them up (2) or down (3). | unused |
| 7 | No effect | One stray cell in 2-3 | 1 cell |
| 6, 9, 12, 15 | No effect | Nothing in the game reacts to them | unused |

Collision is drawn as **thin lines, not filled blocks**:
- A floor is a single row of Solid with empty space below it.
- A wall is a single column.
- Enemy walls (11 and 13) stand as short columns just above the ends of each ledge, which keeps walkers from falling off. When you build a new ledge for enemies, add an 11 above its left end and a 13 above its right end.

<img src="images/editor-collision.png" width="760" alt="Collision brushes">

## Overwriting a room with another

The **Room** panel has **Overwrite with another room**. Pick any room from the game and click **Overwrite**. The current room is replaced with a full copy of it: tiles, tile set, colours, backgrounds, front layer, collision and objects. Use it when you want a level with a completely different look or theme than the one you started from.

The room keeps its place in the level:
* Its exits are rewired to lead where the original room's exits led, so finishing it still takes you to the next part.
* Its entrances take the numbers the neighbouring rooms use, so arriving from either side drops you in the right spot.
* If the copied room has no entrance for one side, the editor adds one next to the matching exit.

The music doesn't change, because the game sets it per level in its code rather than in the room. Undo brings the original room back. You can keep editing the copied room like any other, and the room you copied from is never changed.

## Objects

<img src="images/objects.png" width="760" alt="Every object type">

The Add panel groups all 108 types into categories:

- Pickups
- Enemies
- Characters
- Bosses
- Hazards
- Platforms & gadgets
- Scenery
- Start & exits
- Bonus levels

Selecting a type shows its sprite, how many the game uses and the levels it normally appears in. The [object reference](OBJECTS.md) has the full list.

Things to know:

- **"?" after a name** means the name is our best guess at what the object does.
- **"Didn't appear when placed in 1-1"**: about 16 types, mostly some enemies and the bosses, only load their graphics in their own levels. Use them in the levels listed in the panel.
- **Scenery changes with the world.** Seaweed and coral use per-world art, so the same type looks different in Jellyfish Fields than in Bikini Bottom.
- **Props** is an index into the room's table of object settings, such as patrol distance or NPC dialogue. When placing something new, copy the props of an existing object of the same type in that room; the editor does this for you when it can.
- **Start / door (type 0)** is where the player appears. **Level exit (type 60)** is the invisible trigger at the end of a room. Moving it moves the end of the level.
- Types 1–8 and anything above 115 spawn nothing.

## Exporting

Click **Export ROM**. The editor:

1. Expands the ROM from 8 MB to 16 MB. GBA cartridges and emulators support up to 32 MB.
2. Writes your edited maps (re-compressed), collision (LZ77) and object lists into the new space at `0x08800000` and up.
3. Points the room table at the new data. Original data is left untouched, so exports are always safe to re-open and edit further.

The Windows app shows a Save dialog. The browser version uses Chrome or Edge's save picker, or downloads the file as a fallback.

## Limitations

- New tiles can't be added yet. You paint with each room's existing tile set, which is already large: 800–1200 tiles per room.
- Room sizes are fixed.
- The front overlay layer and the far background layers are view-only.
