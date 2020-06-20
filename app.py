import dash
import dash_html_components as html
from flask import Flask
import geopandas
import pandas as pd
import numpy as np
import folium

import dash_core_components as dcc
import dash_html_components as html
import dash_table
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output

from data_processing import (
    gdf_zold,
    gdf_erdo,
    gdf_erdopoint,
    gdf_combined,
    gdf_combined_filtered,
    gdf_all,
    gdf_aggregated,
    gdf_combined_aggregated,
    gdf_combined_aggregated_filtered,
    mean_visitors,
    gdf_combined_aggregated_adjusted,
    gdf_combined_aggregated_adjusted_trans,
)

maps = folium.Map(
    location=[47.49909, 19.03093], tiles="Stamen Toner", zoom_start=12, min_zoom=11
)

style_function_zold = lambda x: {
    "fillColor": "darkblue",
    "color": "black",
    "weight": 1,
    "fillOpacity": 0.7,
}

style_function_erdo = lambda x: {
    "fillColor": "darkgreen",
    "color": "black",
    "weight": 1,
    "fillOpacity": 0.7,
}

tooltip_zold = folium.GeoJsonTooltip(
    fields=["Nev", "kerulet", "tipus", "mean_visitors", "weighted_visitors"],
    aliases=["Név:", "Kerület:", "Típus:", "Átlagos látogatószám (heti):", "Látogató/négyzetméter (heti):"],
    localize=True,
)

tooltip_erdo = folium.GeoJsonTooltip(
    fields=["tipus"], aliases=["Típus:"], localize=True
)

# tooltip_erdopoint = folium.GeoJsonTooltip(
#         fields=['Nev','kerulet', 'tipus'],
#         aliases=['Név:', 'Kerület:', 'Típus:'],
#         localize=True
#     )

highlight_function = lambda x: {"weight": 2.5, "color": "yellow", "dashArray": "1"}

# gjson_erdo = folium.GeoJson(gdf_erdo, style_function_erdo, highlight_function, tooltip = tooltip_erdo).add_to(maps)
gjson_erdo = folium.GeoJson(gdf_erdo, style_function_erdo).add_to(maps)
gjson_erdopoint = folium.GeoJson(
    gdf_combined_aggregated, style_function_zold, tooltip=tooltip_zold
).add_to(maps)
# gjson_zold = folium.GeoJson(gdf_zold, style_function_zold, highlight_function, tooltip = tooltip_zold).add_to(maps)

# maps.save("budapest_zold.html")
html_string = maps.get_root().render()

# create figures
figure1 = go.Figure(
    data=[
        go.Bar(
            name="Átlagos heti látogatószám",
            x=gdf_combined_aggregated_filtered["Vérmezõ"].index,
            y=gdf_combined_aggregated_filtered["Vérmezõ"],
            marker_color="darkblue",
        ),
        go.Bar(
            name="Előző napi látogató szám",
            x=gdf_combined_filtered["Vérmezõ"].index,
            y=gdf_combined_filtered["Vérmezõ"],
            marker_color="darkgreen",
        ),
    ]
)

figure1.update_layout(
    title={
        "text": "Látogatók számának előző napi és átlagos előző heti óránkénti eloszlása",
        "y": 1,
        "x": 0.5,
        "xanchor": "center",
    },
    xaxis_title="Óránkénti látogatószám",
    yaxis_title="Vérmezõ",
    font=dict(
        # family="Courier New, monospace",
        size=12,
        # color="#7f7f7f"
    ),
    plot_bgcolor="rgba(0,0,0,0)",
    legend=dict(x=0, y=1),
)

figure2 = go.Figure(
    data=[
        go.Scatter(
            name="Átlagos heti látogatószám",
            x=mean_visitors["Vérmezõ"].index,
            y=mean_visitors["Vérmezõ"],
            marker_color="darkblue",
        ),
    ]
)
figure2.update_layout(
    title={
        "text": "Az előző hét napi átlagos látogatószáma",
        "y": 0.88,
        "x": 0.45,
        "xanchor": "center",
    },
    xaxis_title="Átlagos látogatószám",
    yaxis_title="Vérmezõ",
    font=dict(
        # family="Courier New, monospace",
        size=12,
        # color="#7f7f7f"
    ),
    plot_bgcolor="rgba(0,0,0,0)",
    legend=dict(x=0, y=1,),
)

figure3 = go.Figure(
    data=[
        go.Bar(
            name="Látógatók sűrűsége a park négyzetméretéhez képest",
            x=gdf_combined_aggregated_adjusted["Nev"],
            y=gdf_combined_aggregated_adjusted["weighted_visitors"],
            marker_color="darkgreen",
        )
        
    ]
)

