# OpenMotoRacer hybrid core for MiSTer (Moto Racer)

@hybrid/CLAUDE.md

## This core

- Name everywhere: `OpenMotoRacer` (the engine: core, folders `games/dnk/OpenMotoRacer/` and `logs/dnk/OpenMotoRacer/`, `_Other/dnk/dnk-OpenMotoRacer_*.rbf`, release), `openmotoracer` (game submodule, binary in `build/`, log, lock). The games and their menu entries (`_Other/dnk-<title>.mgl`): `package/games.txt` (in the zip as `games/dnk/OpenMotoRacer/games.txt`, from which the database's build makes the launcher's catalogue).
- The game is the `openmotoracer/` submodule, branch `mister`. Its MiSTer code is behind the `MISTER_HYBRID` build option.
- Build: `./build.sh` (game), `./core/build_core.sh` (FPGA), `./package.sh` (zip in `dist/`), `MISTER=root@<address> tools/deploy.sh` (its menu entries in `_Test`, the main menu's *Test*).
- Release: the zip in `releases/`. Players get it once it is published to the database, only when Danik asks: `hybrid/launcher/distribution.py publish ~/dnk_Distribution_MiSTer releases/OpenMotoRacer_YYYYMMDD.zip` (the rule in `hybrid/CLAUDE.md`).
- Try a build on the MiSTer without installing it: `MISTER=root@<address> tools/test_on_mister.sh <id>|list|nodata|log|stop` (the rule in `hybrid/CLAUDE.md`).
- Lines marked `GAME:` in the scripts and `TODO` in the READMEs are the places the template left for this game.

<!-- Notes that are only true for this game go below. -->

- The game's own record is `openmotoracer/docs/NOTES.md`, section 4.25: resolutions, the 640x240 design, input, measurements.
- Danik's decisions (2026-10-31): one menu entry for either copy (GOG's first); race resolutions 320x240 (default) and 640x240, no 200-line modes (the original has none) and, from 2026-11-01, no 640x480 race; menus are 640x480 (the game draws them no other way), Flicker Filter Strong by default for them, HUD (Bottom) moves the main menu's Options and Exit up too; Limit to 30 FPS off by default; HUD margins top and bottom; the logo from the game's art; A accelerate, B brake, X turbo/stunt, Y camera, L/R gears, Select look back, Start pause, R2/L2 by degrees, L3 dashboard, R3 map; cheats: the game's three, No Time Limit, Slow Rivals.
- Speeds on the real core (Speed Bay, 24 riders, 2026-11-01): 320x240 a steady 59.6 (10-14 ms a picture), 640x240 53-60 (14-19 ms). Written out in NOTES 4.25 with what was done: own sound lock and music thread, direct drawing, lazy 2D rows at 640x240, loops split by kind, the ARM build in Thumb with LTO (`port/CMakeLists.txt`). PGO about 2%, dropped.
- `DRAW_AHEAD` 1: a clear gain at 320x240, nothing lost at 640x240 (runs in NOTES 4.25). No 512x384 and no 16:9 on the MiSTer.
- The OLED icon and the screenshots are made from the game's art and stay out of git (`.gitignore`) until Danik decides about publishing them. The logo and the OLED logo are committed (Danik, 2026-11-02), the logo's white outside the oval taken to transparency: the grey there was a shadow flattened onto white, now black with its darkness as the alpha (his review note, round 2).
