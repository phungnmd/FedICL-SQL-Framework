# ARCHIVED — protocol-v1 manuscript skeleton

> Created 2026-08-26 as the P1.4b/P2 handoff. Draft prose against this file;
> do not copy numbers from terminal logs. Paper values come from
> `paper/results/MAIN_RESULTS.md`, and stable artifacts resolve through
> `RESULT_REGISTRY.md`.

## Title

**FedLS-SQL: Execution-Verified Large-to-Small Knowledge Transfer for
Federated NL-to-SQL**

## Abstract — five-sentence contract

1. State the problem: lightweight federated NL-to-SQL models preserve a
   structural data boundary but have limited execution accuracy.
2. State the method: private client LoRA training and sample-weighted FedAvg,
   followed by recurring server refinement from a frozen LLM using public,
   execution-verified SQL targets.
3. State deployment: clients communicate only SLM adapters and the final SLM
   runs without the teacher.
4. State the main evidence: Qwen T3 FedLS-SQL versus pure FL on Spider and the
   two positive final training seeds; mention centralized competitiveness only
   with the registered significance qualifier.
5. State mechanism/scope: hard-target transfer replicates with Gemma; RKL is
   auxiliary; claims are limited to the fixed `K=5, alpha=0.5` setup.

Do not put EM in the abstract unless required by the venue. EX is the primary
endpoint.

## 1. Introduction

### Problem and motivation

- Cross-silo institutions cannot pool private NL-SQL pairs.
- Federating a deployable SLM is communication-efficient but leaves an
  execution-accuracy gap.
- A server can host a stronger LLM and a public SQL corpus without placing the
  teacher or private client rows in the same path.

### Research question

Advisor-level question: can large-to-small collaboration address the accuracy
limitations of lightweight federated NL-to-SQL while retaining the data-
locality, communication, and resource properties motivating FL?

Operational question: can execution-verified guidance from a frozen
server-side LLM improve the EX of a federated LoRA-adapted SLM while client
rows remain local, communication is adapter-only, and deployment is SLM-only?

### Contributions

Use the safe contribution wording in `RELATED_WORK_NOVELTY_MATRIX.md`.
Contributions are: task-specific workflow; execution-verified public transfer
inside the round loop; matched causal and portability evidence; deterministic
communication plus EX-oriented failure analysis. Do not claim a new FedAvg,
LoRA, KD, reverse-KL, or generic LLM-SLM federation algorithm.

## 2. Related work

### 2.1 Federated semantic parsing and NL-to-SQL

Lead with ACL 2023 Federated Learning for Semantic Parsing. Explain that it
establishes the federated task but has no asymmetric server teacher or
execution-verified transfer pool.

### 2.2 Federated PEFT and server refinement

Cover FedPETuning, FedDF, and FedGen. Separate adapter communication from
knowledge-based model fusion.

### 2.3 Federated LLM-SLM collaboration

Cover FedMKT, FedCoLLM, FedCoT, and LaDa. Treat FedCoLLM as the closest
architectural prior and state the frozen-teacher, one-way, task-verified, and
deployment differences explicitly.

### 2.4 LLM-to-SLM transfer for Text-to-SQL

Cover KID, Pure-KD, and Struct-SQL. Acknowledge that Struct-SQL already uses
execution-correct teacher samples; locate the contribution in the federated
round workflow and evidence, not execution filtering alone.

End with the condensed comparison table from
`RELATED_WORK_NOVELTY_MATRIX.md`.

## 3. Method

### 3.1 Problem formulation and boundary

Define `K` clients, private datasets `D_k`, public server corpus `D_pub`, the
shared frozen SLM base, client/global LoRA parameters, and frozen teacher.
State that structural isolation is not differential privacy or protection
against model-update leakage. Present P1.8 only as a separately measured local
Secure Sum compatibility layer, not an end-to-end MPC deployment and not the
source of the accuracy results.

Evidence/source: `system_architecture.md` §§3–5 and `CONVENTION.MD` §5.

### 3.2 Round lifecycle

