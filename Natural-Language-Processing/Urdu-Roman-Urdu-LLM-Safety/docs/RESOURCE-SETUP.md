# External model and dataset setup

On 20 October 2026, all 22 objects listed in `../lfs-resources.json` returned working download endpoints and one-byte probes. They total 763,600,361 bytes including duplicated lexicon content; the mBERT weight is approximately 711 MB. Availability can change. No LFS pointers, corpora or trained binaries are committed to this consolidated project.

Install Git LFS separately. Clone the original repository outside Academic-Projects, pin the audited commit, then download only the inference resources. On PowerShell:

```powershell
$env:GIT_LFS_SKIP_SMUDGE='1'
git clone https://github.com/ahmad4376/Urdu_toxic_prompt_filter.git upstream-toxic-filter
git -C upstream-toxic-filter checkout ec6ee7a17e47105acce859c52d03a2a000353c86
Remove-Item Env:GIT_LFS_SKIP_SMUDGE
git -C upstream-toxic-filter lfs pull --include='models/mbert_toxic_final/*,data/ruhsold/hate_words_roman_urdu.txt' --exclude=''
```

From the consolidated NLP project, `python scripts/import_resources.py --source /absolute/path/to/upstream-toxic-filter` verifies SHA-256/size against the manifest and copies only the model directory and canonical lexicon into ignored local folders. Alternatively set `TOXIC_MODEL_DIR` and `TOXIC_LEXICON_PATH` to their absolute upstream paths; do not set these to empty strings. Keep these local assets out of commits.

For training/baseline reproduction, first review the dataset/base-model terms, then explicitly fetch `data/*,models/baseline/*` in the upstream clone and use `--training-data` with the import helper. This imports the manifest's training assets locally, never the duplicate `notebooks/data` copy. Both old notebook-local data copies and the nested YouTube ZIP duplicate are unnecessary for the runtime demo. Do not load joblib/pickle models from untrusted sources.

Run notebook kernels with `notebooks/` as their working directory. The original Kaggle training notebook now reads `TOXIC_CORPUS_PATH` (default `../data/all_combined.csv`) and writes `TOXIC_MODEL_OUTPUT_DIR` (default `../models/mbert_toxic_final`). The EDA download now writes the canonical `../data/rut/` rather than a redundant notebook-local copy. Other notebooks expect sibling project `data/`, `models/` and `reports/` directories. Training may need GPU resources and environment versions different from a current CPU-only demo installation.

A successful download/hash check only proves retrieval integrity. It does not certify model quality, dataset rights, or reproducibility of every historical metric.
