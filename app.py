import dash
import dash_html_components as html
from flask import Flask
import geopandas
import pandas as pd
import folium

from data_processing import gdf_zold, gdf_erdo, gdf_erdopoint

maps = folium.Map(location = [47.49909, 19.03093], tiles='Stamen Toner', zoom_start = 12, min_zoom = 11)

style_function_zold = lambda x: {
    'fillColor': 'blue',
    'color': 'black',
    'weight': 1.5,
    'fillOpacity': 0.7
}

style_function_erdo = lambda x: {
    'fillColor': 'darkgreen',
    'color': 'black',
    'weight': 1.5,
    'fillOpacity': 0.7
}

tooltip_zold = folium.GeoJsonTooltip(
        fields=['Nev','kerulet', 'tipus'],
        aliases=['Név:', 'Kerület:', 'Típus:'],
        localize=True
    )

tooltip_erdo = folium.GeoJsonTooltip(
        fields=['tipus'],
        aliases=['Típus:'],
        localize=True
    )

tooltip_erdopoint = folium.GeoJsonTooltip(
        fields=['Nev','Kerület', 'tipus'],
        aliases=['Név:', 'Kerület:', 'Típus:'],
        localize=True
    )

highlight_function=lambda x: {'weight':2.5,'color':'yellow', 'dashArray':'1'}
gjson_zold = folium.GeoJson(gdf_zold, style_function_zold, highlight_function, tooltip = tooltip_zold).add_to(maps)
gjson_erdo = folium.GeoJson(gdf_erdo, style_function_erdo, highlight_function, tooltip = tooltip_erdo).add_to(maps)
gjson_erdo = folium.GeoJson(gdf_erdo, style_function_erdo).add_to(maps)
gjson_erdopoint = folium.GeoJson(gdf_erdopoint, tooltip =tooltip_erdopoint).add_to(maps)

#maps.save("budapest_zold.html")
html_string = maps.get_root().render()
#create APP

app = dash.Dash(__name__)


app.layout = html.Div([
    html.H1('Budapest zöldterületei és erdői'),
    html.Iframe(id='map', srcDoc=html_string, width='50%', height='600'),
    #html.Button(id='map-submit-button', n_clicks=0, children='Submit')
])


# @app.callback(
#     dash.dependencies.Output('map', 'srcDoc'),
#     [dash.dependencies.Input('map-submit-button', 'n_clicks')])
# def update_map(n_clicks):
#     if n_clicks is None:
#         return dash.no_update
#     else:
#     	return open('budapest_zold.html', 'r').read()

server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)