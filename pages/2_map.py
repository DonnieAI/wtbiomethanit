# Load shapefile
import os
import streamlit
import pandas as pd
import geopandas as gpd
import streamlit as st
import pydeck as pdk
#https://docs.streamlit.io/develop/api-reference/charts/st.pydeck_chart
#https://docs.mapbox.com/api/maps/styles/


st.set_page_config(page_title="map", layout="wide")
from utils import apply_style_and_logo
apply_style_and_logo()


st.title("Biomethane projects")
st.markdown("""
            ### 🗺️ GIS Location related to operation and planned projects 
                        """)
st.markdown(""" 
            source: GSE 
                        """)


gdf = gpd.read_file("data/Risultati_Aste.shp")
# type set up of data
gdf["Asta"] = pd.to_numeric(gdf["Asta"], errors="coerce")

# Reproject to WGS84 for web maps
gdf = gdf.to_crs(epsg=4326)

# Extract lat/lon
gdf["lon"] = gdf.geometry.x
gdf["lat"] = gdf.geometry.y


color_map = {
    1: [255, 0, 0, 200],    # Red
    2: [0, 255, 0, 200],    # Green
    3: [0, 0, 255, 200],    # Blue
    4: [255, 165, 0, 200],  # Orange
    5: [128, 0, 128, 200]   # Purple
}
gdf["color"] = gdf["Asta"].map(color_map)


# Create pydeck layer
layer = pdk.Layer(
    "ScatterplotLayer",
    data=gdf,
    get_position=["lon", "lat"],
    get_color="color",
    get_radius=3000
)

# Change map style here (instead of black)
view_state = pdk.ViewState(
    latitude=gdf["lat"].mean(),
    longitude=gdf["lon"].mean(),
    zoom=5
)

# Light basemap instead of black
deck = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
   # map_style="mapbox://styles/mapbox/outdoors-v12"  # <- Change here
)

st.pydeck_chart(deck)