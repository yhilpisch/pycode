# Code Runner and Chapter Scripts

Python Primer for Data Science and Deep Learning  
(c) Dr. Yves J. Hilpisch  
AI‑Powered by GPT‑5

This folder contains small, self‑contained scripts for each chapter plus a
convenience runner that validates they work end‑to‑end on your machine.

## Structure

- `NN_name.py` – Python scripts for chapter `NN` (e.g., `01`, `09`).
- `NN_name.sh` – Bash helpers for chapters with shell workflows.
- `run_all.py` – Discovers and runs the chapter scripts and prints a summary.

Scripts write figures to `figures/` and print short results to stdout. All
files include the copyright header required by the project.

## Quick start

From the project root (recommended inside a venv):

```bash
python code/run_all.py             # run Python scripts
python code/run_all.py --with-bash # also run bash scripts (dry‑run)
python code/run_all.py --list      # list discovered scripts
```

The runner sets `MPLBACKEND=Agg` so plotting works in headless setups and
limits each script to a configurable timeout (default 60s).

Exit code is non‑zero if any script fails.

## Make targets

The root `Makefile` provides shortcuts:

```bash
make validate-code         # Python scripts only
make validate-code-all     # Python + bash (dry‑run)
make list-code             # list scripts discovered by the runner
```

## Bash scripts and DRY‑RUN mode

The runner executes shell scripts with `PRIMER_DRY_RUN=1`. Scripts respect this
variable and *echo* the commands they would run instead of changing your
machine. To actually execute a bash script, run it directly without the env var:

```bash
PRIMER_DRY_RUN=0 bash code/12_git_basics.sh   # real actions
```

## Dependencies

Minimal set for the Python examples:

```bash
python -m pip install numpy matplotlib pandas
```

Optional for Chapter 11:

```bash
python -m pip install scikit-learn
```

The runner itself has no extra dependencies beyond the standard library.

## Running an individual script

```bash
python code/09_matplotlib.py
bash code/12_git_basics.sh             # DRY‑RUN by default when called by runner
```

## Output locations

- Figures are written to `figures/`.
- Console output is printed by each script and summarized by the runner.

## Troubleshooting

- `ModuleNotFoundError`: install the missing package in your active venv.
- On Windows shells, prefer `py -m pip install ...` or use WSL.
- If a figure window tries to open, ensure `MPLBACKEND=Agg` or run via the
  runner which sets it automatically.

## Roadmap (to be extended later)

- Add tiny unit tests for selected functions.
- Add a smoke test for generated figures (existence/size check).
- Add CI recipe to run `make validate-code` on pushes.

## Disclaimer

The scripts and guidance in this repository are provided for illustrative and educational purposes only. They are supplied “as is,” without warranty of any kind, express or implied, including but not limited to merchantability, fitness for a particular purpose, or non-infringement. Use of the code is at your own risk, and no guarantee is made that it is error-free, compliant with any regulations, or suitable for production use. By using these materials, you agree that neither the authors nor contributors shall be liable for any damages or losses arising from their use.
