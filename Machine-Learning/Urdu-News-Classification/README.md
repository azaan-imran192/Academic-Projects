# Urdu News Classification

An academic comparison of manually implemented Multinomial Naive Bayes, one-vs-rest logistic regression, and a small PyTorch feed-forward network for classifying Urdu news. The problem is five-way topic classification in a language with relatively limited NLP resources.

## Source and team

Imported from [Urdu-News-Articles](https://github.com/azaan-imran192/Urdu-News-Articles/tree/6773082b0579b603b905849762970786134753d9). The report credits **Hanzalah Sohail Faraz, Azaan Imran, Basil Hassan, and Mujeeb Asad**. No per-person implementation ownership is inferred from the upload history. [Original report](Group4_Report.pdf).

## Technology and layout

Python, NumPy, pandas, scikit-learn, PyTorch, Matplotlib, Seaborn, Beautiful Soup, Requests, and Jupyter.

| Material | Purpose |
|---|---|
| `Group4_MNB.py` / `.ipynb` | Custom bag-of-words and Laplace-smoothed Naive Bayes; scikit-learn comparison |
| `Group4_Logistic.py` / `.ipynb` | TF-IDF, scaling, five one-vs-rest gradient-descent classifiers |
| `Group4_NeuralNetworks.py` / `.ipynb` | Count features, 128-unit ReLU hidden layer, cross-entropy and Adam |
| `Group4_webscraping.py` / `.ipynb` | Original news collection and cleaning workflow |
| `output_file.csv` | Single canonical dataset: 1,465 rows, five columns |
| `Group4_Report.pdf` | Original academic report, not a claim of conference publication |

The duplicate project ZIP is intentionally omitted. Exported scripts and notebooks are alternative execution formats, not separate datasets.

## Setup and execution

Use Python 3.12. From this project directory:

```sh
python -m venv .venv
# Activate .venv (Windows: .venv\Scripts\activate; POSIX: source .venv/bin/activate)
python -m pip install -r requirements.txt
python Group4_MNB.py
python Group4_Logistic.py
python Group4_NeuralNetworks.py
```

Alternatively, install JupyterLab and open the corresponding notebook from this directory. Model input paths now point to `output_file.csv`; the algorithms and historical notebook results are preserved. The scraper is an archival collection workflow, not needed for model execution. Its local output paths and external website selectors may require changes; it was not run against live news sites.

## Data and permissions

The CSV has `id`, `title`, `link`, `content`, and `gold_label`. Counts are world 314, sports 313, entertainment 313, business 311, and science-technology 214. Naive Bayes and the neural network drop missing content/labels, leaving **1,441** rows. Logistic regression fills missing content and uses **1,465** rows. This explains the 289 versus 293 test examples.

Sources: Geo Urdu, Jang, Dunya News Urdu, and Express News Urdu. The portfolio owner confirmed redistribution permission on 19 October 2026. That confirmation does not transfer publisher copyright or grant a blanket open-source license over article text. Preserve article URLs and attribution; downstream reuse requires applicable permission.

## Results and limitations

| Model | Original report accuracy | Status |
|---|---:|---|
| Custom Multinomial Naive Bayes | 97.92% | Reproduced locally on 19 October 2026 (289 held-out rows) |
| One-vs-rest logistic regression | 96.25% | Reproduced locally on 19 October 2026 |
| Neural network | 97.58% | Matched in the local rerun; unseeded training can vary |

See [verification](../../docs/VERIFICATION.md) for reruns. The original logistic and neural workflows fit their vectorizers before splitting; this leaks vocabulary information into evaluation. Historical scores are therefore coursework evidence, not an unbiased benchmark. The logistic and neural feature matrices are dense, and the neural model does not fix a random seed. Class imbalance, near-duplicates, collection bias, and changing news distributions can affect generalization. No production deployment is claimed.
