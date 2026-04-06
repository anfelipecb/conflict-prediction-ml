#!/usr/bin/env bash
# Export milestones/milestone_6/final_doc.ipynb to PDF (webpdf / Playwright).
# Requires: Homebrew jupyter + nbconvert 7.x, mistune 3.0.2, playwright chromium,
# and Jupyter nbconvert templates symlinked (see README in output/).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
export PATH="/opt/homebrew/bin:$PATH"
jupyter nbconvert --to webpdf "milestones/milestone_6/final_doc.ipynb" \
  --output-dir "milestones/milestone_6" \
  --output final_doc
cp "milestones/milestone_6/final_doc.pdf" "notebooks/final_doc.pdf"
echo "Wrote milestones/milestone_6/final_doc.pdf and notebooks/final_doc.pdf"
