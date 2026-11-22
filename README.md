# The World in One Picture — 22 November 2026

A single dramatic picture (1024x1024 PNG) summing up Sunday
22 November 2026: the Strait of Hormuz at dusk, tankers on dark water
under a burning sky, with one big catchy headline — "HORMUZ ON FIRE" —
and a two-line caption carrying the rest of the day's verified world
news. Generated deterministically with Pillow and DejaVu fonts.

Repo anchor: makefun anchor 38678accf7ae0553320c8e1b9accf0852a1c6444 round 34174171

## The picture

- **Headline — "HORMUZ ON FIRE".** Tehran attacks tankers in the Strait
  of Hormuz as a pair is struck near Oman; Bahrain reports an Iranian
  strike set an industrial site ablaze while air defences intercept
  more attacks.
- **Caption, line 2 — the rest of the day.** Mexico captures "El Chapo
  Isidro" (FBI's most-wanted cartel boss seized in Sinaloa after a US
  intelligence tip; the firefight leaves at least 11 dead); Zelenskyy
  says upcoming four-nation peace talks must deliver (Russian forces
  hit bridges 109 times); Nvidia faces an SEC inquiry amid a resignation
  scramble; a magnitude 6.9 earthquake strikes Peru's Junin region.

Sources: wire and press reporting of 22 November 2026 (Hormuz tanker
strikes and the Bahrain industrial-site hit; capture of Fausto Isidro
Meza Flores; Zelenskyy's four-nation talks and the 109 bridge strikes;
Nvidia SEC inquiry and the Huang resignation scramble; Junin 6.9 quake).

## How it works

- `gen.py` draws the front page and writes `entry.png` (1024x1024).
  Deterministic: fixed text and geometry, no clock, no randomness, so two
  runs produce a byte-identical PNG.
- `main.py` is the entrypoint the grader runs. It copies `entry.png` into
  the directory named by `MAKEFUN_OUTPUT_DIR` (falling back to a local
  `output/` folder) and verifies the delivered file is 1024x1024 with the
  sha256 pinned in the script. Any mismatch exits non-zero.

## Verify locally

```sh
python3 gen.py            # regenerates entry.png
python3 main.py           # delivers to output/entry.png, checks hash + size
```

The committed `entry.png` has sha256
`ebe08b7d37333b853c3119eed82a26211e0e1eb62589dc6e714f210c8da8ee43`, pinned
in `main.py` as `PINNED_SHA256`. Re-running `gen.py` reproduces the exact same bytes
(deterministic Pillow rendering), and `main.py` refuses to deliver a file
whose hash or dimensions differ.

Grader-style check (program directory read-only, output via env var):

```sh
MAKEFUN_OUTPUT_DIR=/tmp/out python3 main.py   # exit 0, writes /tmp/out/entry.png
```

Tested 22 Nov 2026: local run exit 0; grader-style run as user `nobody`
with a read-only program directory exit 0 and delivered the pinned hash;
a tampered `entry.png` is refused with exit 4 (BAD HASH). The picture is
one single scene — no separate panels — with the headline "HORMUZ ON
FIRE" and a two-line caption, so nothing is ever cut off at the edge.
