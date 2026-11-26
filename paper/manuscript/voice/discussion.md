# Discussion and limitations

## Rafailov et al., DPO, NeurIPS 2023, Section 7

> **Limitations & Future Work.** Our results raise several important
> questions for future work. How does the DPO policy generalize out of
> distribution, compared with learning from an explicit reward
> function? Our initial results suggest that DPO policies can
> generalize similarly to PPO-based models, but more comprehensive
> study is needed. For example, can training with self-labeling from
> the DPO policy similarly make effective use of unlabeled prompts? On
> another front, how does reward over-optimization manifest in the
> direct preference optimization setting, and is the slight decrease in
> performance in Figure [n]-right an instance of it? Additionally, while
> we evaluate models up to 6B parameters, exploration of scaling DPO to
> state-of-the-art models orders of magnitude larger is an exciting
> direction for future work. [...]
