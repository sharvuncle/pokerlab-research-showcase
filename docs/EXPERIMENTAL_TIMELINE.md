# Experimental timeline

- **Early prototypes:** simplified-simulator imitation/RL and public-behavior priors exposed the difference between winning against known scripts and general poker strength. Historical returns from different engines were never treated as comparable.
- **Public-data opponent modeling:** a bounded PHH/HandHQ subset supported calibrated public-action prediction. Better prediction did not reliably translate into a stronger poker policy. Historical player/session overlap and already consumed holdouts constrain future generalization claims.
- **v1.4–v1.7:** pinned PokerKit rules, independent side-pot/payout checks, persistent identities, teacher/student investigations and contextual opponent probes. The selected neural engineering reference remained preserved.
- **v1.8:** independently verified tabular Kuhn and Leduc CFR across three seeds. Neural behavioral cloning/regret regression failed the strategic gate, so NLHE transfer was skipped.
- **v1.9:** exact own-reach average reconstruction and an all-state neural capacity diagnostic succeeded. Missing-state generalization and the bounded online reservoir learner failed.
- **v2.0:** separated full-stream, reservoir, neural-advantage and average-fitting errors. Policy-preserving target normalization and direct average fitting improved reconstruction; corrected online learning still failed promotion. No larger model or NLHE transfer was forced.
- **v2.1:** diagnosed excessive preflop passivity, froze a position-aware aggression overlay and measured supported overall/six-player chip gains with increased loss risk. A small population-PPO experiment did not establish a stronger neural agent.
- **Current public milestone:** a reviewed, independently runnable reduced-game example and derived aggregate research presentation. Future human-informed research must preserve licensing, actor information boundaries and independent evaluation.

The timeline records both successful checks and rejected candidates. No unsuccessful neural run is omitted to imply uninterrupted progress.
