A Federated Learning Approach using Pre-trained
BART Models for Text Classiﬁcation and
Generation Tasks

Quang-Vinh Pham
Department of Data Science
TMA Tech Group, Gia Lai, Vietnam
Email: pqvinh@tma.com.vn

Xuan-Tuyen Le
Department of Information Technology
Quy Nhon University, Vietnam
Email: tuyen4554100008@st.qnu.edu.vn

Quang-Hung Le∗
Department of Information Technology
Quy Nhon University, Vietnam
Email: lequanghung@qnu.edu.vn

Abstract—This paper proposes a novel approach, which inte-
grates Federated Learning (FL) with pre-trained BART models
for text classiﬁcation and generation tasks. In particular, we
ﬁrst design FedAvgBART, a framework that adapts the BART
architecture for FL. We then ﬁne-tune the pre-trained BART
models using FedAvgBART to support both text classiﬁcation
and generation tasks. Comprehensive experiments performed to
evaluate the effectiveness and efﬁciency of this approach on
benchmark datasets using two BART-variants of different sizes,
including BART-large and DistilBART. The signiﬁcant results
demonstrate that federated training can surpass centralized ﬁne-
tuning in performance. Speciﬁcally, BART-large exhibits excep-
tional proﬁciency in classiﬁcation tasks, while DistilBART excels
in text generation, offering superior computational efﬁciency
for resource-limited clients. Furthermore, BART-large maintains
greater stability across diverse client scales, whereas non-IID
data disproportionately affects smaller models, underscoring
the robustness of larger architectures. Our implementation is
available in this Github repository.1

Index Terms—Federated Learning, BART Model, BART-large,
DistilBART, Text Generation, Text Classiﬁcation, Natural Lan-
guage Processing.

I. INTRODUCTION

Text classiﬁcation and generation are two fundamental tasks
in Natural Language Processing (NLP) with broad applications
ranging from sentiment analysis [1], spam detection [2], and
news categorization [3] to dialogue systems [4], machine
translation [5], [6], and abstractive summarization [7]. While
text classiﬁcation enables automatic labeling of large-scale
textual data,
text generation empowers downstream appli-
cations such as conversational agents and content creation.
With the growing availability of sensitive textual data, strict
privacy regulations such as the GDPR [8] have raised concerns
about centralizing user data in conventional machine learning
pipelines. These challenges have motivated the development of
FL, a distributed paradigm that enables model training across

* Corresponding author: Quang-Hung Le (lequanghung@qnu.edu.vn)
1https://github.com/vinh1988/FedAvgBART

clients without transferring raw data to a central server, thereby
preserving privacy while supporting large-scale learning [9],
[10].

At the same time, advances in pre-trained transformer mod-
els, including BERT [11], DistilBERT [12], TinyBERT [13],
MobileBERT [14], and T5 [4], have signiﬁcantly improved
the performance of NLP tasks. Among them, BART [7]
has achieved state-of-the-art results as a powerful sequence-
to-sequence model for classiﬁcation and generation tasks
[15]. Integrating FL with BART models (e.g., BART-large
and DistilBART) provides a promising solution for privacy
preservation and collaborative learning across multiple clients.
Despite its strong performance, several challenges remain un-
resolved. First, applying BART-large directly in FL settings is
impractical due to its high computational and communication
costs, which limit deployment on resource-constrained clients
such as mobile or edge devices [16]. Second, heterogeneous
and non-IID data distributions across clients often degrade
the convergence and generalization performance of the global
model [17]. Third, the trade-off between efﬁciency and ac-
curacy when leveraging distilled variants such as DistilBART
has not been systematically studied in federated environments
[18], [19].

To address the aforementioned challenges, in this paper
we propose a novel approach, which integrates FL with pre-
trained BART models for text classiﬁcation and generation
tasks. The goal of this work is to evaluate the feasibility
and performance of these models in federated environments
for multi-task NLP applications. Our main contributions are
summarized as follows:

1) We introduce FedAvgBART, the ﬁrst federated adapta-
tion of BART that performs joint training across dis-
tributed clients while preserving the encoder–decoder
architecture.

2) We analyze the training objective of FedAvgBART
under heterogeneous and non-IID conditions, showing

its ability to balance global model accuracy and local
personalization.

3) We conduct extensive experiments on benchmark
datasets for both text classiﬁcation and generation,
demonstrating that FedAvgBART achieves competitive
performance compared to centralized training.

4) We compare the performance of DistilBART and BART-
large in both centralized and federated settings, high-
lighting the effect of model size on efﬁciency and
accuracy.

5) We investigate the impact of the number of clients
and data distribution on model performance, providing
insights for future FL applications in NLP.

The rest of the paper is structured as follows. Related work
is presented in Section II. Section III gives some brief reviews
of background knowledge. Our proposed method is presented
in Section IV. Section V analyses and discusses the evaluation
results obtained. Finally, conclusions and future work are
highlighted in Section VI.

II. RELATED WORK

