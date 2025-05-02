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

As it was explained before, the model predicts the ocurrence/not ocurrence of conflict based on climatologic and socodemographic variables in a certain 50x50km polygon in Africa. For further detail go to Q1.

About the weights size in a logistic regression, we can point out that smaller weights mean less importance of the feature if and only if all features are in the same scale. If that's not the case, then the weight size cannot be interpreted as a sign of feature relevance because weights can be small due to features with big magnitudes. The same logic applies to big weights.

---

#### Q4: What metrics will you use to analyze the performance of your model?

##**Answer Here**
---