figure3.update_layout(
    title={
        "text": "Látógatók sűrűsége a park négyzetméretéhez képest",
        "y": 1,
        "x": 0.5,
        "xanchor": "center",
    },
    xaxis_title="",
    yaxis_title="Sűrűság",
    font=dict(
        # family="Courier New, monospace",
        size=12,
        # color="#7f7f7f"
    ),
    plot_bgcolor="rgba(0,0,0,0)",
    legend=dict(x=0, y=1),
)

# create APP
external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(  # style = {'backgroundColor': 'grey'},
    children=[
        html.H1(
            "Budapest zöldterületei és erdői", style={"font-family": "Times New Roman"}
        ),
        dcc.Dropdown(
            id="park_name",
            options=[{"label": e, "value": e} for e in gdf_combined["Nev"].unique()],
            placeholder="Válaszz egy parkot",
        ),
        html.Div(
            children=[
                html.Iframe(
                    id="map",
                    srcDoc=html_string,
                    width="100%",
                    height=550,
                    style={
                        "marginLeft": 0,
                        "marginRight": 10,
                        "marginTop": 10,
                        "marginBottom": 10,
                        #'border': 'none'
                    },
                )
            ]
        ),
        html.Div(
            className="row",
            children=[
                html.Div(
                    className="six columns",
                    children=[
                        dcc.Graph(
                            id="plot2",
                            figure=figure2,
                            style={
                                "marginLeft": 0,
                                "marginRight": 0,
                                "marginTop": 10,
                                "marginBottom": 10,
                                #"width": 800,
                                "height": 600,
                            },
                        ),
                    ],
                ),
                html.Div(
                    className="six columns",
                    children=[
                        dcc.Graph(
                            id="plot1",
                            figure=figure1,
                            style={
                                "marginLeft": 0,
                                "marginRight": 0,
                                "marginTop": 10,
                                "marginBottom": 10,
                                #"width": 800,
                                "height": 600,
                            },
                        ),
                    ],
                ),
            ],
        ),
        dcc.Dropdown(
            id="zolterulet_name",
            options=[{"label": e, "value": e} for e in gdf_combined_aggregated_adjusted["Nev"].unique()],
            placeholder="Válassz egy parkot",
        ),
        html.Div(
             className="row",
             children=[
                html.Div(
                    className="twelve columns",
                    children=[
                        dcc.Graph(
                            id="plot3",
                            figure=figure3,
                            style={
                                "marginLeft": 0,
                                "marginRight": 0,
                                "marginTop": 10,
                                "marginBottom": 10,
                                #"width": 800,
                                "height": 600,
                    },
                        ),
                    ],
                ),
            ],
            ),
        ],
        )




@app.callback(
    [Output("map", "srcDoc"), Output("plot2", "figure"), Output("plot1", "figure"), Output("plot3", "figure")],
    [Input("park_name", "value"), Input("zolterulet_name", "value")],
)

