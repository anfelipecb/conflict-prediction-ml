import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import matplotlib.pyplot as plt
from pathlib import Path

#Convert the csv of conflict to a geosjon or geopandas?
def convert_conflict_csv_to_geodataframe(csv_path, year_from=2006):
    """
    Convert a CSV file with conflict events to a GeoDataFrame
    IN:
        csv_path : str
        Path to the CSV file containing conflict data
        
    OUT:
        GeoDataFrame with Point geometries for each conflict event
    """
    # Read the CSV file
    df = pd.read_csv(csv_path, low_memory= False)
    df = df[df['year'] >= year_from]
    #  lat/lon columns exists as "latitude","longitude"
    required_cols = ['latitude', 'longitude', 'year']
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        raise ValueError(f"CSV missing required columns: {missing_cols}")
    
    # Create Point geometries from latitude and longitude
    geometry = [Point(xy) for xy in zip(df.longitude, df.latitude)]
    
    # Create GeoDataFrame
    conflict_gdf = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")
    
    print(f"Converted {len(conflict_gdf)} conflict events to GeoDataFrame")
    return conflict_gdf

# Lets start merging grids to conflicts (points to polygons)
def count_conflicts_by_grid_year(conflict_gdf, grid_gdf):
    """
    Count conflicts in each grid cell by year
    IN:
    conflict_gdf : GeoDataFrame
        GeoDataFrame of conflict points with 'year' column
    grid_gdf : GeoDataFrame
        GeoDataFrame of grid polygons
    OUT: 
    GeoDataFrame with grid polygons and conflict counts by year
    """
    # Ensure both GeoDataFrames have the same CRS
    if conflict_gdf.crs != grid_gdf.crs:
        conflict_gdf = conflict_gdf.to_crs(grid_gdf.crs)
    
    # Perform spatial join to determine which grid each point falls into
    joined = gpd.sjoin(conflict_gdf, grid_gdf, how="inner", predicate="within")
    
    # Group by GEOID and year, then count
    grid_id_col = 'GEOID'
    all_grids = grid_gdf[grid_id_col].unique()
    all_years = conflict_gdf['year'].unique()

    # Group by grid and year, count conflicts
    counts = (
        joined.groupby([grid_id_col, 'year'])
        .size()
        .reset_index(name='conflict_count')
    )

    # Create all possible grid-year combinations
    all_combinations = pd.MultiIndex.from_product(
        [all_grids, all_years], names=[grid_id_col, 'year']
    ).to_frame(index=False)

    # Merge counts with all combinations, fill missing with 0
    merged = all_combinations.merge(counts, on=[grid_id_col, 'year'], how='left')
    merged['conflict_count'] = merged['conflict_count'].fillna(0).astype(int)

    # Merge geometry back in
    result = merged.merge(grid_gdf[[grid_id_col, 'geometry']], on=grid_id_col, how='left')
    result_gdf = gpd.GeoDataFrame(result, geometry='geometry', crs=grid_gdf.crs)

    print(f"Created {len(result_gdf)} grid-year rows (long format)")
    return result_gdf

def merge_and_analyze_conflicts(conflict_csv_path, grid_geojson_path, output_path=None):
    """
    Main function to process conflict data and merge with grid polygons
    
    Parameters:
    -----------
    conflict_csv_path : str
        Path to CSV file with conflict events
    grid_geojson_path : str
        Path to GeoJSON file with grid polygons
    output_path : str, optional
        Path to save the output GeoJSON
        
    Returns:
    --------
    GeoDataFrame with grid polygons and conflict counts by year
    """
    # Load data
    conflict_gdf = convert_conflict_csv_to_geodataframe(conflict_csv_path)
    grid_gdf = gpd.read_file(grid_geojson_path)
    
    # Count conflicts by grid and year
    result = count_conflicts_by_grid_year(conflict_gdf, grid_gdf)
    
    # Save result if output_path is provided
    if output_path:
        result = result[['GEOID', 'year', 'conflict_count', 'geometry']]
        result.to_file(output_path, driver="GeoJSON")
        print(f"Saved result to {output_path}")
    
    return result

def merge_data_GEOID_year(file1, dataframe2):
    """
    merges a csv file with a datafeame based o grid_id_col and year
    """
    
    grid_id_col = 'GEOID'
    file1_df = pd.read_csv(file1)
    final = dataframe2.merge(file1_df, on=[grid_id_col, 'year'], how='left')
    
    return final
    
