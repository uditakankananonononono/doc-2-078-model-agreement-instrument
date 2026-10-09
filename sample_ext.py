"""DOC-2-078: sample the external family set from the frozen DOC-2-072 raw UniProt TSV (md5 aa086b6e99d5e84c44789b1a85bc71f1). Writes ext_dataset.tsv."""
import hashlib, io, numpy as np, pandas as pd
raw = open("uniprot_raw.tsv").read(); assert hashlib.md5(raw.encode()).hexdigest() == "aa086b6e99d5e84c44789b1a85bc71f1", "raw md5 mismatch"
used = set(pd.read_csv("dataset.tsv", sep="\t").family)
d = pd.read_csv(io.StringIO(raw), sep="\t"); d.columns = ["accession", "ec", "pfam", "length", "sequence"]
d["pf"] = d.pfam.fillna("").str.strip(";").str.split(";"); d = d[d.pf.str.len() == 1].copy(); d["family"] = d.pf.str[0]
d["lab"] = d.ec.fillna("").str.split(";").apply(lambda l: {x.strip().split(".")[0] for x in l if x.strip()})
d = d[d.lab.apply(len) == 1].copy(); d["label"] = d.lab.apply(lambda s: int(next(iter(s))))
d = d[d.label.between(1, 7) & ~d.sequence.str.contains("[XBZUO]")].sort_values("accession")
cnt = d.family.value_counts(); fams = sorted(f for f in cnt[cnt >= 20].index if f not in used)
rng = np.random.default_rng(54321)
if len(fams) > 250: fams = sorted(rng.choice(fams, 250, replace=False))
out = []
for f in fams:
    g = d[d.family == f]; out.append(g.iloc[np.sort(rng.choice(len(g), 20, replace=False))])
o = pd.concat(out)[["accession", "family", "label", "length", "sequence"]]; o.to_csv("ext_dataset.tsv", sep="\t", index=False)
assert not (set(o.family) & used)
print("EXT_DONE families", len(fams), "n", len(o), "label_counts", o.label.value_counts().sort_index().to_dict())
