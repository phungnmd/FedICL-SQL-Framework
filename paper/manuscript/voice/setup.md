# Experimental setup

## Tritto et al., "GradeSQL" (arXiv 2509.01308), Experimental Setup

> **Datasets.** To evaluate our approach, we use two widely adopted
> Text-to-SQL benchmarks: Spider [ref] and BIRD [ref]. Both are
> cross-domain benchmarks with disjoint databases across train/dev/test
> splits to assess generalization. On Spider, we construct the labeled
> dataset from the training questions, train the ORM, and evaluate it
> on the dev and test sets. On BIRD, we adopt the same setup, using the
> training questions to build the dataset and train the ORM, but, due
> to the hidden test set, evaluate only on the dev set.
>
> **Metrics.** [...] Execution Accuracy (EX) [ref] measures the
> proportion of questions for which the predicted and gold queries
> return identical result sets: [the formula] where 1(·) is the
> indicator function, returning 1 if the condition holds and 0
> otherwise.

## Li et al., "CodeS: Towards Building Open-source Language Models for Text-to-SQL", SIGMOD 2024, Section 9.1

> **Evaluation Metrics.** (1) For Spider-family benchmarks (including
> Spider, Spider-DK, Spider-Syn, Spider-Realistic, and Dr-Spider), we
> consider two prevalent evaluation metrics: execution accuracy (EX)
> [ref] and test-suite accuracy (TS) [ref]. The EX metric evaluates
> whether the predicted and ground-truth SQL queries yield the same
> execution results on the database. [...] To counteract this, the
> test-suite accuracy was developed. It assesses if the generated SQL
> query consistently passes the EX evaluations across multiple database
> instances, which are derived from automated database augmentations.
> [...] It's worth noting that for Spider-DK and Dr.Spider, the TS
> script lacks test suites for their respective databases.
