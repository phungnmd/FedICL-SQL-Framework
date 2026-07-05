KNOWLEDGE DISTILLATION WITH STRUCTURED
CHAIN-OF-THOUGHT FOR TEXT-TO-SQL

6
2
0
2

r
a

M
1
1

]
L
C
.
s
c
[

3
v
3
5
0
7
1
.
2
1
5
2
:
v
i
X
r
a

Khushboo Thaker1, Yony Bresler1
1Crater Labs, Toronto, Canada

§ struct-sql-distillation
Struct-SQL
{khushboo, yony}@craterlabs.io

March 13, 2026

ABSTRACT

Deploying accurate Text-to-SQL systems at the enterprise level faces a difficult trilemma involving
cost, security and performance. Current solutions force enterprises to choose between expensive,
proprietary Large Language Models (LLMs) and low-performing Small Language Models (SLMs).
Efforts to improve SLMs often rely on distilling reasoning from large LLMs using unstructured Chain-
of-Thought (CoT) traces, a process that remains inherently ambiguous. Instead, we hypothesize that
a formal, structured reasoning representation provides a clearer, more reliable teaching signal, as the
Text-to-SQL task requires explicit and precise logical steps. To evaluate this hypothesis, we propose
Struct-SQL, a novel Knowledge Distillation (KD) framework that trains an SLM to emulate a powerful
large LLM. To implement this approach, we adopt the query execution plan as a formal blueprint
to derive structured reasoning. Our SLM, distilled with a structured CoT, achieves an absolute
improvement of 8.1% over an unstructured CoT distillation baseline. A detailed error analysis reveals
that a key factor in this gain is a marked reduction in syntactic errors. This demonstrates that teaching
a model to reason using a structured logical blueprint is beneficial for reliable SQL generation in
SLMs.

1

Introduction

Text-to-SQL (NL2SQL or text2sql) has the potential to democratize data access [1]. The field has seen substantial
performance advancements driven by the advent of Large Language Models (LLMs) [2]. These models enhance the
capabilities of natural language interfaces for databases by automatically translating natural-language user questions
into SQL queries [3]. Nevertheless, widespread adoption in enterprises remains challenging due to a difficult trade-off
among three interdependent factors: cost, security, and performance. This challenge can be understood as an Adoption
Trilemma.

• Cost: High-performing models typically require significant computational resources, leading to high operational

costs, whether using proprietary APIs or privately hosted LLMs [2].

• Security: Relying on external APIs raises serious security concerns, as transmitting potentially sensitive database

schemas and sample records to third-party providers is often unacceptable in enterprise settings [4].

• Performance: Selecting open-source models for local, private deployment to address cost and security issues often
leads to the use of Small Language Models (SLMs), which typically lack adequate zero-shot accuracy for complex
real-world queries [5].

To identify the limitations of current approaches, we examine the impact of recent advances in reasoning-driven
prompting on Text-to-SQL performance. A notable portion of the recent performance gains in Text-to-SQL using LLMs
can be attributed to in-context learning (ICL) [6]. ICL-based methods, particularly those that use decomposition and
multi-step reasoning, have demonstrated substantial gains in performance on the Text-to-SQL task [3]. A prominent
ICL technique for this is Chain-of-Thought (CoT), which encourages models to think step-by-step [7, 8]. Such

A PREPRINT - MARCH 13, 2026

decomposition strategies are beneficial for generating complex SQL queries. For instance, DAIL-SQL [9] enhances CoT
through context-aware examples, while DIN-SQL [10] and Divide-and-Conquer CoT (DC-CoT) [11] improve accuracy
by breaking questions into intermediate sub-queries. Building on this logical foundation, the Query Plan CoT (QP-CoT)
guides the model through the steps that mirror a database execution plan, simulating the logical process by which
databases execute queries. By following this structured path, QP-CoT ensures that the SQL generation path aligns with
the inherent logic of query execution [11]. Although these reasoning techniques achieve considerable success, their
effectiveness is observed almost exclusively in the large LLMs. This reliance on large LLMs constitutes a significant
limitation: these methods depend on the very models that exacerbate the cost and security challenges, thereby limiting
their applicability to resource-constrained enterprise settings and contributing to the ‘Adoption Trilemma’.

The performance limitations of SLMs, suitable for private deployment, are particularly pronounced in the Text-to-SQL
domain. Standard benchmarks highlight a significant gap between large models and smaller open-source alternatives.
For example, on the BIRD mini-dev benchmark, LLMs such as GPT-4o and Claude 3.7 Sonnet (≥150B parameters)
achieve execution accuracies between 30% and 45% using standard prompting, whereas widely used SLMs such
as Mistral, Mixtral and Qwen2.5 Coder (∼7B parameters) achieve only 4% to 12%1. This paper reveals that this
severe performance degradation in SLMs persists even when advanced reasoning prompts are employed, despite their
effectiveness in larger LLMs. This finding is consistent with recent literature, suggesting that large LLMs can adhere
to the schema as long as the schema fits within their context window, a capability not observed in SLMs [12]. In our
experiments, the SLM (Qwen3-4B-Instruct-2507) prompted with QP-CoT fails primarily due to inadequate schema
adherence, with a pronounced tendency toward schema hallucination, often generating non-existent tables or columns
(see Figure 3b). Thus, while large LLMs benefit from structured reasoning strategies, SLMs do not internalize these
logical decompositions. This breakdown in structured reasoning motivates an investigation into whether the structure of
reasoning itself can be effectively transferred from large LLMs to SLMs.

To bridge this performance gap, Knowledge Distillation (KD) [13], which transfers reasoning ability from a capable
teacher model, is a key strategy [2]. KD is a model compression technique in which a smaller "student" model is trained
to mimic the behavior of a larger, pretrained "teacher" model. Beyond compression, KD enables the transfer of complex
reasoning [14] and logical skills [15, 16]. Through KD, our aim is to build SLMs for Text-to-SQL that deliver accuracy
comparable to larger LLMs while meeting enterprise cost and security requirements through private deployment. This
work argues that KD is a promising approach to addressing this trilemma, but its effectiveness depends on the type of
reasoning being distilled.

Figure 1: Unstructured vs. Structured Reasoning Distillation. The figure contrasts the two methods of reasoning
distillation: (Top) Unstructured Distillation (ReasonSQL), which relies on a free-form CoT prompt, with (Bottom) the
proposed Structured Distillation (Struct-SQL), which uses a QP-CoT prompt to generate a structured logical blueprint.
The Teacher Model’s output serves as the supervisory signal for tuning the Student Models.

Given that the core bottleneck for SLMs is replicating the teacher’s complex reasoning, the central question for KD
is identifying the optimal form of the reasoning signal to distill. Building on the success of CoT prompting [7], one
approach is to distill the teacher’s natural language reasoning traces [14]. This approach is exemplified by ReasonSQL,

1Performance on BIRD mini-dev, see https://github.com/bird-bench/mini_dev

2

Natural Language QuestionState the most popular movie?When was it released and who is thedirector for the movie?QP-CoT PromptTrace SchemaChoose Tables/Columns Table/Index Scan SelectionJoiningFilteringGroupingTeacher ModelExpert / AnnotatorKnowledge GenerationKnowledge DistillationReasonSQLStruct-SQLLet me think step by step.First I will go to the MovieTable... then select checkcolumns...forpopularity.....Preparation Steps:Load Movie table.... Scanthrough the schema..UnStructured CoTReasoningStructured ReasoningQuery PlanStudent ModelStudent ModelCoT PromptThink step by step.Tuned StudentModel Selection Steps:movie_title..release_date...Filtering Steps:Based on popularity.. of movie..A PREPRINT - MARCH 13, 2026

where the student model is trained on the teacher’s intermediate CoT steps in addition to the final SQL query. This
unstructured approach provides a better knowledge signal than finetuning on SQL queries alone and has been shown to
improve model accuracy [17]. However, we argue that the structure of the reasoning signal itself is critical for effective
distillation. We hypothesize that distilling knowledge using a more formal, structured representation of the reasoning
process that directly reflects the logical steps of query execution could provide a clearer, less ambiguous, and more
beneficial supervisory signal for distilling SLMs than unstructured CoT explanations.

To evaluate this hypothesis, we introduce Struct-SQL, a framework for distilling structured reasoning. Figure 1 shows
the KD workflow, contrasting the proposed structured reasoning approach against the standard unstructured CoT method.
Within this framework, a state-of-the-art (SOTA) Teacher Model is used to generate a QP-CoT trace, which formally
decomposes the query into a logical execution plan [11]. This structured plan, together with the generated SQL query,
constitutes the supervisory signal. A student model is then trained to replicate the entire structured output sequence
(query plan, SQL). The formal query plan serves as a clear, hierarchical blueprint that guides the student model in
learning the precise, logical steps of query construction, from schema linking and join-path selection to aggregation and
filtering. During inference, this structured reasoning is retained: the student model is given the QP-CoT prompt to
autonomously generate the query plan before synthesizing the final SQL query.

To validate our hypothesis, we perform an extensive comparative analysis on the mini-dev BIRD benchmark [5],
evaluating our Struct-SQL framework against key baselines. Our main contributions are as follows.

• We are the first to systematically evaluate the impact of KD using a structured reasoning signal for Text-to-SQL.
• We provide a comprehensive error analysis, showing that the improvement in Struct-SQL results from a marked
reduction in the syntactic errors (e.g., schema hallucination), demonstrating that the structured signal provides
a clearer curriculum.

• We validate the generalization of our framework through an ablation study on two different SLMs.
• We release the code (https://github.com/craterlabs/struct-sql-distillation) and, the model
and the dataset (https://huggingface.co/collections/craterlabs/struct-sql) to facilitate repro-
ducible research.

Following this introduction, Section 2 details the methodology. Section 3 presents the results, which are contextualized
by the related work in Section 4, and the paper concludes in Section 6.

2 Methodology

2.1 Problem Formulation

The standard Text-to-SQL task involves mapping a natural language question Q and a database schema S to an executable
SQL query YGold. Formally, given an input pair (Q, S), the goal is to learn a model M such that M (Q, S) = ˆY , where
ˆY represents the predicted query intended to give the same result as the ground truth YGold. Our work focuses on
transferring the capabilities of a large, high-performance Teacher Model, MT , to a smaller, more efficient Student
Model, MS, through KD. We formulate the distillation task as learning the Teacher’s intermediate reasoning steps,
RT , in addition to its final output, YT . Let ZT = RT ⊕ YT represent the complete output sequence. Training is
conducted over a distillation dataset DDISTILL. We employ a standard sequence completion loss, minimizing the negative
log-likelihood of the teacher-generated text ZT by updating the parameters θ of the student model:

LKD = −

(cid:88)

log PMS (θ)(ZT |Q, S)

(Q,S,ZT )∈DDISTILL

(1)

We instantiate RT either as an unstructured CoT or a structured QP-CoT to test the hypothesis that a structured
reasoning trace provides a more effective supervisory signal.

2.2 Structured CoT via Query Execution Plan

Our structured CoT strategy is inspired by a database engine’s query execution plan. A query execution plan defines the
precise sequence of steps that a database follows to access and manipulate data, often generated using an EXPLAIN
command. We adopt this ICL prompt strategy from a recent work on a Query Execution Plan-based prompting
strategy, QP-CoT [11]. Instead of a free-form explanation, the Teacher Model is prompted to generate a query plan
along with the final SQL query. As shown in Figure 2, this plan decomposes the query into a sequential execution
flow that explicitly performs selections, filters, joins, and groupings through step-by-step table scanning and data

3

A PREPRINT - MARCH 13, 2026

Figure 2: Sample structured query plan for the input "State the most popular movie? When was it released and who is
the director for the movie?"

manipulation, providing a systematic signal for the student model. Although the query plan has been explored as a
prompting technique [11], the key contribution here is to demonstrate the effectiveness of this structured reasoning as
the primary teaching signal within a KD framework.

2.3 Experimental Setup

The experiments use the SQLite-based BIRD benchmark for the data [5]. The BIRD training dataset is used for model
training, while the BIRD mini-dev dataset serves for evaluation. The Teacher Model (MT ), GPT-4o (OpenAI), is
selected due to its leading performance on the BIRD mini-dev dataset and functions as an oracle to generate high-
quality query plans. The Student Model (MS) is Qwen3-4B-Instruct-2507 (Alibaba Cloud). It was chosen for its
strong performance-to-size ratio, which enables low-latency, private deployment and thus addresses the Adoption
Trilemma [18]. All models utilize a single-pass inference mechanism and operate without multi-agent collaboration,
self-consistency checks or external correction loops. For a fair comparison with baselines, no external reasoning signals
were provided at test time. During inference, the student model autonomously generates the Query Execution Plan
based on the input prompt before generating the final SQL.

2.3.1 Model Configurations

Pretrained Models: These configurations evaluate the model’s intrinsic few-shot ICL capability using QP-CoT without
parameter updates.

• Teacher Model: GPT-4o (MT ) to establish the upper bound.
• Student Model: Qwen3-4B-Instruct-2507 to establish the lower bound.

Tuned Student Models: These configurations evaluate the Student Model after tuning it on specific signals.

• FN-Gold The Student Model was finetuned using the Gold SQL query (YGold) on the BIRD training dataset,

with a basic system instruction that directly maps natural language to SQL [10].

• ReasonSQL (unstructured KD): The Student Model was finetuned on the complete Teacher sequence ZT =
RCoT ⊕ YT , where RCoT is the free-form CoT rationale [17]. This configuration serves as the established
baseline for evaluating the efficacy of standard unstructured reasoning distillation.

4

A PREPRINT - MARCH 13, 2026

• Struct-SQL (Structured KD): The Student Model was finetuned on the entire Teacher sequence ZT = RQP-CoT⊕
YT , where RQP-CoT is the formal query plan CoT trace. This trace represents the structured logical blueprint
designed for the core hypothesis.

During inference, all models use the QP-CoT prompt structure except for ReasonSQL, which employs the unstructured
CoT prompt.

2.3.2 Distillation Dataset Construction

The KD datasets were constructed using an active generation and filtering methodology to maximize data quality
and the diversity of query complexity. To initiate the process, the databases in the corpus are partitioned into a 75%
"in-domain" (ID) database pool and a 25% "out-of-domain" (OOD) database pool, based on unique database identifiers.
This partitioning ensures that the ID pool serves as the source for all training data and the in-domain validation set,
while the OOD pool is used exclusively for the out-of-domain validation set, guaranteeing a robust measure of the
trained model’s generalization capabilities.

We then applied stratified, success-based sampling, where samples are grouped by SQL complexity categories and only
admitted if the Teacher Model generates syntactically valid and execution-correct SQL. The ID corpus is iterated using
predefined SQL structure and syntax categories to achieve target distributions for the training set (1,000 samples) and
the in-domain validation set (150 samples). These categories, as shown in Table 1, are differentiated by the complexity
of the SQL structure, including single-table queries, queries with subqueries, queries with joins/set operations and
queries that combine both joins/set operations and subqueries. For each candidate, inference was performed using
GPT-4o. A sample is admitted only if the generated SQL is both syntactically valid and yields the correct result upon
execution. New samples are generated until 1,000 successful training samples and 150 ID validation samples are
obtained. The OOD validation set (150 samples) is constructed using the same sampling and validation process, but
applied exclusively to the segregated OOD database pool to ensure that no schema overlaps. For both Struct-SQL and
ReasonSQL, we used the same data generation pipeline to ensure a controlled, methodologically fair comparison. The
datasets differ only in the format of the supervisory signal: unstructured CoT traces for ReasonSQL versus structured
QP-CoT for Struct-SQL.

Complexity Category

Training Count

ID Val Count OOD Val Count

Single Table Queries
Subquery (no join or set operations)
With JOINs / Set Ops (no Subquery)
JOINs / Set Ops and Subquery

295 (29.50%)
229 (22.90%)
398 (39.80%)
78 (7.80%)

37 (24.67%)
39 (26.00%)
57 (38.00%)
17 (11.33%)

Total Successful Samples

1000

150

46 (30.67%)
31 (20.67%)
60 (40.00%)
13 (8.67%)

150

Table 1: Distribution of Query Complexity Across Distillation Datasets. The data is partitioned by unique database
identifiers to evaluate generalization. ID Val = In-Domain Validation; OOD Val = Out-of-Domain Validation (databases
unseen in training).

2.4

Implementation and Evaluation Details

2.4.1 Post-Training Details

FN-Gold, ReasonSQL, and Struct-SQL were finetuned using Parameter-Efficient Fine-Tuning (PEFT) using Quantized
Low-Rank Adaptation (QLoRA) [19] to improve training efficiency. PEFT was chosen for its proven effectiveness in
adapting SLMs to new domains with small training datasets. Furthermore, PEFT has been shown to yield more stable
models and mitigate the risk of catastrophic forgetting of foundational knowledge. QLoRA allows recovery of near
full 16-bit finetuning task performance even when the base model is loaded at 4-bit precision [20]. The KD approach
keeps the original model parameters θBASE fixed and only updates a small set of LoRA adapter parameters θADAPTER.
We followed the QLoRA methodology [19] and applied adapters to all linear layers of the Transformer architecture.
Based on preliminary testing on a subset of the development data, we selected r = 64 and an alpha scaling of α = 128
to ensure robust adaptation. Optimization was performed using AdamW with a learning rate of 10−4, a maximum input
length of 15, 000 tokens, and a generation limit of 1, 500 tokens. We utilized a batch size of 6 for ReasonSQL and
Struct-SQL, compared to 15 for the FN-Gold baseline on an NVIDIA H200 GPU. All models minimized completion
loss. To balance in-domain accuracy with out-of-domain generalization, we used an early-stopping strategy (patience=8)
that monitored the aggregated validation loss across both the ID and OOD validation sets.

5

A PREPRINT - MARCH 13, 2026

Error Type

Subcategory

Generation (GEN) —

Description

No SQL output

Syntactic (SYN)

Semantic (SEM)

No Such Column
No Such Table
Keyword Issue
Syntax/Clause Order
Other

Non-existent column reference
Non-existent table reference
Incorrect or misplaced SQL keyword
Incorrect clause order, missing parentheses
Unclassified syntactic errors

Column Mismatch
Row Mismatch
Row & Column Mismatch
Value Mismatch
Empty Output

Incorrect number of columns
Incorrect number of row
Incorrect number of columns and rows
Incorrect data values
Empty result set

Table 2: The proposed hierarchical error taxonomy. This table categorizes Text-to-SQL errors in order of decreasing
severity and is used for subsequent failure analysis.

2.4.2 Evaluation Metrics

The primary metric is Execution Accuracy (EX), which measures the percentage of generated SQL queries that
execute without error and return the same result set as the ground-truth SQL query on the BIRD mini-dev set. A
detailed analysis of model failure modes reveals why and where certain models perform best. To facilitate analysis, we
categorize failures into three distinct types as defined in Table 2. This classification establishes a severity hierarchy for
Text-to-SQL tasks: starting with the most severe Generation Failure (GEN), where the model produces no recognizable
SQL output; followed by Syntactic Failure (SYN), which indicates an unexecutable query due to grammar or schema
errors; and finally, Logical Failure (SEM), representing a query that is syntactically correct but semantically inaccurate.
Recognizing this progression is beneficial for discerning the specific challenges and improvements associated with each
model.

3 Results

3.1 Overall Performance

The execution accuracy of Struct-SQL, compared to all baselines on the BIRD mini-dev dataset, provides strong support
for the central hypothesis. As summarized in Table 3, distilling structured reasoning results in significantly better
performance compared to unstructured distillation, ReasonSQL and traditional finetuning FN-Gold. The native Student
Model’s performance (17.0%) illustrates the Performance Trade-Off in the Adoption Trilemma, indicating that an SLM
is insufficient for production deployment without intervention. Struct-SQL achieved an 8.1-point absolute improvement
from 36.90% to 45.00% over the ReasonSQL baseline. This improvement enables the Student Model to cover 84% of
the Teacher Model’s execution accuracy.

Model

Teacher (GPT-4o)
Student Model

Prompt

QP-CoT
QP-CoT

Tuned Student Models
FN-Gold
ReasonSQL
ReasonSQL (mismatched)2 QP-CoT
QP-CoT
Struct-SQL (Ours)

QP-CoT
CoT

Overall

EX

Avg. Tokens

EX by Difficulty
Simple Moderate Challenging

298 ± 96
53.60%
17.00% 1465 ± 136

68.24%
34.45%

52.00%
9.60%

198 ± 257
34.30%
99 ± 99
36.90%
145 ± 49
29.20%
45.00% 362 ± 201

45.94%
49.32%
46.62%
65.54%

32.80%
33.20%
24.80%
40.4%

36.27%
9.80%

20.58%
27.45%
14.71%
25.49%

Table 3: Overall and difficulty-wise execution accuracy (EX) on the BIRD mini-Dev set, along with average inference
tokens (Avg. Tokens). Struct-SQL achieves the highest EX among all tuned student models, particularly for simpler and
moderate queries. An 8.1-point EX improvement over ReasonSQL requires 3.6 times more tokens.

6

A PREPRINT - MARCH 13, 2026

To isolate whether Struct-SQL’s performance gains stem from the structured QP-CoT prompt format at inference time
or from the structured supervisory signal during training, we conducted an additional ablation study. We evaluated
the ReasonSQL model—trained on unstructured CoT traces—using the QP-CoT prompt at inference, denoted as
ReasonSQL (mismatched) in Table 3. This configuration achieved only 29.2% execution accuracy, a substantial drop
from the 36.9% achieved when ReasonSQL uses its native CoT prompt. This 7.7-point degradation reveals a critical
prompt-training mismatch: a model trained on unstructured reasoning cannot effectively leverage a structured prompt
format, even when the prompt includes few-shot examples demonstrating how to generate the structured query plan.
This suggests that in SLMs, ICL alone is insufficient to bridge the gap; rather, the model must be explicitly trained
on structured reasoning to internalize the required logical decomposition patterns. The strength of the training signal
is further evidenced by Struct-SQL, which achieves 45.0% EX using the identical QP-CoT prompt. This disparity
validates that Struct-SQL’s success stems from internalizing the logical decomposition patterns during training, which
the prompt alone cannot replicate.

3.2 Analysis of Model Failures

Figure 3 presents hierarchical pie charts. The inner ring displays top-level results that depict success versus categorized
error types, while the outer rings further specify subcategories of failures, as defined in Table 2. For successful queries,
the outer ring categorizes results by the difficulty level of the SQL queries in the BIRD dataset. As visually summarized
in the hierarchical pie charts, a key dichotomy emerges between the Teacher and other baselines, primarily distinguished
by their dominant error types. The Teacher Model (MT ), shown in Figure 3a, achieved the highest success rate. Its
failures were predominantly semantic errors (∼30%), indicating challenges with logical complexity. The Student Model
(MS), shown in Figure 3b, had a higher number of syntactic errors, including schema hallucination, underscoring a
fundamental inability to adhere to the database schema before post-training.

The standard finetuning baseline (FN-Gold) reflects the performance achieved by training solely on the gold SQL(YGold),
without incorporating intermediate reasoning. As shown in Figure 3c, this approach focused its gains almost entirely on
reducing semantic errors (from 53.8% to 33.0%, a 20.8-point drop) of the Student Model MS, but failed to address the
syntactic bottleneck: overall syntactic errors remained nearly unchanged (24.6% to 23.6%). These results confirm that
training on only the final query output is insufficient for learning strict SQL grammar.

The unstructured distillation (ReasonSQL) baseline evaluates distillation through an unstructured reasoning trace
(RCoT ). As shown in Figure 3d, this approach achieved an execution accuracy of 36.9%, higher than that of MS and
FN-Gold, indicating that unstructured CoT reasoning provides a better distillation signal than both the naive model
and FN-Gold. ReasonSQL significantly reduced the rate of generation errors compared to the naive Student Model
MS, suggesting that unstructured distillation enhanced the stability of the model. Furthermore, it reduced semantic
errors from 53.8% to 39.8% (a 14.0-point reduction) and reduced syntactic errors from 24.6% to 21.2% (a 3.4-point
reduction), primarily by improving basic schema linking and eliminating ‘No Such Table’ errors. These findings align
with previous research demonstrating that CoT-based distillation improves accuracy [15] and further clarify its specific
advantages.

As established above, unstructured distillation ReasonSQL outperformed both the naive Student Model and standard
finetuning FN-Gold. Struct-SQL, as shown in Figure 3e, outperformed ReasonSQL. By distilling the reasoning signal
into a structured blueprint, Struct-SQL increased execution accuracy from 36.9% to 45.0% (an 8.1-point improvement)
compared to ReasonSQL. This improvement appeared across the error severity hierarchy. Struct-SQL nearly eliminated
generation errors, reducing the rate from 2.2% to 0.4% (a 1.8-point reduction). For syntactic errors, although ReasonSQL
outperformed the naive model, it did not enforce strict schema alignment. In contrast, Struct-SQL reduced the total
syntactic error count from 21.2% in ReasonSQL to 16.8% (a 4.4-point reduction). This reduction included fewer
‘No Such Column’ hallucinations, 19.0% to 15.8% (a 3.2-point reduction) and the elimination of ‘Keyword Issues’,
showing a more precise understanding of SQL syntax. For semantic errors, the structured model showed greater logical
reliability, reducing ‘Empty Output’ errors from 10.6% in ReasonSQL to 7.6% (a 3.0-point reduction). Although this
increased rigidity led to a minor trade-off, ReasonSQL retained a slight advantage in ‘Value Mismatches’ (18.2% vs.
19.6%), suggesting that the structured plan provides a more robust signal.

3.3 Fine-Grained Performance Analysis and Ablation Study

To investigate the precise source of performance of Struct-SQL, we move beyond aggregate metrics to examine the
detailed differences between models. In this section, we deconstruct the model’s capabilities across three dimensions:
its proficiency with complex SQL operations (Figure 4a), the fidelity of its alignment with the teacher model (Figure 4b),
and its ability to systematically rectify the student model’s baseline errors (Figure 4c).

2Distilled using CoT, evaluated with QP-CoT.

7

A PREPRINT - MARCH 13, 2026

(a) Teacher Model using QP-CoT

(b) Student Model using QP-CoT

(c) FN-Gold using QP-CoT

(d) ReasonSQL using CoT

(e) Struct-SQL using QP-CoT

Figure 3: Compared to the Teacher Model (a), both the Student Model (b) and the FN-Gold (c) exhibit substantially
lower performance, primarily due to high syntactic errors. The unstructured distillation baseline ReasonSQL (d)
improves upon both the Student Model and FN-Gold. Struct-SQL (e) achieves the highest success rate among all tuned
student models.

3.3.1 Performance by SQL Construct:

Assessing model performance across the spectrum of query formulations can be insightful; therefore, we analyzed
execution accuracy for key SQL constructs, as shown in Figure 4a. The comparative analysis indicates that Struct-SQL’s
performance gains are most pronounced in tasks that require aggregation and explicit structural decomposition. This is
evidenced by its strong results on specific SQL operations. For queries requiring a GROUP BY clause, the Struct-SQL
model (42.0% EX) outperformed both FN-Gold (33.8% EX) and ReasonSQL (34.3% EX), demonstrating that explicitly
distilling the query execution plan effectively trains the model on the necessary aggregation formulation. An advantage
was also observed for queries requiring an ORDER BY, where Struct-SQL showed a 2.8-point absolute improvement
over ReasonSQL. However, the comparative analysis revealed a notable exception: for queries that require JOIN

8

A PREPRINT - MARCH 13, 2026

operations, ReasonSQL achieved the highest execution accuracy. In contrast, Struct-SQL’s score (25.5% EX) was lower,
suggesting that the unstructured CoT trace provided a unique advantage for learning multi-entity linking. This area
remains a core challenge for all models, as confirmed by the Teacher Model’s performance (36.4% EX). Furthermore,
all baselines, including Struct-SQL, shared a weakness in handling queries that require Set Operations.

(a) EX by SQL Construct

(b) Gains vs. Losses Analysis

(c) Performance State Transitions

Figure 4: Detailed performance analysis. (a) Execution Accuracy across different SQL constructs, highlighting Struct-
SQL’s proficiency in handling complex aggregations. (b) Gains vs. Losses analysis for baseline models relative to
the Teacher model. The losses and gains are correlated with overall performance. (c) Performance State Transitions
illustrates Struct-SQL’s effectiveness in converting severe errors (SYN, GEN) from the Student Model into direct
successes or less severe errors (SEM).

3.3.2 Evaluation of Knowledge Transfer: Gains vs. Losses:

A Gains vs. Losses analysis was conducted to assess the quality of the distilled knowledge (Figure 4b). This approach
compares queries where the Teacher was correct, but the Student Model failed (Losses, red segments) with cases
where the Student Model was correct, but the Teacher Model was incorrect (Gains, green segments), representing true
generalization. The results indicate that Struct-SQL demonstrates the highest net performance relative to the Teacher
Model by exhibiting the fewest losses and the most gains among all student models. This confirms that the structured
reasoning signal leads to better fidelity in knowledge transfer.

9

A PREPRINT - MARCH 13, 2026

Model

Student Model
ReasonSQL
Struct-SQL (Ours)

Overall
EX (%)

7.22
25.10
29.31

EX by Difficulty

Simple Moderate

Challenging

11.49
40.54
49.32

6.00
20.08
23.20

3.92
12.75
14.71

Table 4: Ablation study on Mistral-7B-Instruct-v3.0 demonstrates that Struct-SQL continues to outperform unstructured
ReasonSQL across different base models.

3.3.3 Performance State Transitions:

Figure 4c illustrates the progression of queries from the baseline Student Model to the distilled Struct-SQL, highlighting
the systematic conversion of error states into successful or unsuccessful output. Struct-SQL retained more than 81% of
the initial successes and enhanced stability by reducing generation errors of the Student Model from 4.0% to 0.4%. The
structured framework also corrected 41.3% of semantic errors (SEM → SUCC), confirming that the formal query plan
addresses logical flaws. Additionally, over two-thirds of syntactic failures were upgraded: 29% were corrected (SYN
→ SUCC) and 41% shifted to semantic errors (SYN → SEM).

3.4 Generalization on Mistral-7B:

To validate the transferability of our framework to other architectures, we replicated our experiments on Mistral-7B-
Instruct-v3.0. This model was specifically selected for its low zero-shot accuracy of 7.2% EX on BIRD mini-dev with
QP-CoT prompt. As shown in Table 4, Struct-SQL shows generalizability, achieving a performance advantage (29.3%
EX) over the Student Model (7.2% EX) and the ReasonSQL baseline (25.1% EX), confirming that the structured query
plan offers a robust supervision signal independent of the base model.

3.5 Computational Efficiency:

On a single H200 GPU, using Qwen3-4B-Instruct-2507 as the Student Model, Struct-SQL converged using an early
stopping strategy with a patience of 8 steps and a threshold of 0.001 in 2.24 epochs, requiring only 29.15 minutes.
This training efficiency is comparable to that of the unstructured ReasonSQL, which required 25.24 minutes across 6.4
epochs with the same batch size, sample count and early stopping strategy. This 1,000-sample distillation strategy is
also computationally tractable compared to traditional finetuning on larger datasets. For context, the FN-Gold baseline,
trained on the entire 9,000+ sample BIRD dataset, required 110.57 minutes (4.33 epochs) to converge. This efficiency
underscores the practical deployability of our structured distillation method in resource-constrained environments.

3.6 Official Test Evaluation:

As shown in Table 5, Struct-SQL obtained 60.42% EX on the non-public BIRD benchmark [5], securing the top position
among ≤4B models (as of January 30, 2026) in single model inference. This result is achieved using strict single-model
inference with greedy decoding and no self-consistency.

Table 5: Official BIRD Bench Evaluation Results3. Struct-SQL (4B) ranks first globally among models with ≤ 4B
parameters (as of January 30, 2026).
Model

Simple (%) Moderate (%) Challenging (%) Overall EX (%)

Struct-SQL(4B)

69.02

54.41

43.51

60.42

4 Related Work

4.1 Text-to-SQL with In-Context Learning (ICL)

LLMs fundamentally redefined the field of Text-to-SQL [21], achieving substantial performance on challenging cross-
domain benchmarks such as Spider [22] and BIRD [5]. ICL [6] has emerged as a dominant research paradigm, enabling

3https://bird-bench.github.io/

10

A PREPRINT - MARCH 13, 2026

LLMs to leverage their pre-training by processing instructions and examples for SQL generation [2]. Initially, ICL
approaches utilized foundational zero-shot and few-shot paradigms [23, 24, 25, 26]. However, generating complex
SQL queries that involve nested logic and multitable joins was found to require explicit external guidance [10]. As
a result, the field pivoted toward decomposition, a multi-step reasoning tactic designed to improve accuracy and
reliability [10, 27, 9, 28, 29]. As a form of ICL-based decomposition, basic CoT helped LLMs break down the task,
follow a logical workflow, and improve execution accuracy [29]. This progression led to sophisticated variants such as
DIN-SQL [10], which decomposes the task into sequential stages (e.g., schema linking, query classification). Additional
multi-stage architectural interventions have also been explored [27, 28]. Crucially, these approaches often require
multiple LLM calls to intervene, correct, or gather intermediate data, leading to high latency and cost. To mitigate this,
some approaches focus on optimizing efficiency by creating single-pass Structural CoT approaches [11, 29]. These
methods instruct the LLM to follow a formalized logical blueprint to gain the necessary understanding of the schema
and natural language before generating the SQL. Specialized methods, including QP-CoT and QDecompose, excel here,
as they have been shown to produce better results than non-structured CoT [11, 9]. For example, QP-CoT provides
few-shot query plan examples that require the model to first generate a detailed query plan before generating SQL
code [11]. Although single-pass ICL performs well with large LLMs, its gains are limited when applied to SLMs [12]
or require expensive finetuning [30, 8, 31, 32]. This work addresses this identified gap by introducing Struct-SQL, a
novel KD method that enables single-pass ICL for SLMs.

4.2 KD for Reasoning Transfer

KD has evolved from a model compression technique to a method for complex knowledge transfer, called Skill
Distillation, which is often used to transfer reasoning knowledge from one model to another or to facilitate self-
improvement [13, 2]. Due to the significant resource demands of LLM, recent research has focused on efficiently
transferring their reasoning capabilities from a teacher LLM to a student SLM. This transfer is frequently grounded in
ICL principles, demonstrating that learning from few-shot demonstrations can be successfully distilled into the SLMs’
parameters [33]. The primary established approach to enable reasoning in SLMs is the Finetune-CoT paradigm [14],
which uses unstructured CoT explanations from the teacher as a supervision signal. This distillation approach has been
demonstrated to be effective with multi-step mathematical reasoning [16]. However, relying on unstructured CoT often
leads SLMs to learn spurious correlations rather than deep causal features, thereby reducing robustness on complex
data [34, 35]. Consequently, recent research increasingly favors methods that enforce structural decomposition and
explicit causality. These approaches include creating constrained distillation pipelines with the aim of removing ambigu-
ous input context through advanced structural formats. For example, SocraticCoT provides an explicit structural format
by guiding the model through reasoning using defined subquestion-solution pairs [35]. Alternatively, Mixed Distillation
integrates the CoT with a formal verifiable Program-of-Thought reasoning to provide a less ambiguous supervision
signal [34]. In the Text-to-SQL domain, structured KD has seen limited uptake. Previous studies, while validating
the effectiveness of distillation in this area, have generally relied on less structured signals, such as schema-based
finetuning to improve schema linking [3], the inclusion of enterprise-specific custom examples [4], and unstructured
CoT reasoning transfer [17]. The proposed Struct-SQL framework systematically evaluates whether structure-based
reasoning transfer, specifically QP-CoT, improves the distillation for Text-to-SQL.

5 Limitations

Struct-SQL significantly reduces syntactic errors through the use of structured reasoning; however, several constraints
remain:

• Token Overhead and Efficiency: Struct-SQL significantly reduces syntactic errors through structured
reasoning; however, this approach introduces inference overhead. The generation of an intermediate query
plan requires approximately 3.6 times more tokens than ReasonSQL (Table 3). This increase impacts latency
and operational costs; nevertheless, these requirements may still be lower than those of teacher LLMs. It
would be worthwhile to investigate more concise query plan templates to explore this trade-off.

• Performance Bound: The student model’s capabilities are fundamentally capped by the teacher’s fidelity.
Our distillation pipeline utilizes a strict filtering mechanism, training only on instances where the teacher
model generates an execution-correct SQL query. Although this quality control is essential to prevent error
propagation and provide a stable signal for small models [36], it inherently skews the training data toward
problems that the teacher can solve, potentially limiting the student’s exposure to edge cases that the teacher
itself cannot solve [37]. As a result, even with a competitive 60.42% EX on the BIRD test set, the performance
remains bound by the teacher’s own limitations in handling highly complex multi-level joins and set operations,

11

A PREPRINT - MARCH 13, 2026

as discussed in Figure 4a. To improve performance further, future work could explore using multiple teachers
or human-annotated data to cover edge cases that a single source model may miss.

• Benchmark Selection: A fixed reasoning template is used to minimize syntactic hallucinations through a
constrained logical path; however, we recognize that it may limit flexibility across highly diverse database
dialects. We intentionally prioritize evaluation on the BIRD benchmark, as it represents a more challenging
dataset than SPIDER. As demonstrated in recent literature (e.g., Snowflake Arctic-Text2SQL-R1), state-of-the-
art models frequently exceed 88% EX on the SPIDER-test, yet often struggle to surpass 70% on BIRD-dev
[38]. This performance gap justifies our decision to focus exclusively on BIRD.

6 Conclusion and Future Research

This work presents Struct-SQL, a KD framework that transfers structured reasoning (QP-CoT) from a Teacher LLM
to a smaller student model for the Text-to-SQL task. The central hypothesis is that a formal, structured reasoning
signal provides a superior, less ambiguous teaching blueprint than unstructured reasoning. The experiments confirm
the hypothesis, demonstrating that distilling structured reasoning is a better teaching method. Detailed error analysis
indicates that these improvements are primarily due to a significant reduction in syntactic errors. An additional ablation
study demonstrated generalization to a different base model. Given the demonstrated effectiveness of structured signals
in the refinement of syntactic efficiency and logical reasoning, further research is warranted to validate the effect of
this structured distillation approach on other complex reasoning tasks beyond Text-to-SQL. In summary, the proposed
framework facilitates the deployment of high-performing, cost-effective and private models.

7 Acknowledgments

We thank Khalid Eidoo, Abdul Hamid Dabboussi, María Rodríguez-Liñán and Ting Fung Lam for their insightful
technical discussions and valuable feedback throughout the project and during the review of this manuscript.

References

[1] Fei Li and H. V. Jagadish. Constructing an interactive natural language interface for relational databases. Proc.

VLDB Endow., 8(1):73–84, 2014.

[2] Liang Shi, Zhengju Tang, Nan Zhang, Xiaotong Zhang, and Zhi Yang. A survey on employing large language

models for text-to-sql tasks. ACM Comput. Surv., 58(2), 2025.

[3] Zijin Hong, Zheng Yuan, Qinggang Zhang, Hao Chen, Junnan Dong, Feiran Huang, and Xiao Huang. Next-

generation database interfaces: A survey of llm-based text-to-sql. IEEE TKDE, 2025.

[4] Cong Duy Vu Hoang, Gioacchino Tangari, Clemence Lanfranchi, Dalu Guo, Paul Cayet, Steve Siu, Don
Dharmasiri, Yuan-Fang Li, Long Duong, Damien Hilloulin, Rhicheek Patra, Sungpack Hong, and Hassan Chafi.
Distill-C: Enhanced NL2SQL via distilled customization with LLMs. In NAACL: HLT. ACL, 2025.

[5] Jinyang Li, Binyuan Hui, Ge Qu, Jiaxi Yang, Binhua Li, Bowen Li, Bailin Wang, Bowen Qin, Ruiying Geng,
Nan Huo, et al. Can llm already serve as a database interface? a big bench for large-scale database grounded
text-to-sqls. Advances in Neural Information Processing Systems, 36, 2024.

[6] Qingxiu Dong, Lei Li, Damai Dai, Ce Zheng, Jingyuan Ma, Rui Li, Heming Xia, Jingjing Xu, Zhiyong Wu,
Baobao Chang, Xu Sun, Lei Li, and Zhifang Sui. A survey on in-context learning. In EMNLP. ACL, 2024.
[7] Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Fei Xia, Ed Chi, Quoc V Le, Denny Zhou, et al.

Chain-of-thought prompting elicits reasoning in large language models. NeurIPS, 2022.

[8] Hanbing Liu, Haoyang Li, Xiaokang Zhang, Ruotong Chen, Haiyong Xu, Tian Tian, Qi Qi, and Jing Zhang.
Uncovering the impact of chain-of-thought reasoning for direct preference optimization: Lessons from text-to-sql.
arXiv:2502.11656, 2025.

[9] Dawei Gao, Haibin Wang, Yaliang Li, Xiuyu Sun, Yichen Qian, Bolin Ding, and Jingren Zhou. Text-to-sql

empowered by large language models: A benchmark evaluation. Proc. VLDB Endow., 2024.

[10] Mohammadreza Pourreza and Davood Rafiei. Din-sql: Decomposed in-context learning of text-to-sql with

self-correction. Neural Information Processing Systems, 2023.

[11] Mohammadreza Pourreza, Hailong Li, Ruoxi Sun, Yeounoh Chung, Shayan Talaei, Gaurav Tarlok Kakkar, Yu Gan,
Amin Saberi, Fatma Ozcan, and Sercan Ö. Arik. Chase-sql: Multi-path reasoning and preference optimized
candidate selection in text-to-sql. Intl. Conf. on Learning Representations, 2024.

12

A PREPRINT - MARCH 13, 2026

[12] Karime Maamari, Fadhil Abubaker, Daniel Jaroslawicz, and Amine Mhedhbi. The death of schema linking?

text-to-sql in the age of well-reasoned language models. In NeurIPS RL Wo, 2024.
[13] G Hinton. Distilling the knowledge in a neural network. In DLRL Workshop, NIPS, 2014.
[14] Shiyang Li, Jianshu Chen, Zhiyu Chen, Xinlu Zhang, Zekun Li, Hong Wang, Jing Qian, Baolin Peng, Yi Mao,
Wenhu Chen, et al. Explanations from large language models make small reasoners better. In Sustainable AI,
2024.

[15] Cheng-Yu Hsieh, Chun-Liang Li, Chih-kuan Yeh, Hootan Nakhost, Yasuhisa Fujii, Alex Ratner, Ranjay Krishna,
Chen-Yu Lee, and Tomas Pfister. Distilling step-by-step! outperforming larger language models with less training
data and smaller model sizes. In Findings ACL. ACL, 2023.

[16] Yao Fu, Hao Peng, Litu Ou, Ashish Sabharwal, and Tushar Khot. Specializing smaller language models towards

multi-step reasoning. In Intl. Conf. on Machine Learning, 2023.

[17] Gaetano Rossiello, Nhan H Pham, Michael Glass, Junkyu Lee, and Dharmashankar Subramanian. Rationalization

models for text-to-SQL. In Workshop on Reasoning and Planning for LLM, 2025.

[18] An Yang, Anfeng Li, Baosong Yang, Beichen Zhang, Binyuan Hui, Bo Zheng, Bowen Yu, Chang Gao, Chengen

Huang, Chenxu Lv, et al. Qwen3 technical report. arXiv:2505.09388, 2025.

[19] Tim Dettmers, Artidoro Pagnoni, Ari Holtzman, and Luke Zettlemoyer. Qlora: Efficient finetuning of quantized

llms. NeurIPS, 36:10088–10115, 2023.

[20] Zeyu Han, Chao Gao, Jinyang Liu, Jeff Zhang, and Sai Qian Zhang. Parameter-efficient fine-tuning for large

models: A comprehensive survey. Transactions on ML Research, 2024.

[21] Naihao Deng, Yulong Chen, and Yue Zhang. Recent advances in text-to-SQL: A survey of what we have and
what we expect. In Proc. of the 29th Intl. Conf. on Computational Linguistics, pages 2166–2187, Gyeongju, 2022.
Intl. Committee on Computational Linguistics.

[22] Tao Yu, Rui Zhang, Kai Yang, Michihiro Yasunaga, Dongxu Wang, Zifan Li, James Ma, Irene Li, Qingning Yao,
Shanelle Roman, Zilin Zhang, and Dragomir Radev. Spider: A large-scale human-labeled dataset for complex
and cross-domain semantic parsing and text-to-SQL task. In EMNLP. ACL, 2018.

[23] Xuemei Dong, Chengqi Zhang, Yuhang Ge, Yuren Mao, Yunjun Gao, Lu Chen, Jinshu Lin, and Dongfang Lou.

C3: Zero-shot text-to-sql with chatgpt. arXiv:2307.07306, 2023.

[24] Nitarshan Rajkumar, Raymond Li, and Dzmitry Bahdanau. Evaluating the text-to-sql capabilities of large language

models. arXiv:2204.00498, 2022.

[25] Aiwei Liu, Xuming Hu, Lijie Wen, and Philip S Yu. A comprehensive evaluation of chatgpt’s zero-shot text-to-sql

capability. arXiv:2303.13547, 2023.

[26] Bing Wang, Changyu Ren, Jian Yang, Xinnian Liang, Jiaqi Bai, LinZheng Chai, Zhao Yan, Qian-Wen Zhang,
Di Yin, Xing Sun, and Zhoujun Li. MAC-SQL: A multi-agent collaborative framework for text-to-SQL. In Proc.
of the 31st Intl. Conf. on Computational Linguistics. ACL, 2025.

[27] Hanchong Zhang, Ruisheng Cao, Lu Chen, Hongshen Xu, and Kai Yu. ACT-SQL: In-context learning for

text-to-SQL with automatically-generated chain-of-thought. In Findings: EMNLP, 2023.

[28] Zhishuai Li, Xiang Wang, Jingjing Zhao, Sun Yang, Guoqing Du, Xiaoru Hu, Bin Zhang, Yuxiao Ye, Ziyue Li, Rui
Zhao, and Hangyu Mao. Pet-sql: A prompt-enhanced two-round refinement of text-to-sql with cross-consistency.
arXiv:2403.09732, 2024.

[29] Xiping Liu and Zhao Tan. Divide and prompt: Chain of thought prompting for text-to-sql. arXiv:2304.11556,

2023.

[30] Mohammadreza Pourreza and Davood Rafiei. DTS-SQL: Decomposed text-to-SQL with small large language

models. In Findings ACL: EMNLP, pages 8212–8220, Miami, 2024. ACL.

[31] Satya Krishna Gorti, Ilan Gofman, Zhaoyan Liu, Jiapeng Wu, Noël Vouitsis, Guangwei Yu, Jesse C. Cresswell,
and Rasa Hosseinzadeh. MSc-SQL: Multi-sample critiquing small language models for text-to-SQL translation.
In NAACL. ACL, 2025.

[32] Bohan Zhai, Canwen Xu, Yuxiong He, and Zhewei Yao. Excot: Optimizing reasoning for text-to-sql with

execution feedback. arXiv:2503.19988, 2025.

[33] Charlie Snell, Dan Klein, and Ruiqi Zhong. Learning by distilling context. arXiv:2209.15189, 2022.
[34] Chenglin Li, Qianglong Chen, Liangyue Li, Caiyu Wang, Yicheng Li, Zulong Chen, and Yin Zhang. Mixed

distillation helps smaller language model better reasoning. arXiv:2312.10730, 2023.

13

A PREPRINT - MARCH 13, 2026

[35] Kumar Shridhar, Alessandro Stolfo, and Mrinmaya Sachan. Distilling reasoning capabilities into smaller language

models. In Findings ACL, pages 7059–7073, Toronto, 2023. ACL.

[36] Jianhua Zhang, Yi Gao, Ruyu Liu, Xu Cheng, Houxiang Zhang, and Shengyong Chen. Can students beyond
the teacher? distilling knowledge from teacher’s bias. In Proceedings of the AAAI Conference on Artificial
Intelligence, volume 39, pages 22434–22442, 2025.

[37] Chengyao Qian, Trung Le, and Mehrtash Harandi. A good teacher adapts their knowledge for distillation. In

Proceedings of the IEEE/CVF International Conference on Computer Vision, pages 1239–1248, 2025.

[38] Zhewei Yao, Guoheng Sun, Lukasz Borchmann, Zheyu Shen, Minghang Deng, Bohan Zhai, Hao Zhang, Ang
Li, and Yuxiong He. Arctic-text2sql-r1: Simple rewards, strong reasoning in text-to-sql. arXiv preprint
arXiv:2505.20315, 2025.

14

A PREPRINT - MARCH 13, 2026

A Structured Reasoning Prompt Template (QP-CoT)

The QP-CoT prompt, as detailed in Listing 1, comprises a system instruction followed by two few-shot examples that
demonstrate the query execution plan methodology. The prompt concludes with the target task; for the sake of brevity
in this manuscript, the database schema definitions have been abbreviated.

Answer Repeating the question and evidence , and generating the valid SQLite SQL with a query plan .

Listing 1: Struct-SQL Prompt Template (QP-CoT) - Two-Shot

###
Two examples of this task are below :
###

### Database Schema :
Table : lists_users
... [ Schema details abbreviated ] ...

## User Question :
How many more movie lists were created by the user who created the movie list "250 Favourite Films "?

## Hint :
"250 Favourite Films " refers to list_title .

### Response :
** Query Plan **:
** Preparation Steps :**
1. Initialize the process : Start preparing to execute the query .
2. Prepare storage : Set up storage space ( registers ) to hold temporary results ...
3. Open the lists table : Open the lists table so we can read from it .
4. Open the lists_users table : Open the lists_users table so we can read from it .

** Matching and Finding User ID :**
1. Start reading the lists table : Move to the first row in the lists table .
2. Check if the list title matches : Look at the ‘ list_title ‘ column ... If it ’ s not "250 Favourite Films ,"

skip this row .

3. Identify the matching row : Store the ‘ user_id ‘ of this list entry . This ‘ user_id ‘ is for the creator

of "250 Favourite Films ."

** Counting Movie Lists by User :**
1. Prepare to count : If a ‘ user_id ‘ is found from the previous step , prepare to count .
2. Start reading the lists_users table : Move to the first row ...
3. Check if the user ID matches : Look at the ‘ user_id ‘ column ...
4. Count this match : Increment the count for each row ...
5. Move to the next row in lists_users : Go back to the ‘ lists_users ‘ table ...
6. Finalize the count : Once all relevant rows have been checked ...

** Delivering the Result :**
1. Output the result : Output the final count ...
2. End the process : Stop the query execution process .

## SQL Query :
SELECT COUNT ( list_id ) FROM lists_users WHERE user_id = ( SELECT user_id FROM lists WHERE list_title =

’250 Favourite Films ’ )

## User Question :
What is the director ’ s name of the movie with the highest average rating in 2023 , and what is that

average rating ?

## Hint :
highest average rating refers to MAX ( AVG ( rating_score ) ) ; in 2023 refers to mo v ie _ re l ea s e_ y ea r = 2023;

### Response :
** Query Plan **:
** Preparation Steps :**
1. Initialize the process : Start preparing to execute the query .
... [ Steps abbreviated ] ...
4. Open the ratings table : Open the ratings table so we can read from it .

** Finding the Movie with the Highest Average Rating in 2023 ( Subquery Logic ) :**
1. Start reading the movies and ratings tables .
2. Join movies and ratings tables using their common movie_id column .
3. Filter the joined rows to include only movies where mo v ie _ re l ea s e_ y ea r is 2023.
... [ Steps abbreviated ] ...
6. Select the movie_id of the first ( top ) result .

** Retrieving Director Name and Average Rating ( Main Query Logic ) :**
1. Start reading the movies and ratings tables again .
... [ Steps abbreviated ] ...

15

A PREPRINT - MARCH 13, 2026

5. Select the director_name and calculate the AVG ( rating_score ) for the identified movie .

** Delivering the Result :**
1. Output the director ’ s name and the calculated average rating .
2. End the process : Stop the query execution process .

## SQL Query :
SELECT T1 . director_name , AVG ( T2 . rating_score ) FROM movies AS T1 INNER JOIN ratings AS T2 ON T1 . movie_id =

T2 . movie_id WHERE T1 . movie_id = ( SELECT T1 . movie_id FROM movies AS T1 INNER JOIN ratings AS T2 ON
T1 . movie_id = T2 . movie_id WHERE T1 . m ov i e_ r el e as e _y e ar = 2023 GROUP BY T1 . movie_id ORDER BY AVG ( T2 .
rating_score ) DESC LIMIT 1) GROUP BY T1 . director_name

#
# [ Target Task Input ]
#

### Database Schema :
CREATE TABLE film_text (

film_id INTEGER not null primary key ,
title TEXT not null ,
description TEXT null

)
... [ Target Schema abbreviated ] ...

## User Question :
State the name of the category which has the most number of films .

## Hint :
category refers to name ; most number of films refers to Max ( Count ( film_id ) )

### Response :
** Query Plan **:

B Unstructured Reasoning Prompt Template (CoT)

The ReasonSQL baseline (Listing 2) utilizes a 4-shot prompt to elicit free-form natural language reasoning. By requiring
the model to ’think step-by-step’ without a formal execution plan, this baseline represents the standard unstructured
distillation signal.

The goal of the task is to generate a valid SQLite query to answer the question based on schema provided .

Listing 2: Unstructured CoT Prompt Template (ReasonSQL) - 4-Shot

###
Few examples of this task are :
###
Schema of the database with sample rows :

Table : lists_users
Column user_id : column description -> ID related to the user who created the list .
... [ Schema details abbreviated ] ...

## User Question :
For the list with more than 200 followers , state the title and how long the list has been created ?
## Hint :
more than 200 followers refers to list_followers >200; how long the list has been created refers to

SUBTRACT ( CURRENT_TIMESTAMP , l i s t _ c r e a t i o n _ t i m e s t a m p _ u t c )

A : Let ’ s think step by step . The SQL query for the given question needs these tables = [ lists ] , so we don

’ t need JOIN .

Plus , it doesn ’ t require nested queries , and we need the answer to the sub - questions = [""].
Also we don ’ t need nested queries . Now to find the lists with more than 200 followers , we need to filter

the lists table where list_followers > 200.

Then , we need to select the list_title and calculate the duration since l i s t _ c r e a t i o n _ t i m e s t a m p _ u t c up to

the current date .

So the sqlite SQL query will be :
SQL : SELECT list_title , 365 * ( strftime ( ’%Y ’ , ’now ’) - strftime ( ’%Y ’ , l i s t _ c r e a t i o n _ t i m e s t a m p _ u t c ) ) + 30

* ( strftime ( ’%m ’ , ’now ’) - strftime ( ’%m ’ , l i s t _ c r e a t i o n _ t i m e s t a m p _ u t c ) ) + strftime ( ’%d ’ , ’now ’) -

strftime ( ’%d ’ , l i s t _ c r e a t i o n _ t i m e s t a m p _ u t c ) FROM lists WHERE list_followers > 200

## User Question :
What is the percentage of list created by user who was a subscriber when he created the list ?
## Hint :
was a subscriber refers to user_subscriber = 1; percentage refers to DIVIDE ( COUNT ( user_subscriber = 1) ,

COUNT ( list_id ) )

A : Let ’ s think step by step . The SQL query for the given question needs these tables = [ lists_users ] , so

we don ’ t need JOIN .

16

A PREPRINT - MARCH 13, 2026

Also we don ’ t need nested queries . To calculate the percentage , we need to count the total number of

lists ( COUNT ( list_id ) ) and the number of lists where user_subscriber is 1 ( meaning the user was a
subscriber ) . The count of subscribers needs to be cast to REAL to ensure floating - point division for
the percentage .

So the sqlite SQL query will be :
SQL : SELECT CAST ( SUM ( CASE WHEN user_subscriber = 1 THEN 1 ELSE 0 END ) AS REAL ) * 100 / COUNT ( list_id )

FROM lists_users

## User Question :
What is the average rating for movie titled ’ When Will I Be Loved ’?
## Hint :
average rating = DIVIDE (( SUM ( rating_score where movie_title = ’ When Will I Be Loved ’) ) , COUNT (

rating_score ) ) ;

A : Let ’ s think step by step . For creating the SQL for the given question , we need to join these tables =

[ ratings , movies ].

First of all , for joining these tables we have to use the common column = [ ratings . movie_id = movies .

movie_id ].

Now , we have to filter the rows where movie_title = ’ When Will I Be Loved ’.
Then , we have to find the average of the rating_score .
So the sqlite SQL query will be :
SQL : SELECT AVG ( T2 . rating_score ) FROM movies AS T1 INNER JOIN ratings AS T2 ON T1 . movie_id = T2 . movie_id

WHERE T1 . movie_title = ’ When Will I Be Loved ’

## User Question :
For the user who post the list that contained the most number of the movies , is he / she a paying

subscriber when creating that list ?

## Hint :
the list that contained the most number of the movies refers to MAX ( li st_ mov ie_ nu mbe r ) ;

u s e r _ h a s _ p a y m e n t _ m e t h o d = 1 means the user was a paying subscriber when he created the list ; \
n u s e r _ h a s _ p a y m e n t _ m e t h o d = 0 means the user was not a paying subscriber when he created the list
A : Let ’ s think step by step . the given question can be solved by knowing the answer to the following sub -

questions = [ which list has the most number of movies .]

The sqlite SQL query for the sub - question " which list has the most number of movies " is SELECT MAX (

li st_ mov ie _nu mbe r ) FROM lists

The above query will return the l ist _mo vie _nu mb er of the list which has the most number of movies .
Now , we have to find the u s e r _ h a s _ p a y m e n t _ m e t h o d of the user who has created the list which has the most

number of movies .

To do so , we have to JOIN lists_users and lists table on list_id .
So , the final sqlite SQL query answer to the question the given question is =
SQL : SELECT T1 . u s e r _ h a s _ p a y m e n t _ m e t h o d FROM lists_users AS T1 INNER JOIN lists AS T2 ON T1 . list_id = T2 .

list_id WHERE T2 . li st_ mov ie_ num ber = ( SELECT MAX ( lis t_m ovi e_n umb er ) FROM lists )

#
# [ Target Task Input ]
#

### Database Schema :
CREATE TABLE " country " (

Name TEXT not null constraint ix_county_Name unique ,
Code TEXT default ’’ not null primary key ,
... [ Columns abbreviated ] ...

)

... [ Target Schema abbreviated ] ...

## User Question :
Which two countries does the Detroit River flow through ? Give the full name of the country .

## Hint :

A : Let ’ s think step by step .

C Struct-SQL Output Examples

This section provides examples of the Struct-SQL model’s outputs across three levels of SQL complexity: Simple,
Moderate, and Challenging. These examples demonstrate the model’s ability to generate a human-readable Query Plan
that mirrors the logical execution steps of a database engine before producing the final SQLite SQL. Each entry includes
the Question ID and Database ID for traceability. The following examples are selected based on the first successful
generation encountered for each difficulty tier within the development dataset to ensure an unbiased representation of
the model’s capabilities.

17

A PREPRINT - MARCH 13, 2026

Struct-SQL Output (Difficulty: Simple)

Question ID: 5
Database ID: california_schools
Question: How many schools with an average score in Math greater than 400 in the SAT test are exclusively
virtual?

— Query Plan —
** Preparation Steps:**
1. Initialize the process: Start preparing to execute the query.
2. Prepare storage: Set up storage space (registers) to hold temporary results,

initializing them to NULL.

3. Open the satscores table: Open the satscores table so we can read from it.
4. Open the schools table: Open the schools table so we can read from it.

** Filtering and Joining Tables:**
1. Start reading the satscores table: Move to the first row in the satscores table.
2. Check if the average math score is greater than 400: Look at the ‘AvgScrMath‘ column of

the current row in ‘satscores‘. If it’s not greater than 400, skip this row.

3. Identify the matching row: Store the ‘cds‘ of this score entry. This ‘cds‘ is for schools

with an average math score greater than 400.

4. Start reading the schools table: Move to the first row in the ‘schools‘ table.
5. Check if the school is exclusively virtual: Look at the ‘Virtual‘ column of the current row

in ‘schools‘. If it’s not ’F’, skip this row.

6. Check if the school matches: Look at the ‘CDSCode‘ column of the current row in ‘schools‘.
If it matches any ‘cds‘ found in the previous step, this school is exclusively virtual
and has a high average math score.

** Counting Schools:**
1. Prepare to count: If a matching ‘cds‘ is found from the previous step, prepare to count.
2. Count this match: Increment the count for each row in ‘schools‘ that matches the criteria.
3. Move to the next row in schools: Go back to the ‘schools‘ table and move to the next row,

repeating the process until all rows are checked.

4. Finalize the count: Once all relevant rows have been checked, finalize the count of schools

that are exclusively virtual and have an average math score greater than 400.

** Delivering the Result:**
1. Output the result: Output the final count, which is the total number of schools that are

exclusively virtual and have an average math score greater than 400.

2. End the process: Stop the query execution process.

## SQL Query:

SELECT COUNT ( CDSCode ) FROM schools WHERE Virtual = ’F ’ AND CDSCode IN (

SELECT cds FROM satscores WHERE AvgScrMath > 400 )

18

A PREPRINT - MARCH 13, 2026

Struct-SQL Output (Difficulty: Moderate)

Question ID: 45
Database ID: california_schools
Question: What is the average writing score of each of the schools managed by Ricci Ulrich? List the schools
and the corresponding average writing scores.

— Query Plan —
** Preparation Steps:**
1. Initialize the process: Start preparing to execute the query.
2. Prepare storage: Set up storage space (registers) to hold temporary results, initializing

them to NULL.

3. Open the schools table: Open the schools table so we can read from it.
4. Open the satscores table: Open the satscores table so we can read from it.

** Identifying Schools Managed by Ricci Ulrich:**
1. Start reading the schools table: Move to the first row in the schools table.
2. Check if the administrator’s name matches: Look at the ‘AdmFName1‘ and ‘AdmLName1‘ columns

of the current row in ‘schools‘. If they are not "Ricci" and "Ulrich," skip this row.

3. Identify the matching row: Store the ‘CDSCode‘ of this school entry. This ‘CDSCode‘ is for

the school managed by Ricci Ulrich.

** Calculating Average Writing Scores:**
1. Prepare to calculate: If a ‘CDSCode‘ is found from the previous step, prepare to calculate.
2. Start reading the satscores table: Move to the first row in the ‘satscores‘ table.
3. Check if the school code matches: Look at the ‘cds‘ column of the current row in ‘satscores‘.

If it doesn’t match the ‘CDSCode‘ found in the "Identifying Schools Managed by Ricci Ulrich"
step, skip this row.

4. Calculate the average writing score: For each matching row, calculate the average writing

score using the ‘AvgScrWrite‘ column.

5. Move to the next row in satscores: Go back to the ‘satscores‘ table and move to the next row,

repeating the process until all rows are checked.

** Delivering the Result:**
1. Output the result: Output the list of schools managed by Ricci Ulrich and their corresponding

average writing scores.

2. End the process: Stop the query execution process.

## SQL Query:

SELECT T1 . school , AVG ( T2 . AvgScrWrite ) FROM ( SELECT DISTINCT T1 . school , T1 .

CDSCode FROM schools AS T1 INNER JOIN satscores AS T2 ON T1 . CDSCode = T2 .
cds WHERE T1 . AdmFName1 = ’ Ricci ’ AND T1 . AdmLName1 = ’ Ulrich ’ ) AS T1
INNER JOIN satscores AS T2 ON T1 . CDSCode = T2 . cds GROUP BY T1 . school

19

A PREPRINT - MARCH 13, 2026

Struct-SQL Output (Difficulty: Challenging)

Question ID: 36
Database ID: california_schools
Question: Under whose administration is the school with the highest number of students scoring 1500 or more
on the SAT? Indicate their full names.

— Query Plan —
## Preparation Steps:
1. Initialize the process: Start preparing to execute the query.
2. Prepare storage: Set up storage space (registers) to hold temporary results,

initializing them to NULL.

3. Open the satscores table: Open the satscores table so we can read from it.
4. Open the schools table: Open the schools table so we can read from it.

** Finding the School with the Highest Number of Students Scoring 1500 or More:**
1. Start reading the satscores table: Move to the first row in the satscores table.
2. Check if the score is 1500 or more: Look at the ‘NumGE1500‘ column of the current row in

‘satscores‘. If it’s not greater than or equal to 1500, skip this row.

3. Identify the matching row: Store the ‘cds‘ of this score entry. This ‘cds‘ is for the school

with the highest number of students scoring 1500 or more.

** Retrieving Administrator Full Names:**
1. Prepare to retrieve administrator names: If a ‘cds‘ is found from the previous step, prepare

to retrieve administrator names.

2. Start reading the schools table: Move to the first row in the ‘schools‘ table.
3. Check if the school code matches: Look at the ‘CDSCode‘ column of the current row in ‘schools‘.

If it doesn’t match the ‘cds‘ found in the "Finding the School with the Highest Number of
Students Scoring 1500 or More" step, skip this row.

4. Retrieve administrator names: For each matching row, retrieve the ‘AdmFName1‘, ‘AdmLName1‘,
‘AdmFName2‘, ‘AdmLName2‘, ‘AdmFName3‘, and ‘AdmLName3‘ columns, which represent the full
names of the administrators.

5. Move to the next row in schools: Go back to the ‘schools‘ table and move to the next row,

repeating the process until all rows are checked.

** Delivering the Result:**
1. Output the administrator full names: Output the full names of the administrators for the

school with the highest number of students scoring 1500 or more.

2. End the process: Stop the query execution process.

## SQL Query:

SELECT T1 . AdmFName1 , T1 . AdmLName1 , T1 . AdmFName2 , T1 . AdmLName2 , T1 . AdmFName3 ,
T1 . AdmLName3 FROM schools AS T1 INNER JOIN satscores AS T2 ON T1 . CDSCode
= T2 . cds WHERE T2 . NumGE1500 = ( SELECT MAX ( NumGE1500 ) FROM satscores )

20