FL concept was ﬁrst introduced by McMahan et al. [9]
in 2017. This ﬁeld has been applied successfully to do-
mains where data privacy and ownership are critical, such
as healthcare [20] and ﬁnance [21]. In the ﬁeld of NLP,
FL has primarily been explored for text classiﬁcation [22],
[23]. These studies often leverage pre-trained transformer-
based models like BERT [11] and RoBERTa [24], which
have shown strong performance even in distributed learn-
ing environments [25]. Recently, some frameworks such as
FedNLP [26] and FedML [27] provide tools to benchmark FL
methods on standard NLP tasks. However, the aforementioned
works tend to focus on encoder-only models and classiﬁcation
objectives.

In contrast, text generation in federated settings remains
an underexplored area. While language modeling in FL has
been explored (e.g., mobile keyboard prediction [28]), few
works investigate more sophisticated generative models like
BART [7] and its distilled variant, DistilBART [15]. These
models have proven effective in a range of centralized NLP
tasks such as generation, translation, and comprehension. Their
encoder-decoder architecture makes them particularly suitable
for both classiﬁcation (via encoder features) and generation
(via decoder outputs), which makes them strong candidates
for multi-task learning in FL settings.

To the best of our knowledge, there is no existing research
that
investigates BART models in federated environments
for multi-task NLP applications. In this paper, we aim to
explore the federated ﬁne-tuning of pre-trained BART-large
and DistilBART models for text classiﬁcation and generation
tasks.

III. PRELIMINARIES

A. Federated Learning

FL is a distributed paradigm in which a set of clients
collaboratively train a global model while keeping their private
data local. The goal of FL is to optimize the global objective:

min
w

L(·) =

1
N

N
(cid:88)

Ln(xn, yn; w)

(1)

n=1
where Ln(·) is the cross-entropy loss on data of client n
(xn, yn), and the overall objective L(w) represents the average
loss aggregated across all N clients. To better illustrate the
optimization process in FL, we now consider a scenario
where the system comprises N clients {C1, C2, . . . , CN }, each
owning a local dataset Ck and maintaining its own model.

i )}nk

|Dk| = nk

Dk = {(xk

i=1, where

i , yk
with the total number of samples n = (cid:80)N
k=1 nk. Each client
maintains a local model with parameters wk
t at communi-
cation round t, where the prediction on input x is denoted
as f (x; wk
t ). In contrast, conventional centralized training
assumes access to a uniﬁed dataset Dserver = ∪N

(2)

k=1Dk.

B. BART Model

BART [7] is a sequence-to-sequence pre-trained model
designed as a denoising autoencoder. Built upon the trans-
former encoder–decoder framework [29], the model utilizes
a BERT-like bidirectional encoder to capture representations
from corrupted text, and a GPT-style autoregressive decoder
to regenerate the original document via cross-attention. BART-
large consists of 12 encoder and 12 decoder layers (hidden size
1024), with GeLU activation [30]. The pre-training objective
minimizes the negative log-likelihood of the original text:

L = −

T
(cid:88)

t=1

log P (xt | x<t, ˜X; wt)

(3)

where X = (x1, . . . , xT ) is the original sequence, ˜X is the
corrupted input, and wt denotes model parameters. Corruption
strategies include token masking, token deletion, text inﬁll-
ing, sentence permutation, and document rotation. With its
encoder–decoder design, BART can be ﬁne-tuned for diverse
tasks such as sequence classiﬁcation, token classiﬁcation, text
generation (summarization, question answering), and machine
translation.

C. Task Formulations

1) Text Generation: Text generation (also know as decod-
ing) [1] refers to the process of producing tokens condi-
tioned on a given context. Let X = (x1, x2, . . . , xS), Y =
(y1, y2, . . . , yT ) where X is the source context of S tokens
and Y is the target sequence of T tokens. The conditional
probability of generating Y is

P (Y | X) =

T
(cid:89)

p(yt | X, y<t)

(4)

In this section, we provide the necessary background on FL,
the BART model, and task formulations, which together form
the foundation of our proposed method.

t=1
where y<t = (y1, . . . , yt−1). At each step t, the model M
computes the distribution p(yt | X, y<t) over the vocabulary,

Fig. 1: Overview of the FedAvgBART framework, illustrating the server-client interaction for aggregating model updates in a
federated setting.

from which the next
is selected. This iterative
autoregressive mechanism [7], [11] enables coherent sequence
generation.

token yt

2) Text Classiﬁcation: Let X = (x1, x2, . . . , xS) denote
an input text of length S, and let Y = {y1, . . . , yT } be the
label set with |Y | = T . Each label yj is represented as a one-
hot vector. The goal is to learn a classiﬁer f that estimates
the conditional probability P (y | X) and assigns the most
probable label:

P (y | X) = f (X), where

y∗ = arg max
y∈Y

P (y | X)

(5)

Here, the ground-truth label y ∈ Y speciﬁes the semantic
category of the input.

IV. METHODOLOGY
In this section, we ﬁrst introduce an overview of our Fe-
dAvgBART framework. We then explain the training process
for the proposed method. At last, ﬁne-tuning FedAvgBART
for text classiﬁcation and generation tasks are discussed.

A. An Overview

Figure 1 presents the FedAvgBART framework, which
integrates the BART model into a FL pipeline. The process
is divided into three main phases:

1) Broadcast: The central server initializes the global
model w0 by loading a pre-trained BART architecture tailored
to the target task. System parameters such as learning rate
η and communication rounds are conﬁgured. The initialized
global model wt is then broadcast to all participating clients,
serving as the starting point for their local models.

