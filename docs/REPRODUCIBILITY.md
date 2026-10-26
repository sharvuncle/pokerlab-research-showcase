# Reproducibility

## Included and independently runnable

Python 3.11; tested NumPy 2.4.6, SciPy 1.17.1 and pytest 9.1.1. Install `requirements.txt`, then `python -m pip install --no-deps -e .`. Run `python -m pytest`. Nine tests cover exact known fixtures, analytic equilibria, independent tree/LP/catalog evaluation, regret derivatives, bounded learning and interval arithmetic.

`python -m pokerlab_showcase.demo --game both --iterations 2000 --seeds 1807` is a small CPU demonstration. For the recorded convergence budget, use 20000 iterations with seeds 1807,1829,1843. The explicit game variant, solver and seed initialization are included; minor numerical differences can depend on library/solver versions. Outputs are JSON metrics only. Existing output files are never silently overwritten.

At 20000 iterations, expected Kuhn NashConv is approximately .00321–.00327; expected Leduc is .01410–.01547. Uniform-policy NashConv fixtures are 11/12 and 4.747222222222222 respectively. Kuhn equilibrium value is -1/18; the stated Leduc variant's LP value is approximately -.085606424078.

## Reviewed evidence, not full NLHE reproduction

`examples/published_results.json` includes real recorded convergence points, aggregate v2.1 returns/risks and all ten global block differences. The statistical test recomputes each t95 interval from those differences. This verifies the presentation arithmetic; it does not independently establish the original simulation outcomes.

Excluded: neural weights/optimizers, full NLHE environment integration, historical hand files, detailed public/private action traces, local authentication/configuration, internal debugging files, LFS objects and private Git history. Therefore this repository cannot independently rerun the full v2.1 NLHE experiment. The public solver and its tests require none of those exclusions.

Figures are derived from the reviewed aggregate fixture. Future research updates must add separately reviewed summaries; they must not silently replace frozen historical receipts.
