"""DOC-2-078 frozen analysis (PROTOCOL.md lock-1). Run once. Needs dataset.tsv, emb.npy (train, from DOC-2-072) and ext_dataset.tsv, ext_emb.npy."""
import json, numpy as np, pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.metrics import f1_score, roc_auc_score
rng = np.random.default_rng(12345)
tr = pd.read_csv("dataset.tsv", sep="\t"); Etr = np.load("emb.npy"); ex = pd.read_csv("ext_dataset.tsv", sep="\t"); Eex = np.load("ext_emb.npy")
assert not (set(tr.family) & set(ex.family))
AA = "ACDEFGHIKLMNPQRSTVWY"
comp = lambda d: np.array([[s.count(a) / len(s) for a in AA] + [np.log(len(s))] for s in d.sequence])
Ctr, Cex = comp(tr), comp(ex); ytr, yex, fam = tr.label.values, ex.label.values, ex.family.values
def clf(): return make_pipeline(StandardScaler(), LogisticRegression(C=1.0, max_iter=2000, class_weight="balanced"))
mE, mC = clf().fit(Etr, ytr), clf().fit(Ctr, ytr)
pE, pC = mE.predict_proba(Eex), mC.predict_proba(Cex); predE, predC = mE.classes_[pE.argmax(1)], mC.classes_[pC.argmax(1)]
correct = (predE == yex).astype(int); conf = pE.max(1); agree = (predE == predC).astype(float); n = len(ex)
mf = lambda yy, pp: f1_score(yy, pp, average="macro")
res = {"n_train": len(tr), "n_ext": n, "n_ext_families": len(set(fam)), "ext_label_counts": {int(k): int(v) for k, v in pd.Series(yex).value_counts().sort_index().items()}}
res["macroF1_ext"] = dict(E=mf(yex, predE), C=mf(yex, predC)); res["acc_E"] = float(correct.mean()); res["agree_rate"] = float(agree.mean())
uf = sorted(set(fam)); fold_of = {f: i % 5 for i, f in enumerate(uf)}; fid = np.array([fold_of[f] for f in fam])
def oof(X):
    s = np.zeros(n)
    for k in range(5):
        a, b = fid != k, fid == k; s[b] = LogisticRegression(C=1.0, max_iter=2000).fit(StandardScaler().fit(X[a]).transform(X[a]), correct[a]).decision_function(StandardScaler().fit(X[a]).transform(X[b]))
    return s
logit = np.log(conf / (1 - conf + 1e-9) + 1e-9)
s_conf, s_both = oof(logit[:, None]), oof(np.c_[logit, agree])
oh = pd.get_dummies(pd.Series(predE)).values.astype(float); s_cls = oof(np.c_[logit, oh])
A = lambda s, idx=slice(None): roc_auc_score(correct[idx], s[idx])
sc = {"agree": agree, "conf": conf, "conf_oof": s_conf, "conf_plus_agree_oof": s_both, "conf_plus_predclass_oof": s_cls}
res["AUROC"] = {k: A(v) for k, v in sc.items()}
yperm = rng.permutation(correct); res["G1_perm_AUROC_agree"] = float(roc_auc_score(yperm, agree))
members = {u: np.where(fam == u)[0] for u in uf}; bs = {"agree": [], "delta": []}
for _ in range(2000):
    idx = np.concatenate([members[u] for u in rng.choice(uf, len(uf))])
    if len(set(correct[idx])) < 2: continue
    bs["agree"].append(A(agree, idx)); bs["delta"].append(A(s_both, idx) - A(s_conf, idx))
ci = lambda k: [float(x) for x in np.percentile(bs[k], [2.5, 97.5])]
g1 = res["macroF1_ext"]["E"] > 1 / 7 + 0.05 and abs(res["G1_perm_AUROC_agree"] - 0.5) <= 0.05
res["G1"] = dict(E_macroF1_gt_chance_plus_0p05=bool(res["macroF1_ext"]["E"] > 1 / 7 + 0.05), perm_AUROC_within_0p05_of_half=bool(abs(res["G1_perm_AUROC_agree"] - 0.5) <= 0.05), pass_=bool(g1))
a = res["AUROC"]["agree"]; res["G2"] = dict(auroc=a, ci=ci("agree"), pass_=bool(a >= 0.60 and ci("agree")[0] > 0.55))
d = res["AUROC"]["conf_plus_agree_oof"] - res["AUROC"]["conf_oof"]; res["G3"] = dict(delta_auroc=d, ci=ci("delta"), pass_=bool(d >= 0.02 and ci("delta")[0] > 0))
res["LABEL"] = "INVALID" if not g1 else ("AGREEMENT-ADDS" if res["G2"]["pass_"] and res["G3"]["pass_"] else ("AGREEMENT-INFORMATIVE-BUT-REDUNDANT" if res["G2"]["pass_"] else "HONEST NEGATIVE"))
print("RESULT_JSON", json.dumps(res, default=float)); open("results.json", "w").write(json.dumps(res, default=float, indent=1))
