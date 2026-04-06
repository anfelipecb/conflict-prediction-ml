#!/usr/bin/env bash
# Copy milestone HTML export + root output/ figures into docs/ for the static site
# (Full Report tab + relative paths like docs/output/*.png).
# Used by: vercel.json buildCommand, GitHub Pages workflow (same behavior as manual cp).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
mkdir -p docs/output
cp milestones/milestone_6/final_doc.html docs/full_report.html
# -L follows symlinks (e.g. confusion_* -> confussion_* / LR_confussion.png)
cp -Lf output/*.png docs/output/ 2>/dev/null || true
echo "sync_docs_report_assets: docs/full_report.html + docs/output/*.png"
