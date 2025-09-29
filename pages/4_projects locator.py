# Load shapefile
import os
import streamlit
import pandas as pd
import geopandas as gpd
import streamlit as st
import pydeck as pdk
#https://docs.streamlit.io/develop/api-reference/charts/st.pydeck_chart
#https://docs.mapbox.com/api/maps/styles/
#https://deckgl.readthedocs.io/en/latest/


st.set_page_config(page_title="map", layout="wide")
from utils import apply_style_and_logo
apply_style_and_logo()

st.title("Biomethane projects")
st.markdown("""
            ### 🗺️ GIS Location related to operation and planned projects (location based on Municipality)
                        """)
st.markdown(""" 
            source: Wavetransition database on GSE data 
                        """)

# DATA LOAD AND PREPARATION
# RISULTATI ASTE

# the shapefile has been already processsed using the data in teh database with QGIS based on city not exact coordinates
gdf = gpd.read_file("data/geo_data/Risultati_Aste.shp")
gdf["Asta"] = pd.to_numeric(gdf["Asta"], errors="coerce")
gdf = gdf.to_crs(epsg=4326)
gdf["lon"] = gdf.geometry.x
gdf["lat"] = gdf.geometry.y

# PUNTI IMMISSIONE RETE ATTIVI
pia_gdf = gpd.read_file("data/geo_data/Punti_Biometano_Immissione_Attivi.shp")
gdf["Asta"] = pd.to_numeric(gdf["Asta"], errors="coerce")
pia_gdf = pia_gdf.to_crs(epsg=4326)
pia_gdf["lon"] = pia_gdf.geometry.x
pia_gdf["lat"] = pia_gdf.geometry.y

# RETE SNAM DISPONIBILE
gas_grid_gdf=gpd.read_file("data/geo_data/IT_gas_network_EPSG4326.shp")
gas_grid_gdf=gas_grid_gdf.to_crs(epsg=4326)
# No need to extract lon/lat for lines
gas_grid_gdf["path"] = gas_grid_gdf.geometry.apply(lambda geom: list(geom.coords) if geom.geom_type == "LineString" else [])


# --- Controls: ASTA multiselect (not exclusive; default = all available 1..5) ---
ALL_ASTAS = [1, 2, 3, 4, 5]
available_astas = sorted(
    int(x) for x in gdf["Asta"].dropna().unique() if int(x) in ALL_ASTAS
)

selected_astas = st.multiselect(
    "Select ASTA number(s)",
    options=ALL_ASTAS,
    default=[],  # 👈 no ASTA selected by default
    help="Pick one or more ASTA numbers. Leave all selected to view everything."
)
if selected_astas:
    gdf_plot = gdf[gdf["Asta"].isin(selected_astas)].copy()
else:
    gdf_plot = gdf.iloc[0:0].copy()  # empty selection -> empty map
    st.info("No ASTA selected. Please pick at least one number.")

show_existing_inje_points = st.checkbox("📍 Current Gas Injection point", value=False)
show_layer_grid = st.checkbox("➖ Show available gas grid", value=False)

# Filter according to selection

# Color map per ASTA
color_map = {
    1: [173, 216, 230, 200],  # Pastel light blue
    2: [144, 238, 144, 200],  # Pastel light green
    3: [0, 191, 255, 200],    # Deep sky blue
    4: [152, 251, 152, 200],  # Pale green
    5: [64, 224, 208, 200],   # Turquoise
}


default_color = [200, 200, 200, 120]

gdf_plot["color"] = gdf_plot["Asta"].map(color_map)
gdf_plot["color"] = gdf_plot["color"].apply(
    lambda x: x if isinstance(x, (list, tuple)) else default_color
)

# Safe center: fall back to overall mean if filtered is empty
if len(gdf_plot) > 0:
    center_lat = float(gdf_plot["lat"].mean())
    center_lon = float(gdf_plot["lon"].mean())
    zoom_level = 5
else:
    center_lat = 42.5     # approx center of Italy
    center_lon = 12.5     # approx center of Italy
    zoom_level = 5        # or tweak to 4.8 for a wider view

# Ensure numeric + handle NaNs
gdf_plot["Capacita_m"] = pd.to_numeric(gdf_plot["Capacita_m"], errors="coerce").fillna(0)

# Clip to reasonable range (avoid outliers dominating)
low, high = gdf_plot["Capacita_m"].quantile([0.05, 0.95])
cap_clipped = gdf_plot["Capacita_m"].clip(lower=low, upper=high)

# Map to meters radius (e.g., 500 m .. 5000 m)
r_min, r_max = 500, 5000
gdf_plot["radius_m"] = r_min + (cap_clipped - low) / (high - low + 1e-9) * (r_max - r_min)



# Pydeck layer
layer = pdk.Layer(
    "ScatterplotLayer",
                data=gdf_plot,
                opacity=0.8,
                filled=True,
                stroked=True,
                get_position=["lon", "lat"],
                get_color="color",
                get_line_color=[0, 0, 0],
                line_width_min_pixels=1,

                get_radius="radius_m",
                radius_min_pixels=2,
                radius_max_pixels=80,

                pickable=True
)

additional_layer = None
if show_existing_inje_points:
                additional_layer = pdk.Layer(
                    "ScatterplotLayer",
                    data=pia_gdf,
                    get_position=["lon", "lat"],
                    #get_text='"▲"',
                    get_color=[255, 215, 0],  # Yellow color
                    get_radius=3000,
                    #get_alignment_baseline='"bottom"',
                    pickable=True
                )

additional_layer_2 = None
if show_layer_grid:
    additional_layer_2 = pdk.Layer(
                    "PathLayer",
                    data=gas_grid_gdf,
                    get_path="path",
                    get_color=[255, 215, 0],  # Black transparent lines
                    width_scale=10,
                    width_min_pixels=2,
                    pickable=False
                )

# Tooltip (shows ASTA; add more fields if you have them)
tooltip = {
    "html": """
        <b>ASTA:</b> {Asta} <br/>
        <b>Comune:</b> {Comune} <br/>
        <b>Capacita_m:</b> {Capacita_m} Smch
        <b>PUNTO DI E:</b> {RETE} <br/>
    """,
    "style": {
        "backgroundColor": "black",
        "color": "white",
        "fontSize": "12px"
    }
}



view_state = pdk.ViewState(
    latitude=center_lat,
    longitude=center_lon,
    zoom=5
)

layers = [layer]
if additional_layer:
    layers.append(additional_layer)
if additional_layer_2:
    layers.append(additional_layer_2)


deck = pdk.Deck(
    layers=layers,
    initial_view_state=view_state,
    tooltip=tooltip,
    #map_style="mapbox://styles/mapbox/light-v9",  # optional
    height=900  # 👈 taller map
)


st.pydeck_chart(deck)


# Optional: simple legend
legend_items = [
    ("#ADD8E6", "ASTA 1"),  # Light Blue
    ("#90EE90", "ASTA 2"),  # Light Green
    ("#00BFFF", "ASTA 3"),  # Deep Sky Blue
    ("#98FB98", "ASTA 4"),  # Pale Green
    ("#40E0D0", "ASTA 5"),  # Turquoise
]
st.markdown(
    " ".join(
        f"""<span style="display:inline-block;width:12px;height:12px;background:{c};margin-right:6px;border-radius:2px;"></span>
            <span style="margin-right:16px;">{lbl}</span>"""
        for c, lbl in legend_items if int(lbl.split()[-1]) in selected_astas
    ),
    unsafe_allow_html=True
)