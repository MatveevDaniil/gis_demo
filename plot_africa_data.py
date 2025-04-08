import geopandas as gpd
import matplotlib.pyplot as plt
import os

shapefile_dir = "downloads/Africa_GIS_Supporting_Data/a. Africa_GIS Shapefiles"

def get_shapes():
  return [f for f in os.listdir(shapefile_dir) if f.endswith('.shp')]

def plot_polys(shapefile='AFR_Political_ADM1_Boundaries.shp'):
  gdf = gpd.read_file(f"{shapefile_dir}/{shapefile}")

  if gdf.geometry.iloc[0].geom_type == 'Polygon':
    gdf['area'] = gdf.geometry.area

  gdf.plot(
    column='area', 
    legend=True,
    legend_kwds={
      'label': "Area",
      'orientation': "vertical" 
    }
  )
  plt.title("Geospatial Data Visualization")
  plt.show()

def plot_lines(shapefile='AFR_Infra_Transport_Rail.shp'):
  gdf = gpd.read_file(f"{shapefile_dir}/{shapefile}")

  if gdf.geometry.iloc[0].geom_type == 'LineString':
    gdf['length'] = gdf.geometry.length 

  gdf.plot(
    column='length',
    legend=True,
    legend_kwds={
        'label': "Length",
        'orientation': "vertical"
    }
  )
  plt.title("Line Features Visualization")
  plt.show()

def plot_points(shapefile='AFR_Political_Cities.shp'):
  gdf = gpd.read_file(f"{shapefile_dir}/{shapefile}")

  if gdf.geometry.iloc[0].geom_type == 'Point':
    gdf['size'] = 10

  gdf.plot(
    color='red',
    markersize=gdf['size'],
    legend=True
  )
  plt.title("Point Features Visualization")
  plt.show()


if __name__ == '__main__':
  plot_polys()
  plot_lines()
  plot_points()