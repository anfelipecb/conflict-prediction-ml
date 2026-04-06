# LaTeX paper (publication-style PDF)

Builds `main.pdf` from `main.tex` with **biblatex** + **biber**, **tcolorbox** (green callouts for references/links), and figures from `../output/`.

## Requirements

- TeX Live or MacTeX (`pdflatex`, `biber`, `latexmk`)
- Packages: `tcolorbox`, `biblatex`, `microtype`, etc. (standard in full TeX Live)

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
- **`confusion_LR.png`** and **`confusion_KNN.png`** must be exported from the training notebooks into `output/` (they are not in the repo yet); the PDF shows a clear missing-figure box until you add them.

## Editing

- Main text: `main.tex`
- Bibliography: `references.bib`
- Green “key papers” box: `keypapers` environment; replication link: `linkbox`
