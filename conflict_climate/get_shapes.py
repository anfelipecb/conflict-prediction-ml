import geopandas as gpd

def get_country_shapes(continent: str =  None):
    """
    Get the continent boundaries from geopandas world dataset
    In:
        continent (str)
    """
    
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    if continent:
        return world[world['continent'] == continent]


# load the data of countries boundaries
def main():
    africa = get_country_shapes(continent = 'Africa')
    print(f"Got {len(africa)} countries in Africa")

if __name__ == "__main__":
    main()
