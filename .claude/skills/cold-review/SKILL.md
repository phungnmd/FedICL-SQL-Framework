---
name: cold-review
description: Use when the owner wants an independent, impartial or outside view (cold read, fresh eyes, "góc nhìn độc lập", "công tâm", a reviewer who knows nothing of the project) of the manuscript PDF, a section, a figure or a written plan, from an agent with no project memory, notes or instructions.
---

# Cold review

A subagent of this session is not independent: it inherits CLAUDE.md, AGENTS.md
and the framing of the prompt we write. `run.sh` instead starts separate
`claude -p --safe-mode` sessions in a fresh `/private/tmp/review.XXXXXX`
directory holding only the given files. They load no CLAUDE.md, memory, plugins
or skills, cannot read anything under `/Users`, and have no Bash or Write.
Tested 2026-11-26: such a session reported no instructions, knew nothing of the
project, read the PDF and was denied `AGENTS.md`.

## Steps

1. **Pick the files.** Only the artifact being judged: usually
   `paper/manuscript/build/main.pdf` (run `make -C paper/manuscript` first if
   any source under `paper/manuscript/` is newer than the PDF). Never pass
   notes, `LAB_LOG.md`, briefs, `REVIEW_NOTES.md`, claims or term sheets unless
   the owner names them.
2. **Pick the prompt.** Default: the referee template `prompts/review.md`
   (`-j` sets the journal). For anything else use `-q` with the owner's words
   copied verbatim. Do not write your own prompt, add context, name the
   weaknesses you expect, or summarize the paper; that is the framing this
   skill exists to remove. If the owner's question needs a new template, show
   it to the owner before using it.
3. **Run** (in the background; a full review takes several minutes):
   ```bash
   .claude/skills/cold-review/run.sh -n 2 paper/manuscript/build/main.pdf
   .claude/skills/cold-review/run.sh -q "<owner's words>" paper/figures/x.png
   ```
   `-n 2` or more gives independent reviewers; agreement between them is the
   signal. Model defaults to Opus (project rule for delegated work); change it
   only when the owner asks. Outputs go to `paper/manuscript/cold_reviews/`
   with the prompt, file hashes and paper SHA in the header.
4. **Report in two separate parts.** First what the reviewer(s) said, faithful
   and unsoftened, with the output path. Then, labelled as this session's view,
   where it agrees or conflicts with the notes and the current direction, with
   the evidence. Changing direction is the owner's decision.

## Notes

- The PDF itself names the method and carries its framing; that is the content
  under review, not a leak.
- Each run is independent; nothing carries over between runs, so a follow-up
  question to the same reviewer is not possible. Rerun with the question
  instead.
- If the CLI changes, re-check isolation: run in an empty `/private/tmp` dir and
  ask the session which instruction files it sees and to read a file under
  `/Users`.
