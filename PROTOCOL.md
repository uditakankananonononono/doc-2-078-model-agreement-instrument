# DOC-2-078 "Model agreement as a scientific instrument": on new protein families, does agreement between two differently-featured models flag correct predictions better than the main model's own confidence? (frozen protocol, lock-1)

Written 2026-10-09 IST and committed BEFORE the external set was sampled or embedded.

## Why this is not a re-ask
- DOC-2-073/077/009-R3/009-R4 (four ESM-2 rho-by-features negatives) asked whether zero-shot variant-effect rho varies with protein or assay features. Not touched here.
- DOC-2-072 asked how much a random split inflates family-level function prediction (registered LEAKAGE-CONFIRMED; wording: FAMILY-SHORTCUT CONFIRMED, not a benchmark estimate). This protocol asks a different thing: reliability flagging on held-out families.
- Prior art: disagreement/ensemble-agreement as an uncertainty signal is standard in ML. No novelty claimed; this tests whether it works here under frozen gates and whether it adds beyond the model's own confidence.

## Data (frozen)
- Train: the DOC-2-072 dataset (250 Pfam families x 20, 7 EC level-1 classes, UniProt 2026_03) and its ESM-2 35M embeddings, as produced there (repo doc-2-072-family-split-leakage; md5s in its input_md5.txt: dataset.tsv 122c632550b21d9ef26d4410ce6f8ebb, emb.npy 3e3388cba29c4f3b0765bc0bc29fb7e9).
- External: 250 NEW Pfam families, disjoint from the train families, sampled by sample_ext.py from the same frozen raw TSV (uniprot_raw.tsv md5 aa086b6e99d5e84c44789b1a85bc71f1; no new download), same filters as 072, seed 54321, 20 proteins per family.
- Features E (ESM-2 35M mean-pooled, embed.py identical to DOC-2-072's, md5 8437eda4de9a3e4c05a98684e6cb9623) and C (20 AA frequencies + log length).

## Method
- Fit E-model and C-model (standardize + logistic regression, C=1, balanced) on train only. No tuning, no external labels used for fitting the classifiers.
- On external proteins: correct = (E-model prediction == EC level-1 label); conf = E-model max predicted probability; agree = (E prediction == C prediction).
- Scores for correctness: agree; conf; and out-of-fold logistic combinations fit on the external set with family-held-out folds (families sorted, assigned round-robin to 5 folds): conf only, conf + agree, conf + predicted class (descriptive).
- Metric: AUROC for predicting correct. CI: family-cluster bootstrap over external families, 2,000 resamples, seed 12345, percentile 95%.

## Gates
- G1 (control): E-model external macro-F1 > 1/7 + 0.05 (the model works at all on new families) AND AUROC of agree against permuted correctness within 0.05 of 0.5. If it fails the result is INVALID, a protocol stop.
- G2: AUROC(agree) >= 0.60 and CI lower bound > 0.55.
- G3: AUROC(conf + agree, OOF) minus AUROC(conf only, OOF) >= +0.02 and CI lower bound > 0.
- Label (mechanical): INVALID if G1 fails; AGREEMENT-ADDS if G2 and G3 pass; AGREEMENT-INFORMATIVE-BUT-REDUNDANT if G2 passes and G3 fails; HONEST NEGATIVE if G2 fails.

## Limits stated up front
- The builder has seen DOC-2-072's aggregate results (E family-split macro-F1 0.371, C 0.223), so G1's first clause is expected to pass; it is a control, not a surprise.
- C is a weak model (about 0.22 macro-F1 on held-out families). Agreement with a weak model may partly reflect predicted-class priors (both models favour frequent classes). The predicted-class combination is reported descriptively and cannot change the label.
- Pfam clan leakage between train and external families is not measured; external families are disjoint by Pfam id only, so performance may be inflated by shared clans, which would also change the agree/conf relations.
- One model size, one coarse label, one train set; no claim about other models or tasks. CPU only. No simulated data in results. Smoke test of analysis_078.py was on synthetic random embeddings only (no record saved).
- Single run; crash fixes are dated AMENDMENT-N.md files committed before outcomes exist.
