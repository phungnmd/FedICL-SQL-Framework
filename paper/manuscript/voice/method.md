# Method sections

## Rafailov et al., "Direct Preference Optimization: Your Language Model is Secretly a Reward Model", NeurIPS 2023, Section 4

> Motivated by the challenges of applying reinforcement learning
> algorithms on large-scale problems such as fine-tuning language
> models, our goal is to derive a simple approach for policy
> optimization using preferences directly. Unlike prior RLHF methods,
> which learn a reward and then optimize it via RL, our approach
> leverages a particular choice of reward model parameterization that
> enables extraction of its optimal policy in closed form, without an
> RL training loop. As we will describe next in detail, our key insight
> is to leverage an analytical mapping from reward functions to optimal
> policies, which enables us to transform a loss function over reward
> functions into a loss function over policies. [...]
>
> **What does the DPO update do?** For a mechanistic understanding of
> DPO, it is useful to analyze the gradient of the loss function
> L_DPO. [the gradient, with each factor labelled under its brace:
> "higher weight when reward estimate is wrong", "increase likelihood
> of y_w", "decrease likelihood of y_l"] [...] Intuitively, the
> gradient of the loss function L_DPO increases the likelihood of the
> preferred completions y_w and decreases the likelihood of
> dispreferred completions y_l. Importantly, the examples are weighed
> by how much higher the implicit reward model rates the dispreferred
> completions, scaled by β, i.e, how incorrectly the implicit reward
> model orders the completions, accounting for the strength of the KL
> constraint. Our experiments suggest the importance of this weighting,
> as a naïve version of this method without the weighting coefficient
> can cause the language model to degenerate (Appendix Table [n]).

## McMahan et al., FedAvg, AISTATS 2017, Section 2

> The recent multitude of successful applications of deep learning have
> almost exclusively relied on variants of stochastic gradient descent
> (SGD) for optimization; in fact, many advances can be understood as
> adapting the structure of the model (and hence the loss function) to
> be more amenable to optimization by simple gradient-based methods
> [ref]. Thus, it is natural that we build algorithms for federated
> optimization by starting from SGD.
>
> SGD can be applied naively to the federated optimization problem,
> where a single batch gradient calculation (say on a randomly selected
> client) is done per round of communication. This approach is
> computationally efficient, but requires very large numbers of rounds
> of training to produce good models [...]
>
> [...] To apply this approach in the federated setting, we select a
> C-fraction of clients on each round, and compute the gradient of the
> loss over all the data held by these clients. Thus, C controls the
> global batch size, with C = 1 corresponding to full-batch
> (non-stochastic) gradient descent. We refer to this baseline
> algorithm as FederatedSGD (or FedSGD).

## Zhong et al., "Semantic Evaluation for Text-to-SQL with Distilled Test Suites", EMNLP 2020, Section 1

> However, evaluating the semantic accuracy of a Text-to-SQL model is a
> long-standing problem: we want to know whether the predicted SQL
> query has the same denotation as the gold for every possible
> database. "Single" denotation evaluation executes the predicted SQL
> query on one database and compares its denotation with that of the
> gold. It might create false positives, where a semantically different
> prediction (Figure [n] prediction 1) happens to have the same
> denotation as the gold, on a particular database. In contrast, exact
> string match might produce false negatives: Figure [n] prediction 2 is
> semantically equivalent to the gold but differs in logical form.
