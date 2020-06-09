import dash
import dash_html_components as html
from flask import Flask
import geopandas
import pandas as pd
import folium

import dash_core_components as dcc
import dash_html_components as html
import dash_table
import plotly.express as px

from dash.dependencies import Input, Output

from data_processing import gdf_zold, gdf_erdo, gdf_erdopoint,gdf_combined, gdf_combined_filtered, gdf_all, gdf_aggregated, gdf_combined_aggregated_filtered

maps = folium.Map(location = [47.49909, 19.03093], tiles='Stamen Toner', zoom_start = 12, min_zoom = 11.5)

style_function_zold = lambda x: {
    'fillColor': 'darkblue',
    'color': 'black',
    'weight': 1,
    'fillOpacity': 0.7
}

style_function_erdo = lambda x: {
    'fillColor': 'darkgreen',
    'color': 'black',
    'weight': 1,
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
        fields=['Nev','kerulet', 'tipus'],
        aliases=['Név:', 'Kerület:', 'Típus:'],
        localize=True
    )

highlight_function=lambda x: {'weight':2.5,'color':'yellow', 'dashArray':'1'}

gjson_erdo = folium.GeoJson(gdf_erdo, style_function_erdo).add_to(maps)
gjson_erdopoint = folium.GeoJson(gdf_all, tooltip =tooltip_erdopoint).add_to(maps)
gjson_zold = folium.GeoJson(gdf_zold, style_function_zold, highlight_function, tooltip = tooltip_zold).add_to(maps)

#maps.save("budapest_zold.html")
html_string = maps.get_root().render()

#create figures
figure1 = px.bar(
    gdf_combined_filtered,
    x=gdf_combined_filtered['Vérmezõ'].index,
    y = gdf_combined_filtered['Vérmezõ']
)

figure2 = px.bar(
    gdf_combined_aggregated_filtered,
    x=gdf_combined_aggregated_filtered['Vérmezõ'].index,
    y = gdf_combined_aggregated_filtered['Vérmezõ']
)
#create APP
external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


app.layout = html.Div( #style = {'backgroundColor': 'grey'},
	children = [ 
		html.H1('Budapest zöldterületei és erdői',style={'font-family':'Times New Roman'}), 
    	dcc.Dropdown(
    		id= 'park_name', 
    		options=[{"label": e, "value": e} for e in gdf_combined["Nev"].unique()],
    		placeholder = 'Válaszz egy parkot',
    	),
    	html.Div(
    		children =[
    					html.Iframe(
    							id='map', 
    							srcDoc=html_string, 
    							width = '100%',
    							height = 550,
     			 				style={'marginLeft': 0, 
    			 					'marginRight': 10, 
    			 					'marginTop': 10, 
    			 					'marginBottom': 10,
    			 					'border': 'none'}, 
    			 				)
    						]
    					),
    	html.Div(
    		className = "row",
    		children = [
    			html.Div(
    				className="six columns",
    				children =[
    					dcc.Graph(
    			 				id = 'plot2', 
    			 				figure = figure2,
    			 				style={'marginLeft': 0, 
    			 					'marginRight': 0, 
    			 					'marginTop': 10, 
    			 					'marginBottom': 10,
    			 					'width': 800,
    			 					'height': 600},							
    						),
    				], 
    			),
    			 html.Div(
    			 	className="six columns",
    			 	children = [
    			 		dcc.Graph(
    			 				id = 'plot1', 
    			 				figure = figure1,
    			 				style={'marginLeft': 0, 
    			 					'marginRight': 0, 
    			 					'marginTop': 10, 
    			 					'marginBottom': 10,
    			 					'width': 800,
    			 					'height': 600},
    			 			),
    			 		],
    			 	),
    			]
    		),
    	]
	)

### ezt még megkell oldani, hogy mindkétt callback működjön
# @app.callback(
#     dash.dependencies.Output("plot", "figure"),
#     [dash.dependencies.Input("park_name", "value")],
# )
@app.callback(
	[Output('map','srcDoc'),
	Output("plot2", "figure"),
	Output("plot1", "figure")],
    [Input('park_name', 'value')],

)


def update_map(value):
	if (value is None) or (value == "Válassz egy parkot"):
		bp_map = maps.get_root().render()
		fig = px.bar(gdf_combined_filtered, x=gdf_combined_filtered.index, y = gdf_combined_filtered['Vérmezõ'])
		fig.update_layout(yaxis_title="Vérmezõ")
		fig2 = px.bar(gdf_combined_aggregated_filtered, x=gdf_combined_aggregated_filtered.index, y = gdf_combined_aggregated_filtered['Vérmezõ'])
		fig2.update_layout(yaxis_title="Vérmezõ")
		return bp_map, fig, fig2
	else:
		bp_map = folium.Map(location = [gdf_all[gdf_all['Nev'] == value].centroid_lat, gdf_all[gdf_all['Nev'] == value].centroid_lon], tiles='Stamen Toner', zoom_start = 17, min_zoom = 11.5)
		gjson_erdo = folium.GeoJson(gdf_erdo, style_function_erdo).add_to(bp_map)
		gjson_erdopoint = folium.GeoJson(gdf_all, tooltip =tooltip_erdopoint).add_to(bp_map)
		gjson_zold = folium.GeoJson(gdf_zold, style_function_zold, highlight_function, tooltip = tooltip_zold).add_to(bp_map)
		bp_map = bp_map.get_root().render()
		filt_df = gdf_combined_filtered.loc[:, gdf_combined_filtered.columns.isin([value])]
		fig = px.bar(filt_df, x=filt_df.index, y = filt_df[value])
		filt_df2 = gdf_combined_aggregated_filtered.loc[:, gdf_combined_aggregated_filtered.columns.isin([value])]
		fig2 = px.bar(filt_df2, x=filt_df2.index, y = filt_df2[value])		
		return bp_map, fig, fig2


server = app.server
if __name__ == '__main__':
    app.run_server(debug=True)