# Methodology

## Reduced-game mathematical verification

Kuhn uses three ranks, one private card each, ante 1 and one betting round with bet 1 and at most one bet. The equilibrium value for player0 is -1/18. Leduc uses two cards per rank, one private card each, one public board card, ante 1, bet 2/4 and at most two total bets per round; a pair beats high card. Both players retain their full public action history.

Each CFR iteration freezes the strategy before simultaneous player updates. Counterfactual regret increments weight chance and opponent reach; own reach is excluded. Average strategy uses own reach. Positive cumulative regrets are normalized over legal actions; no positive regret gives a uniform legal fallback. The final regret-matched strategy is not interchangeable with the average strategy.

NashConv is the sum of both unilateral best-response improvements, equal to BR0+BR1 in this zero-sum convention. Exploitability is NashConv/2, in ante chips per hand. Tree evaluation, sequence-form linear programs and independent terminal enumeration are checked numerically. No LP solution is used as a training target for the tabular CFR runs.

## NLHE empirical evaluation

The v2.1 comparison used the same corrected PokerKit engine for both policies, all five table sizes, equal/unequal stacks, rotated identities/seats and matched initial deals/opponent RNG seeds. Each hand resets stacks; this is not a bankroll-survival or tournament experiment. Eleven controlled opponent categories included compatible older policies and separately implemented tactical opponents.

The primary difference is the macro mean across table/stack/opponent cells within each of ten independent global seed blocks. A two-sided Student-t95 interval is computed across those ten block differences. Hands and decisions are not used as independent samples for that interval. Higher PFR is a behavioral outcome, not an optimization reward or success criterion.

Promotion required supported overall and six-player gains, fixed opponent/table-size regression guards, controlled stack/large-loss rates and zero correctness failures. The reserved historical final test remained unopened. Pressure-opponent subgroup means were positive but individually uncertain.

## Information and data boundaries

The actor sees its own cards, current public board, legal actions/sizes, public commitments/history and observed player behavior. Opponent hidden cards and future board cards never enter policy features. Actual terminal showdown reveals are distinct from unknown folded cards. Public-action prediction is not a counterfactual response model.

PPO records actual masked sampling probabilities. Deterministic rule-overlay actions must not be assigned fictitious neural PPO likelihoods. Environment rewards are terminal net chips; there are no unconditional betting/raising bonuses. Train/evaluation sessions and deal namespaces are separated, and known consumed historical holdouts are not renamed fresh tests.
