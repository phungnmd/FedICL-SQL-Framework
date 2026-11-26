# Related work

## Li et al., FedProx, MLSys 2020, Section 2

> Recent optimization methods have been proposed that are tailored to
> the specific challenges in the federated setting. These methods have
> shown significant improvements over traditional distributed
> approaches such as ADMM [ref] or mini-batch methods [ref] by allowing
> both for inexact local updating in order to balance communication vs.
> computation in large networks, and for a small subset of devices to
> be active at any communication round [ref]. For example, Smith et al.
> (2017) propose a communication-efficient primal-dual optimization
> method that learns separate but related models for each device
> through a multi-task learning framework. Despite the theoretical
> guarantees and practical efficiency of the proposed method, such an
> approach is not generalizable to non-convex problems, e.g., deep
> learning, where strong duality is no longer guaranteed. In the
> non-convex setting, Federated Averaging (FedAvg), a heuristic method
> based on averaging local Stochastic Gradient Descent (SGD) updates in
> the primal, has instead been shown to work well empirically [ref].
>
> [...] Although some recent works [ref] have explored convergence
> guarantees in statistically heterogeneous settings, they make the
> limiting assumption that all devices participate in each round of
> communication, which is often infeasible in realistic federated
> networks [ref]. Further, they rely on specific solvers to be used on
> each device (either SGD or GD), as compared to the solver-agnostic
> framework proposed herein [...]