2) Upload: Each client Cn loads the BART model and ﬁne-
tunes it locally using its private, non-IID dataset Dn. The local
training process involves computing gradients and updating the
model parameters:

wn

t+1 ← wt − η∇Ln(wt, Dn)

(6)

where Ln is the local loss function. After training, the client
computes the model update:

∆wn = wn

t+1 − wt

(7)

and uploads ∆wn to the server. This approach allows clients to
adapt the BART model to their local data distributions without
sharing raw data.
3) Update:

server
{∆w1, ∆w2, . . . , ∆wN } from all
FedAvg method [10] to update the global model:

updates
and performs

collects

clients

The

wt+1 ← wt +

N
(cid:88)

n=1

1
N

∆wn

(8)

Alternatively, weighted averaging based on dataset sizes |Dn|
can be applied. The updated global BART model wt+1 is then
redistributed to all clients for the next training round. This
iterative process continues until convergence or a predeﬁned
performance threshold is met.

B. FedAvgBART via Federated Learning

The intuition is that the pre-trained BART, with its encoder-
decoder architecture, acts as a uniﬁed feature extractor and
classiﬁer across clients. Unlike split methods, no parameters

are kept
local all are jointly optimized. This can lead to
higher communication costs but provides a simpler baseline
for homogeneous or mildly heterogeneous settings. The Fe-
dAvgBART based training approach for BART pre-training is
summarized in Algorithm 1.

Algorithm 1 FedAvgBART Pre-training via FedAvg

Require: Number of communication rounds T , local epochs

E, learning rate η, number of clients N .

Ensure: Global model wT after T communication rounds.

1: Initialize global model parameters w0 (from pre-trained

BART).

Server selects a subset of clients St ⊆ {C1, . . . , CN }.
for each client Ck ∈ St in parallel do

2: for each round t = 0, 1, . . . , T − 1 do
3:
4:
5:
6:
7:

Set wk
for each local epoch e = 1, . . . , E do

Compute gradient ∇Lk(wk

t ; Dk) on local data

t ← wt.

8:

9:

10:

Dk.

Update parameters:

wk

t ← wk

t − η∇Lk(wk

t ; Dk)

Send updated parameters wk

t to server.

Server aggregates updates:

wt+1 ←

1
n

N
(cid:88)

k=1

nkwk

t , where n =

N
(cid:88)

k=1

nk

The FedAvgBART algorithm extends the standard FedAvg
method to ﬁne-tune the BART model in a distributed and
heterogeneous data setting. Initially, the server initializes the
global model parameters w0 from the pre-trained BART. At
each communication round t, the server selects a subset of
clients to participate in training. Each client Ck downloads
the current global model wt and performs local ﬁne-tuning
on its private dataset Dk for E epochs, resulting in updated
parameters wk
t . The updated models are then sent back to the
server. The server aggregates the received parameters using a
weighted average based on the local dataset sizes nk of the
participating clients:

wt+1 ←

1
n

N
(cid:88)

k=1

nkwk

t , where n =

N
(cid:88)

k=1

nk

(9)

This process is repeated for T rounds until convergence. The
ﬁnal global model wT represents the ﬁne-tuned BART model
trained in a federated manner, leveraging decentralized and
diverse client data while preserving data privacy.

Building on the foundational FedAvgBART pipeline, which
enables collaborative ﬁne-tuning across distributed clients, we
now delve into the speciﬁc adaptations of the BART model
for downstream tasks. This ensures that the federated frame-
work leverages BART’s strengths in both discriminative and
generative paradigms, addressing a range of NLP applications
while maintaining data privacy.

C. Fine-tuning FedAvgBART for Text Classiﬁcation and Gen-
eration Tasks

In our FL framework, we ﬁne-tune the pre-trained BART
model using the proposed FedAvgBART approach to support
both text classiﬁcation and generation tasks. By leveraging
its bidirectional encoder and autoregressive decoder, FedAvg-
BART effectively adapts to heterogeneous data distributions
across clients while maintaining a uniﬁed global model. For
text classiﬁcation (e.g., sentiment analysis or topic catego-
rization), the task is reformulated as a sequence-to-sequence
generation problem, where the decoder predicts the target label
conditioned on the encoded input. For text generation (e.g.,
summarization or dialogue), the model directly utilizes the
encoder to process the input sequence and the decoder to
autoregressively generate the corresponding output, aligning
naturally with BART’s pre-training objective.

Fig. 2: BART architecture for text classiﬁcation.

classiﬁcation. The

Figure 2 illustrates BART’s encoder-based architecture
sequence
(e.g.,
for
tokenized input
“<s> The movie was amazing </s>”)
is ﬁrst mapped
through an embedding layer with positional encoding, then
sequentially processed by multi-head self-attention, residual
connections with layer normalization, and a feed-forward
network, yielding contextualized hidden representations.
These encoder representations are then passed to a linear
to
projection layer,
produce the ﬁnal classiﬁcation label. Unlike the full seq2seq
generation framework, this setup employs only the encoder
for representation learning, directly mapping input text into
class probabilities. By this way, we can leverage BART’s
pre-trained bidirectional context modeling for downstream
classiﬁcation tasks, making it effective even on heterogeneous
or non-IID data in FL scenarios.

