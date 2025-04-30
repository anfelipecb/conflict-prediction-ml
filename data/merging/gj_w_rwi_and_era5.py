import json
import pandas as pd

# Load the GeoJSON
with open("data/output/africa_with_rwi.geojson", 'r', encoding='utf-8') as f:
    geojson_data = json.load(f)

# Load the CSV
csv_data = pd.read_csv("data/output/era5_yearly_climate.csv")

# Filter CSV for only 2021 entries
csv_2021 = csv_data[csv_data['year'] == 2021]

# Create a dictionary for quick lookup by GEOID
csv_dict = csv_2021.set_index('GEOID').to_dict(orient='index')

# Go through each feature in the GeoJSON and add the relevant CSV data
for feature in geojson_data['features']:
    geoid = feature['properties'].get('GEOID')
    
    # If this GEOID exists in the CSV 2021 data
    if geoid in csv_dict:
        csv_row = csv_dict[geoid]
        
        # Add the CSV columns as new properties, converting NaN to null
        feature['properties']['temp_mean'] = csv_row['temp_mean'] if pd.notna(csv_row['temp_mean']) else None
        feature['properties']['temp_max'] = csv_row['temp_max'] if pd.notna(csv_row['temp_max']) else None
        feature['properties']['precip_total'] = csv_row['precip_total'] if pd.notna(csv_row['precip_total']) else None
        feature['properties']['sp_mean'] = csv_row['sp_mean'] if pd.notna(csv_row['sp_mean']) else None

# Keys of interest to keep in the GeoJSON properties
keys_of_interest = [
    "featurecla", "scalerank", "LABELRANK", "SOVEREIGNT", "SOV_A3",
    "TYPE", "ADMIN", "NAME", "NAME_LONG", "BRK_NAME", "POP_EST",
    "GDP_MD", "ECONOMY", "INCOME_GRP", "ISO_A3", "UN_A3",
    "CONTINENT", "SUBREGION", "REGION_WB", "NAME_EN", "GEOID", "rwi_2021",
    "temp_mean", "temp_max", "precip_total", "sp_mean"
]

# Filter the properties of each feature to keep only the keys of interest
for feature in geojson_data['features']:
    feature['properties'] = {key: feature['properties'].get(key) for key in keys_of_interest if key in feature['properties']}

# Save the updated GeoJSON
with open("data/output/merged_rwi_era5_polygons.geojson", 'w', encoding='utf-8') as f:
    json.dump(geojson_data, f, ensure_ascii=False, indent=2)

print('✅ Done! Updated GeoJSON saved.')
