# Style measures of the reference papers

Written by `tools/style_profile.py profile`. Do not edit.

Papers: GradeSQL (J. Intell. Inf. Syst. 2026, arXiv 2509.01308); CodeS (SIGMOD 2024, arXiv 2402.16347); BIRD (NeurIPS 2023 (Datasets and Benchmarks), arXiv 2305.03111); Test suites (EMNLP 2020, arXiv 2010.02840); CodeLutra (arXiv 2411.05199); DPO (NeurIPS 2023, arXiv 2305.18290); LoRA (ICLR 2022, arXiv 2106.09685); FedAvg (AISTATS 2017, arXiv 1602.05629); FedProx (MLSys 2020, arXiv 1812.06127); OpenFedLLM (arXiv 2402.06954).

## By kind of section, the ten papers together

| | words | sentence mean | sentence sd | paragraph sentences | letters per word | long words % | we sentences % | passive sentences % | hedges /1k | intensifiers /1k | -ly adverbs /1k | everyday verbs /1k | citations per paragraph | narrative citations % |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| introduction | 8,921 | 26.3 | 14.0 | 4.0 | 5.78 | 20.7 | 43.6 | 18.3 | 2.8 | 2.2 | 20.2 | 1.0 | 1.6 | 4.1 |
| related work | 5,181 | 23.0 | 10.7 | 5.1 | 6.13 | 22.7 | 18.1 | 19.3 | 2.5 | 2.3 | 21.8 | 0.8 | 4.2 | 4.1 |
| method | 12,106 | 22.5 | 11.6 | 3.8 | 5.58 | 17.9 | 39.0 | 20.8 | 4.0 | 1.5 | 20.3 | 1.7 | 0.6 | 8.0 |
| experiments | 21,427 | 21.4 | 10.3 | 4.6 | 5.57 | 18.4 | 47.3 | 14.1 | 4.0 | 3.1 | 19.4 | 2.8 | 0.9 | 6.0 |
| discussion and conclusion | 4,556 | 23.6 | 9.4 | 3.7 | 5.88 | 21.3 | 32.5 | 13.6 | 10.3 | 3.3 | 24.8 | 1.3 | 0.8 | 4.8 |

## By paper, all sections

| | words | sentence mean | sentence sd | paragraph sentences | letters per word | long words % | we sentences % | passive sentences % | hedges /1k | intensifiers /1k | -ly adverbs /1k | everyday verbs /1k | citations per paragraph | narrative citations % |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| GradeSQL | 6,342 | 22.1 | 10.1 | 3.1 | 5.96 | 22.0 | 16.6 | 15.7 | 3.2 | 3.9 | 24.0 | 1.4 | 0.8 | 1.2 |
| CodeS | 7,646 | 20.2 | 9.3 | 5.2 | 5.86 | 20.2 | 37.2 | 17.6 | 3.9 | 2.0 | 22.0 | 1.6 | 1.3 | 0.0 |
| BIRD | 3,579 | 20.3 | 10.2 | 5.8 | 5.86 | 21.8 | 28.9 | 19.8 | 2.8 | 1.7 | 14.8 | 1.1 | 1.2 | 0.0 |
| Test suites | 3,925 | 23.0 | 11.5 | 3.1 | 5.44 | 15.4 | 53.2 | 9.5 | 6.1 | 0.8 | 23.4 | 2.0 | 0.5 | 13.3 |
| CodeLutra | 3,994 | 21.9 | 10.1 | 5.9 | 5.93 | 22.8 | 44.6 | 7.7 | 2.0 | 5.0 | 21.0 | 0.3 | 1.6 | 3.8 |
| DPO | 5,042 | 25.0 | 12.2 | 5.0 | 5.60 | 18.7 | 50.0 | 15.1 | 2.4 | 1.6 | 17.5 | 1.8 | 1.3 | 5.4 |
| LoRA | 4,498 | 20.6 | 9.5 | 4.0 | 5.39 | 17.0 | 51.0 | 14.4 | 5.6 | 3.6 | 17.8 | 2.7 | 1.1 | 17.4 |
| FedAvg | 5,133 | 25.8 | 13.6 | 4.3 | 5.36 | 15.6 | 47.9 | 24.7 | 3.3 | 2.3 | 20.8 | 2.3 | 0.9 | 25.6 |
| FedProx | 5,928 | 23.8 | 10.9 | 4.1 | 5.56 | 18.9 | 49.8 | 22.4 | 5.6 | 1.9 | 20.4 | 2.7 | 0.6 | 10.3 |
| OpenFedLLM | 6,435 | 25.5 | 14.0 | 4.0 | 5.76 | 20.0 | 39.0 | 19.3 | 6.2 | 2.3 | 19.3 | 2.8 | 2.6 | 0.0 |

