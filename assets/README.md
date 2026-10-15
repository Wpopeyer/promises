# promises — brand assets

Two inks on paper, printed slightly off-register. One character.

| File | Use |
|---|---|
| `mark.svg` | The mark: two hooks, linked. Two inks with the overprint drawn in. Transparent background. |
| `mark-mono.svg` | One ink, no overprint. Favicons, 16–32 px, anywhere two inks would muddy. |
| `mark-on-ink.svg` | Blue tile with the mark in orange and paper. App icons, avatars, dark backgrounds. |
| `lockup.png` / `lockup.svg` | Mark + wordmark on paper. README footers, docs headers. |
| `banner.png` / `banner.svg` | README hero, 1280×400 (rendered at 2×). |
| `social-preview.png` / `.svg` | GitHub social preview, 1280×640 (rendered at 2×). Upload under *Settings → Social preview*. |
| `witness.svg` | The Witness, on a paper card. |

## The Witness

Wasn't in the meeting. Has the notes anyway. He writes down what one repo promised another and reads it back to whoever is about to change it. He never writes code, never has opinions about your architecture, and never raises his voice. Always: the clipboard, the pinky, the flat "you said."

## Inks

| | Hex | Used for |
|---|---|---|
| Blue ink | `#1D3FB8` | Text, lines, the Witness. |
| Orange ink | `#FF5A1F` | The promise, numbers, stamps, highlights. |
| Overprint | multiply | Where the two inks meet. Never a flat hex in the artwork; `#1D1616` when a renderer can't multiply. |
| Paper | `#EFEDE6` | Ground. |

No greys, no gradients, no dark mode. Fills sit 2–3 px off their outlines on purpose.

## Type

- **Bricolage Grotesque** (800 for headlines, 600 for subheads) — the talking.
- **JetBrains Mono** — the facts: commands, keys, file names.

Headlines are tight (−3.5 % tracking), set in sentence case, and end in full stops. No exclamation marks, anywhere, ever.

## Rebuilding

`build.py` regenerates every file here. It needs `cairosvg` and `shapely`, plus the two typefaces installed locally — the `@fontsource/bricolage-grotesque` and `@fontsource/jetbrains-mono` npm packages ship the `.woff` files, which `fontTools` converts to `.ttf`. The overprint shapes are computed geometrically so the mark renders identically in browsers, GitHub, and anything else that can't do `mix-blend-mode`.
