import geopandas
import pandas as pd
import geojson
import folium
import shapely.geometry
from simpledbf import Dbf5
from shapely import wkt



gdf_zold = pd.read_csv("https://raw.githubusercontent.com/horn1994/ProjectGreenCity/master/test_data/zoldter_pg_region.csv")
gdf_zold['geometry'] = gdf_zold['geometry'].apply(wkt.loads)
gdf_zold = geopandas.GeoDataFrame(gdf_zold)
gdf_zold.set_geometry('geometry', crs={'init': u'epsg:'+str(4326)}, inplace=True)
gdf_erdo = pd.read_csv("https://raw.githubusercontent.com/horn1994/ProjectGreenCity/master/test_data/erdo_pg_region.csv")
gdf_erdo['geometry'] = gdf_erdo['geometry'].apply(wkt.loads)
gdf_erdo = geopandas.GeoDataFrame(gdf_erdo)
gdf_erdo.set_geometry('geometry', crs={'init': u'epsg:'+str(4326)}, inplace=True)
gdf_erdopoint = pd.read_csv("https://raw.githubusercontent.com/horn1994/ProjectGreenCity/master/test_data/erdo_pt_point.csv")
gdf_erdopoint['geometry'] = gdf_erdopoint['geometry'].apply(wkt.loads)
gdf_erdopoint = geopandas.GeoDataFrame(gdf_erdopoint)
gdf_erdopoint.set_geometry('geometry', crs={'init': u'epsg:'+str(4326)}, inplace=True)


