# dashboard app Based on tutorial https://realpython.com/python-dash/
# http://localhost:8050 to view

# Import libraries
import dash
from dash import dcc
from dash import html
import pandas as pd
import dash_leaflet as dl
import dash_leaflet.express as dlx
import csv
from geojson import Feature, FeatureCollection, Point
import json

# Create an instance of the Dash class
app = dash.Dash(__name__)

# # Great mile end coffee shops
# coffee_shops = [
#    dict(name="In Gamba", lat=-33.828064, lon=151.11586),
#    dict(name="Cafe Olympico", lat=-33.828064, lon=151.11586),
#    dict(name="The Standard", lat=-33.828064, lon=151.11586),
# ]
#
# # Creating a geojson from the input points
# geojson_coffee = dlx.dicts_to_geojson(
#    [{**shop, **dict(tooltip=shop["name"])} for shop in coffee_shops]
# )

# load geojson into the app

with open("./property_map.json") as data:
    geo = json.load(data)

# this following block has no effect because you overwrite it in the next block
# Putting the map in our app layout
app.layout = dl.Map(
   [dl.TileLayer(), dl.GeoJSON(data='',
                               id="geojson",
                               zoomToBounds=True)],
   style={"width": "1000px", "height": "500px"},
)





# Data for dashboard
# data = pd.read_csv("avocado.csv")
# data = data.query("type == 'conventional' and region == 'Albany'")
# data["Date"] = pd.to_datetime(data["Date"], format="%Y-%m-%d")
# data.sort_values("Date", inplace=True)


# Defining the layout of the app
app.layout = html.Div(  # Dash HTML components
    children=[
        html.H1(children="Data visualisation",),     # H1 - heading
        html.P(     # P - Paragraph
            children="Properties that matches our search terms",
        ),
        dl.Map(
            [dl.TileLayer(), dl.GeoJSON(data=geo,
                                        id="geojson",
                                        zoomToBounds=True)],
            style={"width": "1000px", "height": "500px"},
        ),

     ]
)

if __name__ == "__main__":          # make it possible to run Dash application locally using Flask’s built-in server
    app.run_server(debug=True)      # enables the hot-reloading option in app

