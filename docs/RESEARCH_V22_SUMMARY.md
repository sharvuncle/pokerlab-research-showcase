# PokerLab v2.2 — Human-informed modeling and controlled aggression

The public research showcase is now available independently of the private working repository. This stage audited historical poker data, tested a bounded new-table extension, and compared separate preflop and postflop aggression additions against the preserved v2.1 control. **Neither candidate qualified for promotion.** The supported experimental NLHE policy remains the v2.1 overlay over the unchanged v1.4 neural reference.

## Historical data and what the models learn

The [University of Toronto PHH collection](https://github.com/uoftcprg/phh-dataset) distributes anonymized historical HandHQ poker logs. PHH is the format and collection; mirrors are not independent human datasets. Existing strict preparation accepted 13,202 hands and 86,444 public betting decisions. Earlier validation/test partitions had already been consumed and were not relabeled as fresh data.

New fitting used 46,124 old TRAIN decisions; temperature and private-card tilt were chosen on 10,488 old calibration decisions. A bounded extension downloaded two pinned-revision files totaling 1,452,750 bytes. After excluding old table groups and quarantining invalid hands, 1,052 new accepted hands produced 6,783 decisions: 2,900 validation and 3,883 test decisions. Table groups and canonical hands are disjoint between prepared partitions. Actor pseudonyms overlap: validation and test share 23 labels, and globally stable human identities cannot be guaranteed. Unseen-label subset diagnostics were also retained privately.

Historical fold/check-call/bet-raise labels train an observational public-action classifier, not a teacher of optimal actions. A separate regressor learns observed raise increment relative to pot plus call. Unknown folded cards remain unknown; showdown cards are selection-biased and excluded from behavior features. Old source-private/post-hoc card entries are distinguished from explicit public reveals. The ambiguous legacy public-10k artifact could not be certified as a separate human-only dataset; the standard NLHE reference uses its aggregate priors rather than its contextual classifier.

The preserved neural reference instead comes from simulated teacher demonstrations and DAgger. Prior PPO experience consists of simulated terminal-chip rewards. The v2.2 playing traces are evaluation data, not policy-training examples. These three data roles are not interchangeable.

## Prediction and simulator fidelity

On the 3,883-decision new-table test partition:

- Preserved public-context predictor log loss: **0.73608**.
- New public-context model: **0.73509**.
- Difference: **−0.00098**, table-cluster bootstrap 95% interval **[−0.00417, +0.00162]**.
- Private-card-marginal proposal diagnostic: **0.74038**, worse than the public-only models.
- Observed-raise log-size MAE: **0.15328**, versus **0.17633** for the TRAIN-median baseline.

Simulated proxies combine these observational priors with their own actual cards, legal-action masks, price guards, residual sizing noise, fixed style variations and a fallback outside training support. Position-conditioned predictions, calibration, action/player-hand distributions, sizing and unseen-label diagnostics were inspected. **Credible full-policy human realism was not established.** The uniform unknown-card marginal is a diagnostic, not a reconstructed human range; legal/price guards alter the actual simulated policy. A small public-action prediction gain does not identify a human's response to an unobserved alternative bet. Results against these proxies must not be presented as results against humans.

## Frozen playing comparison

The final comparison includes **28,800 policy-hands**, covering 2–6 players, equal/unequal stacks, eight independent global seed blocks and five populations. Mixed rosters include previous PokerLab policies, tight/station/aggressive/bluff-heavy/switching agents, human-informed proxies and independent tactical opponents. Initial deals, hero placement, stacks and button match within candidate pairs; public identity memories persist within sessions and reset between sessions.

A is unchanged v2.1. B expands selected position-aware preflop openings and value three-bets. C adds bounded postflop value bets, strong-draw aggression and selectively conditioned continuation bets. An audit caught C borrowing a folded player's fold tendency; the original traces were preserved, and only C was rerun after a live-opponent lookup correction. A/B were reused without replay. Strategy thresholds and selection criteria were unchanged. The correction used the same paired seeds after partial trace inspection, so it is disclosed rather than described as pristine untouched validation.

Overall paired change versus A, in bb/100 (two-sided 97.5% block-t intervals, Bonferroni-adjusted for B/C):

- **B: −1.00 [−4.67, +2.67].**
- **Corrected C: +1.07 [−0.96, +3.09].**

Six-player paired changes (secondary 95% block-t intervals):

- **B: −0.65 [−3.25, +1.95].**
- **Corrected C: +3.33 [−2.60, +9.27].**

Against human-informed proxies, B changed chips by +4.27 [−3.47, +12.01] and C by +1.33 [−7.88, +10.53]. Against independent tactical opponents, B changed chips by +0.16 [−1.83, +2.15] and C by −1.07 [−4.34, +2.20]. These secondary 95% intervals are exploratory.

A/B/C overall PFR was 7.33%/7.86%/7.33%. Full-stack loss rates were 1.198%/1.208%/1.219%; losses of at least 10BB were 3.292%/3.344%/3.302%. Slightly more aggression did not establish chip improvement. Each extension intervened in only about 50 of 9,600 candidate hands, limiting power and strategic coverage. The frozen promotion gate required at least +5 bb/100, a positive adjusted lower bound, six-player/pressure safeguards and controlled loss risk. Neither passed.

## Selection, verification and reproducibility limits

Combined aggression requires B and C to qualify separately; reinforcement learning requires a qualified fixed candidate. Both gates stayed closed. **No v2.2 RL model was trained or promoted.** The v2.1 overlay, v1.4 reference, all 177 previous model/progress artifacts and 15 registered backups remain preserved. The reserved NLHE final test and private main branch remain unchanged.

All **280 private project tests passed**. The final-comparison hands passed independent payout, chip-conservation, legal-action and card-uniqueness checks; raw/source hashes and paired conditions were verified. Corrected C had zero live-profile violations. Original and corrected traces and negative findings were retained. The original run, C correction and smoke checks totaled 472.70 measured game-session seconds, below the prospective 1,800-second cap, on local CPU with one numerical thread. No paid compute or large new training run was launched.

The [public toy-game example](REPRODUCIBILITY.md) remains runnable with nine tests. This update publishes a reviewed derived summary, not raw historical hands, actor identities, model binaries, full traces or private repository history. Full v2.2 NLHE experiments cannot be reconstructed from this showcase alone. The repository's [source-visible rights notice](../NOTICE.md) remains unchanged; upstream dataset licensing does not grant a blanket license to this project.

The next useful study is a separately frozen diagnosis of rare intervention exposure and six-player/tactical action-value errors, followed by validation of the actual guarded human-informed simulator. More policy training is not yet justified. Future Arena work should retain separate actor-private observations, public events and actual showdown reveals, with consenting invited players on a private play-money server. Arena was not built in v2.2.
