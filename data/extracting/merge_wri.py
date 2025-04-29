import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

def main():
    # Load the DataFrame with point data
    df = pd.read_parquet("data/extracted/wealth_index.parquet")

    # Create a GeoDataFrame for the points
    points_gdf = gpd.GeoDataFrame(
        df,
        geometry=gpd.points_from_xy(df.longitude, df.latitude),
        crs="EPSG:4326"
    )

    # Load the GeoJSON containing the polygons
    polygons_gdf = gpd.read_file('data/output/Africa_grid_50km.geojson')
    polygons_gdf = polygons_gdf.to_crs(epsg=4326)

    # Spatial join: assign each point to a polygon
    joined = gpd.sjoin(points_gdf, polygons_gdf, how="inner", predicate="within")

    # Now, joined contains both point attributes + polygon attributes
    # Group by polygon ID and compute average RWI
    rwi_avg = joined.groupby('index_right')['rwi'].mean()

    # Assign the average RWI back to the polygons
    polygons_gdf['rwi'] = polygons_gdf.index.map(rwi_avg)

    # Save to file
    polygons_gdf.to_file("data/output/africa_with_rwi.geojson", driver="GeoJSON")

# Run it
main()

