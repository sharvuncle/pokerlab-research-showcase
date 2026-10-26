# References and provenance

- Zinkevich, Johanson, Bowling and Piccione (2007), [Regret Minimization in Games with Incomplete Information](https://proceedings.neurips.cc/paper/2007/file/08d98638c6fcd194a4b1e6992063e944-Paper.pdf).
- Ross, Gordon and Bagnell (2011), [A Reduction of Imitation Learning and Structured Prediction to No-Regret Online Learning](https://proceedings.mlr.press/v15/ross11a.html).
- Brown et al. (2019), [Deep Counterfactual Regret Minimization](https://arxiv.org/abs/1811.00164). The private full-tree prototype was inspired by this work, not a claimed faithful reproduction of external-sampling Deep CFR.
- Schulman et al. (2017), [Proximal Policy Optimization Algorithms](https://arxiv.org/abs/1707.06347).
- [OpenSpiel](https://github.com/google-deepmind/open_spiel), for external game conventions and uniform-policy fixture values. No OpenSpiel source is vendored here.
- [PokerKit](https://github.com/uoftcprg/pokerkit), the separately licensed engine used in the full-NLHE research. The private adapter's corrections are described as engineering results, not distributed engine source here.
- [University of Toronto PHH collection](https://github.com/uoftcprg/phh-dataset) and its [upstream license](https://github.com/uoftcprg/phh-dataset/blob/main/LICENSE). Earlier private work used a bounded historical HandHQ-derived subset. Raw records, player IDs and prepared datasets are not distributed. Upstream's MIT notice does not become a license for this showcase or settle every underlying data-rights question.
- [NumPy license](https://numpy.org/doc/stable/license.html), [SciPy license](https://github.com/scipy/scipy/blob/main/LICENSE.txt), [pytest license](https://github.com/pytest-dev/pytest/blob/main/LICENSE). Dependencies are not vendored.

The finite-game source is original project implementation. Algorithm ideas and factual fixture values are attributed above. Aggregate numerical results are derived from completed project receipts; they are not copied benchmark claims about an external system. This showcase has an independent, newly initialized Git history.
