# FedLS-SQL figure sources

`fedls_sql_architecture.svg` is the canonical editable source for the Method
architecture/privacy-boundary figure.

Suggested caption:

> **Figure 1. FedLS-SQL architecture and data-isolation boundary.** A frozen
> server LLM constructs a teacher-specific execution-verified public pool.
> During each round, clients train only SLM LoRA adapters on private NL-to-SQL
> rows, the server performs sample-weighted factor-wise FedAvg, and the
> aggregated SLM is refined using public teacher-target CE plus auxiliary
> reverse KL. Only LoRA tensors cross the client/server boundary; deployment
> uses the final SLM adapter without the teacher or public pool. This is a
> structural data-locality design, not a formal privacy guarantee.

The figure deliberately separates:

- the one-time public target-construction path;
- the recurring private-client/federated round;
- server-only LLM-to-SLM transfer;
- SLM-only deployment;
- structural locality from formal privacy.

Do not add raw-data arrows across the client/server boundary or depict the LLM
as a client/deployment component. Export to PDF at manuscript packaging time to
preserve vector text and lines.