Describe broadcast → private local CE → sample-weighted factor-wise FedAvg →
public server refinement → rebroadcast. Mention the optional masked-sum wrapper
separately. Make clear that mixed-lineage
pre-server T2/T3 checkpoints already contain earlier teacher knowledge.

Evidence/source: `system_architecture.md`; implementation definitions should
be cited from the inner repository at manuscript freeze.

### 3.3 Execution-verified public targets

Describe teacher-specific full-source generation, 8-second quick execution,
official result-equivalent EX scoring, retained target pool, and equal-row gold
control. Report Qwen/Gemma pool sizes only through registered audit artifacts.

Evidence: `audit.bird.train.gold.t60`,
`audit.teacher.qwen-gemma.commonmask`, and `MAIN_RESULTS.md` §2.2.

### 3.4 Server objective

Define hard teacher-target CE as the portable core. Define reverse KL only for
teacher/student pairs with identical token-to-ID mappings and label it an
auxiliary Qwen component. Do not call it cross-tokenizer KD.

Evidence: `MAIN_RESULTS.md` §§2.2 and 4.

### 3.5 Communication and deployment

State exactly what crosses the boundary: SLM LoRA adapter tensors. The frozen
LLM stays at the server and is absent from deployment inference.

Evidence: `audit.paper.tables.qwen.s0`; 18,464,768 trainable LoRA parameters,
738,590,720 logical tensor bytes per round, and 2,215,772,160 through T3.

## 4. Experimental setup

### 4.1 Data and partition

- Private/client task: Spider grouped-domain split, fixed `K=5`,
  Dirichlet `alpha=0.5`.
- Public teacher pool: BIRD train; no test row enters training or retrieval.
- Evaluation: Spider primary; Realistic, Syn, DK, and BIRD diagnostics.
- Explain why BIRD evaluation is public-domain-adjacent and not the headline.

### 4.2 Models and training

- Primary: Qwen2.5 1.5B student / Qwen2.5-Coder 7B frozen teacher.
- Portability: Gemma 2 2B student / Gemma 2 9B frozen teacher.
- Greedy, no-ICL evaluation; EX primary, EM secondary.
- Document LoRA, rounds, local epochs, target pool, and RKL constraints from
  immutable configs rather than prose memory.

### 4.3 Baselines and controls

Mandatory table rows: untouched base where relevant, centralized-standard,
pure FL, matched public-gold CE, teacher-target CE, and full FedLS-SQL.
FedProx-LoRA remains the recommended missing reviewer baseline. There is no
federated-7B experiment; do not imply one.

### 4.4 Metrics and statistics

Define result-equivalent execution accuracy, execution errors, secondary EM,
paired exact McNemar tests, and training-seed mean/sample SD. Distinguish
question-level paired uncertainty from training-seed uncertainty.

## 5. Results

### 5.1 Main accuracy

Artifact: `MAIN_RESULTS.md` §2.1.

Headline: Qwen T3 FedLS-SQL reaches 69.54 Spider EX versus 64.31 pure FL and
67.31 centralized-standard. Phrase the centralized result as competitive:
the +2.22 difference is not significant (`p=0.0865`). Include OOD values with
dataset-specific significance rather than claiming uniform superiority.

### 5.2 What produces the gain?

Artifact: `MAIN_RESULTS.md` §4.1.

Use the matched T1 ladder. Public-gold CE does not materially improve over FL;
teacher-target CE does; full Qwen endpoint is highest. State that standalone
RKL is provisional across training seeds.

### 5.3 Repeated-round behavior and reliability

Artifacts: `MAIN_RESULTS.md` §§3.1–3.2 and the seed-1 trajectory registry row.

Plot independent pure FL and post-server FedLS-SQL at T1/T2/T3 for seeds 0
and 1. Show mixed-lineage pre-server checkpoints as a diagnostic style, never
as pure FL. Report final seed-0/1 gains of +5.23 and +3.77 EX. Seed 2 remains
deferred for final three-seed reporting.

### 5.4 Model-family portability

Artifact: `MAIN_RESULTS.md` §2.2.

