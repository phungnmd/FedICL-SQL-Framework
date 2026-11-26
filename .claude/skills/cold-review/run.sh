#!/usr/bin/env bash
# Run one or more Claude Code sessions that see nothing of this project except
# the files given: no CLAUDE.md/AGENTS.md, no memory, no plugins or skills, no
# read access outside a fresh temporary directory.
#
# usage: run.sh [-t TEMPLATE | -q QUESTION] [-j JOURNAL] [-n N] [-m MODEL]
#               [-e EFFORT] [-l LABEL] [-o OUTDIR] FILE...
#   -t  prompt template in prompts/ (default: review)
#   -q  the owner's own question, used verbatim instead of a template
#   -j  journal name put into the template (default: Journal of Intelligent
#       Information Systems)
#   -n  number of independent sessions, run in parallel (default: 1)
#   -m  model (default: opus)     -e  effort level (default: CLI default)
#   -l  label for the output file names (default: template name or "question")
#   -o  output directory (default: paper/manuscript/cold_reviews)
set -euo pipefail

here="$(cd "$(dirname "$0")" && pwd)"
repo="$(cd "$here/../../.." && pwd)"

template=review; question=""; journal="Journal of Intelligent Information Systems"
n=1; model=opus; effort=""; label=""; outdir="$repo/paper/manuscript/cold_reviews"
while getopts "t:q:j:n:m:e:l:o:" opt; do
  case $opt in
    t) template=$OPTARG ;; q) question=$OPTARG ;; j) journal=$OPTARG ;;
    n) n=$OPTARG ;; m) model=$OPTARG ;; e) effort=$OPTARG ;;
    l) label=$OPTARG ;; o) outdir=$OPTARG ;;
    *) sed -n '2,17p' "$0"; exit 2 ;;
  esac
done
shift $((OPTIND - 1))
[ $# -ge 1 ] || { echo "error: give at least one file to review" >&2; exit 2; }
for f in "$@"; do [ -f "$f" ] || { echo "error: not a file: $f" >&2; exit 2; }; done

if [ -n "$question" ]; then
  prompt="$question"; source_desc="owner question (verbatim)"; label=${label:-question}
else
  tfile="$here/prompts/$template.md"
  [ -f "$tfile" ] || { echo "error: no template $tfile" >&2; exit 2; }
  prompt="$(sed "s|{{JOURNAL}}|$journal|g" "$tfile")"
  source_desc="template prompts/$template.md (journal: $journal)"; label=${label:-$template}
fi
names=""; for f in "$@"; do names="$names $(basename "$f")"; done
prompt="$prompt

Files in your working directory:$names"

mkdir -p "$outdir"
stamp="$(date +%Y-%m-%d_%H%M)"
effort_args=(); [ -n "$effort" ] && effort_args=(--effort "$effort")
dirs=(); pids=(); outs=()

for i in $(seq 1 "$n"); do
  # Neutral path: the session sees its cwd, so the name must not reveal the project.
  d="$(mktemp -d /private/tmp/review.XXXXXX)"; dirs+=("$d")
  for f in "$@"; do cp "$f" "$d/"; done
  out="$outdir/${stamp}_${label}_$i.md"; outs+=("$out")
  {
    echo "<!-- cold review | $(date '+%Y-%m-%d %H:%M') | model: $model ${effort:+| effort: $effort }| session $i of $n"
    echo "     prompt: $source_desc"
    for f in "$@"; do echo "     file: $f sha256 $(shasum -a 256 "$f" | cut -c1-12)"; done
    echo "     paper git: $(git -C "$repo" rev-parse --short HEAD)$(git -C "$repo" diff --quiet || echo ' (dirty)') -->"
    echo; echo "## Prompt"; echo; echo '```text'; echo "$prompt"; echo '```'; echo; echo "## Response"; echo
  } > "$out"
  (
    cd "$d"
    printf '%s' "$prompt" | claude -p --safe-mode --no-session-persistence \
      --model "$model" ${effort_args[@]+"${effort_args[@]}"} \
      --allowedTools WebSearch WebFetch \
      --disallowedTools Bash Edit Write NotebookEdit \
        "Read(~/**)" "Read(//Users/**)" "Read(//Volumes/**)" "Read(//private/tmp/claude-501/**)" \
      2> >(grep -v "sign-in ends" >&2) >> "$out"
  ) &
  pids+=($!)
done

status=0
for p in "${pids[@]}"; do wait "$p" || status=1; done
for d in "${dirs[@]}"; do rm -rf "$d"; done
printf '%s\n' "${outs[@]}"
exit $status