def update_map(value, value2):
    if (value is None) or (value == "Válassz egy parkot"):
        bp_map = maps.get_root().render()
        gdf_combined_aggregated_filtered['Average'] = gdf_combined_aggregated_filtered.mean(axis = 1)
        gdf_combined_filtered['Average'] = gdf_combined_filtered.mean(axis = 1)
        figure1 = go.Figure(
            data=[
                go.Bar(
                    name="Átlagos heti látogatószám",
                    x=gdf_combined_aggregated_filtered["Average"].index,
                    y=gdf_combined_aggregated_filtered["Average"],
                    marker_color="darkblue",
                ),
                go.Bar(
                    name="Előző napi látogató szám",
                    x=gdf_combined_filtered["Average"].index,
                    y=gdf_combined_filtered["Average"],
                    marker_color="darkgreen",
                ),
            ]
        )

        figure1.update_layout(
            title={
                "text": "Látogatók számának előző napi és átlagos előző heti óránkénti eloszlása",
                "y": 0.88,
                "x": 0.5,
                "xanchor": "center",
            },
            xaxis_title="Óránkénti látogatószám",
            yaxis_title="Összes terület átlaga",
            font=dict(
                # family="Courier New, monospace",
                size=12,
                # color="#7f7f7f"
            ),
            plot_bgcolor="rgba(0,0,0,0)",
            legend=dict(x=0, y=1),
        )
        mean_visitors['Average'] = mean_visitors.mean(axis = 1)
        figure2 = go.Figure(
            data=[
                go.Scatter(
                    name="Átlagos heti látogatószám",
                    x=mean_visitors["Average"].index,
                    y=mean_visitors["Average"],
                    marker_color="darkblue",
                ),
            ]
        )
        figure2.update_layout(
            title={
                "text": "Az előző hét napi átlagos látogatószáma",
                "y": 0.88,
                "x": 0.45,
                "xanchor": "center",
            },
            xaxis_title="Átlagos látogatószám",
            yaxis_title="Összes terület átlaga",
            font=dict(
                # family="Courier New, monospace",
                size=12,
                # color="#7f7f7f"
            ),
            plot_bgcolor="rgba(0,0,0,0)",
            legend=dict(x=0, y=1,),
        )

    else:
        bp_map = folium.Map(
            location=[
                gdf_all[gdf_all["Nev"] == value].centroid_lat,
                gdf_all[gdf_all["Nev"] == value].centroid_lon,
            ],
            tiles="Stamen Toner",
            zoom_start=17,
            min_zoom=11.5,
        )
        gjson_erdo = folium.GeoJson(gdf_erdo, style_function_erdo).add_to(bp_map)
        gjson_erdopoint = folium.GeoJson(
            gdf_combined_aggregated, style_function_zold, tooltip=tooltip_zold
        ).add_to(bp_map)
        bp_map = bp_map.get_root().render()
        filt_df = gdf_combined_filtered.loc[
            :, gdf_combined_filtered.columns.isin([value])
        ]
        filt_df2 = gdf_combined_aggregated_filtered.loc[
            :, gdf_combined_aggregated_filtered.columns.isin([value])
        ]
        filt_df3 = mean_visitors.loc[:, mean_visitors.columns.isin([value])]
        # fig = px.bar(filt_df, x=filt_df.index, y = filt_df[value])
        figure1 = go.Figure(
            data=[
                go.Bar(
                    name="Átlagos heti látogatószám",
                    x=filt_df2.index,
                    y=filt_df2[value],
                    marker_color="darkblue",
                ),
                go.Bar(
                    name="Előző napi látogató szám",
                    x=filt_df.index,
                    y=filt_df[value],
                    marker_color="darkgreen",
                ),
            ]
        )

        figure1.update_layout(
            title={
                "text": "Látogatók számának előző napi és átlagos előző heti óránkénti eloszlása",
                "y": 0.88,
                "x": 0.5,
                "xanchor": "center",
            },
            xaxis_title="Óránkénti látogatószám",
            yaxis_title=value,
            font=dict(
                # family="Courier New, monospace",
                size=12,
                # color="#7f7f7f"
            ),
            plot_bgcolor="rgba(0,0,0,0)",
            legend=dict(x=0, y=1),
        )
        figure2 = go.Figure(
            data=[
                go.Scatter(
                    name="Átlagos heti látogatószám",
                    x=filt_df3.index,
                    y=filt_df3[value],
                    marker_color="darkblue",
                ),
            ]
        )
        figure2.update_layout(
            title={
                "text": "Az előző hét napi átlagos látogatószáma",
                "y": 0.88,
                "x": 0.45,
                "xanchor": "center",
            },
            xaxis_title="Átlagos látogatószám",
            yaxis_title=value,
            font=dict(
                # family="Courier New, monospace",
                size=12,
                # color="#7f7f7f"
            ),
            plot_bgcolor="rgba(0,0,0,0)",
            legend=dict(x=0, y=1,),
        )
    if (value2 is None) or (value2 == "Válassz egy parkot"):
        figure3 = go.Figure(
            data=[
                go.Bar(
                    name="Látógatók sűrűsége a park négyzetméretéhez képest",
                    x=gdf_combined_aggregated_adjusted["Nev"],
                    y=gdf_combined_aggregated_adjusted["weighted_visitors"],
                    marker_color="darkgreen",
                )]
        )

        figure3.update_layout(
            title={
                "text": "Látógatók sűrűsége a park négyzetméretéhez képest",
                "y": 1,
                "x": 0.5,
                "xanchor": "center",
            },
            xaxis_title="",
            yaxis_title="Sűrűság",
            font=dict(
                # family="Courier New, monospace",
                size=12,
                # color="#7f7f7f"
            ),
            plot_bgcolor="rgba(0,0,0,0)",
            legend=dict(x=0, y=1),
        )

        
    else:
        
        ind = np.where(gdf_combined_aggregated_adjusted["Nev"].values == value2)[0][0]
        indexer = slice(max(0, ind - 10), ind + 10)
        filt_df = gdf_combined_aggregated_adjusted.iloc[indexer, :]
        
        figure3 = go.Figure(
            data=[
                go.Bar(
                    name="Látógatók sűrűsége a park négyzetméretéhez képest",
                    x=filt_df["Nev"],
                    y=filt_df["weighted_visitors"],
                    marker_color="darkgreen",
                )]
        )

        figure3.update_layout(
            title={
                "text": "Látógatók sűrűsége a park négyzetméretéhez képest",
                "y": 1,
                "x": 0.5,
                "xanchor": "center",
            },
            xaxis_title="",
            yaxis_title="Sűrűség",
            font=dict(
                # family="Courier New, monospace",
                size=12,
                # color="#7f7f7f"
            ),
            plot_bgcolor="rgba(0,0,0,0)",
            legend=dict(x=0, y=1),
        )
        
       
    return bp_map, figure1, figure2, figure3





server = app.server
if __name__ == "__main__":
    app.run_server(debug=True)