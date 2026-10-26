# Limitations and negative findings

1. Toy-game equilibrium verification does not solve NLHE. Game variants, betting abstractions and player counts matter.
2. Complete-state neural fitting is a capacity diagnostic, not unseen-state, unseen-opponent or online-learning success. Several neural regret/average-strategy gates failed despite favorable prediction losses.
3. Exact reproduction of a weak strategy mixture preserves its weakness. It does not demonstrate successful strategic improvement dynamics.
4. v2.1 gains are relative to a conservative neural engineering reference against a finite scripted population. The strong result is a controlled within-simulator improvement, not human-level strength or real-money profitability.
5. More aggressive play increased full-stack and large-pot losses. The published finite-sample guards do not bound future bankroll risk or rare tails.
6. The PPO budget was deliberately small: 3,072 hands across two seeds. It did not establish a stronger learned neural policy. This does not prove PPO cannot work at a different justified budget/design.
7. Historical human hand histories may be convenience samples, overlap across distributions and reveal private cards only selectively. Showdown records are selection-biased; unknown folded cards remain unknown.
8. Public betting predictors cannot identify what a human would do after a different action that never occurred. Simulator calibration is not causal human-response identification.
9. Full NLHE reproduction is intentionally unavailable here: private weights, complete integration and raw local traces are excluded. Public aggregate statistics permit checking reported interval arithmetic, not independently rerunning the full benchmark.
10. Public source has no approved general reuse license. Referenced datasets/dependencies retain their own licenses and terms.

No real players or third-party gambling services are controlled by this repository. A future consented play-money Arena would require separate privacy, access and experimental-design work.
