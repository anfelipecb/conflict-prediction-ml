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

def extract_forest_loss(points_asset, start_year=2001, end_year=2023, output_path=None):
    """
    Extract yearly forest cover loss for each point from Hansen dataset
    
    Args:
        points_asset: Path to points asset in GEE
        start_year: Start year for analysis (earliest 2001)
        end_year: End year for analysis (latest 2023)
        output_path: Path to save output CSV
    """
    # Load Hansen dataset
    hansen = ee.Image('UMD/hansen/global_forest_change_2023_v1_11')
    
    # Load points and buffer by 25km
    points = ee.FeatureCollection(points_asset)
    buffered_points = points.map(lambda f: f.buffer(25000))
    
    # Function to create yearly loss area for each year
    def process_year(year):
        # Hansen encodes loss year as (year - 2000)
        year_offset = ee.Number(year).subtract(2000)
        
        # Create binary mask for this year's loss
        # 1 where loss occurred in this year, 0 elsewhere
        year_mask = hansen.select('lossyear').eq(year_offset)
        
        # Get tree cover in 2000 (baseline)
        treecover = hansen.select('treecover2000')
        
        # Calculate area of loss in this year
        # Pixel area in hectares (~0.09 ha per 30m pixel at equator)
        pixel_area = ee.Image.pixelArea().divide(10000)  # convert m² to ha
        loss_area = year_mask.multiply(pixel_area)
        
        # Rename the band to reflect the year
        loss_area = loss_area.rename(f'loss_{year}')
        
        return loss_area
    
    # Generate loss area images for each year
    years = list(range(start_year, end_year + 1))
    loss_images = [process_year(year) for year in years]
    
    # Combine all year bands into one multi-band image
    all_years = ee.Image.cat(loss_images)
    
    # Reduce regions to get loss per point per year
    reduced = all_years.reduceRegions(
        collection=buffered_points,
        reducer=ee.Reducer.sum(),
        scale=30  # Hansen data is 30m resolution
    )
    
    # Export columns
    export_columns = ['GEOID'] + [f'loss_{year}' for year in years]
    
    # Export to Google Drive
    task = ee.batch.Export.table.toDrive(
        collection=reduced,
        description='Forest_Cover_Loss',
        folder='climate-data',
        fileNamePrefix='forest_cover_loss',
        selectors=export_columns
    )
    task.start()
    print(f"Export task started: {task.status()}")
    return task

def main():
    # Set up paths
    root_dir = pathlib.Path(__file__).parent.parent
    output_dir = root_dir / "data" / "output"
    output_dir.mkdir(exist_ok=True, parents=True)
    output_file = output_dir / "forest_cover_loss_africa.csv"
    
    # Initialize Earth Engine
    initialize_gee()
    
    # Use your points asset (centroids)
    points_asset = 'projects/climate-effects-453719/assets/conflict_africa/Africa_points'
    
    # Extract forest loss data (2001-2023)
    print("Extracting yearly forest cover loss...")
    task = extract_forest_loss(points_asset, start_year=2001, end_year=2023, output_path=str(output_file))
    
    print("Task initiated. Monitor status in the GEE Code Editor:")
    print("https://code.earthengine.google.com/tasks")
    print(f"Once completed, download the CSV from Google Drive and move it to: {output_file}")

if __name__ == "__main__":
    main()