import ee
import geemap
import geopandas as gpd
import pathlib
import os
import math
from typing import List
import time

def initialize_gee():
    """Initialize Earth Engine"""
    try:
        ee.Authenticate()
        ee.Initialize(project='climate-effects-453719')
        print("Successfully initialized Earth Engine")
    except Exception as e:
        print(f"Error initializing Earth Engine: {str(e)}")
        raise

def upload_geojson_to_ee(in_file: str, asset_id: str) -> None:
    """
    Upload a GeoJSON file to Earth Engine as a single asset
    
    Args:
        in_file: Path to GeoJSON file
        asset_id: Asset ID in Earth Engine
    """
    if not os.path.exists(in_file):
        raise FileNotFoundError(f"GeoJSON file not found: {in_file}")
    
    print(f"Loading {in_file}...")
    # Read the GeoJSON using geopandas
    gdf = gpd.read_file(in_file)
    print(f"Total features: {len(gdf)}")
    
    # Convert to ee.FeatureCollection
    print(f"Converting to Earth Engine FeatureCollection...")
    fc = geemap.geopandas_to_ee(gdf)
    
    # Export to Earth Engine
    print(f"Exporting to Earth Engine asset: {asset_id}...")
    task = ee.batch.Export.table.toAsset(
        collection=fc,
        description=os.path.basename(asset_id),
        assetId=asset_id
    )
    
    # Start the task
    task.start()
    print(f"Upload initiated. Task ID: {task.id}")
    
    # Monitor task status
    print("Monitoring task status...")
    while task.status()['state'] in ['READY', 'RUNNING']:
        print(f"Task status: {task.status()['state']}")
        time.sleep(5)
    
    final_state = task.status()['state']
    print(f"Final status: {final_state}")
    
    if final_state == 'COMPLETED':
        print(f"✅ Upload successful: {asset_id}")
    else:
        print(f"❌ Upload failed: {task.status()}")
        raise Exception("Failed to upload GeoJSON")
    
def main():
    # Initialize GEE
    initialize_gee()
    
    # Set up paths
    root_project = pathlib.Path(__file__).parent.parent
    
    # Local GeoJSON files
    points_geojson = root_project / "data/output/Africa_centroids_50km.geojson"
    grid_geojson = root_project / "data/output/Africa_grid_50km.geojson"
    
    # Earth Engine asset paths
    points_asset = "projects/climate-effects-453719/assets/conflict_africa/Africa_points"
    grid_asset = "projects/climate-effects-453719/assets/conflict_africa/Africa_grid"
    
   # Upload points data
    print("\n=== Uploading points Data ===")
    try:
        upload_geojson_to_ee(str(points_geojson), points_asset)
        print("\n✅ Grid points data uploaded successfully!")
    except Exception as e:
        print(f"\n❌ Error uploading points data: {str(e)}")
    
     # Upload grid polygons
    print("\n=== Uploading Grid Polygons Data ===")
    try:
        upload_geojson_to_ee(str(grid_geojson), grid_asset)
        print("\n✅ Grid polygons data uploaded successfully!")
    except Exception as e:
        print(f"\n❌ Error uploading grid polygons data: {str(e)}")
        
if __name__ == "__main__":
    main()