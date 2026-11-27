#!/usr/bin/env bash
# Run Claude Code sessions that see nothing of this project except the files
# given: no CLAUDE.md/AGENTS.md, no memory, no plugins or skills, no user
# settings, and file tools confined to a fresh temporary directory.
#
# start:    run.sh [-t TEMPLATE | -q TEXT | -f FILE] [-j JOURNAL] [-d DIR] [-n N]
#                  [-m MODEL] [-e EFFORT] [-l LABEL] [-o OUTDIR] [-w] [-N] [-k] [FILE...]
# continue: run.sh -r HANDLE (-q TEXT | -f FILE) [-d DIR] [-c] [FILE...]
# close:    run.sh -r HANDLE -c
#   -t  prompt template in prompts/ (default: review)
#   -q  prompt or message text, used verbatim
#   -f  prompt or message read from a file, used verbatim
#   -j  journal name put into the template (default: Journal of Intelligent
#       Information Systems)
#   -d  pack directory: its tree is copied into the session directory
#   -n  number of independent sessions, run in parallel (default: 1)
#   -m  model (default: opus)     -e  effort level (default: CLI default)
#   -l  label for output file names (default: template name, "question" or
#       the prompt file's name)
#   -o  output directory (default: paper/manuscript/cold_reviews)
#   -w  write mode: the session may write inside its directory only; files it
#       creates or changes are copied to OUTDIR (OUTDIR/<stamp>_<label>_<i>/
#       when N > 1), and prompt, replies and provenance go to a .log there
#   -N  no web: WebSearch and WebFetch are off
#   -k  keep the session for follow-ups; prints its HANDLE
#   -r  continue the kept session HANDLE (same model, effort, tools, output);
#       -d DIR and FILE... given with it are copied into the session directory
#       before the turn, and their names are appended to the message
#   -c  with -r: close the session after this turn, or at once without a
#       message (removes its directory and its stored transcript)
# FILE... are copied flat; their names are appended to a start prompt. A pack
# keeps its paths and is not listed.
set -euo pipefail

here="$(cd "$(dirname "$0")" && pwd)"
repo="$(cd "$here/../../.." && pwd)"
state="$HOME/.cache/cold-session"         # kept sessions; outside any session's reach
scratch="/private/tmp/claude-$(id -u)"    # where the CLI puts per-session scratchpads

template=review; text=""; pfile=""; journal="Journal of Intelligent Information Systems"
pack=""; n=1; model=opus; effort=""; label=""; outdir="$repo/paper/manuscript/cold_reviews"
write=0; web=1; keep=0; handle=""; close=0
while getopts "t:q:f:j:d:n:m:e:l:o:wNkr:c" opt; do
  case $opt in
    t) template=$OPTARG ;; q) text=$OPTARG ;; f) pfile=$OPTARG ;; j) journal=$OPTARG ;;
    d) pack=$OPTARG ;; n) n=$OPTARG ;; m) model=$OPTARG ;; e) effort=$OPTARG ;;
    l) label=$OPTARG ;; o) outdir=$OPTARG ;; w) write=1 ;; N) web=0 ;; k) keep=1 ;;
    r) handle=$OPTARG ;; c) close=1 ;;
    *) sed -n '2,32p' "$0"; exit 2 ;;
  esac
done
shift $((OPTIND - 1))

die() { echo "error: $*" >&2; exit 2; }
sha() { shasum -a 256 "$1" | cut -c1-12; }
gitsha() { echo "$(git -C "$repo" rev-parse --short HEAD)$(git -C "$repo" diff --quiet || echo ' (dirty)')"; }
snap() { (cd "$1" && find . -type f -print0 | xargs -0 shasum -a 256 | LC_ALL=C sort); }
fence() { echo; echo "## $1"; echo; echo '```text'; printf '%s\n' "$2"; echo '```'; echo; echo "## Response"; echo; }
[ -z "$pfile" ] || [ -f "$pfile" ] || die "not a file: $pfile"
if [ -n "$text" ]; then msg=$text; src="text given with -q (verbatim)"
elif [ -n "$pfile" ]; then msg=$(cat "$pfile"); src="file $pfile sha256 $(sha "$pfile") (verbatim)"
else msg=""; fi

