# Figure standard for diagrams

Every diagram of the paper is drawn to this standard, so that the
figures read as one set and pass the figure rules of CMC. It covers
diagrams (method, setting, pipeline), not result charts; a chart takes
the font, the sizes, the colours and the line widths from here
(`paper/manuscript/tools/charts.py`).

| File | What it is |
|---|---|
| `template.svg` | the style sheet: the style block, the markers and icons, and one specimen of every element (`template.png` shows it) |
| `fig_method_overview.svg` | the reference figure, drawn to this standard |
| `render.py` | renders a figure to PNG, PDF and EPS |

A new figure starts as a copy of `template.svg`: keep its `<style>` and
`<defs>` unchanged and replace the specimen. Files are named
`fig_<topic>.svg`, with the rendered `.png` and `.pdf` beside them.

## The look

Few colours on white, each a pale fill with a line of the same colour,
used only where a role has to be told apart: blue for the server and
what is sent to it, amber for what is private to a client, and the
method colour for our part where it stands beside a baseline. Steps,
baselines and everything else are neutral: white cards, slate lines.
Icons are two-tone (a line and a tint) and large enough to anchor a
block. The figure shows its content where it can (a sample as a chip, a
label as a mark, a pair as two chips) and uses a sentence only where a
picture would not carry it. Nothing decorative: no gradients, shadows,
3D, glow or clip-art, and no icon that stands for nothing in the method.

## Canvas and units

- The SVG is drawn in points at its printed size:
  `viewBox="0 0 468 H"` is the text width of CMC, 165.1 mm. Height as
  needed, at most 567 (200 mm); a figure aims at about half its width
  or less, as framework figures in CMC and in the Text-to-SQL papers we
  cite do.
- One user unit is one point, so a `font-size` of 8 is 8 pt in print.
  The figure goes into the paper at its own size,
  `\includegraphics{figures/fig_<topic>.pdf}`, never with a `width`;
  if it has to be another width it is drawn again at that width.
- No margin around the drawing: the outermost shapes sit 1 unit inside
  the canvas.

## Text

- Arial (Helvetica as fallback), black, in every figure. Colour belongs
  to shapes, never to text.
- Two sizes: 9 pt bold for a heading or the name of a party, 8 pt for
  every label. A subscript is set at 6 pt, the only text below 8 pt.
  Both stay below the 11 pt of the running text.
- Bold marks a name, a step title or the one key term of a caption.
  Italic marks a variable (*θ*, *k*, *N*) or a side note.
- Sentence case: "Preference pairs", not "Preference Pairs".
- A step has a one-word title and at most three short lines under its
  picture. What needs more belongs in the caption of the figure.
- SQL and data are printed verbatim, on one line each.

## Colour

| Role | Classes | Fill | Line |
|---|---|---|---|
| Server and what is sent to it | `blue`, `chip-blue`, `ic-blue`, `comm` | `#E8F0FE` | `#2563EB` |
| Private to a client: panel, boundary, data | `client`, `boundary`, `ic-amber` | `#FFF7E6`, icon tint `#FBDFA6` | `#B45309`, boundary dashed 3 2 |
| Our part beside a baseline | `method`, `chip-method`, `ic-method`, `card-badge` | `#F8EAF2`, tint `#EFD3E3` | `#A8528A` |
| Neutral: steps, baselines, everything else | `plain`, `card`, `card-band`, `card-line`, `chip`, `ic-slate`, `flow`, `rule` | `#F1F5F9`, card white | `#94A3B8`, icons `#475569`, arrows `#334155` |
| Correct / incorrect | `chip-ok`, `ok` / `chip-bad`, `bad` | `#DDF3EB` / `#FBE5D8` | `#009E73` / `#D55E00` |

- A colour is used only for its role, the same in every figure and
  chart. The method colour marks our part only where a baseline stands
  next to it (a panel, a box of the run, a series of a chart); the
  steps inside the method stay neutral, with the method tint on their
  badges and model icons.
- Green and vermillion appear only as correct and incorrect, always
  with a check or a cross, or as the two sides of a pair with a `>`
  between them (Okabe-Ito colours).
- Colour is never the only carrier: every role is also named in text or
  drawn by shape (the dashed boundary, a check or cross). The three role
  colours stay apart under red-green colour blindness; checked by
  simulation on 2026-11-28 (blue against method colour, Machado 2009,
  deutan: distance 148 of 255; the earlier violet scored 2).
