#!/usr/bin/env bash
# Sync report assets into docs/ for the static site.
# Used by: vercel.json buildCommand, GitHub Pages workflow.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
mkdir -p docs/output
# Copy LaTeX PDF (Full Report tab points to main.pdf)
cp -f latex/main.pdf docs/main.pdf 2>/dev/null || true
# Keep legacy notebook export for reference
cp -f milestones/milestone_6/final_doc.html docs/full_report.html 2>/dev/null || true
# -L follows symlinks (e.g. confusion_* -> confussion_*)
cp -Lf output/*.png docs/output/ 2>/dev/null || true
echo "sync_docs_report_assets: docs/main.pdf + docs/output/*.png"
