# DOC-2-078 RESULTS - review pending (independent gate has not cleared; no claim is final)

Label (set mechanically by analysis_078.py): **HONEST NEGATIVE**. G1 pass, G2 fail, G3 fail.

| item | value |
|---|---|
| train | DOC-2-072 dataset, 5,000 proteins, 250 families (md5s in input_md5.txt) |
| external | 5,000 proteins, 250 NEW Pfam families (disjoint, asserted in code), same UniProt 2026_03 raw file, seed 54321 |
| E-model external macro-F1 / accuracy | 0.436 / 0.480 (C-model macro-F1 0.202) |
| G1 control | pass: E macro-F1 0.436 > 0.193; permuted-correctness AUROC of agree 0.499 |
| agree rate (E pred == C pred) | 0.266 |
| AUROC for predicting E-correct: agree | 0.489, 95% family-bootstrap CI [0.460, 0.519] - G2 needed >= 0.60 and CI lb > 0.55: fail |
| AUROC: E confidence (max prob) | 0.677 |
| AUROC OOF: conf only / conf + agree | 0.672 / 0.675; delta +0.002, CI [-0.005, +0.009] - G3 needed >= +0.02 and CI lb > 0: fail |
| AUROC OOF: conf + predicted class (descriptive, cannot change label) | 0.730 |

## What this shows and does not show
- A single binary agreement score between the ESM-2 model and this weak, balanced-weight composition model carries no detectable information about whether the ESM-2 prediction is right on new Pfam families (AUROC 0.489, 95% CI [0.460, 0.519]; the point estimate is slightly below 0.5). "No information" is not claimed: the CI upper bound is 0.52. The model's own confidence is moderately informative (AUROC 0.677) and adding agreement did not meet the +0.02 gain gate (G3 delta +0.002, CI [-0.005, +0.009]; the point gain is not exactly zero and the CI upper bound reaches +0.009).
- This does not show that model agreement is useless in general. Two specific reasons: the second model is weak (macro-F1 0.202) and class-balanced; and only one agreement definition (hard argmax equality) was tested. Soft agreement (probability distance) and a stronger second model are untested.
- Structural reading (exploratory; reproduced by the independent verifier in the declared sklearn 1.7.2 environment): P(E correct | agree) = 0.4586 (n = 1,328 of 5,000, agree rate 0.2656), P(E correct | disagree) = 0.4877. The 0.488 figure in an earlier version of this file is P(correct | disagree), not the base rate and not an AUROC; overall E accuracy (base rate) is 0.480. E predicts class 2 or 3 for 58.2% of proteins; this does not by itself show that predictions follow class priors, and the balanced C-model spreads its predictions more evenly, so a mechanism of the form "agreement mostly means C landed on E's class" is a hypothesis, not tested.
- Per-predicted-class AUROC of binary agreement for E-correct (verifier, declared environment; descriptive, post-hoc, 7 looks, no class-specific CIs or multiplicity control): class 1 0.453 (n 662), class 2 0.511 (n 1455), class 3 0.451 (n 1455), class 4 0.467 (n 652), class 5 0.497 (n 512), class 6 0.500 (n 91), class 7 0.699 (n 173). Agreement sits at or below chance within every E-predicted class except class 7 (about 0.68 to 0.70, n about 173). Exploratory only.
- Gate-derived rerun figures (n agreeing 1,333; P(correct|agree) 0.460; P(correct|disagree) 0.486; class 7 about 0.683) come from a sklearn 1.9.1 / numpy 2.5.3 stack and are environment-dependent: the gate attributes the difference to 5 near-tied argmax predictions flipping. The declared-environment numbers above are canonical. G1 pass, G2 fail and G3 fail reproduce in both environments.
- The descriptive conf + predicted-class combination (OOF AUROC 0.730 vs 0.672) is exploratory only and cannot change the label (PROTOCOL.md). It indicates that E's per-class accuracy differs. It does not show that predicted-class identity is a useful confidence signal on new data: its OOF folds are fit on the same external set and it was not checked on held-out data.
- External families are disjoint from train families by Pfam id only; clan-level overlap is not measured.
- E external macro-F1 0.436 is not comparable to DOC-2-072's 0.371 (different samples, full vs 4/5 training); no inference drawn.
- Power was not formally assessed. The G2 CI [0.460, 0.519] excludes the registered 0.60 threshold by a wide margin, but this is not an equivalence or absence-of-effect test.

## Verification scope (independent verifier)
- Embeddings were supplied and hash-verified, not regenerated. The bootstrap is conditional on the existing out-of-fold predictions. Lock ancestry (tag precedes the run) is not proof that no earlier scoring happened.
- Verdict: SCOPED PASS. All registered numbers reproduced exactly in the declared environment.

## Disclosures
- The builder had seen DOC-2-072's aggregate results before locking (stated in PROTOCOL.md).
- Run once. analysis_078.py md5 cec7baf0f9d742dba6e001cbbd0c2d86 equals the lock-1 file. tag_tree_check.txt records the lock-1 tag tree (4 files). Run log run_log.txt: UTC 16:44:52-16:45:07, exit 0, python 3.10.12, numpy 2.2.6, pandas 2.3.3, sklearn 1.7.2, torch 2.14.1+cpu, transformers 5.19.0. embed.py ran as locked (embed.log); no amendments were needed.
- "Smoke test on synthetic data" is a builder statement; no record saved. Synthetic noise gave INVALID, as expected.
- Single seed, single model size, single coarse label.
- Large files (ext_dataset.tsv, ext_emb.npy) are on Drive only; md5s in input_md5.txt. dataset.tsv, emb.npy and the raw TSV are in the DOC-2-072 Drive folder (1R5vBpk5lbF_IRwT0OZNY6rzNrN2JzvF1).