Gemma target CE improves over FL by +4.06 EX and full FedLS-SQL by +4.25; the
full-vs-target difference is only +0.19 and not significant. Conclude that
execution-verified hard targets transfer; do not claim robust portable RKL.

### 5.5 Communication and resource trade-offs

Artifact: `audit.paper.tables.qwen.s0` and `MAIN_RESULTS.md` efficiency table.

Communication is closed and deterministic. P1.1b-v2 closes the scoped
deployment comparison: over five eligible repetitions on the same fixed 32
Spider rows, the BF16 FedLS-SQL student has median latency 0.7873 s/query and
3,474.6 MB peak allocated VRAM, versus 1.6460 s/query and 6,776.8 MB for the
4-bit teacher. Report the student as `2.09x` faster with `48.73%` less allocated
VRAM. Do not turn this into a training, energy, concurrency, full-test, or
federated-7B claim.

### 5.6 EX-oriented error analysis

Artifacts: `audit.qwen.t3.fl-fedls.ex-transfer` and companion examples.

Report 121 corrected versus 67 regressed cases and execution errors 193→101.
Aggregation/order/limit structures improve; set operations are the clearest
negative stratum. Use fixed-rule representative examples, not cherry-picked
terminal outputs.

## 6. Discussion

- Why teacher-generated SQL can be more useful than equal-row BIRD gold for a
  Spider-trained student: target style and student learnability are plausible,
  but keep causal language within the matched evidence.
- Why EM is secondary: result-equivalent SQL can differ in form across BIRD
  supervision and Spider evaluation.
- Why the teacher remains frozen and server-only.
- Relation to FedCoLLM and Struct-SQL: acknowledge both explicitly.
- Practical interpretation of adapter-only communication and SLM-only
  deployment.

## 7. Limitations and responsible claims

- One primary `K=5, alpha=0.5` partition; no broad heterogeneity robustness.
- Two positive final training seeds; seed 2 not yet closed at T3.
- No formal DP or update-leakage defense.
- No matched federated 7B baseline and no measured claim against 7B FL.
- Shared-server resource evidence is limited to repeated 32-row steady-state
  inference; hardware exclusivity, training cost, and energy are not measured.
- Public teacher-pool dependence and teacher-specific retention rates.
- RKL's independent increment is unstable; only hard-target transfer clearly
  replicates across families.
- FedCoLLM and Struct-SQL narrow the algorithmic novelty; the contribution is
  a federated NL-to-SQL workflow plus evidence.

## 8. Conclusion

Answer the scoped research question: in the tested fixed federated setting,
recurring execution-verified teacher supervision improves SLM execution
accuracy while retaining private-row locality, adapter-only communication, and
SLM-only deployment. Do not generalize beyond the tested partitions, teachers,
or federated optimizer.

## Core artifact freeze checklist

| Paper artifact | Evidence owner | State |
|---|---|---|
| Architecture/privacy-boundary figure | `paper/drafts/FEDLS_SQL_METHOD.md`; `paper/drafts/figures/fedls_sql_architecture.svg` | paper-ready draft; SVG visually verified |
| Main accuracy table | `MAIN_RESULTS.md` §2.1 | values ready |
| Matched transfer ablation | `MAIN_RESULTS.md` §4 | values ready |
| Two-seed convergence figure | `MAIN_RESULTS.md` §3 | values ready |
| Gemma portability table | `MAIN_RESULTS.md` §2.2 | values ready |
| Communication/resource table | `audit.paper.tables.qwen.s0`; P1.1b-v2 | ready for adapter communication and scoped deployment inference |
| EX-oriented error analysis | `audit.qwen.t3.fl-fedls.ex-transfer` | values ready |
| Nearest-work comparison | `RELATED_WORK_NOVELTY_MATRIX.md` | ready |

The Method prose and architecture/privacy-boundary figure are complete in
`paper/drafts/`. Next design the matched FedProx-LoRA baseline, one audited
stronger-skew screen, and seed-2 T3. A federated-7B run is excluded unless a
direct empirical large-model-FL claim is introduced.
