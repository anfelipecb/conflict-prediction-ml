## Milestone 3: Training our model

Conflict remains a major barrier to development, stability, and humanitarian well-being, particularly in regions affected by environmental stress and resource scarcity. Understanding and predicting the spatial and temporal dynamics of conflict events can provide critical insights for policymakers, aid organizations, and local communities to better allocate resources, anticipate humanitarian crises, and design targeted interventions. 

Africa, given its complex dynamics of resource-driven conflicts, economic inequalities, and climate-induced stress, serves as an ideal context to explore how environmental and socioeconomic factors interact and influence conflict risks. With this in mind, we seek to answer the following research question: 

**_Can the ocurrence of violence in a given geography be predicted using local socioeconomic and environmental data?_**

To answer our research question, we took climate data from satellite images (temperature, precipitation, lighting level, deforestation, and surface pressure) and socioeconomic indicators (Relative Wealth Index, measuring wealth distribution) to predict the ocurrence/not ocurrence of conflict in a certain 50x50km polygon in Africa.

The methodology of the model is explained in the following paragraphs.

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

We fit this model by minimizing the conditional log-likelihood of $y_i$ given $x_i$ using the following negative log-loss function, which includes an _elastic net_ regularizer:

$$
\ell(w,b) = - \sum_{i=1}^n \left[ \log \sigma(y_i(w^T x_i + b)) \right] + \lambda \left[ \alpha \sum_{j = 1}^p |w_j| + (1 - \alpha) \sum_{j = 1}^p w_j^2 \right]
$$

We have opted for a logistici 

---

#### Q2: Which regularization term did you pick? Why did you pick that regularizer for your model?

During our preliminary training, we use an L2 regularization term to handle high correlation between features, specifically `light_sum` and `light_mean`. We expect L2 to distribute the weights so that they preserve the contribution of each of these variables to the model rather than penalizing this correlation to the extent of eliminating one variable through the use of an L1 term. However, future deployment of our model specification aspires to make use of an _elastic net_ setup that validates an additional parameter describing the optimal mix between L1 and L1 terms for our training problem.

---

#### Q3: How do you plan on describing your linear model and its output? What do small or large weights mean?

---

#### Q4: What metrics will you use to analyze the performance of your model?

---