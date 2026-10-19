# Repository and project inventory

Audit date: **19 October 2026**. Seven public repositories were discoverable under `azaan-imran192`; the connected identity was verified. Private or inaccessible repositories cannot be certified by this inventory.

| Repository | Audit finding | Consolidation disposition |
|---|---|---|
| Academic-Projects | 32 commits; HCI materials, empty Urdu placeholder, Culinary placeholder; a deleted Culinary ZIP exists in history | Preserve history; relocate the complete unchanged HCI project; add categorized projects |
| Urdu-News-Articles | Four notebooks, four script exports, CSV, report, duplicate ZIP; machine-specific paths | Complete source/data/report imported once; paths fixed; ZIP omitted |
| plant-disease-classifier | Three notebooks, report, MIT license, ten LFS checkpoint pointers | Source/report imported; model references retained without binaries |
| plant-phenotyping-dashboard | 2,204 tracked files; backend/frontend, captured media, database, vendor trees and LFS weights; exposed configuration and commercial template | Sanitized authored backend imported; data/weights/vendor code excluded; frontend held |
| azaan-imran192 | Profile README says student/aspiring engineer and uses many remote image services | Audited; final redesign deferred until project work is ready |
| AnatoNamikaza | Profile-style repository with upstream author history | Inspiration only; no content imported |
| RB2-Android | Android/game-related upstream work, unrelated to requested academic portfolio | Audited at source/history inventory level; excluded |

## Shared project source

Only `CulinaryCloud_RecipeSharingPlatform` and `ScreenTimeand StudentLife` from `HanzalahSohail/Projects` were selected. The latter contains one notebook, a 202-response CSV, and an article URL. The shared root license has two MIT notices separated by merge markers; both notices are preserved and separators removed in imported copies. Bulk history does not establish exact individual contributions.

Voice AI Pipeline, MediQ, Tomato Leaf Classification, Movie Recommender, and other unrelated shared folders are excluded. No standalone LangChain/Agentic AI project is invented. CSaLT is deferred.

## Project readiness

| Category / project | Available | Remaining |
|---|---|---|
| [HCI / ParkinsonPal](../Human-Computer-Interaction/ParkinsonPal/) | All 30 original files and READMEs relocated unchanged | Named-quotation concern reported; any content change requires explicit approval |
| [ML / Urdu News](../Machine-Learning/Urdu-News-Classification/) | Code, notebooks, canonical CSV, report, runnable setup and reruns | Evaluation redesign for leakage-free benchmarking is future work |
| [Data Science / Mobile Usage](../Data-Science/Mobile-Usage-Analysis/) | Notebook, timestamp-free data, original article link, execution verification | Complete team roster/contribution detail; no causal claims |
| [Software Engineering / Culinary Cloud](../Software-Engineering/Culinary-Cloud/) | Frontend/backend source, dependencies, environment templates, build | Full team roster; independent service credentials and end-to-end integration validation |
| [CV / Plant Disease](../Deep-Learning-Computer-Vision/Plant-Research/Disease-Classification/) | Three experiments, report, MIT notice, checkpoint references | Authorized datasets/weights and exact historical environment for training reproduction |
| [CV / Phenotyping](../Deep-Learning-Computer-Vision/Plant-Research/Phenotyping-Dashboard/) | Backend, local configuration, setup, endpoint checks | Otis written redistribution permission; FYP team statement; authorized data/model execution |
| [CV / Building Height](../Deep-Learning-Computer-Vision/Building-Height-Estimation/) | Status only | Original local source |
| [NLP / LLM Safety](../Natural-Language-Processing/Urdu-Roman-Urdu-LLM-Safety/) | Status only | Original local source |
| [Databases / CineLog](../Databases/CineLog/) | Status only | Original local source |

## History and integrity

Existing Academic-Projects history is retained. Other repositories are imported as reviewed snapshots, not merged wholesale: their historical objects contain sensitive material, large artifacts, and unrelated code. Source repositories are left unchanged. [import-manifest.json](import-manifest.json) records source commits, source paths, source hashes, final hashes, and modifications; the source-commit table below provides repository-wide provenance. All 30 HCI files are byte-identical to their original Git blobs; no file is added or omitted inside that project. No force-push or history rewrite is performed.

| Source | Audited commit | Commits |
|---|---|---:|
| Academic-Projects | `ddd2b5349bf271bfc5261a812b6111f20c7ec89e` | 32 |
| AnatoNamikaza | `274edc0d9f41c5775b8652f665dd80fe3bf70668` | 36 |
| azaan-imran192 | `a2c5b736e1b76383068102b449f49489077a6cf7` | 2 |
| plant-disease-classifier | `a2146971953eaa87b345d1cb502d761f49a29b34` | 6 |
| plant-phenotyping-dashboard | `edd9125a7411a22d95884c9a87f8002cadcf10f7` | 2 |
| RB2-Android | `2965cfeac81200b43676822c7d82b1e8e79726de` | 17 |
| shared-projects | `ded2c287a9a7f52b3c6fde837965b21a1d7c274c` | 21 |
| Urdu-News-Articles | `6773082b0579b603b905849762970786134753d9` | 2 |