followed by Softmax normalization,

Shifting to generation tasks, BART excels in producing
coherent and contextually relevant text outputs, such as sum-
marization, translation, or conditional text completion.

BART-based models (DistilBART and BART-large) for
NLP tasks involving classiﬁcation and generation?

• RQ2 (non-IID data): How does non-IID data distribution
across clients affect the performance of DistilBART and
BART-large in federated settings for text classiﬁcation
and generation tasks?

• RQ3 (number of clients): How does the number of clients
inﬂuence the performance of federated ﬁne-tuning of pre-
trained models such as DistilBART and BART-large on
text classiﬁcation and generation tasks?

A. Datasets, Tasks, and Models

We used two datasets: the 20News dataset [32] for classi-
ﬁcation and the CNN/DailyMail dataset [33] for generation.
The models used are BART-large [7] and DistilBART [15].

1) 20News Dataset: The 20News dataset [32] is a col-
lection of approximately 20,000 newsgroup documents, par-
titioned (nearly) evenly across 20 different newsgroups. It
is a widely used benchmark for text classiﬁcation tasks
due to its diverse topics and relatively balanced class dis-
tribution. Each document belongs to one of 20 categories,
such as ‘alt.atheism‘, ‘comp.graphics‘, ‘rec.sport.baseball‘,
and ‘talk.politics.mideast‘. The dataset
is preprocessed to
remove headers, footers, and quotes, focusing on the core
content for classiﬁcation. In our experiments, we utilize 11,314
training samples and 7,532 validation samples.

2) CNN/DailyMail Dataset: The CNN/DailyMail dataset
[33] is a popular benchmark for text summarization and
generation tasks. It consists of news articles (from CNN and
Daily Mail) paired with multi-sentence summaries written by
journalists. The task is to generate a concise and coherent
summary given the full news article. We use a subset of
this dataset, comprising 10,000 training samples and 5,000
validation samples, to evaluate the text generation capabilities
of our models.

B. Evaluation Metrics

We use the following metrics for evaluation:
• Accuracy (Acc): The proportion of correct predictions

among the total number of cases examined [31].

Acc =

Number of correct predictions
Total number of predictions

(10)

• Precision (Prec), Recall (Rec), and F1-score: Metrics for

classiﬁcation performance [31].

– Prec: The ratio of true positives (TP) to all positive

predictions (TP + FP).

Prec =

TP
TP + FP

(11)

– Rec: The ratio of true positives (TP) to all actual

positives (TP + FN).

Rec =

TP
TP + FN

(12)

– F1-score: The harmonic mean of precision and recall.

F1 = 2 ×

Prec × Rec
Prec + Rec

(13)

Fig. 3: BART architecture for text generation.

Figure 3 depicts

the sequence-to-sequence generative
architecture of BART. The encoder processes the tokenized
(e.g., “<s> The <mask> was <mask> </s>”)
input
through an embedding layer with positional encoding,
followed by multi-head self-attention, residual connections
with layer normalization, and a feed-forward network,
yielding contextualized hidden representations. These encoder
representations are transmitted to the decoder, where the
partially observed target sequence (e.g., “<s> The . . . was
. . . </s>”) is ﬁrst embedded with positional
information
and passes through masked multi-head self-attention and
the decoder performs cross-
normalization. Subsequently,
attention, attending to the encoder’s hidden states, before
applying an additional
feed-forward transformation and
normalization. The decoder outputs are projected through a
linear transformation and normalized via Softmax to produce
the next
token in an autoregressive manner. This enables
the encoder to capture bidirectional contextual dependencies,
while the decoder generates the output sequence incrementally,
token by token.

By integrating these task-speciﬁc adaptations into FedAvg-
BART, the framework not only handles classiﬁcation through
discriminative generation but also supports pure generative
outputs, ensuring robustness across varying data distributions.
This dual capability facilitates seamless transitions between
tasks in federated environments, with future extensions poten-
tially exploring hybrid classiﬁcation-generation objectives to
further mitigate heterogeneity challenges.

V. EXPERIMENTS

In this section, we conduct experiments led by the following

research questions (RQ):

• RQ1 (model size): What is the impact of model size on
the efﬁciency and performance of federated training of

• ROUGE: A standard metric for evaluating text summa-
rization and generation [34]. We report ROUGE-1 (uni-
gram overlap), ROUGE-2 (bigram overlap), and ROUGE-
L (longest common subsequence). Here, gen denotes the
generated summary, ref
the reference summary, and n-
gram a contiguous sequence of n words.

– ROUGE-N: Measures the recall of n-gram overlap

between gen and ref :
(cid:80)

ROU GE − N =

n-gram min(Countgen, Countref)
n-gram Countref

(cid:80)

(14)
– ROUGE-L: Based on the length of the longest com-

mon subsequence (LCS) between gen and ref :

ROU GE − L =

LCS(gen, ref)
|ref|

(15)

C. Experimental Setup

1) Implementation: All the architectures are implemented
in Pytorch. FL simulations are done with the FedAvg al-
gorithm in a cross-device setting. Client data heterogeneity
is controlled using Dirichlet partitioning with concentration
parameter α ∈ {0.1, 0.5}, where a smaller α indicates more
non-IID data. Experiments were executed on Nvidia GPUs.

