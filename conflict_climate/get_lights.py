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

def extract_NASA_yearly_data(points_asset, start_year: int, end_year: int, output_path: str):
    """
    Extract yearly lights - from NASA data
    for each point in the asset, for the given year range.
    
    Args:
        start_date: Start year
        end_date: End year
        output_path: Path to save the output CSV file
    """
    # Load ERA5 collection
    viirs = ee.ImageCollection('NOAA/VIIRS/DNB/MONTHLY_V1/VCMSLCFG')
    
    # Load schools feature collection from assets
    points = ee.FeatureCollection(points_asset)
    buffered_points = points.map(lambda f: f.buffer(25000))
    
    lights_band = 'avg_rad'
    
    # Prepare list of years
    years = list(range(start_year, end_year + 1))

    def yearly_lights_aggregate(year):
        year = ee.Number(year)
        start = ee.Date.fromYMD(year, 1, 1)
        end = start.advance(1, 'year')
        year_coll = viirs.filterDate(start, end)
        # Aggregate: mean radiance for the year
        lights_mean = year_coll.select(lights_band).mean().rename('lights_mean')
        # Optionally, sum or max can also be calculated
        lights_sum = year_coll.select(lights_band).sum().rename('lights_sum')
        return lights_mean.addBands(lights_sum).set('year', year)

    # Map over years to get yearly images
    yearly_images = ee.ImageCollection(ee.List(years).map(yearly_lights_aggregate))

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
    export_columns = ['GEOID', 'year', 'lights_mean', 'lights_sum']

    # Export to Google Drive as CSV
    task = ee.batch.Export.table.toDrive(
        collection=all_results,
        description='VIIRS_Yearly_Lights',
        folder='climate-data',
        fileNamePrefix='viirs_yearly_lights',
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
    output_file = output_dir / "viirs_yearly_lights_africa.csv"
    
    # Initialize Earth Engine
    initialize_gee()
    
    # Use your points asset (centroids)
    points_asset = 'projects/climate-effects-453719/assets/conflict_africa/Africa_points'

    # Last 5 years
    end_year = datetime.now().year - 1
    start_year = end_year - 5

    print(f"Extracting yearly VIIRS lights data for {start_year}-{end_year}...")
    task = extract_NASA_yearly_data(points_asset, start_year, end_year, str(output_file))
    print("Task initiated. Monitor status in the GEE Code Editor:")
    print("https://code.earthengine.google.com/tasks")
    print(f"Once completed, download the CSV from Google Drive and move it to: {output_file}")
    
if __name__ == "__main__":
    main()