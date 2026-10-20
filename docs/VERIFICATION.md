# Verification record

Executed locally on **19 October 2026**, Windows, Python 3.12.14 and Node.js 24.14.0. Results below distinguish code execution from build/static inspection. External credentials, production systems, and model-training jobs were not used.

| Check | Outcome | Scope / limit |
|---|---|---|
| Urdu custom Naive Bayes script | PASS; accuracy 97.92%, macro precision 97.89%, recall/F1 97.88% | 1,441 usable rows; 1,152 train / 289 test; random_state=42 |
| Urdu logistic script | PASS; accuracy 96.25% | 1,465 rows; 293 test; all 10,000 iterations per one-vs-rest class executed |
| Urdu neural-network script | PASS; accuracy 97.58% in this run | 20 training epochs; 289 test rows; training is unseeded, so future runs may differ |
| Mobile notebook | PASS; 56 code cells executed in order | Executed in a Python namespace, without a Jupyter kernel; plots use a noninteractive backend; no individual records logged |
| Mobile classifier outputs | PASS; 34.1463%, 39.0244%, 46.3415% | Matches original saved accuracies; bootstrapping varies because it is not seeded |
| Culinary frontend | PASS; Vite 6.4.4 production build, 435 modules after compatible dependency updates | No authenticated backend integration; bundle-size warning and missing optional background asset noted |
| Culinary dependency audit | Both final `npm audit --omit=dev` runs report zero vulnerabilities | Frontend full audit still reports seven development dependency advisories (five high, two moderate); see security review |
| Culinary backend | PASS; JavaScript syntax for every backend JS file; dependencies installed | Database/OAuth/S3/Gemini/Edamam integration not run |
| Django backend | PASS; `manage.py check`; migrations on a fresh local SQLite DB | Debug defaults off; MySQL disabled; no existing source database copied |
| Django API checks | PASS; two empty-list endpoints return 200 and four missing-record endpoints return 404 | `/api/images/`, `/api/filters/`, image traits/leaves, plant dashboard/temporal; no inference/data-filled scenarios |
| Notebook format | PASS; imported notebooks parse as nbformat 4 JSON | Not a full JSON-schema/kernel validation |
| Plant research | SOURCE/OUTPUT REVIEW ONLY | No TensorFlow training, checkpoint loading, or GPU verification |
| HCI | PRESERVATION CHECK PASS | All 30 relocated files match original Git-blob bytes; no omissions, additions, or content edits; original subdirectory spelling retained |
| Publication checks | PASS; 46 Python files parse, eight notebooks parse, 29 relative Markdown links resolve | No provider-key/private-key pattern matches or prohibited model/database/environment files in proposed tree; pattern scan is not exhaustive |

The scraper export initially contained an IPython `!pip` command invalid in plain Python; it was replaced by a setup comment. Scraping against live publishers was not performed. The report and original notebook metrics remain historical evidence. The Urdu logistic/neural vectorizers are fitted before splitting, so matching scores do not eliminate evaluation leakage.

Library versions used for model/analysis reruns: NumPy 1.26.4, pandas 2.2.0, scikit-learn 1.4.0, PyTorch 2.9.1, Matplotlib 3.8.2, Seaborn 0.13.2, SciPy 1.12.0, statsmodels 0.14.6. Django verification used Django 5.2.8, DRF 3.15.2, django-cors-headers 4.4.0, and PyMySQL 1.1.1. The full segmentation requirements were not installed or exercised. Project requirements describe dependency ranges, not a claim of exact historical environments.

The existing Culinary frontend lacks `cooking-background.jpg`, `default.jpg`, and `timer-finished.mp3` referenced by source. Build success does not supply those assets. No screenshot was fabricated; browser access to the local preview timed out, so visual/live UI verification remains unconfirmed. ParkinsonPal retains its original prototype PDFs and all other original materials; the generated preview and rewritten documents were removed from the proposed project tree.

External links to source GitHub trees are verified against cloned commits. The article and Figma links are preserved from project evidence but their anonymous/public accessibility is unverified. Links to upstream model repositories identify dependency sources; no checkpoint availability is claimed.

## Three-project extension — 20 October 2026

