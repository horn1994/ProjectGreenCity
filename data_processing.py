import geopandas
import pandas as pd
import geojson
import folium
import shapely.geometry
from simpledbf import Dbf5
from shapely import wkt
from datetime import date


gdf_zold = pd.read_csv(r"C:\Users\T440s\Google Drive\rajk\rajkos_kurzusok\prog2\PROJECT\data\test\zoldter_pg_region.csv")
gdf_zold['geometry'] = gdf_zold['geometry'].apply(wkt.loads)
gdf_zold = geopandas.GeoDataFrame(gdf_zold)
gdf_zold.set_geometry('geometry', crs={'init': u'epsg:'+str(4326)}, inplace=True)
gdf_erdo = pd.read_csv(r"C:\Users\T440s\Google Drive\rajk\rajkos_kurzusok\prog2\PROJECT\data\test\erdo_pg_region.csv")
gdf_erdo['geometry'] = gdf_erdo['geometry'].apply(wkt.loads)
gdf_erdo = geopandas.GeoDataFrame(gdf_erdo)
gdf_erdo.set_geometry('geometry', crs={'init': u'epsg:'+str(4326)}, inplace=True)
gdf_erdopoint = pd.read_csv(r"C:\Users\T440s\Google Drive\rajk\rajkos_kurzusok\prog2\PROJECT\data\test\erdo_pt_point.csv")
gdf_erdopoint['geometry'] = gdf_erdopoint['geometry'].apply(wkt.loads)
gdf_erdopoint = geopandas.GeoDataFrame(gdf_erdopoint)
gdf_erdopoint.set_geometry('geometry', crs={'init': u'epsg:'+str(4326)}, inplace=True)
gdf_erdopoint.rename(columns = {'Kerület': 'kerulet'}, inplace = True)
#gdf_erdopoint.drop('Unnamed: 0', axis = 1, inplace = True)
#gdf_zold.drop('Unnamed: 0', axis = 1, inplace = True)
gdf_all = gdf_zold.append(gdf_erdopoint)

def create_data(gdf_all):
    
    start_date = date.fromisoformat("2020-06-05")  # this is the day of the first data
    today = date.today()
    day_since_start = (today - start_date).days
    
    load = False
    while load == False:
        try:
            new_data = pd.read_excel(
                r"C:\Users\T440s\Google Drive\rajk\rajkos_kurzusok\prog2\PROJECT\data\test\test{}.xlsx".format(
                    day_since_start
                )
            )
            load = True
        except:
            day_since_start -= 1

    gdf_combined = pd.merge(gdf_all, new_data, on=["Nev", "kerulet"], how="outer")
    gdf_combined["mean_visitors"] = gdf_combined.iloc[:, 11:].mean(axis=1).round(0)
    # gdf_combined["mean_visitors"] = gdf_combined["mean_visitors"]
    gdf_combined_filtered = (
        gdf_combined.set_index("Nev")
        .iloc[:, 10:-1]
        .rename(lambda x: str(x) + " óra", axis=1)
        .T
    )

    return gdf_combined, gdf_combined_filtered


gdf_combined, gdf_combined_filtered = create_data(gdf_all)


def create_agg_data(gdf_all):
    
    start_date = date.fromisoformat("2020-06-05")  # this is the day of the first data
    today = date.today()
    day_since_start = (today - start_date).days
    
    missing_file_count = 0
    load = False
    while load == False:
        try:
            new_data = pd.read_excel(
                r"C:\Users\T440s\Google Drive\rajk\rajkos_kurzusok\prog2\PROJECT\data\test\test{}.xlsx".format(
                    day_since_start
                )
            )
            load = True
        except FileNotFoundError:
            missing_file_count += 1
            day_since_start -= 1
            
    gdf_aggregated = new_data.iloc[:, 4:]
    for data in range(day_since_start-7, day_since_start): #1-6 ig megy, így a legújabb napnak nincs kétszeres súlya 
        try:
            read_new = pd.read_excel(
                r"C:\Users\T440s\Google Drive\rajk\rajkos_kurzusok\prog2\PROJECT\data\test\test{}.xlsx".format(
                    data
                )
            )
            gdf_aggregated += round(read_new.iloc[:, 4:])
        except FileNotFoundError:
            pass

    gdf_aggregated = round(gdf_aggregated / day_since_start)
    gdf_aggregated = pd.concat(
        [
            new_data.iloc[:, :4].reset_index(drop=True),
            gdf_aggregated.reset_index(drop=True),
        ],
        axis=1,
    )
    gdf_combined_aggregated = pd.merge(
        gdf_all, gdf_aggregated, on=["Nev", "kerulet"], how="outer"
    )
    gdf_combined_aggregated["mean_visitors"] = (
        gdf_combined_aggregated.iloc[:, 11:].mean(axis=1).round(0)
    )
    gdf_combined_aggregated_filtered = (
        gdf_combined_aggregated.set_index("Nev")
        .iloc[:, 10:-1]
        .rename(lambda x: str(x) + " óra", axis=1)
        .T
    )
    return gdf_aggregated, gdf_combined_aggregated, gdf_combined_aggregated_filtered


gdf_aggregated,gdf_combined_aggregated, gdf_combined_aggregated_filtered = create_agg_data(gdf_all)

def figure2():
    start_date = date.fromisoformat("2020-06-05")  # this is the day of the first data
    today = date.today()
    day_since_start = (today - start_date).days
    avg_visitors = []
    load = False
    while load == False:
        try:
            mean_visitors = pd.read_excel(
                r"C:\Users\T440s\Google Drive\rajk\rajkos_kurzusok\prog2\PROJECT\data\test\test{}.xlsx".format(
                    day_since_start
                )
            )
            mean_visitors['{}. nap'.format(day_since_start)] = mean_visitors.iloc[:,4:].mean(axis=1).round(0)
            mean_visitors = mean_visitors.set_index('Nev').iloc[:,-1:]
            load = True
        except FileNotFoundError:
            day_since_start -= 1
    for data in range(day_since_start-7, day_since_start): 
        try:
            read_new = pd.read_excel(
                r"C:\Users\T440s\Google Drive\rajk\rajkos_kurzusok\prog2\PROJECT\data\test\test{}.xlsx".format(
                    data
                )
            )
            read_new['{}. nap'.format(data)] = read_new.iloc[:,4:].mean(axis=1).round(0)
            read_new = read_new.set_index('Nev').iloc[:,-1:]
            mean_visitors = mean_visitors.merge(read_new, right_index=True, left_index=True)
            
        except FileNotFoundError:
            pass
    mean_visitors = mean_visitors.T.sort_index()
    return mean_visitors

mean_visitors = figure2()