## Milestone 5: Implementing Non-Linear Models

Our project seeks to answer the following research question: 

**_Can the ocurrence of violence in a given geography be predicted using local socioeconomic and environmental data?_**

To answer this question, we are using climate data from satellite imagery (temperature, precipitation, light radiance, deforestation, and surface pressure) and socioeconomic indicators (Relative Wealth Index, a measure of wealth distribution) to predict the level of conflict (no conflict, low, medium, high)[^1] in specific 50x50km polygon of Africa.

For this specific milestone, we have begun developing three non linear models to check which of them performs better when predicting the level of conflict based on our data and attributes. The models to be trained are:

- Random Forest

- K Nearest Neighbors

- K Means Clustering

To compare outcomes across models, we also ensure that hyperparameters are tuned so that our decision is informed by the best possible predictions. We then will select the model that produces the best predictions out of the specifications considered. 

---

#### Q1: Which nonlinear model do you plan on implementing? Why?

1. **Random Forest:** We've selected Random Forest as our primary nonlinear model because it excels at capturing complex relationships between environmental factors and conflict that linear models cannot detect. Random Forest provides valuable feature importance rankings, helping us identify which climate and socioeconomic variables most strongly predict conflict occurrence. The model's ensemble approach naturally resists overfitting through bootstrap sampling and averaging across multiple decision trees, while effectively handling our mixed data types and class imbalance after SMOTE application. These advantages make Random Forest particularly well-suited for understanding the multifaceted relationships between climate conditions, wealth distribution, and conflict patterns across diverse African regions.

2. **K Nearest Neighbors:** Our choice for KNN as an alternative approach for prediction stems from the intuition that conflict is likely to spread across space and that similar geographies are likely to experience comparable levels of conflict. We use a weighted KNN specification to account for the potential shortcomings of distance-based learning in higher dimensions and hence give stronger predictive influence to samples that are closer in distance to the sample being analyzed.

3. **K Means Clustering:** This model is very powerful when reducing the complex patterns of our features based on climate variables into a single cluster ID. Eventhough we learned that Clustering is for unsupervised learning, our research points that it can also be used to supervised learning, which is our case due to the multiclass labels of 'No conflict', 'Low conflict', 'Medium Conflict', 'High Conflict'.

   For it, the methodology will be to cluster based on 4 centroids considering also the labels. Finally, we will label the new data considering which 'original label' is the one   that's most present in that cluster. That way, we can regroup our data.

   The main challenge for the Clustering model will be the selection of the initial centroids, which we will tackle using the K-means++ variation of Lloyd's algorithm.


---

#### Q2: Explain how this model is nonlinear

1. **Random Forest:** Random Forest is nonlinear because it uses decision trees that create complex, stair-step shaped boundaries rather than straight lines. While linear models can only draw a straight line to separate different classes, each tree in a Random Forest makes yes/no decisions that split the data in multiple directions. When hundreds of these trees vote together, they create intricate decision boundaries that can capture complex patterns like threshold effects (where conflict only occurs after a certain temperature) or interaction effects (where the combination of low rainfall AND high temperature increases conflict risk). This nonlinear approach allows our model to detect relationships between environmental factors and conflict that simple linear models would completely miss.

2. **KNN:** The non-linearity of the decision boundary produced by KNN is a result of classification being defined locally based on distance calculations that are determined by the features of training samples in proximity rather than following a single decision rule that globally describes the separation across the entirety of datapoints in a linear fashion. 

3. **Clustering:** This model is non linear since it uses the distance from each datapoint to each centroid to assign a label for the data, where there's no specific linear relation from the features of the datapoint to the final label. Through each 'epoch', the model is relocating the centroids to the average coordinates of the points that belong to each centroid after each epoch, until it converges or a certain number of 'epochs' is accomplished.

---

#### Q3: How will you interpret the model's results?

We will interpret our models' results through multiple complementary approaches. We'll use ROC curves and AUC scores to compare model performance across Random Forest, KNN, and Clustering, which is especially valuable for our imbalanced conflict data. For Random Forest and KNN, we'll analyze feature importance to identify which environmental and socioeconomic factors best predict conflict. Partial dependence plots will help visualize how specific features like temperature extremes affect conflict probability. For Clustering, we'll examine cluster compositions to understand which environmental conditions tend to group together with different conflict levels. All models' predictions will be visualized geographically to identify spatial patterns where models perform well or struggle. We'll pay particular attention to false negatives (missed conflicts) given their serious policy implications, and validate our findings against existing literature on conflict drivers.

---

#### Q4: What twist do you plan on adding? Why do you think this will be a good addition to your model?

1. **Random Forest:** Our main twist is implementing a multiclass Random Forest that predicts not just conflict occurrence but also conflict intensity levels (none, low, medium, high). This leverages ensemble learning to combine hundreds of decision trees, which dramatically reduces overfitting, increases predictive accuracy, and provides more stable results than any single decision tree could achieve on our complex conflict prediction task. We're enhancing this with grid search hyperparameter optimization focused on recall_weighted to ensure our model is sensitive to all conflict classes despite imbalance. This approach provides more nuanced predictions than standard implementations, allowing us to identify not just where conflicts might occur but also their potential severity, enabling better-targeted prevention and response strategies.

2. **KNN:** Given that conventional KNN is highly dependent on distance-based metrics that produce unreliable predictions when data is high-dimensional, and that our data is largely concerned with geospatial attributes whose recontribution to the model may not be well captured by euclidean distance, we plan on executing the model using different distance metrics, like haversine and manhattan, to identify whether performance can be improved. Another possible extension to the baseline KNN model would be to implement dimensionality reduction via Principal Component Analysis to reduce noise that may be limiting model accuracy. 

3. **Clustering:** As we mentioned before, the main twist here will be to use the labeled data as a decision tree node after clustering eventhough we learned that Clustering was only for unsupervised learning. We will do this by checking the most frequent label of conflict within each cluster. For it, we will have to define a method for our imbalance dataset, otherwise many non-conflict labels will be classified as with conflict.


[^1]: We classify our label into different levels of conflict based on the distribution of counts across the data. Accordingly, we label samples with 0 when there are no conflicts, 1 when conflicts are 'low' (up to q1), 2 when conflicts are medium (between q1 and q3), and 3 when conflict are 'high' (at or above q3). 