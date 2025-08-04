# Load shapefile
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px 
from pathlib import Path
from plotly.subplots import make_subplots

#https://docs.streamlit.io/develop/api-reference/charts/st.pydeck_chart
#https://docs.mapbox.com/api/maps/styles/


st.set_page_config(page_title="projects", layout="wide")
from utils import apply_style_and_logo
apply_style_and_logo()


st.title("DM 2022 - Statistics and Analysis ")
st.markdown("""
            ### 🗺️ Figures related to the biomethane projects under the DM 2022
            
            """)
st.markdown(""" 
            source: GSE 
                        """)

df=pd.read_csv("data/impianti_biometano_sintesi_aggregata.csv")

custom_colors = {
    "energy": "#7FDBFF",  # Soft pastel yellow
    "taxes": "#77DD77",   # Powder blue
    "vat": "#8EE5EE"      # Muted salmon/peach  #66CDAA  #8EE5EE
}

# Create a single-subplot figure
# Create subplot with 1 row and 2 columns
# Create the subplot container
fig = make_subplots(
    rows=1, cols=2,
    subplot_titles=("DM 2018", "Plot B", "Plot D", "Plot C")
)

# Create fig1 separately
fig1 = px.bar(
    df.query("DECRETO=='DM2022'"),
    y="NUM_IMPIANTI",
    x="TIPO",
    color="DIETA",
    barmode="group",
    color_discrete_map=custom_colors
)

# Add fig1 traces to subplot position (row=1, col=1)
for trace in fig1.data:

    trace.showlegend = False      # Show for first subplot
    fig.add_trace(trace, row=1, col=1)

# Optionally, adjust layout
fig.update_layout(
    height=600,
    width=1000,
    showlegend=False
)

# Create fig1 separately
fig2 = px.bar(
    df.query("DECRETO=='DM2022'"),
    y="NUM_IMPIANTI",
    x="ACCESSO",
    color="DIETA",
    barmode="group",
    color_discrete_map=custom_colors
)
# Add fig1 traces to subplot position (row=1, col=1)
for trace in fig2.data:
    fig.add_trace(trace, row=1, col=2)

# Optionally, adjust layout
fig.update_layout(
    height=600,
    width=1000,
    showlegend=True
)

# Display in Streamlit
st.plotly_chart(fig, use_container_width=True, key="subplot_breakdown_chart")