# Repository and project inventory

Audit dates: **19–20 October 2026**. Seven public repositories were discoverable under `azaan-imran192`; the connected identity was verified. Private or inaccessible repositories cannot be certified by this inventory.

| Repository | Audit finding | Consolidation disposition |
|---|---|---|
| Academic-Projects | 32 commits; HCI materials, empty Urdu placeholder, Culinary placeholder; a deleted Culinary ZIP exists in history | Preserve history; relocate the complete unchanged HCI project; add categorized projects |
| Urdu-News-Articles | Four notebooks, four script exports, CSV, report, duplicate ZIP; machine-specific paths | Complete source/data/report imported once; paths fixed; ZIP omitted |
| plant-disease-classifier | Three notebooks, report, MIT license, ten LFS checkpoint pointers | Source/report imported; model references retained without binaries |
| plant-phenotyping-dashboard | 2,204 tracked files; backend/frontend, captured media, database, vendor trees and LFS weights; exposed configuration and commercial template | Sanitized authored backend imported; data/weights/vendor code excluded; frontend held |
| azaan-imran192 | Public profile README says student/aspiring engineer and uses many remote image services | Audited; graduate/AI-engineering profile draft prepared locally for approval. Public profile unchanged. |
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
| [CV / Building Height](../Deep-Learning-Computer-Vision/Building-Height-Estimation/) | Eight notebooks, original README/three PNGs, course report/presentation, portable paths and metric evidence | Authorized dataset, exact historical splits/checkpoints and native GDAL/GPU environment for retraining |
| [NLP / LLM Safety](../Natural-Language-Processing/Urdu-Roman-Urdu-LLM-Safety/) | Pipeline, Gemini/Streamlit demo, six notebooks, reports/proposal/deliverables; actual-model and offline tests | User-supplied Gemini key; full benchmark replication and separate dataset/base-model rights |
| [Databases / CineLog](../Databases/CineLog/) | Three course parts plus extra credit, canonical ASP.NET backend/WinForms frontend, SQL and deployment source; builds pass | Isolated SQL Server/data-backed testing, exact raw-to-cleaned CSV pipeline, desktop UI validation |

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

## Archive import extension — 20 October 2026

The three previously missing projects are now imported on the same review branch. [New import manifest](new-project-import-manifest.json) records 126 selected original files and hashes: NLP 22, Building Height 14, CineLog 90. Added documentation, verification tests, resource importer and historical-variant patch are consolidation additions, not claimed original coursework.

Complete inventories include every outer archive entry and reviewed nested members: [NLP](archive-inventories/nlp.json) (51 files), [Building Height](archive-inventories/height.json) (40 files including embedded Git metadata), [CineLog](archive-inventories/cinelog.json) (995 files, approximately 1.214 GB uncompressed). They record archive SHA-256, sizes, CRCs, reviewed-file hashes, inclusion decisions and duplicate mappings. CineLog has 103 reviewed duplicate-content groups; the NLP corpus has redundant notebook-local copies. Embedded repositories, caches, binaries and duplicate ZIP containers are not copied.

The NLP ZIP is byte-identical to the 51 Git blobs at `ahmad4376/Urdu_toxic_prompt_filter` commit `ec6ee7a17e47105acce859c52d03a2a000353c86`; Git blobs were used for comparison to avoid checkout line-ending differences. Team attribution is Azaan Imran and Ahmad Bilal Habib. All 22 LFS objects were endpoint-probed; seven inference resources were fully downloaded and SHA-256 checked locally. No pointers or weights were published.

Building Height preserves the experiment progression and original output evidence, including failed/worse alternatives. The accompanying course presentation establishes Azaan Imran and Muhammad Ibrahim as Group 31. The extra report/presentation were recovered alongside the explicitly supplied local project folder. CineLog's reports establish Azaan Imran, Hanzalah Sohail Faraz, Muhammad Hashaam Tauseef and Raahem Azam as Group 10. Its three numbered parts and separately packaged Kubernetes extra credit remain distinct. Nonidentical alternate backend implementation is retained as a sanitized historical patch, rather than copied as a second runnable application.
