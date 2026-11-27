# Calibration material (for the editor)

Nothing in this folder is given to the writer. The writer's voice comes
from `../VOICE_GUIDE.md` and from the register of the brief itself
(owner, 2026-11-27); the passages from published papers that stood here
until that day were removed, and no text of a published paper reaches
the writer.

| File | What it is for |
|---|---|
| `style_profile.md` | the register of ten published papers by kind of section, and the terms of the field; `TERMS.md` rests on its last table |
| `style_profile_data.md`, `style_reference.json` | the measures behind it, written by `tools/style_profile.py profile`; `compare` reads the JSON |
| `section_rhetoric.md` | paragraph roles by kind of section (from PaperOrchestra); one of the sources of `VOICE_GUIDE.md`, kept for the editor |

How the main session uses it:

- `tools/style_profile.py compare FILE --kind KIND` on every brief
  before the writer starts and on every draft after it. A brief far
  from the range of the papers is rewritten before any prose exists.
- `make overlap`: the share of each section in runs of five or more
  words of the closest papers (CodeLutra, OpenFedLLM), whose arXiv
  sources are kept in `.sources/`, outside Git.

The voice guide was drawn up from a reading of LESFT (CMC 2026),
OpenFedLLM, CodeS, LoRA, FedProx and the measures above. It quotes none
of them.
