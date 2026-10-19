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
