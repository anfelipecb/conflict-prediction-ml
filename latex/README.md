# LaTeX paper (publication-style PDF)

Builds `main.pdf` from `main.tex` with **biblatex** + **biber**, **hyperref** (subtle PDF link borders on citations, cross-refs, and URLs), and figures from `../output/`.

## Requirements

- TeX Live or MacTeX (`pdflatex`, `biber`, `latexmk`)
- Packages: `biblatex`, `hyperref`, `xurl`, `microtype`, etc. (standard in full TeX Live)

## Build

```bash
cd latex
latexmk -pdf main.tex
# or
make
```

## Figures

Paths are `../output/<name>.png` relative to this folder. The repo uses these filenames on disk:

- `ROC_Models.png`, `Precision_Recall.png` (capital letters as shown)
- `confusion_RF.png` / `confusion_NN.png` are **symlinks** to `confussion_RF.png` / `confussion_NN.png` (historic spelling)
- Logistic regression and K-NN matrices: **`LR_confussion.png`**, **`KNN_confussion.png`** (same spelling convention as RF/NN). Optional symlinks `confusion_LR.png` → `LR_confussion.png` and `confusion_KNN.png` → `KNN_confussion.png` keep older paths working.

## Editing

- Main text: `main.tex`
- Bibliography: `references.bib`
