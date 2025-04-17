Milestone 2: Data exploration
For Milestone 2, you will collect data to train your machine learning models so that you can investigate your research question. 

Find at least one dataset that has data relevant to your research question. Explore the dataset. Print or plot basic statistics, minimum and maximum values, etc. 

You should also begin thinking about how to clean your dataset. Are there missing or null values? Does the data have the correct types? Units?

Make sure you have enough examples to train models. The number of examples needed to train a model and get reasonable results depends on the model and the data. Simple models like logistic regression can perform well with a few hundred examples. Clean data without much noise also requires fewer examples. For this project, you will need 300-500 examples in order to train a model and get reasonable results. Ideally more. 

Think about the features you will use to train your models. What features are available to you in your dataset? You need at least 3-5 features. You also need to extract one additional feature from your data. What features could you create? Be creative and thoughtful. What features would help your model make predictions? You can manually extract the feature or use an automated tool. 

Given the data available, your initial research question might need to change. That is fine. 

This is also a good time to start your final report. For Milestone 6 (the final milestone) you will participate in a project fair and turn in a report that explains what you did over the course of your project. 

To complete Milestone 2 create a file named milestones/milestone2.md in your group repository. Write a short sentence with a new formulation of your research question and whether you had to change your proposal. In a new paragraph, write 100-200 words about your dataset, where you found it, what features you plan on using, the new feature you plan on extracting, etc. 

Upload the contents of your repo to the "Project Milestone 2" assignment on Gradescope. Milestone 2 is due 04/17 at 11:59pm. 

- Collect data:
    
    - Find at least one dataset
    - Print or plot basic statistics
    - Think about how to clean the dataset. Are there missing values? Correct types?
    - 300-500 examples at least.
    - Think Features to train the model. At least 3-5 features.
    - Extract one additional feature.

[Andres Camacho]
New project: 

Conflict remains a major barrier to development, stability, and humanitarian well-being, particularly in regions affected by environmental stress and resource scarcity. Understanding and predicting the spatial and temporal dynamics of conflict events can provide critical insights for policymakers, aid organizations, and local communities to better allocate resources, anticipate humanitarian crises, and design targeted interventions. Nigeria, given its complex dynamics of resource-driven conflicts, economic inequalities, and climate-induced stress, serves as an ideal context to explore how environmental and socioeconomic factors interact and influence conflict risks.


Description of data sources: 

    - UCDP: the Upsala conflict data registers georreferenced record of organized violence ecents, including state-bases conflicts, non-state conflicts, and one-sided violence with specific latitude/longitude and date.
    - ERA5 Reanalysis Data: Offers monthly aggregates and estimates of various atmospheric variables, including temperature, precipitation, and surface pressure, on a global (~31 km resolution).  ￼
    - Meta Relative Wealth Index (RWI): Predicts relative standard of living within countries using de-identified connectivity data and satellite imagery, provided at approximately 2.4 km resolution.  ￼
    - Hansen Global Forest Change Dataset: Supplies annual data on global forest extent and change from 2000 onwards, derived from Landsat imagery with a spatial resolution of approximately 30 meters per pixel.  ￼
    - NASA VIIRS Nighttime Lights: Captures nighttime light emissions to offer insights into human settlements and economic activity, with data available at a resolution of approximately 500 meters.

Methodology for data cleaning, integration and features: 

For Nigeria, we aim to divide the cotinent in grids of 50km x 50km, inside of which we would count the points of conflict to classify them as 'conflict' or 'no conflict' for an specific year. Environmental and socioeconomic features from the auxiliary datasets will be aggregated within these grid cells. To enhance our feature set, we will extract two aditional features: 

1. the year-over-year change in nighttime light intensity, serving as a proxy for economic development or decline.
2. the anomalies in temperature measured as temperature abnormally high or low (1 std deviation from long term trend)

Data cleaning steps will involve checking for missing values, ensuring consistent data types and units, and normalizing data distributions where necessary.

Final Features to Predict Conflict

The final predictive feature set will include:
    - Conflict prevalence:
        - Conflict occurrence to predict as bynary variable
        - Number of conflict events in prior years
    - Climate and Environmental Variables:
        - Average annual temperature
        - Max anual temperature
        - Annual precipitation totals
        - Surface pressure (mean annual values)
        - Forest cover loss (annual % change from Hansen dataset)
        - [new feature] Temperature anomaly (binary feature indicating abnormal deviation from historical norms)
	- Socioeconomic Variables:
        - Relative Wealth Index (average RWI within grid)
        - Nighttime lights intensity (annual mean)
        - [new feeture] Year-over-year change in nighttime light intensity (economic growth proxy)

By integrating these diverse and robust features, the project will produce meaningful insights into the drivers of conflict, facilitating accurate predictions and actionable strategies for conflict prevention and mitigation in Nigeria.


