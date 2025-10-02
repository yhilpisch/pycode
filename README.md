<img src="https://theaiengineer.dev/tae_logo_gw_flatter.png" width=35% align=right>

# Python Primer — Companion Code Repository

This is the companion code repository for the book “Python Primer for Machine & Deep Learning”. Here you’ll find the repository structure, setup instructions, and how to validate and run all materials. If you’ve cloned or downloaded this repo, you’re ready to start.

© Dr. Yves J. Hilpisch — AI‑Powered by GPT‑5

## What This Repo Contains

- `notebooks/` — Jupyter notebooks for each chapter
- `code/` — Stand‑alone scripts that mirror the chapter content
- `tools/validate_notebooks.py` — Execute notebooks headlessly to verify they run
- `tools/validate_code.py` — Run Python scripts (and optionally bash) with a summary report

No book source files are included here. This code repo is designed to accompany the book PDF as a hands‑on learning resource.

## Quickstart

1) Create and activate a virtual environment (Python 3.10+ recommended):

```
python -m venv .venv
. .venv/bin/activate    # Windows: .venv\Scripts\activate
python -m pip install -U pip
```

2) Install minimal runtime and validation tools:

```
python -m pip install nbclient nbformat numpy pandas matplotlib scikit-learn
```

3) Validate notebooks and scripts:

```
# Run notebooks (non-interactive; figures use MPLBACKEND=Agg)
python tools/validate_notebooks.py --timeout 300 --report-md tools/nb_report.md --report-json tools/nb_report.json

# Run chapter scripts (Python only)
python tools/validate_code.py --timeout 90 --report-md tools/code_report.md --report-json tools/code_report.json

# Include bash scripts too (dry-run by default)
python tools/validate_code.py --with-bash
```

## Notes and Conventions

- Executed notebook outputs are not tracked. Any `*.executed.ipynb` or `tools/_executed/` files are ignored.
- Some notebooks may reference optional cloud‑specific features (e.g., Google Colab). These cells are guarded and will print a message instead of failing when unavailable.
- Figures are generated on the fly by matplotlib; no binary assets are required.

## Troubleshooting

- If you encounter missing cell `id` warnings from `nbformat`, the validator already normalizes IDs before execution. Running the validator once typically resolves these warnings.
- Network‑heavy installs inside notebooks (e.g., `pip install`) are minimized. If you are offline, comment those lines or preinstall packages in your environment.

## License and Credits

© Dr. Yves J. Hilpisch — All rights reserved. Educational use encouraged.

The materials are AI‑powered with GPT‑5 assistance and maintained for reliability and clarity.

<img src="https://theaiengineer.dev/tae_logo_gw_flatter.png" width=35% align=right>