| Check | Result and practical limit |
|---|---|
| NLP LFS availability | 22/22 download endpoints passed one-byte probes; seven inference objects (715,367,269 bytes) downloaded and SHA-256 checked, including actual mBERT weights. External training corpora were not fully downloaded. |
| NLP original model example | PASS with actual checkpoint: expected toxic words found, grammatical-word false positives absent, sanitization preserved; a separate benign input returned allow. This is a small smoke test, not a new benchmark. |
| NLP offline tests | Eight PASS: allow/block/sanitize boundaries, lexicon handling, script detection, masking, missing-key rejection and environment configuration. Inference and Gemini calls are mocked. |
| NLP Streamlit | AppTest initial render and a benign-input action with actual mBERT passed with zero exceptions. No live Gemini call, paid request, or graphical browser screenshot. |
| Building Height saved results | Baseline, both main improvements and four alternative experiments checked against original saved cells. All original notebook outputs and three PNG bytes preserved; no retraining. |
| Building Height function checks | Original extracted delta-metric function passes identical/large-error inputs; original height-bin function passes inverse-log/bin assignment checks. Does not validate geospatial preprocessing or trained predictions. |
| New notebooks | All 14 parse; all 201 code cells compile after IPython syntax transformation. This is not top-to-bottom notebook execution. |
| CineLog backend / frontend | Both compile with .NET SDK 10.0.101 targeting .NET 9. Initial full builds report five backend and 34 frontend warnings (nullability/unused members), zero errors. Compatible OpenAPI patch rebuilt successfully. |
| CineLog local API | Five PASS after dependency patch: default EF mode, SP/EF/invalid-mode handling, Swagger JSON. Database address deliberately unreachable; no SQL queries were performed. |
| CineLog dependencies | Initial audit found Microsoft.OpenApi 2.3.0 advisory; explicit 2.7.5 dependency replaces unused preview OpenAPI package. Final backend/transitive NuGet audit reports no vulnerable packages. |
| CineLog SQL | No automatic DROP DATABASE/forced rollback remains; SQLCMD stop-on-error guard protects existing CineLog. Two missing GO batch separators repaired; exploratory calls (including an undefined procedure name) commented. Batch-first checks pass. Full T-SQL execution, million-row loading and Kubernetes deployment were not performed. |
| Preservation/security | 30/30 ParkinsonPal original blob matches; root README unchanged; no key/private-key pattern matches, raw LFS pointers or new files over 30 MB. Office XML scanned; existing PDFs reviewed as course evidence. Pattern checks are not an exhaustive security guarantee. |

NLP inference/demo versions actually exercised: Python 3.12.14, torch 2.9.1, transformers 4.57.3, Streamlit 1.51.0, google-generativeai 0.8.5 and regex 2024.9.11. `constraints-tested.txt` records these direct versions without claiming a complete historical environment. The original Gemini SDK integration is retained; provider/model availability and live service behavior require the user's own key.

The source NLP notebook's saved 0.383 accuracy evaluation remains present alongside its higher transformer-training result; no single score is presented as definitive. Building Height's better delta metrics do not imply better RMSE/MAE. CineLog report row counts were not regenerated. SQL-backed UI behavior, exact dataset cleaning, and GPU training remain unverified. See [compact evidence](verification-evidence/) and project READMEs.

Final publication check: **53 Python files parse, 22 notebooks parse, and all 52 checked relative Markdown links resolve**. The two broken links in the original NLP final-deliverable README were corrected to the imported files. The 126 selected original-file hashes are recorded in `new-project-import-manifest.json`; archive inventories separately record excluded and redundant artifacts. ParkinsonPal remains 30 unchanged original files. These lightweight checks were rerun after final documentation fixes; expensive model/build tests were not repeated.

## Portfolio presentation — 20 October 2026

The root README is now intentionally redesigned, superseding the earlier source-consolidation statement that it remained unchanged. Project-level files and original artifacts remain unchanged. All nine project READMEs were reviewed; the new homepage reuses only existing experimental imagery and distinguishes historical results from executed checks.

Lightweight presentation validation covers 31 local file/image targets, five homepage section anchors and ten profile links to verified source-commit targets. All resolve. The two external homepage GitHub destinations resolve via the canonical API. Profile icon/statistics services return valid images and render in the browser. The existing LinkedIn URL is retained exactly; automated access is restricted, so its current destination is not independently certified.

Both local GitHub-style HTML previews were visually inspected at the browser's default desktop viewport, with no broken images or horizontal overflow observed. These previews approximate GitHub rendering rather than guaranteeing identical layout. ParkinsonPal's 30 original files again match the original Git blob hashes. No model training, application builds or expensive tests were rerun for this documentation-only change.

The profile remains a separate unpublished draft. GitHub-hosted project links use an existing verified commit instead of assuming the unmerged directories exist on main. See [merge readiness](MERGE-READINESS.md) for remaining approvals, security/licensing items and external dependencies.
