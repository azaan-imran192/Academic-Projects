# Mobile Usage Analysis

An exploratory data-science study of mobile-phone use among university students: screen time, academic performance, anxiety, social habits, and app preferences. This is an observational survey analysis, not evidence that phone use causes a particular health or academic outcome.

## Source and attribution

Recovered from [ScreenTimeand StudentLife](https://github.com/HanzalahSohail/Projects/tree/ded2c287a9a7f52b3c6fde837965b21a1d7c274c/ScreenTimeand%20StudentLife). Azaan Imran confirms this was shared academic work with Hanzalah Sohail. The notebook filename identifies Group 7 but does not establish the complete roster; no individual contribution percentages are invented. The [associated article](https://medium.com/@raahem619/mobile-phone-usage-among-university-students-d896e45df7b2) is linked as provided by the source, not copied or attributed solely to Azaan. Both source MIT notices are preserved in [LICENSE](LICENSE).

## Materials and stack

- `markhor_group7_ahmedfaraz.ipynb`: cleaning, exploratory plots, classification, bootstrapping, correlation tests, and observational regression calculations.
- `Mobile Phone Usage Among University Students Dataframe.csv`: 202 survey responses, with collection timestamps removed in this import.
- `bloglink.txt`: original article reference.
- Python, NumPy, pandas, Matplotlib, Seaborn, scikit-learn, SciPy, statsmodels, and Jupyter.

## Run

Use Python 3.12. From this directory:

```sh
python -m venv .venv
# Activate .venv.
python -m pip install -r requirements.txt
python -m pip install jupyterlab
python -m jupyter lab markhor_group7_ahmedfaraz.ipynb
```

Run cells in order. The notebook expects the CSV next to it. Timestamp removal now tolerates an already anonymized CSV. Existing row previews and outputs were cleared before publication so raw records are not duplicated throughout the notebook. The algorithmic analysis remains attributable to its original authors.

## Findings and limits

The original saved notebook reports classifier accuracies of **34.1463%, 39.0244%, and 46.3415%**, and weak screen-time correlations whose bootstrap intervals include zero. The three classifier accuracies were reproduced locally on 19 October 2026; bootstrap estimates varied. See [verification](../../docs/VERIFICATION.md) for the execution outcome and exact limits.

The convenience sample is small; screen time and other measures are self-reported. Cleaning imputes some friend-circle values and maps categorical CGPA ranges to numbers. Bootstrap randomness is not fully seeded. Multiple comparisons and confounding limit inference. Notebook variables called “ATE” do not make the study causal; no randomized assignment or validated causal identification strategy is demonstrated.

The portfolio owner confirmed consent and redistribution permission on 19 October 2026. Names, emails, and phone numbers are not dataset columns; timestamps were removed. Demographic combinations can still be sensitive: do not attempt re-identification or append identifiable records. The dataset is not covered by a blanket software license.