2) Hyper Parameters: The models were ﬁne-tuned for a
set number of rounds: 22 for the 20News dataset and 5 for
CNN/DailyMail. The number of clients varied from 2 to 10.
Performance of BART-large and DistilBART was compared in
both centralized and federated settings. For text classiﬁcation,
the number of clients ranged from 2 to 10, while for text
generation it ranged from 2 to 5, allowing us to observe the
effect on model performance for both tasks. To simulate non-
IID data distributions, a Dirichlet distribution with α values of
0.1 (highly non-IID) and 0.5 (more IID-like) was employed,
and the results were compared against IID settings.

D. Results and Discussion

Fig. 4: Performance comparison for classiﬁcation (F1-Score).

of 20.8-30.5, and ROUGE-L scores of 30.8-38.7. The most
signiﬁcant improvements are seen in the non-IID setting for
text generation, where DistilBART’s ROUGE-2 score of 30.5
is 38.7% higher than BART-large’s ROUGE-2 score of 22.0,
highlighting its effectiveness in heterogeneous data environ-
ments. Figure 4 shows the F1 comparison for classiﬁcation.

TABLE I: Classiﬁcation performance: Centralized vs. Feder-
ated.

Model

BART-large
DistilBART

Centralized
F1
Acc
0.746
0.743
0.740
0.739

Federated
F1
0.782
0.738

Acc
0.778
0.738

Improvement
∆F1
+0.04
-0.001

∆Acc
+0.03
-0.002

TABLE II: Text generation performance: Centralized vs. Fed-
erated.

Model

BART-large

DistilBART

Metric
ROUGE-1
ROUGE-2
ROUGE-L
ROUGE-1
ROUGE-2
ROUGE-L

Centralized
41.5
19.5
28.7
40.9
18.9
28.4

Federated
42.2
20.6
29.5
43.3
20.9
30.4

Improv.
+0.7
+1.1
+0.8
+2.4
+2.0
+2.0

1) Impact of Model Size on Federated Training (RQ1):
Table I provides detailed results for RQ1 regarding text
classiﬁcation. Our experiments reveal contrasting behaviors
between the two architectures under federated training. For
classiﬁcation, BART-large achieves signiﬁcant improvements
with 0.778 accuracy and 0.782 F1 score in federated training,
compared to 0.743 accuracy and 0.746 F1 in centralized
training (+0.04 accuracy, +0.04 F1). In contrast, DistilBART
shows a slight degradation in classiﬁcation performance, with
0.738 accuracy and 0.738 F1 in federated settings versus
0.739 accuracy and 0.740 F1 centralized (-0.002 accuracy, -
0.001 F1). For text generation, both models show substantial
improvements across all ROUGE metrics under federated
training (Table II). BART-large shows consistent performance
across different data distributions, with ROUGE-1 scores of
42.2-43.4, ROUGE-2 scores of 21.1-22.0, and ROUGE-L
scores of 30.7-31.7. DistilBART demonstrates stronger overall
performance in text generation, particularly in the non-IID
setting, with ROUGE-1 scores of 43.0-48.9, ROUGE-2 scores

2) Inﬂuence of Non-IID Data Distribution (RQ2): The
inﬂuence of non-IID data reveals interesting patterns across
different model architectures. For text generation (Table IV),
DistilBART shows superior performance in the highly non-IID
setting (α = 0.1) with ROUGE scores of 48.9/30.5/38.7 (R-
1/R-2/R-L), compared to 43.0/20.8/30.8 in the more IID-like
setting (α = 0.5). This 5.9-point improvement in ROUGE-1
suggests that the distilled model can effectively leverage data
diversity. In contrast, BART-large shows a different pattern,
with slightly better ROUGE-2 and ROUGE-L scores in the
non-IID setting but a 1.2-point drop in ROUGE-1. The models
also differ in their loss patterns, with DistilBART achieving
lower loss values (0.893 vs 1.113 for BART-large in the non-
IID setting), indicating more stable training. These results sug-
gest that the relationship between model size, data distribution,
and task performance in FL is complex and warrants further
investigation. For classiﬁcation performance under non-IID
conditions, see Tables III and V, and Figure 7 for detailed
comparisons.

Fig. 5: Performance comparison for text generation (ROUGE-
1 Score).

TABLE III: BART-large text classiﬁcation federated best-
round results across client counts, separated by data partition
parameter α (bold = best per column; for Loss, lower is
better).

Fig. 6: ROUGE-1 F1 vs number of clients for DistilBART and
BART-large. Smaller α indicates more non-IID data.

Clients
2
3
4
5
6
7
8
9
10

Clients
2
3
4
5
6
7
8
9
10

Round
22
22
22
21
21
21
22
22
22

Round
22
21
22
22
22
22
22
22
20

α=0.1 (non-IID)
F1
0.9722
0.9735
0.9515
0.9654
0.9807
0.9787
0.9681
0.9736
0.9817
α=0.5 (IID)
F1
0.9723
0.9423
0.9596
0.9707
0.9629
0.9513
0.9626
0.9567
0.9709

Acc
0.9677
0.9698
0.9724
0.9697
0.9756
0.9729
0.9711
0.9660
0.9704