# The claude call. Deny rules apply in every mode; Edit(path) rules also cover Write.
claude_args() {
  tools=Read,Glob,Grep
  args=(-p --safe-mode --restricted --permission-prompts none --model "$model")
  [ -z "$effort" ] || args+=(--effort "$effort")
  deny=(Bash NotebookEdit "Read(~/**)" "Read(//Users/**)" "Read(//Volumes/**)" "Read(/$scratch/**)")
  if [ "$write" = 1 ]; then
    tools=$tools,Write,Edit; args+=(--permission-mode acceptEdits)
    deny+=("Edit(~/**)" "Edit(//Users/**)" "Edit(//Volumes/**)" "Edit(/$scratch/**)")
  else
    deny+=(Edit Write)
  fi
  if [ "$web" = 1 ]; then tools=$tools,WebSearch,WebFetch; args+=(--allowedTools WebSearch WebFetch); fi
  args+=(--tools "$tools")
}

# run_turn DIR OUT MESSAGE SESSION-ARGS...: one turn, reply appended to OUT.
run_turn() {
  local d=$1 out=$2 m=$3; shift 3
  ( cd "$d"
    printf '%s' "$m" | claude "${args[@]}" "$@" --disallowedTools "${deny[@]}" \
      2> >(grep -v "sign-in ends" >&2) >> "$out" )
}