def merge_dataframe_geojson(df, geojson):
    """
    Merge RWI to DATAFRAME
    """
    grid_id_col = 'GEOID'
    #read the geojson 
    geojson_gdf = gpd.read_file(geojson)
    geojson_gdf = geojson_gdf[['GEOID','rwi_2021']]
    result = df.merge(geojson_gdf, on=[grid_id_col], how='left')
    
    return result

def clean_deforestation_file(csv_file):
    """
    Read the csv file to transform it from wide to long
    Returns a pandas df
    """
    
    df = pd.read_csv(csv_file)
    # Convert from wide to long format
    df_long = pd.melt(
    df,
    id_vars=['GEOID'],
    value_vars=[col for col in df.columns if col.startswith('loss_')],
    var_name='year',
    value_name='forest_loss'
    )
    df_long['year'] = df_long['year'].str.replace('loss_', '').astype(int)
    
    return df_long

    
    
    
def main(): 
    project_path = Path(__file__).parent.parent
    conflict_csv = project_path / "data/ucdp/GEDEvent_v24_1.csv"
    grid_geojson = project_path / "data/output/Africa_grid_50km.geojson" 
    #output_file = project_path / "data/output/grid_conflict.geojson"
    
    result_gdf = merge_and_analyze_conflicts(conflict_csv, grid_geojson)
    
    # Merge with Climate
    era5_path = project_path / "data/output/era5_yearly_climate.csv"
    result_gdf = merge_data_GEOID_year(era5_path, result_gdf)
    
    #Merge with RWI 
    rwi_path = project_path / "data/output/africa_with_rwi.geojson"
    result_gdf = merge_dataframe_geojson(result_gdf, rwi_path)
    
    #Deforestacion
    deforestation_path = project_path / "data/output/forest_cover_loss.csv"
    deforestation_df = clean_deforestation_file(deforestation_path)
    result_gdf = result_gdf.merge(deforestation_df, on = ['GEOID', 'year'], how = 'left')
    
    # Lights VIIRS 
    lights_path = project_path / "data/output/viirs_yearly_lights.csv"
    result_gdf = merge_data_GEOID_year(lights_path, result_gdf)
    
    #Aditional features
    result_gdf['accumulated_conflicts'] = result_gdf.groupby('GEOID')['conflict_count'].transform(
        lambda x: x.shift(1).fillna(0).cumsum()
    ).astype(int)

        
    # Calculate the historical mean temperature for each grid cell
    baseline_data = result_gdf[(result_gdf['year'] >= 2006) & (result_gdf['year'] <= 2018)].copy()
    temp_col = 'temp_mean'
    baseline_means = baseline_data.groupby('GEOID')[temp_col].mean().reset_index()
    baseline_means = baseline_means.rename(columns={temp_col: 'baseline_temp'})
    result_gdf = result_gdf.merge(baseline_means, on='GEOID', how='left')
    
    result_gdf['temp_deviation'] = result_gdf[temp_col] - result_gdf['baseline_temp']
    result_gdf = result_gdf.drop('baseline_temp', axis=1)
    
    
    #Save this final output:
    result_gdf.drop(columns=['geometry']).to_parquet(project_path / "data/output/grid_conflict_climate.parquet")
    # only 2019 - 2023
    result_gdf[(result_gdf['year'] >=2019) & (result_gdf['year'] <=2023)].drop(columns=['geometry']).to_parquet(project_path / "data/output/grid_conflict_climate_2019_23.parquet")

    # 2. WITH geometry (for Kepler.gl visualization)
    # Convert geometry to WKT format for parquet compatibility
    result_gdf_viz = result_gdf.copy()
    result_gdf_viz["geometry_wkt"] = result_gdf_viz["geometry"].apply(lambda x: x.wkt)

    # Save with geometry as WKT string (no raw geometry column in parquet)
    result_gdf_viz.drop(columns=["geometry"]).to_parquet(
        project_path / "data/output/grid_conflict_climate_with_geometry.parquet"
    )
    result_gdf_viz[
        (result_gdf_viz["year"] >= 2019) & (result_gdf_viz["year"] <= 2023)
    ].drop(columns=["geometry"]).to_parquet(
        project_path / "data/output/grid_conflict_climate_2019_23_with_geometry.parquet"
    )

    # 3. GeoJSON for Kepler.gl (large files — keep out of git; see .gitignore)
    result_gdf.to_file(
        project_path / "data/output/grid_conflict_climate_with_geometry.geojson",
        driver="GeoJSON",
    )
    result_gdf[
        (result_gdf["year"] >= 2019) & (result_gdf["year"] <= 2023)
    ].to_file(
        project_path / "data/output/grid_conflict_climate_2019_23_with_geometry.geojson",
        driver="GeoJSON",
    )


if __name__ == "__main__":
    main()