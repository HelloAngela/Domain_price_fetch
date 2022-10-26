# dashboard app Based on tutorial https://realpython.com/python-dash/
# http://localhost:8050 to view

# Import libraries
import dash
from dash import dcc
from dash import html
import pandas as pd
import dash_leaflet as dl
import dash_leaflet.express as dlx
from geojson import Feature, FeatureCollection, Point
import json
from csv import DictReader

# Create an instance of the Dash class
app = dash.Dash(__name__)

# Example if creating geojson from dict
# coffee_shops = [
#    dict(name="In Gamba", lat=-33.828064, lon=151.11586),
#    dict(name="Cafe Olympico", lat=-33.828064, lon=151.11586),
#    dict(name="The Standard", lat=-33.828064, lon=151.11586),
# ]

# geojson input list of dict
with open("C:\\Users\\hello\\Dropbox\\Python\\property_list_combined.csv", 'r') as f:
    dict_reader = DictReader(f)
    list_of_dict = list(dict_reader)

# Creating a geojson from the input points, check https://dash-leaflet.herokuapp.com/
# Generate geojson with tooltip
geo = dlx.dicts_to_geojson([{**price, **dict(tooltip=price['lower_bound']+"-"+ price['upper_bound']+" m"+'<br>'
                                                     + price['listing.propertyDetails.displayableAddress'] + '<br>'
                                                     + price['listing.propertyDetails.bedrooms'] + " bed, "
                                                     + price['listing.propertyDetails.bathrooms'] + " bath" + '<br>',
                                             lon=price['listing.propertyDetails.longitude'],
                                             lat=price['listing.propertyDetails.latitude'])} for price in list_of_dict])


# load geojson file straight into the app
# with open("C:\\Users\\hello\\Dropbox\\Python\\property_map.json") as data:
#     geo = json.load(data)

# Putting the map in our app layout
# app.layout = dl.Map(
#    [dl.TileLayer(), dl.GeoJSON(data=mapping,
#                                id="geojson",
#                                zoomToBounds=True)],
#    style={"width": "1000px", "height": "500px"},
# )


# Defining the layout of the app
app.layout = html.Div(  # Dash HTML components
    children=[
        html.H1(children="Property price guide",),     # H1 - heading
        html.P(     # P - Paragraph
            children="For properties that matches our search terms",
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

