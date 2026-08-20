# ICL negative result

ICL is not part of the FedLS-SQL method. It is retained as a negative ablation
because it was evaluated under a matched federated protocol before the
2026-08-19 advisor decision.

## Decision-relevant evidence

- Client ICL training reduced the pre-server result by `2.90 EX` (`p=0.008`).
- Adding demonstrations at inference reduced EX by `3.87` (`p=0.003`) within
  the ICL-trained model.
- The matched endpoint difference was not significant.
- ICL training cost approximately `2.35x` the no-ICL client training time.
- Zero-shot teacher target generation outperformed tested teacher-side ICL.

Therefore the canonical protocol is:

```text
client train_k = 0
server k_teacher = 0
evaluation k = 0
```

Detailed reports, commands, emails, and screenshots are preserved under
`paper/archive/pre_fedls_2026-08/icl/` and `old_emails/`. Existing ICL code and
artifacts remain unchanged for reproducibility; no additional ICL experiment is
in the active queue.
