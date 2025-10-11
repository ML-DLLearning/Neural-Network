# BM3D Paper Reproduction (Image Denoising by Sparse 3-D Transform-Domain Collaborative Filtering)

This repository documents my step-by-step reproduction of BM3D (Dabov et al., IEEE TIP 2007). It includes experiment configs, scripts, evaluation, and comparisons under common AWGN noise levels.

## Goals
- Reproduce PSNR/SSIM on standard sets (Set12, BSD68, Kodak24) at σ ∈ {15, 25, 50}.
- Validate pipeline details: grayscale/color settings, two-step BM3D (hard-thresholding + Wiener), parameter sensitivity.
- Provide fully reproducible scripts, fixed seeds, env, and results CSVs.

## References
- Paper: K. Dabov, A. Foi, V. Katkovnik, K. Egiazarian (2007).
- Official BM3D page (MATLAB/C code & docs, non-GitHub): http://www.cs.tut.fi/~foi/GCF-BM3D/

## Repository Structure
```
.
├── src/                    # library code (dataset, metrics, runners)
├── scripts/                # end-to-end scripts (noise, run, evaluate)
├── configs/                # YAML configs for experiments
├── data/                   # (gitignored) place datasets or symlinks
├── results/                # metrics, logs, denoised images
├── notebooks/              # analysis & figures
├── .github/workflows/      # CI
├── .gitattributes          # LFS patterns for images
├── .gitignore
├── CITATION.cff
├── LICENSE
├── Makefile
├── requirements.txt
└── README.md
```

## Quickstart
1) Create environment:
```
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pre-commit install
```

2) Prepare data:
- Place test images under `data/BSD68`, `data/Set12`, etc. (see scripts & notes).
- Or add your own images.

3) Add noise:
```
python scripts/add_noise.py --input data/BSD68 --output data/BSD68_sigma25 --sigma 25 --seed 123
```

4) Run BM3D:
- Option A (Python package): requires a Python BM3D package (if available), otherwise fallback instructs compilation/Matlab.
```
python scripts/run_bm3d.py --input data/BSD68_sigma25 --output results/BSD68_sigma25_bm3d --sigma 25
```

5) Evaluate:
```
python scripts/evaluate.py --clean data/BSD68 --denoised results/BSD68_sigma25_bm3d --out_csv results/metrics_BSD68_sigma25.csv
```

6) Reproduce tables:
- Use `configs/` presets and `Makefile` targets to batch-run experiments and aggregate metrics.

## Reproducibility Notes
- Always specify data range (0–255 vs 0–1). This repo uses 0–255 by default (see scripts).
- Fixed seeds for noise generation.
- Record commit SHA, environment, and wall-clock time in metrics CSV.

## Roadmap
- [ ] Add color BM3D path and opponent-color transform option.
- [ ] Parameter sweep and ablation.
- [ ] Compare to later baselines (e.g., DnCNN) for context (optional).