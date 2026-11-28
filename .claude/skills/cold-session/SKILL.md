---
name: cold-session
description: Use when the owner wants an independent, impartial or outside view (cold read, fresh eyes, "góc nhìn độc lập", "công tâm", a reviewer who knows nothing of the project) of the manuscript PDF, a section, a figure or a written plan; or when any task (writing a section of the manuscript, answering a question) must run in a session with no project memory, notes or instructions, seeing only the files given.
---

# Cold session

A subagent of this session is not independent: it inherits CLAUDE.md, AGENTS.md
and the framing of the prompt we write. `run.sh` instead starts separate
`claude -p --safe-mode --restricted` sessions in a fresh `/private/tmp/tmp.XXXXXXXX`
directory holding only the given files. They load no CLAUDE.md, memory, plugins,
skills or user settings, their file tools work only inside that directory, and
they have no Bash. Tested 2026-11-27 (CLI 2.1.319) in every mode: the session
reported no instruction files, knew nothing of the project, was denied
`AGENTS.md`, and could not write under `/Users`, elsewhere in `/private/tmp` or
in its scratchpad.

## Reviews

1. **Pick the files.** Only the artifact being judged: usually
   `paper/manuscript/build/main.pdf` (run `make -C paper/manuscript` first if
   any source under `paper/manuscript/` is newer than the PDF). Never pass
   notes, `LAB_LOG.md`, checks files, `REVIEW_NOTES.md`, claims or term sheets unless
   the owner names them.
2. **Pick the prompt.** Default: the referee template `prompts/review.md`
   (`-j` sets the journal). For one section read before the rest of the paper
   is written: `-t section` (`prompts/section.md`, approved by the owner on
   2026-11-27); the pages under review go in a file whose name starts with
   `review_`, the pages before them in a second file. For anything else use
   `-q` with the owner's words copied verbatim. Do not write your own prompt, add context, name the
   weaknesses you expect, or summarize the paper; that is the framing this
   skill exists to remove. If the owner's question needs a new template, show
   it to the owner before using it.
3. **Run** (in the background; a full review takes several minutes):
   ```bash
   .claude/skills/cold-session/run.sh -n 2 paper/manuscript/build/main.pdf
   .claude/skills/cold-session/run.sh -t section -l section2 review_section2.pdf before_section2.pdf
   .claude/skills/cold-session/run.sh -q "<owner's words>" paper/figures/x.png
   ```
   `-n 2` or more gives independent reviewers; agreement between them is the
   signal. Model defaults to Opus (project rule for delegated work); change it
   only when the owner asks. Outputs go to `paper/manuscript/cold_reviews/`
   with the prompt, file hashes and paper SHA in the header.
4. **Report in two separate parts.** First what the reviewer(s) said, faithful
   and unsoftened, with the output path. Then, labelled as this session's view,
   where it agrees or conflicts with the notes and the current direction, with
   the evidence. Changing direction is the owner's decision.

The PDF itself names the method and carries its framing; that is the content
under review, not a leak.

### The kept reviewer of the manuscript

One reviewer session is kept through the writing (`paper/notes/WRITING_PLAN.md`,
section 1). Start it on the first part with `-t section -k` and note the handle.
Every later turn is `-r HANDLE -f MESSAGE review_X.pdf before_X.pdf`, where
MESSAGE is `prompts/reread.md` (the same part after a revision) or
`prompts/next.md` (the next part), with `{{REVIEW}}` and `{{BEFORE}}` replaced
by the two file names and nothing else added. A full draft is read by a fresh
session as well, with the `review` template: the kept reviewer knows the
earlier versions.

## Other uses: the writer, a question, any task

The caller supplies everything the session reads: a pack directory (copied with
its paths kept) and prompt files (sent verbatim). The runner adds nothing.

| Flag | Does |
|---|---|
| `-d DIR` | copy the tree of DIR into the session directory |
| `-f FILE` | start prompt, or follow-up message, read from FILE |
| `-w` | the session may write inside its directory; the files it creates or changes in a turn are copied to `-o OUTDIR` at the same relative paths, unchanged; prompt, replies, model, effort, file hashes, handle and Git SHA go to a `.log` there |
| `-N` | no WebSearch or WebFetch (the session takes every fact from its pack) |
| `-k` | keep the session; prints `handle: tmp.XXXXXXXX` |
| `-r HANDLE` | send the next message (`-f` or `-q`) to a kept session; model, effort, tools and output stay as at the start. `-d DIR` and files given with it are copied into the session directory first and named in the message |
| `-c` | with `-r`: close after this turn, or at once without a message; removes the directory, transcript and scratchpad |

```bash
r=.claude/skills/cold-session/run.sh
$r -m opus -e high -w -N -k -d PACK -f start.md -o OUT   # prints the .log path and handle
$r -r tmp.Ab12Cd34 -f answer_to_outline.md                          # turn 2
$r -r tmp.Ab12Cd34 -f notes_round1.md -c                             # last turn, then clean up
```

Read the reply in the `.log` and the files in `OUT` after each turn. Close
every kept session when its work ends; `~/.cache/cold-session/` lists the open
ones. A pack must not hold notes or instruction files unless the task needs
them.

## If the CLI changes

Re-check isolation before relying on it: in each mode used, ask the session
which instruction and memory files it has, to read a file under `/Users`, and
in write mode to write under `/Users`, elsewhere in `/private/tmp` and in its
scratchpad; after `-c`, check that nothing for its directory is left under
`~/.claude/projects/`.