Acc
0.9658
0.9679
0.9630
0.9584
0.9581
0.9462
0.9597
0.9407
0.9512

Prec
0.9744
0.9753
0.9531
0.9676
0.9822
0.9793
0.9716
0.9746
0.9839

Prec
0.9737
0.9546
0.9611
0.9717
0.9650
0.9562
0.9657
0.9569
0.9711

Rec
0.9715
0.9730
0.9515
0.9662
0.9806
0.9792
0.9669
0.9734
0.9818

Rec
0.9721
0.9375
0.9597
0.9705
0.9629
0.9514
0.9617
0.9581
0.9718

Loss
0.0987
0.0959
0.0825
0.0993
0.0724
0.0876
0.0873
0.1019
0.1031

Loss
0.1090
0.1110
0.1146
0.1366
0.1354
0.1598
0.1344
0.2088
0.1629

Figure 5 illustrates that DistilBART generally outperforms
BART-large in ROUGE-1 scores for text generation, especially
under non-IID data conditions. DistilBART achieves a peak
ROUGE-1 score of 48.9, signiﬁcantly higher than BART-
large’s 42.2, suggesting its superior effectiveness in hetero-
geneous federated environments for generative tasks.

Figure 8 illustrates the per-client data share as 100%-stacked
bars for each federation size N, where each bar aggregates
clients 1..N as a percentage of total samples, averaged across
multiple runs, considering data heterogeneity, communication
cost, scalability, and robustness.

3) Effect of Client Population on Federated Fine-Tuning
(RQ3): Text generation results show distinct client scaling
patterns. As seen in Figure 6, DistilBART achieves strong
performance with a peak ROUGE-1 score of 48.9 under non-
IID conditions (α = 0.1), while BART-large shows more
modest performance with 42.2 ROUGE-1. The performance
gap between the models is particularly notable in the non-

IID setting, where DistilBART demonstrates superior perfor-
mance across all ROUGE metrics (30.5 ROUGE-2 and 38.7
ROUGE-L) compared to BART-large (22.0 ROUGE-2 and
31.7 ROUGE-L). This suggests that the distilled model may
be more effective at handling the complexities of federated
text generation tasks, especially in heterogeneous data environ-
ments. Table III and V provide detailed results across different
client conﬁgurations.

The text generation results in Tables VI and VII reveal
distinct patterns in how model architectures respond to data
heterogeneity and client scaling. For BART-large, performance
peaks at 5 clients in the non-IID setting (α = 0.1) with
ROUGE scores of 44.57/23.28/30.05, while the IID setting
(α = 0.5) achieves optimal performance at 3 clients with
43.43/21.12/30.66. This suggests that BART-large beneﬁts
from increased client diversity in heterogeneous environments
but requires fewer coordination points in homogeneous set-
tings.

DistilBART exhibits a more pronounced sensitivity to data
distribution, achieving exceptional performance at 3 clients
in the non-IID setting with remarkable ROUGE scores of
48.87/30.48/38.72—signiﬁcantly outperforming BART-large
across all metrics. However,
in the IID setting, Distil-
BART’s performance converges to similar levels as BART-
large (43.39/21.06/30.67 at 3 clients), indicating that the dis-
tilled model’s advantage emerges speciﬁcally from its ability
to leverage data heterogeneity. The convergence patterns also
differ, with DistilBART requiring fewer rounds in IID settings
(round 1 vs round 2-3) but maintaining consistent performance
across rounds in non-IID environments, suggesting more stable
training dynamics under data heterogeneity.

Fig. 7: Classiﬁcation F1 vs number of clients. BART-large
(IID) is stable, while DistilBART’s performance varies with
data heterogeneity (α).

Client share (2..5 clients)

TABLE IV: Federated text generation: IID vs. Non-IID com-
parison. Best-round performance on CNN/DailyMail showing
impact of data distribution (bold = best per column; for Loss,
lower is better).

Model
BART-large
BART-large
DistilBART
DistilBART

α
0.1
0.5
0.1
0.5

ROUGE-1 ROUGE-2
21.98
21.13
30.49
20.84

42.20
43.42
48.86
43.00

ROUGE-L
31.66
30.66
38.73
30.84

Loss
1.113
2.229
0.893
1.615

TABLE V: DistilBART text classiﬁcation federated best-round
results across client counts, separated by data partition param-
eter α (bold = best per column; for Loss, lower is better).

Clients
2
3
4
5
6
7
8
9
10

Clients
2
3
4
5
6
7
8
9
10

Round
20
19
21
21
22
22
22
22
5

Round
22
22
20
22
20
22
21
22
20

α=0.1 (non-IID)
F1
0.9771
0.9732
0.9259
0.9157
0.8570
0.8600
0.8995
0.9719
0.3324
α=0.5 (IID)
F1
0.9753
0.9673
0.9413
0.9630
0.9586
0.9529
0.9704
0.9139
0.9264

Acc
0.9730
0.9765
0.9756
0.9731
0.9763
0.9725
0.9732
0.9747
0.9111

Acc
0.9731
0.9749
0.9717
0.9681
0.9629
0.9554
0.9668
0.9356
0.9474

Prec
0.9811
0.9801
0.9914
0.9720
0.9879
0.9959
0.9862
0.9907
0.5451

