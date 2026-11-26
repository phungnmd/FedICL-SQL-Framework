# Figure standard for diagrams

Every diagram of the paper is drawn to this standard, so that the
figures read as one set and pass the figure rules of both target
journals (CMC and JIIS) without being redrawn. It covers diagrams
(method, setting, pipeline), not result charts; a chart takes the font,
the sizes, the colours and the line widths from here.

| File | What it is |
|---|---|
| `template.svg` | the style sheet: the style block, the markers and icons, and one specimen of every element (`template.png` shows it) |
| `fig_method_overview.svg` | the reference figure, drawn to this standard |
| `render.py` | renders a figure to PNG, PDF and EPS |

A new figure starts as a copy of `template.svg`: keep its `<style>` and
`<defs>` unchanged and replace the specimen. Files are named
`fig_<topic>.svg`, with the rendered `.png` and `.pdf` beside them.

## The look

Three role colours on white, each a pale fill with a line of the same
colour: blue for the federated side, violet for the method, amber for
what is private to a client. Icons are two-tone (a line and a tint of
the role colour) and large enough to anchor a block. The figure shows
its content where it can (a sample as a chip, a label as a mark, a pair
as two chips) and uses a sentence only where a picture would not carry
it. Nothing decorative: no gradients, shadows, 3D, glow or clip-art, and
no icon that stands for nothing in the method.

## Canvas and units

- The SVG is drawn in points at its printed size:
  `viewBox="0 0 337 H"` is 119 mm wide, the figure width of JIIS and
  inside the limit of CMC. Height as needed, at most 552 (195 mm).
- One user unit is one point, so a `font-size` of 8 is 8 pt in print.
  A figure is never scaled in the paper; if it has to be another width
  it is drawn again at that width.
- No margin around the drawing: the outermost shapes sit 1 unit inside
  the canvas.

## Text

- Arial (Helvetica as fallback), black, in every figure. Colour belongs
  to shapes, never to text.
- Two sizes: 9 pt bold for a heading or the name of a party, 8 pt for
  every label. A subscript is set at 6 pt, the only text below 8 pt.
- Bold marks a name, a step title or the one key term of a caption.
  Italic marks a variable (*θ*, *k*, *N*) or a side note.
- Sentence case: "Preference pairs", not "Preference Pairs".
- A step has a one-word title and at most three short lines beside its
  picture. What needs more belongs in the caption of the figure.

## Colour

| Role | Classes | Fill | Line |
|---|---|---|---|
| Federated side: server, FedAvg, what is sent | `blue`, `chip-blue`, `ic-blue`, `comm` | `#E8F0FE` | `#2563EB` |
| The method: its stage, its steps | `violet`, `card-band`, `card-badge`, `card-line`, `chip-violet`, `ic-violet` | `#F1EBFE`, band `#E9DFFD`, badge `#CDBBFA` | `#7C3AED` |
| Private to a client: panel, boundary, data | `client`, `boundary`, `ic-amber` | `#FFF7E6`, icon tint `#FBDFA6` | `#B45309`, boundary dashed 3 2 |
| Neutral: a part outside the three roles | `plain`, `chip`, `legend`, `flow` | `#F1F5F9`, chip white | `#94A3B8`, arrows `#334155` |
| Correct / wrong | `chip-ok`, `ok` / `chip-bad`, `bad` | `#DDF3EB` / `#FBE5D8` | `#009E73` / `#D55E00` |

- A colour is used only for its role, the same in every figure. A
  figure with other roles keeps blue for the shared or central side and
  amber for private data.
- Green and vermillion appear only as correct and wrong, always with a
  check or a cross, or as the two sides of a pair with a `>` between
  them; the two are distinguishable under colour blindness (Okabe-Ito).
- Colour is never the only carrier: every role is also named in text,
  and the figure has to read in greyscale. A colour key at the bottom
  names the roles.

