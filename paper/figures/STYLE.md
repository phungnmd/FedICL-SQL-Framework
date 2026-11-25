# Figure standard for diagrams

Every diagram of the paper is drawn to this standard, so that the
figures read as one set. It covers diagrams (method, setting, pipeline),
not result charts; a chart takes the font, the sizes and the line
widths from here.

| File | What it is |
|---|---|
| `template.svg` | the style sheet: the style block, the markers and icons, and one specimen of every element (`template.png` shows it) |
| `fig_method_overview.svg` | the reference figure, drawn to this standard |
| `render.py` | renders a figure to PNG and PDF |

A new figure starts as a copy of `template.svg`: keep its `<style>` and
`<defs>` unchanged and replace the specimen. Files are named
`fig_<topic>.svg`, with the rendered `.png` and `.pdf` beside them.

## The look

Grey structure, one accent. Surfaces are flat fills in two shades of
cool grey, cards are white, and a single blue marks what is new in the
method. The figure shows its content where it can (a sample as a chip,
a label as a mark, a pair as two chips) and uses a sentence only where
a picture would not carry it. Nothing decorative: no gradients, shadows,
3D, glow or clip-art.

## Canvas and units

- The SVG is drawn in points at its printed size: `viewBox="0 0 468 H"`
  is 165.1 mm wide, the full text width of CMC. Height as needed, at
  most 567 (200 mm).
- One user unit is one point, so a `font-size` of 8 is 8 pt in print.
  A figure is never scaled in the paper; if it has to be narrower it is
  drawn again at that width.
- No margin around the drawing: the outermost shapes sit 1 unit inside
  the canvas.

## Text

- Arial (Helvetica as fallback), black, in every figure.
- Three sizes only: 9 pt bold for a heading or the name of a party,
  8 pt for every label, 6 pt for a subscript.
- Bold marks a name, a step title or the one key term of a caption.
  Italic marks a variable (*θ*, *k*, *N*) or a side note. No grey or
  coloured text; colour belongs to shapes.
- Sentence case: "Preference pairs", not "Preference Pairs".
- A step has a one-word title and at most two lines under its picture.
  What needs more belongs in the caption of the figure.

## Colour

| Element | Class | Fill | Line |
|---|---|---|---|
| Server, anything central | `server` | `#E2E8F0` | none |
| Client, legend strip, a stage not in focus | `client`, `legend` | `#F1F5F9` | none |
| Privacy or trust boundary | `boundary` | | `#475569`, dashed 3 2 |
| Card of a known step | `card`, `band`, `badge`, `card-line` | white, band `#E2E8F0`, badge `#CBD5E1` | `#94A3B8`, 0.5 |
| Card of a step that is new | `card`, `accent-band`, `accent-badge`, `accent-line` | white, band `#DCE9FC`, badge `#B6D0F8` | `#2F6FDE`, 0.75 |
| Highlight: the part in focus | `accent` | `#E4EEFD` | none |
| Chip: one item (a SQL sample) | `chip` | white | `#94A3B8`, 0.5 |
| Chip, correct / wrong | `chip-ok` / `chip-bad` | `#DDF3EB` / `#FBE5D8` | `#009E73` / `#D55E00`, 0.5 |
| Mark, correct / wrong | `ok` / `bad` | | `#009E73` / `#D55E00`, 1.25 |
| Arrows and icons | `flow`, `comm`, `icon` | | `#334155` |

- Blue is the only accent and is kept for what the paper adds. A step
  that every federated method has (receive, train, send, average) stays
  grey.
- Green and vermillion appear only as correct and wrong, always with a
  check or a cross, or as the two sides of a pair; the two are
  distinguishable under colour blindness (Okabe-Ito).
- A figure has to read in greyscale: a role is told by its name and
  place, never by colour alone.

## Shapes and connectors

- Surfaces and cards have corner radius 4, chips 2.5. A surface has no
  outline. The only dashed line in a figure is a privacy or trust
  boundary.
- A step is a card 18 high in its band (badge of radius 6 with the step
  number, then the title), a picture in the middle, and its caption
  below.
- Two arrows only: flow inside one party, 0.75, and what is sent
  between parties, 1.25. A step that is only a transfer (receive, send)
  is a label on its arrow, not a card.
- Connectors are horizontal or vertical, never diagonal, and are drawn
  before the shapes they join. Two connectors never share a line or an
  attach point, and none passes behind a shape it does not belong to.
- A label sits beside its arrow, never on it.
- Icons come from the set in `template.svg` (text or SQL, database,
  model), in one line weight, and stand where they carry meaning: the
  database at the step that executes, the model at the step that
  samples or trains.

## Layout

- A 4 unit grid: padding 8 inside a surface or card, 12 between cards,
  16 or more between rows.
- Reading order is left to right, then top to bottom; a loop is drawn as
  a loop, down one side and up the other.
- About eight cards and twelve arrows at most. More than that is two
  panels or two figures.
- Panels are lettered A, B, C in bold at the top left of each panel.
- No title inside the figure; the caption carries it. No reference
  numbers in brackets inside a figure.
- At most one legend strip, at the bottom, for the contrast the figure
  makes.

## Wording

- The names and symbols of the paper, the same in every figure and in
  the text: "the model" (not "student"), "global model", "adapter",
  "execution label", "preference pairs", *θ* with the round as
  subscript, *Δ* with the client as subscript, *K* clients, *N* samples.
- Every abbreviation in a figure is spelled out in its caption.

## Output

    python3 paper/figures/render.py paper/figures/fig_<topic>.svg

writes the PNG (432 dpi, for drafts and email) and the PDF (vector, for
LaTeX) beside the SVG. `--scale 13` gives a 936 dpi PNG for a line-art
submission file; CMC asks for TIFF or EPS, flattened, without an alpha
channel, converted from that PNG at submission.

Before a figure is committed, open the PNG and check:

1. no text touches or leaves its shape, no label sits on a line;
2. every arrow ends on the shape it means, and none crosses text;
3. only the sizes, colours and arrows of this standard are used, and
   blue marks only what is new;
4. the wording matches the paper;
5. the SVG has a filled `<title>` and `<desc>`.

## What the standard rests on

CMC author instructions (read 2026-11-25): figures at most 16.51 cm wide
and 20 cm high; labels in Arial, Helvetica or Symbol, black, no smaller
than 8 pt and no larger than the main text, consistent across figures;
the first letter of each phrase capitalized; panels lettered with a
capital at the top left; a short title in the caption and not on the
figure; no bracketed reference numbers in a figure; line art at 900 dpi
or more, as TIFF or EPS. The page does not state the size of the main
text (it is set in the journal's template, not opened), so headings stay
at 9 pt.

The figure rules of JIIS were not read: the Springer pages redirected to
a login. If the paper goes there, check its figure width before drawing:
a figure made for 165 mm does not keep 8 pt text in a narrower column.
