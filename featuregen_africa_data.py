import geopandas as gpd
import pandas as pd
import os
import matplotlib.pyplot as plt


shapefile_dir = "downloads/Africa_GIS_Supporting_Data/a. Africa_GIS Shapefiles"

def generate_adm1_features(shapefile_path, output_csv):
  gdf = gpd.read_file(shapefile_path)
  gdf['area'] = gdf.geometry.area
  gdf['perimeter'] = gdf.geometry.length
  gdf['centroid_x'] = gdf.geometry.centroid.x
  gdf['centroid_y'] = gdf.geometry.centroid.y
  gdf[['area', 'perimeter', 'centroid_x', 'centroid_y']].to_csv(output_csv, index=False)
  print(f"Features for ADM1 boundaries saved to {output_csv}")

def generate_rail_features(shapefile_path, output_csv):
  gdf = gpd.read_file(shapefile_path)
  gdf['bounding_box_area'] = gdf.geometry.envelope.area
  gdf[['Country', 'Shape_Leng', 'bounding_box_area']].to_csv(output_csv, index=False)
  print(f"Features for transport rail saved to {output_csv}")

def generate_city_features(shapefile_path, output_csv, boundary_shapefile_path):
    gdf_cities = gpd.read_file(shapefile_path)
    gdf_boundaries = gpd.read_file(boundary_shapefile_path)

    gdf_cities = gdf_cities.to_crs(epsg=3857)
    gdf_boundaries = gdf_boundaries.to_crs(epsg=3857)

    gdf_boundaries['boundary'] = gdf_boundaries.geometry.boundary

    gdf_cities = gdf_cities[gdf_cities.geometry.is_valid]
    gdf_boundaries = gdf_boundaries[gdf_boundaries.geometry.is_valid]

    def calculate_distance(city):
      country_name = city['Country']
      country_boundary = gdf_boundaries[gdf_boundaries['Country'] == country_name]
      if not country_boundary.empty:
          return country_boundary['boundary'].distance(city.geometry).min()
      return None

    gdf_cities['nearest_boundary_distance'] = gdf_cities.apply(calculate_distance, axis=1)

    gdf_cities[['City', 'Country', 'Latitude', 'Longitude', 'nearest_boundary_distance']].to_csv(output_csv, index=False)
    print(f"Features for political cities saved to {output_csv}")

# here scale is not consistent
def generate_country_border_images(shapefile_path, output_folder):
  gdf = gpd.read_file(shapefile_path)
  os.makedirs(output_folder, exist_ok=True)
  for country in gdf['Country'].unique():
    country_gdf = gdf[gdf['Country'] == country]
    fig, ax = plt.subplots(figsize=(5.12, 5.12))
    country_gdf.plot(ax=ax, color='black')
    ax.axis('off')
    image_path = os.path.join(output_folder, f"{country}.png")
    plt.savefig(image_path, bbox_inches='tight', pad_inches=0, dpi=100)
    plt.close()
  print(f"Country border images saved to {output_folder}")


if __name__ == "__main__":
  generate_adm1_features(
    shapefile_path=f"{shapefile_dir}/AFR_Political_ADM1_Boundaries.shp",
    output_csv="features/adm1_features.csv"
  )
  generate_rail_features(
    shapefile_path=f"{shapefile_dir}/AFR_Infra_Transport_Rail.shp",
    output_csv="features/rail_features.csv"
  )
  generate_city_features(
    shapefile_path=f"{shapefile_dir}/AFR_Political_Cities.shp",
    output_csv="features/city_features.csv",
    boundary_shapefile_path=f"{shapefile_dir}/AFR_Political_ADM0_Boundaries.shp"
  )
  generate_country_border_images(
    shapefile_path=f"{shapefile_dir}/AFR_Political_ADM1_Boundaries.shp",
    output_folder="features/country_border_images"
  )
