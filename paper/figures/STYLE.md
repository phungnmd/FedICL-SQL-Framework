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

The look of method figures in current machine learning papers: a white
canvas, rounded boxes with a pale tint and a darker outline of the same
hue, one hue per role, short sans-serif labels, thin arrows, numbered
steps, and a single line at the bottom that says what the figure
contrasts. Nothing decorative: no gradients, shadows, 3D, glow or
clip-art.

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
- Three sizes only: 9 pt bold for a heading or the name of a container,
  8 pt for every label, 6 pt for a subscript. Nothing is smaller than
  8 pt except subscripts, nothing larger than 9 pt.
- Bold marks a name or the one key term of a box. Italic marks a
  variable (*θ*, *k*, *N*) or a side note. No grey or coloured text;
  colour belongs to shapes.
- Sentence case: "Build preference pairs", not "Build Preference Pairs".
- At most three lines in a box. A label that needs more is two boxes or
  belongs in the caption.

## Colour

One hue per role, the same in every figure. Hues come from the
Okabe-Ito palette, which stays distinct under colour blindness; the two
marks also differ in shape.

| Role | Used for | Outline | Fill | Band |
|---|---|---|---|---|
| Server | aggregation, anything central | `#0072B2` | `#E5F1F8` | `#C9E2F1` |
| Client | local steps, the private side | `#B87A00` | `#FDF4E1` | `#F8E3B5` |
| Model | parameters, adapters, what is sent or deployed | `#A8507F` | `#F7EAF2` | `#EDCFE0` |
| Data | questions, SQL, databases | `#595959` | `#F2F2F2` | `#DEDEDE` |
| Step | a step inside a container | `#595959` | `#FFFFFF` | |
| Correct | check mark | `#009E73` | | |
| Wrong | cross | `#D55E00` | | |

At most three role hues in one figure, plus the correct and wrong marks.
A figure has to stay readable in greyscale: a role is also told by its
name, never by colour alone.

## Shapes and connectors

- Box: corner radius 3, outline 0.75. A container carries its name in a
  band 16 high at the top; a step box carries a numbered badge (circle of
  radius 6.5) on the left.
- Flow inside one party: dark arrow, 0.75. Anything sent between
  parties: model-coloured arrow, 1.25. These are the only two arrows.
- Privacy or trust boundary: the outline of the container, dashed 3 2.
- Several of the same kind: two copies stacked behind, offset by 4.
- Connectors are horizontal or vertical, never diagonal, and are drawn
  before the boxes they join. Two connectors never share a line or an
  attach point, and none passes behind a box it does not belong to.
- A label sits beside its arrow, never on it.

## Layout

- A 4 unit grid: padding 8 inside a box, 8 or 12 between boxes, 16
  between columns.
- Reading order is left to right, then top to bottom; a loop is drawn as
  a loop, down one side and up the other.
- About ten boxes (containers not counted) and twelve arrows at most. More than that is two
  panels or two figures.
- Panels are lettered A, B, C in bold at the top left of each panel.
- No title inside the figure; the caption carries it. No reference
  numbers in brackets inside a figure.

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

1. no text touches or leaves its box, no label sits on a line;
2. every arrow ends on the box it means, and none crosses text;
3. only the sizes, colours and arrows of this standard are used;
4. the wording matches the paper;
5. the SVG has a filled `<title>` and `<desc>`.

## What the standard rests on

CMC author instructions (read 2026-11-25): figures at most 16.51 cm wide
and 20 cm high; labels in Arial, Helvetica or Symbol, black, no smaller
than 8 pt and no larger than the main text, consistent across figures;
the first letter of each phrase capitalized; panels lettered with a
capital at the top left; a short title in the caption and not on the
figure; no bracketed reference numbers in a figure; line art at 900 dpi
or more, as TIFF or EPS.

The figure rules of JIIS were not read: the Springer pages redirected to
a login. If the paper goes there, check its figure width before drawing:
a figure made for 165 mm does not keep 8 pt text in a narrower column.