- No colour key: the figure names its parts. No paper of the seven read
  for this standard (three in CMC, four on Text-to-SQL and federated
  fine-tuning) has one.

## Shapes and connectors

- Surfaces and cards have corner radius 4, chips 2.5. The only dashed
  line in a figure is a privacy or trust boundary.
- A step is a white card: a band 18 high (badge of radius 6 with the
  step number, then the title), a picture, and its caption under the
  picture.
- Two arrows only: flow inside one party, 0.75, slate; what is sent
  between parties, 1.25, blue. A step that is only a transfer (receive,
  send) is a label on its arrow, not a card.
- Connectors are horizontal or vertical, never diagonal. Draw them after
  the surfaces they cross and before the cards and chips they join. Two
  connectors never share a line or an attach point, and none passes
  behind a shape it does not belong to.
- A label sits beside its arrow, never on it.
- Icons come from the set in `template.svg` (model, database, server,
  text or SQL, lock), take the colour of the role they stand in, and
  stand where they carry meaning: the database at the step that
  executes, the model where it samples or trains.
- No line is thinner than 0.5.

## Layout

- A 4 unit grid: padding 8 inside a surface or card, 8 to 16 between
  cards and rows.
- Reading order is left to right, then top to bottom. Steps in sequence
  sit in one row; a loop closes through the other party, its arrows
  ending on the panel of the party they reach.
- Several parties of one kind (the K clients) are one panel with two
  copies of its frame offset by 4 behind it.
- Kinds of round that share the exchange with the server are rows of
  one client panel, each named with its rounds (t = 1, ..., T_w).
- About six cards and twelve arrows at most. More than that is two
  panels or two figures.
- Panels are lettered with bold capitals (A, B) at the top left of each
  panel.
- No title and no caption sentence inside the figure; the caption
  carries them and names every element. No reference numbers in
  brackets inside a figure.

## Wording

- The names and symbols of the paper, the same in every figure and in
  the text: "the model" (not "student"), "global model", "adapter",
  "execution label", "preference pairs", "correct" and "incorrect",
  "warm-up rounds" and "preference rounds"; the notation of
  `paper/manuscript/TERMS.md`: *θ* with the round as superscript and
  the client as subscript (the global model of round *t* is sent as
  *θ* with superscript *t*−1 and aggregated into *θ* with superscript
  *t*), *K* clients, *N* samples. A superscript is set as a subscript
  is, at 6 pt.
- Every abbreviation in a figure is spelled out in its caption.
- A worked example comes from a committed result and is printed as it
  is there.

## Output

    python3 paper/figures/render.py paper/figures/fig_<topic>.svg

writes the PNG (432 dpi, for drafts and email) and the PDF (vector,
fonts embedded, for LaTeX) beside the SVG. With `--eps` it also writes a
vector EPS; it is made at submission and not committed. The PDF is
copied to `paper/manuscript/figures/`.

Figures of the paper are drawn as vector code. An image made by an
image generator does not go into the paper.

Before a figure is committed, open the PNG and check:

1. no text touches or leaves its shape, no label sits on a line;
2. every arrow ends on the shape it means, and none crosses text;
3. only the sizes, colours and arrows of this standard are used, each
   colour in its role;
4. the wording matches the paper;
5. the SVG has a filled `<title>` and `<desc>`;
6. on the built page, the figure text is smaller than the running text.

## What the standard rests on

The CMC author instructions were read on 2026-11-25; the text width is
that of the CMC class (`Definitions/tsp.cls`, `\textwidth` 469.76 TeX
points), measured on 2026-11-28.

| Rule | CMC | Here |
|---|---|---|
| Width | at most 165.1 mm | 165.1 mm (468 pt) |
| Height | at most 200 mm | at most 200 mm |
| Font | Arial, Helvetica or Symbol, black | Arial, black |
| Size at final size | 8 pt or more, not above the main text, consistent | 8 and 9 pt, printed at 1:1 |
| Title | in the caption, not on the figure | none |
| Panels | capital at the top left | A, B |
| File | line art at 900 dpi or more, TIFF or EPS | vector PDF and EPS |
| Other | capital first letter of each phrase; no bracketed reference numbers | followed |

Framework figures compared on 2026-11-28 (height over width, by eye on
the printed page): LESFT (CMC 87(1)) 0.73, FedCO (CMC 89(1)) 0.54, an
SQL-agent system (CMC 88(2)) 0.47, OmniSQL 0.34, DIN-SQL 0.33. Their
text is at or below the running text, and they use two or three colours
with neutral outlines.
