# The World in One Picture — 22 November 2026

A one-page newspaper infographic (1024x1024 PNG) summarising five verified
world-news stories from Sunday 22 November 2026. Teal-and-amber front-page
design, generated deterministically with Pillow and DejaVu fonts.

Repo anchor: makefun anchor 38678accf7ae0553320c8e1b9accf0852a1c6444 round 34174171

## The five stories

1. **Lead — Iran strikes tankers in Hormuz.** Tehran attacks tankers in
   the Strait of Hormuz as a pair is struck near Oman; Bahrain reports an
   Iranian strike set an industrial site ablaze while air defences
   intercept more attacks.
2. **Diplomacy — Zelenskyy: peace talks must deliver.** Ukraine's
   president says upcoming four-nation talks must bring meaningful
   progress as Russian forces hit bridges 109 times.
3. **Justice — Mexico captures "El Chapo Isidro".** FBI's most-wanted
   cartel boss seized in Sinaloa after a US intelligence tip; the
   firefight leaves at least 11 dead.
4. **Markets — Nvidia faces SEC inquiry.** Nvidia's finances come under
   SEC scrutiny as a resignation scramble shakes the chip giant.
5. **Disaster — 6.9 quake rocks Peru.** A magnitude 6.9 earthquake
   strikes Peru's Junin region on Sunday.

Also in the news: Alcaraz faces Zverev in the ATP Finals decider; France
sees a 4th weekend of cost-of-living protests; Norway court voids oil
licences; Gaza flooding: four nations urge Israel to open aid access.

Sources: wire and press reporting of 22 November 2026 (Hormuz tanker
strikes and the Bahrain industrial-site hit; Zelenskyy's four-nation
talks and the 109 bridge strikes; capture of Fausto Isidro Meza Flores;
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
`a69b0268305836a24748e8580e36210e1237ad56be0da19718b5e36de35ab633`, pinned
in `main.py` as `PINNED_SHA256`. Re-running `gen.py` reproduces the exact same bytes
(deterministic Pillow rendering), and `main.py` refuses to deliver a file
whose hash or dimensions differ.

Grader-style check (program directory read-only, output via env var):

```sh
MAKEFUN_OUTPUT_DIR=/tmp/out python3 main.py   # exit 0, writes /tmp/out/entry.png
```

Tested 22 Nov 2026: local run exit 0; grader-style run as user `nobody`
with a read-only program directory exit 0 and delivered the pinned hash;
a tampered `entry.png` is refused with exit 4 (BAD HASH). The footer
ticker runs on two lines so no item is ever cut off at the right edge.
