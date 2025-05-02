## Milestone 3: Training our model

Conflict remains a major barrier to development, stability, and humanitarian well-being, particularly in regions affected by environmental stress and resource scarcity. Understanding and predicting the spatial and temporal dynamics of conflict events can provide critical insights for policymakers, aid organizations, and local communities to better allocate resources, anticipate humanitarian crises, and design targeted interventions. 

Africa, given its complex dynamics of resource-driven conflicts, economic inequalities, and climate-induced stress, serves as an ideal context to explore how environmental and socioeconomic factors interact and influence conflict risks. With this in mind, we seek to answer the following research question: 

**_Can the ocurrence of violence in a given geography be predicted using local socioeconomic and environmental data?_**

To answer our research question, we took climate data from satellite images (temperature, precipitation, lighting level, deforestation, and surface pressure) and socioeconomic indicators (Relative Wealth Index, measuring wealth distribution) to predict the ocurrence/not ocurrence of conflict in a certain 50x50km polygon in Africa.

The methodology of the model is explained in the following paragraphs.

---

#### Q1: Which linear model did you pick? Why?

##**Logit: elaborate on this**
---

#### Q2: Which regularization term did you pick? Why did you pick that regularizer for your model?

Preliminary, we are using the Ridge regularizer because as it was explained before, we have variables which are highly correlated (light_sum and light_mean). Taking that into consideration, L2 manages better this kind of variables because it distributes the weights of it so each one can contribute in some way to the model. If we were using L1, the model could eliminate one variable when it has highly correlated variables.

For the purpose of the assignment, and to have the best accuracy and the best recall, we are going to test the model using L2, L1 and also a elastic net (mix of both). After checking them all, we'll decide which one suites better to the purpose of our research question.

---

#### Q3: How do you plan on describing your linear model and its output? What do small or large weights mean?

Our logistic regression model predicts the binary outcome of conflict occurrence (1) or absence (0) in 50x50km grid cells across Africa from 2019 to 2023. The model uses climatological variables (temperature, precipitation, temperature anomalies), environmental indicators (forest loss, night lights), and socioeconomic factors (relative wealth index) to estimate the probability of conflict.

To interpret the weights in our logistic regression model, we first standardize all features using StandardScaler. This transformation ensures all variables have mean=0 and standard deviation=1, making weight magnitudes directly comparable. After standardization, larger positive weights indicate features that strongly increase conflict **probability**, while large negative weights represent factors that decrease conflict likelihood. For example, a large positive weight for "accumulated_conflicts" would suggest past conflict history strongly predicts future conflicts, while a negative weight for "rwi_2021" might indicate wealthier areas experience fewer conflicts.
---

#### Q4: What metrics will you use to analyze the performance of your model?

To evaluate the performance of our model, we will prioritize recall as our primary metric across both training and test sets. This decision is based on two critical factors: First, our dataset exhibits significant class imbalance, with approximately 93% of grid cell-years showing no conflict and only 7% experiencing conflict. Second, in conflict prediction, false negatives (predicting no conflict when one occurs) are substantially more costly than false positives, as missed conflict predictions could lead to lack of preventive measures in areas where lives are at risk.

While we will report standard metrics like accuracy and precision, recall offers a more meaningful evaluation of our model's ability to identify areas of potential conflict. To address the class imbalance, we're implementing SMOTE (Synthetic Minority Over-sampling Technique) during training and using a confusion matrix to analyze the distribution of predictions. We will also be examining the ROC curve and AUC score to assess the model's discriminative ability across different threshold settings. This approach ensures we will build a model that minimizes missed conflict predictions while maintaining reasonable overall performance.

After first base estimations of the model with l2 regularization, we observe this result:

```
--- SMOTE Model ---
Accuracy: 0.8521
Recall: 0.7536

Confusion Matrix:
[[5381  870]
 [ 136  416]]

Classification Report:
              precision    recall

           0       0.98      0.86     
           1       0.32      0.75      

Accuracy: 0.85
```
---