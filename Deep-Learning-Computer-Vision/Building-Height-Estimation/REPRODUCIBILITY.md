# Building Height Estimation: reproduction and evidence

**Team:** Azaan Imran and Muhammad Ibrahim (Group 31), established by the original accompanying presentation. Original notebook filenames retain authorship cues. The archive's eight notebooks, three output images and README are retained; the report and presentation found alongside the supplied local folder are preserved under `course-deliverables/`. No training weights or raw dataset were present in the selected archive outside its embedded Git database, which is excluded.

## Experiment progression

| Original notebook | Role and saved output |
|---|---|
| `Dataset/Dataset.ipynb` | RGB/SAR/DSM inspection, merging and preparation |
| `Baseline/Baseline_Model.ipynb` | RGB, ResNet/PSP, sigmoid, DSM divided by 184; normalized RMSE 0.0312 / MAE 0.0182 |
| `Improvement 1/Improvement_1.ipynb` | RGB+SAR, ASPP/DeepLab-style model, ReLU and SmoothL1; RMSE 6.0782 m / MAE 2.5996 m; delta 0.5174 / 0.5381 / 0.5527 |
| `Improvement 2/Improvement_2.ipynb` | Log-normalized SAR/DSM, auxiliary height-bin head plus regression; RMSE 6.8623 m / MAE 3.4793 m; delta 0.6440 / 0.6885 / 0.7251 |
| `Experiments/dl-proj-improvement1 (1).ipynb` | Sigmoid alternative; saved RMSE 0.0474 / MAE 0.0289 and delta 0.0565 / 0.0822 / 0.1092; do not compare without checking its scaling |
| `Experiments/Log_improvement_ibrahim.ipynb` | Log-normalized regression-only variant; RMSE 6.3394 / MAE 2.7256; delta 0.5656 / 0.6252 / 0.6632 |
| `Experiments/ibrahim-building-height-log-normalized-dsn-simple.ipynb` | Softplus experiment; two saved evaluation cells report 9.4269 / 4.4952 and 7.1957 / 3.5839; keep both, not one cherry-picked result |
| `Experiments/hgdnet-copy-azaan-outputs.ipynb` | ConvNeXt/UPerNet-inspired dual-decoder experiment; RMSE 7.9646 / MAE 3.7871; README identifies missing inverse log transform in delta evaluation |

Numbers were checked against original saved output cells, not recreated by training. Baseline rescaling gives **5.7408 m RMSE and 3.3488 m MAE** from the rounded saved values; the original README's 3.34 m is an approximation. Improvement 2 improves the recorded delta scores over Improvement 1 while worsening RMSE and MAE. Batch-averaged RMSE and pixel weighting/split differences limit comparisons; these are not official contest leaderboard results. Historical notebook outputs remain intact after path edits.

## Data and environment

The project uses **DFC 2023 Track 2** optical/SAR data and reference nDSM, rather than the earlier DFC 2018 exploration in the literature presentation. Obtain authorized data through the [official contest](https://www.grss-ieee.org/community/technical-committees/2023-ieee-grss-data-fusion-contest/) and follow its access/usage terms. Expected layout: `track2/train/rgb/`, `track2/train/sar/`, `track2/train/dsm/`. Filenames must align as expected by each notebook. The original exact split files/checkpoints were not supplied; code generates split lists, so a fresh run need not reproduce the historical run.

Suggested environment (not claimed to be an exact historical lock): Python 3.12, PyTorch/torchvision, NumPy, OpenCV, matplotlib, rasterio, GDAL, tqdm, Jupyter; experimental ConvNeXt notebooks also use timm. GDAL must be installed with matching native libraries, for example through a conda-forge environment. Install the additional Python packages from `requirements.txt` after obtaining GDAL.

Set **absolute paths** before starting Jupyter:

```powershell
$env:DFC_DATA_ROOT='D:\datasets\track2'
$env:DFC_WORK_ROOT='D:\experiments\height-baseline'
python -m jupyter lab
```

Run `Dataset` for inspection, then the desired Baseline/Improvement notebook top-to-bottom. Each begins with a portable configuration cell. Use a **different work directory per notebook**: preprocessing writes merged images, converted DSM arrays, split lists and model checkpoints. Do not point the work directory at your original dataset. Original `/kaggle/input/.../track2` and `/kaggle/working/...` literals now use those two variables; algorithms, training loops and saved result/image outputs were preserved.

## Attribution and limitations

The baseline is adapted from [AICyberTeam/DFC2023-baseline](https://github.com/AICyberTeam/DFC2023-baseline); the later work is inspired by [HGDNet](https://arxiv.org/abs/2308.05387). Preserve upstream credit; the inspected baseline repository did not expose a top-level license grant, so no new blanket software/data license is asserted. Consult upstream owners before broader relicensing or reuse. Dataset rights remain with their providers. The accompanying course report/presentation are early literature-review material, not final experimental evidence.

GPU training, the original geospatial environment and dataset-based predictions were not rerun during consolidation. See repository verification for static and extracted-function checks. The three original PNGs show actual historical RGB/ground-truth/prediction comparisons and are not newly generated demonstrations.
