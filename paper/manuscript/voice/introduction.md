# Introductions

## Hu et al., "LoRA: Low-Rank Adaptation of Large Language Models", ICLR 2022, Section 1

> Many applications in natural language processing rely on adapting
> one large-scale, pre-trained language model to multiple downstream
> applications. Such adaptation is usually done via fine-tuning, which
> updates all the parameters of the pre-trained model. The major
> downside of fine-tuning is that the new model contains as many
> parameters as in the original model. As larger models are trained
> every few months, this changes from a mere "inconvenience" for GPT-2
> [ref] or RoBERTa large [ref] to a critical deployment challenge for
> GPT-3 [ref] with 175 billion trainable parameters.
>
> Many sought to mitigate this by adapting only some parameters or
> learning external modules for new tasks. This way, we only need to
> store and load a small number of task-specific parameters in addition
> to the pre-trained model for each task, greatly boosting the
> operational efficiency when deployed. However, existing techniques
> often introduce inference latency [ref] by extending model depth or
> reduce the model's usable sequence length [ref] (Section 3). More
> importantly, these method often fail to match the fine-tuning
> baselines, posing a trade-off between efficiency and model quality.
>
> We take inspiration from [ref] which show that the learned
> over-parametrized models in fact reside on a low intrinsic dimension.
> We hypothesize that the change in weights during model adaptation
> also has a low "intrinsic rank", leading to our proposed Low-Rank
> Adaptation (LoRA) approach. [...]

## Li et al., "Federated Optimization in Heterogeneous Networks" (FedProx), MLSys 2020, Section 1

> While FedAvg has demonstrated empirical success in heterogeneous
> settings, it does not fully address the underlying challenges
> associated with heterogeneity. In the context of systems
> heterogeneity, FedAvg does not allow participating devices to perform
> variable amounts of local work based on their underlying systems
> constraints; instead it is common to simply drop devices that fail to
> compute E epochs within a specified time window [ref]. From a
> statistical perspective, FedAvg has been shown to diverge empirically
> in settings where the data is non-identically distributed across
> devices [ref]. [...]
>
> In this work, we propose FedProx, a federated optimization algorithm
> that addresses the challenges of heterogeneity both theoretically and
> empirically. A key insight we have in developing FedProx is that an
> interplay exists between systems and statistical heterogeneity in
> federated learning. [...] To mitigate this issue, we propose adding a
> proximal term to the objective that helps to improve the stability of
> the method. This term provides a principled way for the server to
> account for heterogeneity associated with partial information. [...]

## McMahan et al., "Communication-Efficient Learning of Deep Networks from Decentralized Data" (FedAvg), AISTATS 2017, Section 1

> We term our approach Federated Learning, since the learning task is
> solved by a loose federation of participating devices (which we refer
> to as clients) which are coordinated by a central server. Each client
> has a local training dataset which is never uploaded to the server.
> Instead, each client computes an update to the current global model
> maintained by the server, and only this update is communicated. [...]
>
> A principal advantage of this approach is the decoupling of model
> training from the need for direct access to the raw training data.
> Clearly, some trust of the server coordinating the training is still
> required. [...]
