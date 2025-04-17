
#### New project: 

Conflict remains a major barrier to development, stability, and humanitarian well-being, particularly in regions affected by environmental stress and resource scarcity. Understanding and predicting the spatial and temporal dynamics of conflict events can provide critical insights for policymakers, aid organizations, and local communities to better allocate resources, anticipate humanitarian crises, and design targeted interventions. Nigeria, given its complex dynamics of resource-driven conflicts, economic inequalities, and climate-induced stress, serves as an ideal context to explore how environmental and socioeconomic factors interact and influence conflict risks.


#### Description of data sources: 

    - UCDP: the Upsala conflict data registers georreferenced record of conflicts around the world with specific latitude/longitude and date.
    - ERA5 Reanalysis Data: Offers monthly aggregates and estimates of various atmospheric variables, including temperature, precipitation, and surface pressure, on a global (~31 km resolution).  ￼
    - Meta Relative Wealth Index (RWI): Predicts relative standard of living within countries using de-identified connectivity data and satellite imagery.
    - Hansen Global Forest Change Dataset: Supplies annual data on global forest extent and change from 2000's onwards.
    - NASA VIIRS Nighttime Lights: Captures nighttime light emissions to offer insights into human settlements and economic activity.

#### Methodology for data cleaning, integration and features: 

For Nigeria, we aim to divide the cotinent in grids of 50km x 50km, inside of which we would count the points of conflict to classify them as 'conflict' or 'no conflict' for an specific year. Environmental and socioeconomic features from the auxiliary datasets will be aggregated within these grid cells. To enhance our feature set, we will extract two aditional features: 

1. the year-over-year change in nighttime light intensity, serving as a proxy for economic development or decline.
2. the anomalies in temperature measured as temperature abnormally high or low (1 std deviation from long term trend)

Data cleaning steps will involve checking for missing values, ensuring consistent data types and units, and normalizing data distributions where necessary.

#### Final Features to Predict Conflict

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

By integrating these features, the project will produce meaningful insights into the drivers of conflict, facilitating accurate predictions and actionable strategies for conflict prevention and mitigation in Nigeria.


