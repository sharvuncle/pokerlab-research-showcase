# PokerLab v2.3 — Six-player diagnostics and full-simulator validation

**The v2.1 policy remains selected. No tactical correction or new learned policy was promoted.** This stage investigated actual six-player contexts rather than increasing general aggression, tested the complete guarded human-informed simulator, and prepared an in-memory contract for a future private play-money Arena.

## Tightness needs context

Cached six-player evaluation contained 1,920 dealt hands. The supported agent's VPIP was 6.35% and PFR 4.01%, but those rates alone do not identify errors. Button unopened raises were 15/62 opportunities and cutoff raises 12/98. Premium QQ+/AK hands were raised in all 16 qualifying unopened and all 18 legal three-bet opportunities. Other premium responses depend on price, stack depth and prior raises.

The earlier aggression extensions were especially rare at six players: six extra preflop decisions in six hands, and six extra postflop decisions in four hands. These are insufficient to infer a dependable performance improvement. Forced blinds, checks, voluntary participation, legal opportunities and repeat decisions were counted separately.

## Conditional tactical investigation

Nineteen cached contexts were selected by frozen hash-ranked strata: premium responses, late unopened folds, draws facing a price, river defense, checked value proxies and large pressure losses. Original hidden opponent cards and future runouts were excluded from the estimator. New unknown holdings and future boards were sampled under documented beliefs; the public prefix was reconstructed and alternatives continued on the corrected engine with actor-only observations.

Alternatives used common random worlds within an opponent assumption. Independent pot-control and range/strength-sensitive tactical assumptions were included alongside an explicitly experimental historical proxy. These are conditional continuation-policy estimates, not GTO action values or causal human-response evidence. The history tilt is a heuristic, and subsequent hero memory covers the current hand rather than the entire original session.

The study stopped with **5,088 completed alternative continuations in 41 of 57 planned node-assumption cells**. It remained incomplete. Its original implementation checked the time budget between whole batches, causing **1,512.30 seconds** of work against a 1,200-second stage cap. The overrun is disclosed; completed values were retained, no more continuations were launched, and finer deadline checks plus closed-study replay refusal were added. Conservative overall compute accounting remained below the separate 3,600-second version cap.

River facing-bet value raises and premium-hand responses are the leading hypotheses, with only one robust sampled context each under the two independent assumptions. Broad late-position expansion was model-dependent rather than consistently favorable. No class reached the prespecified repeated-exposure and robust-node requirements. A selected favorable example cannot establish overall improvement.

**No targeted candidate was implemented or independently tournament-tested.** There is consequently no new overall or six-player policy-performance delta to report. The unchanged selected policy must not be described as having passed a new zero-delta validation experiment. No PPO, large training run, self-play cycle or reserved final test was launched.

## Testing the actual guarded simulator

The previous public-action predictor is not the full simulator. This study reconstructed public historical before-action states and executed the unchanged actor-card-aware simulator, including legal masks, private-card adjustments, sizing noise, price/effective-stack guards and fallbacks.

A fixed sample used 96 accepted historical hands from each previously table-held-out partition: **586 validation decisions across 15 tables** and **595 test decisions across 18 tables**. Those partitions were already inspected in v2.2; they are not newly untouched human tests. Player pseudonyms overlap and are not asserted to be stable real identities.

Unknown historical cards remained unknown. A stated uniform latent-card belief was marginalized with 24 draws per style/decision and explicit probability smoothing; future reveals never supplied the actor's cards. These are approximate diagnostic probabilities, not an identified human range or exact full-policy likelihood.

On the same 595 test decisions:

- Preserved public predictor log loss: **0.69893**.
- Full neutral guarded marginal log loss: **0.73684**.
- Degradation: **+0.03791**, table-bootstrap 95% interval **[+0.01817, +0.05974]**; latent Monte Carlo uncertainty is not included.
- Maximum common-stratum action-distribution total variation: **0.310**, exceeding the frozen 0.10 criterion.
- The conditional sizing diagnostic passed its threshold, but action fidelity and human-range identification did not.

A separate **1,440-hand** free-running study exercised complete policies at every seat across 2–6 players, equal/unequal stacks and neutral/tight/calling profiles. Each style contributed 1,920 actor-hands. VPIP was 40.89%/36.30%/41.77%; PFR was 19.64%/18.65%/18.96%. These percentages encounter different states from historical play and are not direct human matches. Restricted N/street/facing reweighting covered only 60% of selected test decision mass, leaving substantial support and contextual limitations.

**The full human-simulator fidelity gate failed.** These policies remain experimental stress proxies. They cannot substantiate human playing strength or be the sole training population. Showdown-selection bias and unobserved counterfactual responses remain unresolved. No new dataset was downloaded or behavior model fitted.

## Arena handoff and preservation

All **288 private project tests passed**. Sampled continuations and free-running hands passed independent payout, chip-conservation, legality and uniqueness checks. All 178 pre-existing model/progress artifacts and 15 selected backups remain preserved; main and the reserved final test are unchanged.

A tested private in-memory scaffold supports frozen v1.4/v2.1 loading, owner-scoped cards, legal turn tokens, authoritative settlement, persistent positive stacks and explicit consent/provenance labels. The server application must still implement authentication, transport, storage, consent persistence, room lifecycle and busted-seat handling. **The agent/interface are ready for Arena development; a real human playtest is not yet available.** No website, live human data collection, third-party platform automation or payment feature was built.

The recommended next step is a first private play-money Arena with the frozen v2.1 agent, usability/correctness checks and an explicit consent/evaluation plan. Future human evaluation must remain separate from later training. Keep the tactical hypotheses for a better-powered, separately frozen study rather than force another aggression change.

This is a separately reviewed aggregate summary. Raw historical hands, identities, private actor traces, model weights, machine details and private Git history are excluded. The [public reduced-game example](REPRODUCIBILITY.md) remains runnable with nine tests; full NLHE studies are not reproducible from this showcase alone. The [source-visible rights notice](../NOTICE.md) is unchanged and grants no new broad reuse license.