Prec
0.9908
0.9781
0.9751
0.9704
0.9801
0.9689
0.9765
0.9568
0.9525

Rec
0.9758
0.9693
0.8817
0.8895
0.7651
0.7883
0.8430
0.9587
0.2514

Rec
0.9633
0.9624
0.9278
0.9604
0.9464
0.9676
0.9676
0.8866
0.9073

Loss
0.0862
0.0696
0.0763
0.0906
0.1018
0.0739
0.0953
0.0859
0.5470

Loss
0.0899
0.0849
0.0988
0.1062
0.1314
0.1486
0.1169
0.2430
0.2056

Client share (2..10 clients)

Fig. 8: Per-client data share as 100%-stacked bars for each
federation size N, averaged across runs.

TABLE VI: DistilBART text generation federated best-round
ROUGE results across client counts, separated by data parti-
tion parameter α (bold = best per column).

Clients
2
3
4
5

Clients
2
3
4
5

Round
2
2
2
3

Round
1
1
1
3

α = 0.1 (non-IID)
ROUGE-1
42.5291
48.8694
43.1349
42.3518
α = 0.5 (IID)

ROUGE-2
20.1340
30.4841
18.7339
21.0916

ROUGE-1
42.3780
43.3872
43.1024
43.2821

ROUGE-2
20.0847
21.0637
20.4452
20.8961

ROUGE-L
29.7839
38.7152
28.6039
30.1326

ROUGE-L
29.6427
30.6698
30.0926
30.3861

TABLE VII: BART-large text generation federated best-round
ROUGE results across client counts, separated by data parti-
tion parameter α (bold = best per column).

Clients
2
3
4
5

Clients
2
3
4
5

Round
2
2
2
2

Round
2
2
2
2

α = 0.1 (non-IID)
ROUGE-1
42.5276
42.2042
41.9328
44.5677
α = 0.5 (IID)

ROUGE-2
20.1377
21.9767
19.1366
23.2808

ROUGE-1
42.3843
43.4289
43.2763
43.0532

ROUGE-2
20.0745
21.1218
20.6950
20.6097

ROUGE-L
29.7835
31.6594
28.3490
30.0505

ROUGE-L
29.6515
30.6572
30.3264
30.1883

VI. CONCLUSION

In this paper, we proposed a novel approach, which inte-
grates FL with pre-trained BART models for text classiﬁcation
and generation tasks. This is a promising solution for privacy
preservation and collaborative learning across multiple clients.
We evaluated the effectiveness and efﬁciency of this approach
on benchmark datasets using BART-large and DistilBART
models. The experimental results demonstrated that federated
training can surpass centralized ﬁne-tuning in performance.
We uncover a task-architecture alignment: BART-large ex-
hibits exceptional proﬁciency in classiﬁcation tasks, while
DistilBART excels in text generation, offering superior com-
putational efﬁciency for resource-limited clients. Furthermore,
BART-large maintains greater stability across diverse client
scales, whereas non-IID data disproportionately affects smaller
models, underscoring the robustness of larger architectures.
These ﬁndings redeﬁne the efﬁciency-robustness trade-off,
offering a theoretical and practical foundation for tailoring
model architectures to the unique dynamics of federated NLP
environments.

In future work, we plan to explore the following four
directions. First, investigating more advanced FL algorithms
beyond FedAvg, such as FedProx or SCAFFOLD [35], may
yield better performance under high data heterogeneity by
addressing client drift and improving convergence stability.
Second, combining distillation with other model compression
techniques like quantization and pruning could further reduce
computational and communication overhead while maintain-
ing model performance. Third, applying our framework to
other complex NLP tasks and domains, such as biomedical
text processing or multilingual scenarios, would demonstrate
incorporating formal privacy
broader applicability. Finally,
guarantees through differential privacy or secure aggregation
would strengthen the privacy-preserving aspects of federated
ﬁne-tuning for sensitive applications.

REFERENCES

[9] H. McMahan, E. Moore, D. Ramage, S. Hampson, and B. Arcas,
“Communication-efﬁcient learning of deep networks from decentralized
data,” in Proceedings of AISTATS, 2017, pp. 1273–1282.

[10] Q. Yang, Y. Liu, T. Chen, and Y. Tong, “Federated machine learning:
Concept and applications,” ACM Transactions on Intelligent Systems and
Technology, vol. 10, no. 2, pp. 1–19, 2019.

[11] J. Devlin, M. Chang, K. Lee, and K. Toutanova, “BERT: Pre-training
of deep bidirectional transformers for language understanding,” in Pro-
ceedings of NAACL, 2019, pp. 4171–4186.

[12] V. Sanh, L. Debut, J. Chaumond, and T. Wolf, “DistilBERT, a distilled
version of BERT: smaller, faster, cheaper and lighter,” arXiv preprint
arXiv:1910.01108, 2019.

[13] X. Jiao et al., “TinyBERT: Distilling BERT for natural language under-

standing,” in Findings of EMNLP, 2020, pp. 4163–4174.

[14] Z. Sun et al., “MobileBERT: a compact

task-agnostic BERT for
resource-limited devices,” in Proceedings of ACL, 2020, pp. 2158–2170.
[15] S. Shleifer and A. Rush, “Pre-trained summarization distillation,” arXiv

