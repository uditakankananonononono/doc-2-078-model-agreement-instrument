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
- A single binary agreement score between the ESM-2 model and this weak, balanced-weight composition model carries no detectable information about whether the ESM-2 prediction is right on new Pfam families (AUROC 0.489, 95% CI [0.460, 0.519]; the point estimate is slightly below 0.5). "No information" is not claimed: the CI upper bound is 0.52. The model's own confidence is moderately informative (AUROC 0.677) and agreement adds nothing to it (G3 delta +0.002).
- This does not show that model agreement is useless in general. Two specific reasons: the second model is weak (macro-F1 0.202) and class-balanced; and only one agreement definition (hard argmax equality) was tested. Soft agreement (probability distance) and a stronger second model are untested.
- Structural reading (exploratory, my recomputation from the run inputs): P(E correct | agree) = 0.459 (n = 1,328), P(E correct | disagree) = 0.488, so agreement is marginally anti-informative. E predicts class 2 or 3 for 58% of proteins (follows class priors), while the balanced C-model spreads predictions near-uniformly, so agreement mostly means "C landed on E's class", which is unrelated to correctness. The independent gate reported 1,333 agreeing, 0.460 vs 0.486 and per-class agree AUROCs (class 6 about 0.68 on n = 91, others about 0.45 to 0.51); these are gate-derived, from a rerun with sklearn 1.9.1, and I did not reproduce the per-class figures.
- The descriptive conf + predicted-class combination (OOF AUROC 0.730 vs 0.672) is exploratory only and cannot change the label (PROTOCOL.md). It indicates that E's per-class accuracy differs. It does not show that predicted-class identity is a useful confidence signal on new data: its OOF folds are fit on the same external set and it was not checked on held-out data.
- External families are disjoint from train families by Pfam id only; clan-level overlap is not measured.
- E external macro-F1 0.436 is not comparable to DOC-2-072's 0.371 (different samples, full vs 4/5 training); no inference drawn.
- G2 power: with 1,328 agreeing proteins and a CI half-width of about 0.03, an AUROC of 0.60 would have been detected (gate-stated).

## Disclosures
- The builder had seen DOC-2-072's aggregate results before locking (stated in PROTOCOL.md).
- Run once. analysis_078.py md5 cec7baf0f9d742dba6e001cbbd0c2d86 equals the lock-1 file. tag_tree_check.txt records the lock-1 tag tree (4 files). Run log run_log.txt: UTC 16:44:52-16:45:07, exit 0, python 3.10.12, numpy 2.2.6, pandas 2.3.3, sklearn 1.7.2, torch 2.14.1+cpu, transformers 5.19.0. embed.py ran as locked (embed.log); no amendments were needed.
- "Smoke test on synthetic data" is a builder statement; no record saved. Synthetic noise gave INVALID, as expected.
- Single seed, single model size, single coarse label.
- Large files (ext_dataset.tsv, ext_emb.npy) are on Drive only; md5s in input_md5.txt. dataset.tsv, emb.npy and the raw TSV are in the DOC-2-072 Drive folder (1R5vBpk5lbF_IRwT0OZNY6rzNrN2JzvF1).
