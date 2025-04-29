import ee
import pathlib
import os
from datetime import datetime, timedelta
from typing import Dict, Any, List

def initialize_gee():
    """Initialize Earth Engine"""
    try:
        ee.Authenticate()
        ee.Initialize(project='climate-effects-453719')
        print("Successfully initialized Earth Engine")
    except Exception as e:
        print(f"Error initializing Earth Engine: {str(e)}")
        raise

def load_ee_asset(asset_path: str) -> ee.FeatureCollection:
    """Load a FeatureCollection from GEE asset"""
    return ee.FeatureCollection(asset_path)

def extract_era5_yearly_data(points_asset, start_year: int, end_year: int, output_path: str):
    """
    Extract yearly ERA5 data (mean/max 2m temperature, total precipitation, mean surface pressure)
    for each point in the asset, for the given year range.
    
    Args:
        start_date: Start year
        end_date: End year
        output_path: Path to save the output CSV file
    """
    # Load ERA5 collection
    era5 = ee.ImageCollection('ECMWF/ERA5_LAND/MONTHLY_AGGR')
    
    # Load schools feature collection from assets
    points = ee.FeatureCollection(points_asset)
    buffered_points = points.map(lambda f: f.buffer(25000))
    
    temp_band = 'temperature_2m'  # K
    temp_band_max = 'temperature_2m_max'  # K
    precip_band = 'total_precipitation_sum'    # m
    sp_band = 'surface_pressure'           # Pa
    
    # Prepare list of years
    years = list(range(start_year, end_year + 1))

    def yearly_aggregate(year):
        year = ee.Number(year)
        start = ee.Date.fromYMD(year, 1, 1)
        end = start.advance(1, 'year')
        
        # Filter monthly images for the year
        year_coll = era5.filterDate(start, end)
        
        # First check if the collection has images
        collection_size = year_coll.size()
        
        return ee.Algorithms.If(
        collection_size.gt(0),
        # When collection has data:
        ee.Image(
            year_coll.select(temp_band).mean().rename('temp_mean')
            .addBands(year_coll.select(temp_band_max).max().rename('temp_max'))
            .addBands(year_coll.select(precip_band).sum().rename('precip_total'))
            .addBands(year_coll.select(sp_band).mean().rename('sp_mean'))
            .set('year', year)
        ),
        # When collection is empty, return a placeholder image with the bands
        ee.Image.constant(0).rename('temp_mean')
        .addBands(ee.Image.constant(0).rename('temp_max'))
        .addBands(ee.Image.constant(0).rename('precip_total'))
        .addBands(ee.Image.constant(0).rename('sp_mean'))
        .set('year', year)
    )

    # Map over years to get yearly images
    yearly_images = ee.ImageCollection(ee.List(years).map(yearly_aggregate))

    # For each year, extract values at points
    def extract_for_year(image):
        year = ee.Number(image.get('year'))
        # Reduce at points
        reduced = image.reduceRegions(
            collection=buffered_points,
            reducer=ee.Reducer.first(),
            scale=27000  # ~27km
        )
        # Add year property to each feature
        return reduced.map(lambda f: f.set('year', year))

    # Flatten all yearly results
    all_results = yearly_images.map(extract_for_year).flatten()

    # Export columns
    export_columns = ['GEOID', 'year', 'temp_mean', 'temp_max', 'precip_total', 'sp_mean']

    # Export to Google Drive as CSV
    task = ee.batch.Export.table.toDrive(
        collection=all_results,
        description='ERA5_Yearly_Climate',
        folder='climate-data',
        fileNamePrefix='era5_yearly_climate',
        selectors=export_columns
    )
    task.start()
    print(f"Export task started: {task.status()}")
    return task

def main():
    # Set paths
    root_dir = pathlib.Path(__file__).parent.parent
    output_dir = root_dir / "data" / "output"
    output_dir.mkdir(exist_ok=True, parents=True)
    output_file = output_dir / "era5_yearly_climate_africa.csv"
    
    # Initialize Earth Engine
    initialize_gee()
    
    # Use your points asset (centroids)
    points_asset = 'projects/climate-effects-453719/assets/conflict_africa/Africa_points'

    # Last 20 years
    end_year = datetime.now().year - 1
    start_year = end_year - 19

    print(f"Extracting yearly ERA5 data for {start_year}-{end_year}...")
    task = extract_era5_yearly_data(points_asset, start_year, end_year, str(output_file))

    print("Task initiated. Monitor status in the GEE Code Editor:")
    print("https://code.earthengine.google.com/tasks")
    print(f"Once completed, download the CSV from Google Drive and move it to: {output_file}")

if __name__ == "__main__":
    main()
