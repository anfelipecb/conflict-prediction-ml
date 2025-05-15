## Milestone 5: Training our model with non-linear models

First of all, we want you to remember our research question: 

**_Can the ocurrence of violence in a given geography be predicted using local socioeconomic and environmental data?_**

To answer it, we are using climate data from satellite images (temperature, precipitation, light radiance, deforestation, and surface pressure) and socioeconomic indicators (Relative Wealth Index, a measure of wealth distribution) to predict the level of conflict (no conflict, low, medium, high) in specific 50x50km polygon of Africa.

For this specific milestone, we are proposing our work guidelines to train non linear models. Specifically, we are developing three non-linear models to check which one performs better when predicting the level of conflict in 50x50km African grids using the mentioned attributes. The models to be trained are:

- Random Forest

- KNN

- Clustering

For each of this models, we will try to find the best hyperparameters that can make the model the best predictor.

Finally, we will use the model that best predicts among the three of them.

---

#### Q1: Which nonlinear model do you plan on implementing? Why?

1. **Random Forest:** [AFC] [Use pros/cons]

2. **KNN:** [PH] [Use pros/challenges]

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

[Here we should have one common answer]
