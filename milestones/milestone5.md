## Milestone 5: Implementing Non-Linear Models

Our project seeks to answer the following research question: 

**_Can the ocurrence of violence in a given geography be predicted using local socioeconomic and environmental data?_**

To answer this question, we are using climate data from satellite imagery (temperature, precipitation, light radiance, deforestation, and surface pressure) and socioeconomic indicators (Relative Wealth Index, a measure of wealth distribution) to predict the level of conflict (no conflict, low, medium, high)[^1] in specific 50x50km polygon of Africa.

For this specific milestone, we have begun developing three non linear models to check which of them performs better when predicting the level of conflict based on our data and attributes. The models to be trained are:

- Random Forest

- K Nearest Neighbors

- Clustering

To compare outcomes across models, we also ensure that hyperparameters are tuned so that our decision is informed by the best possible predictions. We then will select the model that produces the best predictions out of the specifications considered. 

---

#### Q1: Which nonlinear model do you plan on implementing? Why?

1. **Random Forest:** [AFC] [Use pros/cons]

2. **K Nearest Neighbors:** Our choice for KNN as an alternative approach for prediction stems from the intuition that conflict is likely to spread across spaces and that similar geographies are likely to experience similar levels of conflict. We use a weighted KNN specification to account for potential dimensionality issues and hence give stronger predictive influence to samples that are closer in distance to the sample being analyzed. 

3. **Clustering:** This model is very powerful when reducing the complex patterns of our features based on climate variables into a single cluster ID. Eventhough we learned that Clustering is for unsupervised learning, our research points that it can also be used to supervised learning, which is our case due to the multiclass labels of 'No conflict', 'Low conflict', 'Medium Conflict', 'High Conflict'.

   For it, the methodology will be to cluster based on 4 centroids considering also the labels. Finally, we will label the new data considering which 'original label' is the one   that's most present in that cluster. That way, we can regroup our data.

   The main challenge for the Clustering model will be the selection of the initial centroids, which we will tackle using the K-means++ variation of Lloyd's algorithm.



---

#### Q2: Explain how this model is nonlinear

1. **Random Forest:** [AFC] 

2. **KNN:** [PH] 

3. **Clustering:** This model is non linear since it uses the distance from each datapoint to each centroid to assign a label for the data, where there's no specific linear relation from the features of the datapoint to the final label. Through each 'epoch', the model is relocating the centroids to the average coordinates of the points that belong to each centroid after each epoch, until it converges or a certain number of 'epochs' is accomplished.

---

#### Q3: How will you interpret the model's results?

[Here we should have one common answer]

---

#### Q4: What twist do you plan on adding? Why do you think this will be a good addition to your model?

1. **Random Forest:** [AFC] 

2. **KNN:** [PH] 

3. **Clustering:** As we mentioned before, the main twist here will be to use the labeled data as a decision tree node after clustering eventhough we learned that Clustering was only for unsupervised learning. We will do this by checking the most frequent label of conflict within each cluster. For it, we will have to define a method for our imbalance dataset, otherwise many non-conflict labels will be classified as with conflict.


[^1]: We classify our label into different levels of conflict based on the distribution of counts across the data. Accordingly, we label samples with 0 when there are no conflicts, 1 when conflicts are 'low' (up to q1), 2 when conflicts are medium (between q1 and q3), and 3 when conflict are 'high' (at or above q3). 