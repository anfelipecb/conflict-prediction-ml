Figures referenced from milestones/milestone_6/final_doc.ipynb as ../../output/*.png
The static site copies PNGs to docs/output/ so full_report.html can use paths like output/Data_Africa.png (see GitHub Actions deploy step).
For filenames: confusion_RF.png and confusion_NN.png in this folder are symlinks to confussion_RF.png / confussion_NN.png. Export confusion_LR.png and confusion_KNN.png from the training notebooks if missing (required for notebook + LaTeX paper).

Generate them by running the training EDA notebooks and saving with these filenames:
  conflicts_africa_89-23.png
  conflicts_africa_country.png
  Data_Africa.png
  confusion_LR.png
  confusion_KNN.png
  confusion_RF.png
  RF_Importance.png
  confusion_NN.png
  ROC_Models.png
  Precision_Recall.png
(on disk; confussion_RF / confussion_NN match the spellings above)

Or add plotting cells to final_doc.ipynb that write PNGs here.

Regenerate docs/full_report.html after editing the notebook:
  jupyter nbconvert --to html --output-dir docs --output full_report milestones/milestone_6/final_doc.ipynb
  (Requires a working nbconvert/Jupyter template install.)

Vercel: import the GitHub repo and set Root Directory to "docs", or from the repo run:
  cd docs && vercel deploy --prod
  Project name: climate-conflict-ml — production URL: https://climate-conflict-ml.vercel.app (see dashboard for team-specific URLs).
