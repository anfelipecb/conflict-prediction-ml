import geopandas as gpd
import os
import numpy as np
from shapely.geometry import box
import urllib.request
import zipfile
import tempfile
from pathlib import Path

def get_country_shapes(continent: str = None, country: str = None, cache_dir="../data/raw"):
    """
    Get country boundaries from Natural Earth dataset
    
    Args:
        continent (str): Optional name of continent to filter by
        country (str): Optional name of country to filter by
        cache_dir (str): Directory to cache the downloaded shapefile
    
    Returns:
        GeoDataFrame: Filtered country boundaries
    """
    # Ensure cache directory exists
    os.makedirs(cache_dir, exist_ok=True)
    
    # Path for cached shapefile
    ne_file = os.path.join(cache_dir, "ne_110m_admin_0_countries.shp")
    
    # Download the data if it doesn't exist
    if not os.path.exists(ne_file):
        print("Downloading Natural Earth data...")
        url = "https://naturalearth.s3.amazonaws.com/110m_cultural/ne_110m_admin_0_countries.zip"
        
        # Create a temporary file for the zip download
        with tempfile.NamedTemporaryFile(delete=False, suffix=".zip") as temp_file:
            temp_path = temp_file.name
        
        # Add a custom User-Agent header to the request
        headers = {'User-Agent': 'Mozilla/5.0'}
        req = urllib.request.Request(url, headers=headers)
        
        # Download the zip file
        with urllib.request.urlopen(req) as response, open(temp_path, 'wb') as out_file:
            out_file.write(response.read())
        
        # Extract the zip file to the cache directory
        with zipfile.ZipFile(temp_path, 'r') as zip_ref:
            zip_ref.extractall(cache_dir)
            
        # Clean up the temporary file
        os.unlink(temp_path)
        print("Download complete.")
    
    # Read the shapefile
    world = gpd.read_file(ne_file)
    
    # Filter by continent if provided (using CONTINENT field in Natural Earth data)
    if continent:
        world = world[world['CONTINENT'] == continent]
    
    # Filter by country if provided (using NAME field in Natural Earth data)
    if country:
        world = world[world['NAME'] == country]
    
    return world


def create_grid(gdf, cell_size_km=50, output_folder="../data/output"):
    """
    Create a grid of polygons covering the geometry in the GeoDataFrame.
    
    Args:
        gdf (GeoDataFrame): GeoDataFrame with geometries to create a grid for
        cell_size_km (float): Approximate cell size in kilometers
        output_folder (str): Folder to save the output files
    
    Returns:
        GeoDataFrame: Grid polygons that intersect with the input geometries
    """
    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)
    
    # Get the total bounds of the GeoDataFrame
    minx, miny, maxx, maxy = gdf.total_bounds
    
    # Convert km to approximate decimal degrees (at the equator, 1 degree ≈ 111 km)
    cell_size_deg = cell_size_km / 111.0
    
    # Adjust for latitude (longitude distances vary with latitude)
    center_lat = (miny + maxy) / 2
    lon_factor = np.cos(np.radians(center_lat))
    cell_size_x = cell_size_deg / lon_factor  # Adjust longitude cell size
    cell_size_y = cell_size_deg  # Latitude cell size remains constant
    
    # Create grid cells
    grid_cells = []
    nx = int(np.ceil((maxx - minx) / cell_size_x))
    ny = int(np.ceil((maxy - miny) / cell_size_y))
    
    for i in range(nx):
        for j in range(ny):
            x1 = minx + i * cell_size_x
            y1 = miny + j * cell_size_y
            x2 = minx + (i + 1) * cell_size_x
            y2 = miny + (j + 1) * cell_size_y
            cell = box(x1, y1, x2, y2)
            grid_cells.append(cell)
    
    # Create a GeoDataFrame from the grid cells
    grid_gdf = gpd.GeoDataFrame(geometry=grid_cells, crs=gdf.crs)
    
    # Filter to keep only cells that intersect with the input geometries
    dissolved = gdf.dissolve().reset_index(drop=True)
    filtered_grid = gpd.sjoin(grid_gdf, dissolved, predicate='intersects').drop(columns=['index_right'])
    
    # Add a unique GEOID to each grid cell
    filtered_grid['GEOID'] = range(1, len(filtered_grid) + 1)
    
    # Extract centroids of the grid polygons
    centroids = filtered_grid.geometry.centroid
    centroids_gdf = gpd.GeoDataFrame(geometry=centroids, crs=gdf.crs)
    centroids_gdf['GEOID'] = filtered_grid['GEOID']
    
    # Determine region name for file naming
    region_name = "region"
    if 'CONTINENT' in gdf.columns and len(gdf['CONTINENT'].unique()) == 1:
        region_name = gdf['CONTINENT'].iloc[0]
    elif 'NAME' in gdf.columns and len(gdf['NAME'].unique()) == 1:
        region_name = gdf['NAME'].iloc[0]
    
    # Save the boundaries
    boundaries_path = os.path.join(output_folder, f"{region_name}_boundaries.geojson")
    gdf.to_file(boundaries_path, driver="GeoJSON")
    print(f"Saved boundaries to {boundaries_path}")
    
    # Save the grid
    grid_path = os.path.join(output_folder, f"{region_name}_grid_{cell_size_km}km.geojson")
    filtered_grid.to_file(grid_path, driver="GeoJSON")
    print(f"Saved grid to {grid_path}")
    
    # Save the centroids
    centroids_path = os.path.join(output_folder, f"{region_name}_centroids_{cell_size_km}km.geojson")
    centroids_gdf.to_file(centroids_path, driver="GeoJSON")
    print(f"Saved centroids to {centroids_path}")
    
    return filtered_grid

# load the data of countries boundaries
def main():
    raw_path = Path(__file__).parent.parent / "data/raw"
    
    continent = get_country_shapes(continent = 'Africa', cache_dir= raw_path)
    print(f"Got {len(continent)} countries in Africa")
    
    # Create standard 50km grid
    out_path = Path(__file__).parent.parent / "data/output"
    africa_grid = create_grid(continent, output_folder=out_path )
    print(f"Created grid with {len(africa_grid)} cells for Africa")
    
    # For an specific country and smaller grid size
    #kenya = get_country_shapes(country='Kenya')
    #kenya_grid = create_grid(kenya, cell_size_km=25)
    #print(f"Created grid with {len(kenya_grid)} cells for Kenya")


if __name__ == "__main__":
    main()
