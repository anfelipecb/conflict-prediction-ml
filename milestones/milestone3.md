## Milestone 3: Training our model

Conflict remains a major barrier to development, institutional stability, and humanitarian well-being, particularly in regions affected by environmental stress and resource scarcity. Understanding and predicting the spatial and temporal dynamics of conflict events can provide critical insights for policymakers, aid organizations, and local communities to better allocate resources, anticipate humanitarian crises, and design targeted interventions. 

Given its complex dynamics of resource-driven conflicts, economic inequalities, and climate-induced stress, the African continent serves as an ideal context to explore how environmental and socioeconomic factors interact to exert their influence on the risk of conflict. With this in mind, we seek to answer the following research question: 

**_Can the ocurrence of violence in a given geography be predicted using local socioeconomic and environmental data?_**

To answer our research question, we use climate data from satellite images (temperature, precipitation, light radiance, deforestation, and surface pressure) and socioeconomic indicators (Relative Wealth Index, a measure of wealth distribution) to predict the ocurrence or absence of conflict in specific 50x50km polygon of Africa.

---

#### Q1: Which linear model did you pick? Why?

Our baseline model specification is defined by the following logistic regression:

$$
P(y_i = +1 | x_i)  = \sigma (w^Tx_i + b) = \frac{1}{1+e^{-(w^Tx_i + b)}}
$$

where $i$ is one of 13,036 50km x 50km grids in Africa ~ _our samples_, 

$y_i$ is a binary label encoding the following classes:    
  - $y_i = -1$: There were no reported conflict events in grid $i$    
  - $y_i = +1$: There was at least one conflict event in grid $i$

$x_i$ is a feature vector containing the following information for grid $i$: 

  - Average annual temperature ($K$)
  - Maximum annual temperature ($K$)
  - Temperature anomaly (difference between measured temperature and long-term average) ($K$)\*
  - Total annual precipitation ($m$)
  - Mean annual surface pressure ($Pa$)
  - Forest cover loss ($ha$)
  - Average Relative Wealth Index 
  - Average annual nighttime light intensity $(nW/cm^2/sr)$
  - Year: A discrete variable denoting the year the conflict event occured, spanning 2019 through 2023 (one-hot encoded)
  - Cummulative variation in conflict ocurrences between 2019 and 2022\*

\* Engineered features

$w^T$ is the learning weights vector, 

and $b$ is our model bias. 

We follow the conventional definition of a binary probabilistic decision rule, where our prediction is given by $\hat{y_i} = sign(w^T x_i + b)$: 

  - if $\sigma (w^Tx_i + b) >  0, \hat{y_i} = +1$
  - if $\sigma (w^Tx_i + b) <  0, \hat{y_i} = -1$

We fit this model by minimizing the conditional log-likelihood of $y_i$ given $x_i$ using the following negative log-loss function, which includes an _elastic net_ regularizer:

$$
\ell(w,b) = - \sum_{i=1}^n \left[ \log \sigma(y_i(w^T x_i + b)) \right] + \lambda \left[ \alpha \sum_{j = 1}^p |w_j| + (1 - \alpha) \sum_{j = 1}^p w_j^2 \right]
$$

We have opted for a logistic regression specification due to its ability to predict the likelihood of an event happening, in this case the occurence of a violent encounter, based on contextual attributes assigned to a specific geography. Likewise, we see value in this model's ease of adapting to our future expectations of training an alternative multinomial logistic specification to classify grids into no conflict, low conflict and high conflict classes. 

---

#### Q2: Which regularization term did you pick? Why did you pick that regularizer for your model?

During our preliminary training, we use an L2 regularization term to handle high correlation between features, specifically `light_sum` and `light_mean`. We expect L2 to distribute the weights so that they preserve the contribution of each of these variables to the model rather than penalizing this correlation to the extent of eliminating one variable through the use of an L1 term. However, future deployment of our model specification aspires to make use of an _elastic net_ setup that validates an additional parameter describing the optimal mix between L1 and L1 terms for our training problem.

---

#### Q3: How do you plan on describing your linear model and its output? What do small or large weights mean?

Our logistic regression model predicts the binary outcome of conflict occurrence (1) or absence (-1) in 50x50km grid cells across Africa from 2019 to 2023. The model uses climatological variables (temperature, precipitation, temperature anomalies), environmental indicators (forest loss, night lights), and socioeconomic factors (relative wealth index) to estimate the probability of conflict.

To interpret the weights in our logistic regression model, we first standardize all features using StandardScaler. This transformation ensures all variables have mean=0 and standard deviation=1, making weight magnitudes directly comparable. After standardization, larger positive weights indicate features that strongly increase conflict **probability**, while large negative weights represent factors that decrease conflict likelihood. For example, a large positive weight for "accumulated_conflicts" would suggest past conflict history strongly predicts future conflicts, while a negative weight for "rwi_2021" might indicate wealthier areas experience fewer conflicts.

---

#### Q4: What metrics will you use to analyze the performance of your model?

To evaluate the performance of our model, we will prioritize recall as our primary metric across both training and test sets. This decision is based on two critical factors. First, our dataset exhibits significant class imbalance, with approximately 93% of grid cell-years showing no conflict and only 7% experiencing conflict. Second, in conflict prediction, false negatives (predicting no conflict when one occurs) are substantially more costly than false positives, as missed conflict predictions could lead to lack of preventive measures in areas at risk.

While we will report standard metrics like accuracy and precision, recall offers a more meaningful evaluation of our model's ability to identify areas of potential conflict. To address the class imbalance, we implement a SMOTE (Synthetic Minority Over-sampling Technique) approach during training and provide a confusion matrix to analyze the distribution of predictions. We will also be examining the ROC curve and AUC score to assess the model's discriminative ability across different threshold settings. This approach ensures that the model we build is capable of minimizing the amount of mistakes in predicting true conflict ocurrences while maintaining reasonable overall performance.

We provide the following results after training our baseline model on the data, which includes an L2 regularizer: 

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