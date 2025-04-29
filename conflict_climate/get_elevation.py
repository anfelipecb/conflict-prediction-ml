import ee
import pathlib
from datetime import datetime

def initialize_gee():
    """Initialize Earth Engine"""
    try:
        ee.Authenticate()
        ee.Initialize(project='climate-effects-453719')
        print("Successfully initialized Earth Engine")
    except Exception as e:
        print(f"Error initializing Earth Engine: {str(e)}")
        raise

def extract_elevation(points_asset, output_path):
    """
    Extract mean elevation for each point (buffered) from SRTM DEM.
    """
    # use SRTM (global, 30m) or MERIT DEM (90m, global)
    dem = ee.Image('USGS/SRTMGL1_003')  # SRTM 30m
    # dem = ee.Image('COPERNICUS/DEM/GLO30')  #  to use Copernicus DEM 30m

    # Load points and buffer by 25km
    points = ee.FeatureCollection(points_asset)
    buffered_points = points.map(lambda f: f.buffer(25000))

    # Reduce mean elevation within each buffer
    reduced = dem.reduceRegions(
        collection=buffered_points,
        reducer=ee.Reducer.mean(),
        scale=30  # SRTM native resolution
    )

    # Export columns (adjust 'GEOID' if your ID field is different)
    export_columns = ['GEOID', 'mean']

    # Rename the 'mean' property to 'mean_elevation'
    reduced = reduced.map(lambda f: f.set('mean_elevation', f.get('mean')).select(['GEOID', 'mean_elevation']))

    # Export to Google Drive as CSV
    task = ee.batch.Export.table.toDrive(
        collection=reduced,
        description='Elevation_Mean',
        folder='climate-data',
        fileNamePrefix='elevation_mean',
        selectors=export_columns
    )
    task.start()
    print(f"Export task started: {task.status()}")
    return task

def main():
    root_dir = pathlib.Path(__file__).parent.parent
    output_dir = root_dir / "data" / "output"
    output_dir.mkdir(exist_ok=True, parents=True)
    output_file = output_dir / "elevation_mean_africa.csv"

    # Initialize Earth Engine
    initialize_gee()

    # Use your points asset (centroids)
    points_asset = 'projects/climate-effects-453719/assets/conflict_africa/Africa_points'

    print("Extracting mean elevation for buffered points...")
    task = extract_elevation(points_asset, str(output_file))

    print("Task initiated. Monitor status in the GEE Code Editor:")
    print("https://code.earthengine.google.com/tasks")
    print(f"Once completed, download the CSV from Google Drive and move it to: {output_file}")

if __name__ == "__main__":
    main()