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
- Under this frozen design, agreement between the ESM-2 model and the composition model carries no information about whether the ESM-2 prediction is right on new Pfam families (AUROC 0.489, about chance, CI includes 0.5). The model's own confidence is moderately informative (AUROC 0.677), and agreement adds nothing to it.
- This does not show that model agreement is useless in general. The C-model is weak (macro-F1 0.202, near chance 0.143 plus a little) and agrees with E only 27% of the time; a stronger or more independent second model might behave differently. Not tested.
- The descriptive predicted-class combination (0.730 vs 0.672) suggests which class E predicts carries more information about correctness than confidence alone. This is descriptive only, not a registered result.
- External families are disjoint by Pfam id only; clan-level overlap with train families is not measured.
- E external macro-F1 0.436 is higher than DOC-2-072's 5-fold family-split 0.371. The two runs use different samples and training size (full 5,000 vs 4/5), so they are not directly comparable; no inference drawn.

## Disclosures
- The builder had seen DOC-2-072's aggregate results before locking (stated in PROTOCOL.md).
- Run once. analysis_078.py md5 cec7baf0f9d742dba6e001cbbd0c2d86 equals the lock-1 file. tag_tree_check.txt records the lock-1 tag tree (4 files). Run log run_log.txt: UTC 16:44:52-16:45:07, exit 0, python 3.10.12, numpy 2.2.6, pandas 2.3.3, sklearn 1.7.2, torch 2.14.1+cpu, transformers 5.19.0. embed.py ran as locked (embed.log); no amendments were needed.
- "Smoke test on synthetic data" is a builder statement; no record saved. Synthetic noise gave INVALID, as expected.
- Single seed, single model size, single coarse label.
- Large files (ext_dataset.tsv, ext_emb.npy) are on Drive only; md5s in input_md5.txt. dataset.tsv, emb.npy and the raw TSV are in the DOC-2-072 Drive folder (1R5vBpk5lbF_IRwT0OZNY6rzNrN2JzvF1).