## Shapes and connectors

- Surfaces and cards have corner radius 4, chips 2.5. The only dashed
  line in a figure is a privacy or trust boundary.
- A step is a white card: a band 18 high (badge of radius 6 with the
  step number, then the title), a picture, and its caption beside the
  picture.
- Two arrows only: flow inside one party, 0.75, slate; what is sent
  between parties, 1.25, blue. A step that is only a transfer (receive,
  send) is a label on its arrow, not a card.
- Connectors are horizontal or vertical, never diagonal, and are drawn
  before the shapes they join. Two connectors never share a line or an
  attach point, and none passes behind a shape it does not belong to.
- A label sits beside its arrow, never on it.
- Icons come from the set in `template.svg` (model, database, server,
  text or SQL, lock), take the colour of the role they stand in through
  `ic-blue`, `ic-violet` or `ic-amber`, and stand where they carry
  meaning: the database at the step that executes, the model where it
  samples or trains.
- No line is thinner than 0.5.

## Layout

- A 4 unit grid: padding 8 inside a surface or card, 12 to 16 between
  cards and rows.
- Reading order is left to right, then top to bottom; a loop is drawn as
  a loop, down one side and up the other, with numbered steps.
- About six cards and twelve arrows at most. More than that is two
  panels or two figures.
- Panels are lettered in bold at the top left of each panel: capitals
  (A, B) for CMC, lowercase (a, b) for JIIS.
- No title and no caption sentence inside the figure; the caption
  carries them and names every element. No reference numbers in
  brackets inside a figure.
- At most one strip at the bottom, the colour key.

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

## Output

    python3 paper/figures/render.py paper/figures/fig_<topic>.svg

writes the PNG (432 dpi, for drafts and email) and the PDF (vector,
fonts embedded, for LaTeX) beside the SVG. With `--eps` it also writes a
vector EPS, the file both journals take for line art; it is made at
submission and not committed.

Figures of the paper are drawn as vector code. An image made by an
image generator does not go into the paper.

Before a figure is committed, open the PNG and check:

1. no text touches or leaves its shape, no label sits on a line;
2. every arrow ends on the shape it means, and none crosses text;
3. only the sizes, colours and arrows of this standard are used, each
   colour in its role;
4. the wording matches the paper;
5. the figure still reads in greyscale;
6. the SVG has a filled `<title>` and `<desc>`.

## What the standard rests on

Both sets of author instructions were read on 2026-11-25.

| Rule | CMC | JIIS | Here |
|---|---|---|---|
| Width | at most 165.1 mm | 119 mm (small-sized journal) | 119 mm |
| Height | at most 200 mm | at most 195 mm | at most 195 mm |
| Font | Arial, Helvetica or Symbol, black | Helvetica or Arial | Arial, black |
| Size at final size | 8 pt or more, not above the main text, consistent | about 8 to 12 pt, little variance | 8 and 9 pt |
| Lines | | 0.3 pt or more, none faint | 0.5 pt or more |
| Title | in the caption, not on the figure | no title or caption in the figure | none |
| Panels | capital at the top left | lowercase letters | per journal |
| Colour | | free online; has to read in black and white; not the only carrier; lettering contrast 4.5:1 or more | black text on pale fills, roles named in text |
| File | line art at 900 dpi or more, TIFF or EPS | vector as EPS with fonts embedded; bitmap line art at 1200 dpi | vector PDF and EPS |
| Other | capital first letter of each phrase; no bracketed reference numbers | caption identifies every element; RGB; Springer policy on generative AI images | followed |

JIIS is a small-sized Springer journal: its pages are 155 by 235 mm and
the text block of a 2026 article measures 122 mm, so its figures are
119 mm wide. The CMC page does not state the size of its main text (it
is set in the journal's template, not opened), so headings stay at 9 pt.
Springer's policy page on generative AI images was not opened; the JIIS
instructions only point to it.