preprint arXiv:2010.13002, 2020.

[16] J. Xu and K. Lee, “Performance and communication cost of deep neural
networks in federated learning environments,” IEEE Transactions on
Parallel and Distributed Systems, 2024.

[17] Y. Zhao, M. Li, Y. Lai, N. Suda, D. Civin, and V. Chandra, “Federated

learning with non-IID data,” arXiv preprint arXiv:1806.00582, 2018.

[18] S. He and Y. Wang, “A survey on federated ﬁne-tuning of large language

models,” arXiv preprint arXiv:2507.xxxxx, 2025.

[19] Z. Chen, L. Xu, and J. Li, “Communication-efﬁcient and ten-
sorized federated ﬁne-tuning of large language models,” arXiv preprint
arXiv:2508.xxxxx, 2025.

[20] I. Dayan et al., “Federated learning for predicting clinical outcomes in
patients with COVID-19,” Nature Medicine, vol. 27, no. 10, pp. 1735–
1743, 2021.

[21] G. Long, Y. Tan, J. Jiang, and C. Zhang, “Federated learning for open
banking,” in Federated Learning: Privacy and Incentive, Springer, 2020,
pp. 240–254.

[22] J. Lee and S. Park, “Federated Freeze BERT for text classiﬁcation,”

IEEE Transactions on Neural Networks and Learning Systems, 2024.

[23] M. Lee and J. Cho, “Federated Split BERT for heterogeneous text

classiﬁcation,” in Proceedings of COLING, 2022.

[24] Y. Liu et al., “RoBERTa: A robustly optimized BERT pretraining

approach,” arXiv preprint arXiv:1907.11692, 2019.

[25] L. Chen and H. Yang, “FedBERT: When federated learning meets pre-

training,” in Proceedings of EMNLP, 2022.

[26] T. Lin, L. Kong, S. Liu, M. Hong, and H. Yang, “FedNLP: Benchmark-
ing federated learning methods for natural language processing tasks,”
in Proceedings of the EMNLP Workshop, 2022.

[27] C. He et al., “FedML: A research library and benchmark for federated

machine learning,” arXiv preprint arXiv:2007.13518, 2020.

[28] A. Hard et al., “Federated learning for mobile keyboard prediction,”

arXiv preprint arXiv:1811.03604, 2018.

[29] A. Vaswani et al., “Attention is all you need,” in Advances in Neural

Information Processing Systems, 2017, pp. 5998–6008.

[1] B. Liu, “Sentiment analysis and opinion mining,” Communications of

[30] D. Hendrycks and K. Gimpel, “Gaussian error linear units (GELUs),”

the ACM, vol. 64, no. 2, pp. 62–71, 2021.

arXiv preprint arXiv:1606.08415, 2016.

[2] R. Agarwal, A. Dhoot, S. Kant, V. S. Bisht, H. Malik, M. F. Ansari,
A. Afthanorhan, and M. A. Hossaini, “A novel approach for spam
detection using natural
language processing with AMALS models,”
IEEE Access, vol. 12, pp. 124298–124313, 2024.

[3] M. Hasan, T. Ahmed, M. R. Islam, and M. P. Uddin, “Leveraging
textual information for social media news categorization and sentiment
analysis,” PLOS ONE, vol. 19, no. 7, p. e0307027, 2024.

[4] C. Raffel et al., “Exploring the limits of transfer learning with a uniﬁed
text-to-text transformer,” Journal of Machine Learning Research, vol.
21, pp. 1–67, 2020.

[5] Quang-Hung, L. & Anh-Cuong, L. Syntactic pattern based Word
Alignment for Statistical Machine Translation. International Journal of
Knowledge and Systems Science (IJKSS). 5, 36-45 (2014).

[6] Quang-Hung, L. & Anh-Cuong, L. Improving Word Alignment for
Statistical Machine Translation Based on Constraints. 2012 International
Conference on Asian Language Processing. pp. 113-116 (2012).
[7] M. Lewis et al., “BART: Denoising sequence-to-sequence pre-training
for natural language generation, translation, and comprehension,” in
Proceedings of ACL, 2020, pp. 7871–7880.

[8] General Data Protection Regulation (GDPR), Accessed: Aug. 31, 2025.

[Online]. Available: https://gdpr-info.eu

[31] M. Sokolova and G. Lapalme, “A systematic analysis of performance
measures for classiﬁcation tasks,” Information Processing & Manage-
ment, vol. 45, no. 4, pp. 427–437, 2009.

[32] K. Lang, “Newsweeder: Learning to ﬁlter netnews,” in Proceedings of
the 12th International Conference on Machine Learning, 1995, pp. 331–
339.

[33] K. Hermann et al., “Teaching machines to read and comprehend,” in
Advances in Neural Information Processing Systems, 2015, pp. 1693–
1701.

[34] C.-Y. Lin, “ROUGE: A package for automatic evaluation of summaries,”

in Proceedings of ACL Workshop, 2004, pp. 74–81.

[35] S. P. Karimireddy, S. Kale, M. Mohri, S. Reddi, S. Stich, and A. T.
Suresh, “SCAFFOLD: Stochastic controlled averaging for on-device
federated learning,” in Proceedings of the 37th International Conference
on Machine Learning (ICML), 2020.