## Words, by kind of section (count in the ten papers)

### Hedges

| Kind of section | Most used |
|---|---|
| introduction | likely 6, may 5, might 4, could 4, potentially 3, indicates 1, possibly 1, hypothesize 1 |
| related work | could 5, may 4, might 1, suggests 1, potentially 1, seems 1 |
| method | may 8, potentially 7, might 5, could 5, likely 4, roughly 4, approximately 4, possibly 3, suggest 2, indicate 2 |
| experiments | may 17, could 12, suggests 11, indicates 11, might 10, suggest 5, appears 3, possibly 3, potentially 3, indicate 2 |
| discussion and conclusion | could 15, might 8, may 7, potentially 4, suggests 3, indicate 3, indicates 2, likely 2, suggest 1, appears 1 |

### Transitions

| Kind of section | Most used |
|---|---|
| introduction | while 17, however 16, since 9, specifically 8, instead 8, thus 7, that is 6, in particular 5, hence 5, moreover 4 |
| related work | however 20, while 18, since 7, therefore 5, thus 4, for example 4, although 4, because 4, in contrast 3, instead 3 |
| method | specifically 17, while 17, since 16, however 15, thus 12, therefore 10, for example 9, for instance 8, in practice 8, that is 8 |
| experiments | while 50, however 25, therefore 16, since 16, specifically 15, additionally 12, thus 10, finally 10, because 10, in particular 9 |
| discussion and conclusion | while 20, since 13, however 7, for instance 6, additionally 6, for example 5, finally 4, moreover 3, similarly 3, although 3 |

### Reporting and method verbs

| Kind of section | Most used |
|---|---|
| introduction | use 19, compared 11, propose 8, introduce 8, show 7, improve 7, evaluate 7, consider 7, demonstrate 6, achieved 6 |
| related work | proposed 12, improve 6, used 5, shown 4, compared 4, propose 3, introduce 3, improved 3, leverage 3, demonstrated 2 |
| method | use 23, used 20, employ 14, note 12, introduce 10, denote 10, show 6, proposed 6, denoted 6, consider 6 |
| experiments | use 52, evaluate 43, shows 26, show 23, consider 22, achieves 19, compared 19, observe 18, report 18, shown 17 |
| discussion and conclusion | compared 7, shown 5, shows 4, propose 4, achieve 4, achieves 4, used 4, show 3, proposed 3, demonstrate 3 |

## How the papers name things (count in the ten papers, all sections)

| Concept | Terms |
|---|---|
| the SQL a model outputs | samples 62, candidate 46, candidates 25, outputs 21, completions 19, sampled 18, responses 17, predicted sql 10, candidate sql 10, generated sql 7, predictions 1 |
| the reference SQL | gold 50, ground truth 22, gold query 15, ground-truth 14, gold sql 5 |
| producing SQL | generate 47, generated 42, sample 36, sampling 23, generating 21, generates 10, predict 5, predicts 3, write 1 |
| running SQL | execution 55, executed 15, running 12, run 11, runs 9, executes 5, execute 4, executing 1 |
| outcome of a query | correct 70, incorrect 24, preferred 16, executable 11, failed 10, dispreferred 10, wrong 8, rejected 3, erroneous 1, execution error 1 |
| federated roles | client 82, devices 79, clients 69, round 54, device 40, server 26, local training 26, rounds 25, global model 20, local model 13, communication round 7, aggregation 7 |
| adapting a model | training 278, fine-tuning 96, optimization 62, train 45, adaptation 29, fine-tuned 23, optimize 20, adapt 14, fine-tune 11 |

Section titles not assigned to a kind: BIRD: Acknowledgement; Test suites: Acknowledgement; DPO: Acknowledgements; FedProx: Acknowledgements; OpenFedLLM: Acknowledgement.