# collect DIR SNAPSHOT DEST LOG: copy files created or changed since SNAPSHOT.
collect() {
  snap "$1" | LC_ALL=C comm -13 "$2" - | cut -c67- | while IFS= read -r p; do
    p=${p#./}; mkdir -p "$3/$(dirname "$p")"; cp "$1/$p" "$3/$p"
    echo "wrote: $3/$p"; echo "     wrote: $p sha256 $(sha "$1/$p")" >> "$4"
  done
}

# close_dir DIR: remove the session directory, its transcript and its scratchpad.
close_dir() {
  claude purge -y "$1" >/dev/null 2>&1 || true
  rm -rf "$1" "$scratch/$(printf '%s' "$1" | tr '/.' '--')" "$state/$(basename "$1").snap"
}

save() { for v in dir sid model effort web write out files turn; do printf '%s=%q\n' "$v" "${!v}"; done > "$state/$1"; }

mkdir -p "$state"

# ---- continue or close a kept session ----
if [ -n "$handle" ]; then
  [ -f "$state/$handle" ] || die "no kept session $handle"
  . "$state/$handle"
  [ -n "$msg" ] || [ "$close" = 1 ] || die "give a message with -q or -f, or -c to close"
  for f in "$@"; do [ -f "$f" ] || die "not a file: $f"; done
  [ -z "$pack" ] || [ -d "$pack" ] || die "not a directory: $pack"
  [ -n "$msg" ] || { [ $# -eq 0 ] && [ -z "$pack" ]; } || die "files need a message with -q or -f"
  status=0
  if [ -n "$msg" ]; then
    turn=$((turn + 1)); claude_args
    # files sent with the message: copied in before the snapshot, so they do not count as written
    added=""
    for f in "$@"; do cp "$f" "$dir/"; added="$added $(basename "$f")"; done
    if [ -n "$pack" ]; then
      cp -RL "$pack/." "$dir/"
      added="$added $(cd "$pack" && find . -type f | LC_ALL=C sort | sed 's|^\./||' | tr '\n' ' ')"
    fi
    [ -z "$added" ] || msg="$msg

Files added to your working directory:$added"
    { echo; echo "<!-- turn $turn | $(date '+%Y-%m-%d %H:%M') | message: $src | paper git: $(gitsha)"
      for f in "$@"; do echo "     file: $f sha256 $(sha "$f")"; done
      [ -z "$pack" ] || echo "     pack: $pack"
      echo "-->"
      fence "Message (turn $turn)" "$msg"; } >> "$out"
    snap "$dir" > "$state/$handle.snap"
    run_turn "$dir" "$out" "$msg" --resume "$sid" || status=1
    [ "$write" = 0 ] || collect "$dir" "$state/$handle.snap" "$files" "$out"
    save "$handle"; echo "$out"
  fi
  if [ "$close" = 1 ]; then close_dir "$dir"; rm -f "$state/$handle"; echo "closed: $handle"; fi
  exit $status
fi

# ---- start new sessions ----
[ "$close" = 0 ] || die "-c needs -r HANDLE"
[ $# -ge 1 ] || [ -n "$pack" ] || die "give at least one file or -d DIR"
for f in "$@"; do [ -f "$f" ] || die "not a file: $f"; done
[ -z "$pack" ] || [ -d "$pack" ] || die "not a directory: $pack"

if [ -n "$msg" ]; then
  prompt=$msg; source_desc=$src
  if [ -n "$text" ]; then label=${label:-question}; else b=$(basename "$pfile"); label=${label:-${b%.*}}; fi
else
  tfile="$here/prompts/$template.md"
  [ -f "$tfile" ] || die "no template $tfile"
  prompt="$(sed "s|{{JOURNAL}}|$journal|g" "$tfile")"
  source_desc="template prompts/$template.md (journal: $journal)"; label=${label:-$template}
fi
if [ $# -ge 1 ]; then
  names=""; for f in "$@"; do names="$names $(basename "$f")"; done
  prompt="$prompt

Files in your working directory:$names"
fi

claude_args
mkdir -p "$outdir"
stamp="$(date +%Y-%m-%d_%H%M)"; ext=md; [ "$write" = 0 ] || ext=log
dirs=(); pids=(); outs=(); sids=(); fdirs=()

for i in $(seq 1 "$n"); do
  # Neutral path: the session sees its cwd, so the name must not reveal the project or task.
  dir="$(mktemp -d /private/tmp/tmp.XXXXXXXX)"; dirs+=("$dir")
  [ -z "$pack" ] || cp -RL "$pack/." "$dir/"
  for f in "$@"; do cp "$f" "$dir/"; done
  out="$outdir/${stamp}_${label}_$i.$ext"; outs+=("$out")
  files="$outdir"; [ "$n" = 1 ] || files="$outdir/${stamp}_${label}_$i"; fdirs+=("$files")
  sid=""; sargs=(--no-session-persistence)
  if [ "$keep" = 1 ]; then sid=$(uuidgen | tr 'A-Z' 'a-z'); sargs=(--session-id "$sid"); fi
  sids+=("${sid:--}")
  {
    echo "<!-- cold session | $(date '+%Y-%m-%d %H:%M') | model: $model ${effort:+| effort: $effort }| session $i of $n"
    echo "     prompt: $source_desc"
    echo "     tools: $tools"
    [ "$keep" = 0 ] || echo "     handle: $(basename "$dir") | session id: $sid"
    for f in "$@"; do echo "     file: $f sha256 $(sha "$f")"; done
    [ -z "$pack" ] || (cd "$pack" && find . -type f | LC_ALL=C sort | while IFS= read -r p; do
      echo "     pack: $pack/${p#./} sha256 $(sha "$p")"; done)
    echo "     paper git: $(gitsha) -->"
    fence "Prompt" "$prompt"
  } > "$out"
  snap "$dir" > "$state/$(basename "$dir").snap"
  run_turn "$dir" "$out" "$prompt" "${sargs[@]}" &
  pids+=($!)
done

status=0
for i in $(seq 0 $((n - 1))); do
  wait "${pids[$i]}" || status=1
  dir=${dirs[$i]}; out=${outs[$i]}; files=${fdirs[$i]}; sid=${sids[$i]}; h=$(basename "$dir")
  [ "$write" = 0 ] || collect "$dir" "$state/$h.snap" "$files" "$out"
  echo "$out"
  if [ "$keep" = 1 ]; then turn=1; save "$h"; echo "handle: $h"; else close_dir "$dir"; fi
done
exit $status
