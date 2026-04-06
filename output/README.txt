Figures referenced from milestones/milestone_6/final_doc.ipynb as ../../output/*.png

Generate them by running the training EDA notebooks and saving with these filenames:
  conflicts_africa_89-23.png
  conflicts_africa_country.png
  Data_Africa.png
  confusion_LR.png
  confusion_KNN.png
  confusion_RF.png
  RF_Importance.png
  confusion_NN.png
  ROC_models.png
  precision_Recall.png

Or add plotting cells to final_doc.ipynb that write PNGs here.

Regenerate docs/full_report.html after editing the notebook:
  jupyter nbconvert --to html --output-dir docs --output full_report milestones/milestone_6/final_doc.ipynb
  (Requires a working nbconvert/Jupyter template install.)

Vercel: import the GitHub repo and set Root Directory to "docs", or from the repo run:
  cd docs && vercel deploy --prod
  Production alias example: https://docs-wheat-sigma.vercel.app (see your Vercel dashboard for the current URL).
