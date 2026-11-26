# Results, ablations, analysis

## Zhong et al., test suites, EMNLP 2020, Section 6.2

> Given that test suite evaluation empirically provides an improved
> approximation of semantic equivalence, we use test suite accuracy as
> ground truth and retrospectively examine how well ESM approximates
> semantic accuracy. We calculate the false positive/false negative
> rate for each difficulty split and report the mean, standard
> deviation, and max for all 21 submissions.
>
> Table [n] shows the results. ESM leads to a nontrivial false negative
> rate of 2.6% on average, and 8.1% in the worst case. The error
> becomes larger for harder fractions of queries characterized by more
> complex queries. On the hard fraction, false negative rate increases
> to 4% on average and 12.1% in the worst case.

## Li et al., CodeS, SIGMOD 2024, Section 9.5 (ablation)

> **Schema Filter and Value Retriever.** We explore the effects of the
> schema filter and value retriever on performance. Without the schema
> filter, there's both a drop in performance and a slower generation
> speed due to longer input sequences. Omitting the value retriever
> also leads to a marked decrease in text-to-SQL performance,
> especially on the BIRD benchmark, highlighting its crucial role in
> generating SQL query predicates.
>
> **Metadata.** We perform ablations on metadata. As per Table [n],
> column data types have a minor performance impact, possibly because
> the model infers types from column names and comments. Removing
> comments notably affects performance on the BIRD benchmark due to its
> ambiguous schemas. Additionally, both representative database values
> and primary/foreign keys are essential for performance on Spider and
> BIRD. The first offers insight into value format, and the latter
> helps in accurate JOIN ON clause generation.

## Hu et al., LoRA, ICLR 2022, Section 7

> We perform a sequence of empirical studies to answer the following
> questions: 1) Given a parameter budget constraint, which subset of
> weight matrices in a pre-trained Transformer should we adapt to
> maximize downstream performance? 2) Is the "optimal" adaptation
> matrix ΔW really rank-deficient? If so, what is a good rank to use in
> practice? 3) What is the connection between ΔW and W? [...]
>
> [after the table] Note that putting all the parameters in ΔW_q or
> ΔW_k results in significantly lower performance, while adapting both
> W_q and W_v yields the best result. This suggests that even a rank of
> four captures enough information in ΔW such that it is preferable to
> adapt more weight matrices than adapting a single type of weights
> with a larger rank.

## Tritto et al., GradeSQL, Results and Discussion

> **RQ1: Cross-Family Trainability of ORMs.** Table [n] reports ORM
> performance on BIRD and Spider using the unbalanced training set,
> across Granite, Llama, Qwen, and OmniSQL backbones. The trained ORMs
> exhibit tightly clustered scores: Bird dev ranges from 66.88 to
> 68.64, Spider dev from 82.30 to 84.42, and Spider test from 85.14 to
> 86.91. [...]
>
> A closer look reveals three key patterns. The first is that the scale
> effect is modest: larger variants such as Granite-3.3-8B or
> Qwen2.5-7B yield only small improvements (typically below two points)
> over their smaller counterparts, suggesting that ORM effectiveness is
> not strongly tied to parameter count. [...]
