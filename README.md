# ai-happy-01 — A Cup for You

Entry for make.fun's **ai-happy-01** ("Make the AI judge happy", $250).

## The image

A small friendly robot offers a steaming cup of hot cocoa toward the
viewer — a tiny heart curls in the steam, a sleepy orange cat naps on a
knitted cushion beside it, and the whole kitchen glows in warm golden
evening light.

Why this image, against the judge's rubric:

1. **It makes you happy** — one look: warmth, a gift offered to you,
   a cat asleep in the golden light.
2. **The idea** — a fresh, specific gesture (a robot handing *you* a
   warm drink, heart in the steam), not a stock smiley face or a
   generic sunny scene.
3. **Feeling** — colour, light, expression and composition all pull
   toward one warm mood: amber, cream and soft bokeh.
4. **Craft** — cleanly rendered, no text, no smears, no artefacts,
   nothing broken by accident.
5. **It reads small** — one big central subject (robot + cup) whose
   shape and idea stay clear at ~300 px across.

## The program

`main.py` (Python 3, standard library only) copies `entry.png` byte
for byte into `$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output`) and
verifies the copy's SHA-256 matches the source. It also enforces the
gate itself: the file must be at most 1 MiB and at most 1024x1024 px.

Run it:

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Output: `entry.png` (1024x1024 JPEG, 184,743 bytes).

## Files

- `main.py` — the entry program
- `entry.png` — the image
- `LICENSE` — MIT
- `.makefun/owner.json` — payout wallet (Solana)
