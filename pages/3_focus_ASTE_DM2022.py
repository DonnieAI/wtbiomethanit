import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px 
from pathlib import Path
from plotly.subplots import make_subplots

#https://docs.streamlit.io/develop/api-reference/charts/st.pydeck_chart
#https://docs.mapbox.com/api/maps/styles/

palette_blue = [
    "#A7D5F2",  # light blue
    "#94CCE8",
    "#81C3DD",
    "#6FBBD3",
    "#5DB2C8",
    "#A9DEF9",  # baby blue
]

palette_green = [
    "#6DC0B8",  # pastel teal
    "#7DCFA8",
    "#8DDC99",
    "#9CE98A",
    "#ABF67B",
    "#C9F9D3",  # mint green
    "#C4E17F",  # lime green
]

palette_other = [
    "#FFD7BA",  # pastel orange
    "#FFE29A",  # pastel yellow
    "#FFB6C1",  # pastel pink
    "#D7BDE2",  # pastel purple
    "#F6C6EA",  # light rose
    "#F7D794",  # peach
    "#E4C1F9",  # lavender
]

st.set_page_config(page_title="projects", layout="wide")
from utils import apply_style_and_logo
apply_style_and_logo()

st.title("Focus Aste D.M 2022")
st.markdown("""
            ### 🗺️ Plant Category
            
            """)
st.markdown(""" 
            source: GSE. RIE
                        """)

custom_colors_feedstock= {
    "FORSU": palette_blue[1],  # Soft pastel yellow
    "AGRI": palette_green[1],   # Powder blue
   
}

df=pd.read_csv("data/impianti_biometano_sintesi_aggregata.csv")
df = df.rename(columns={"DIETA": "FEEDSTOCK"})
# Create fig1 separately
fig1 = px.bar(
            df.query("DECRETO=='DM2022'"),
            y="NUM_IMPIANTI",
            x="ASTA",
            color="FEEDSTOCK",
            barmode="group",
            color_discrete_map=custom_colors_feedstock,
           # text_auto=True
        )
# Add fig1 traces to subplot position (row=1, col=1)

# Display in Streamlit
st.plotly_chart(fig1, use_container_width=True, key="subplot_breakdown_chart_1")

#---------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------
st.divider()  # <--- Streamlit's built-in separator
#---------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------

# Create fig1 separately
fig2 = px.bar(
            df.query("DECRETO=='DM2022'"),
            y="CAPACITA_MEDIA_smch",
            x="ASTA",
            color="FEEDSTOCK",
            barmode="group",
            color_discrete_map=custom_colors_feedstock,
            #text_auto=True
        )
# Add fig1 traces to subplot position (row=1, col=1)

# Display in Streamlit
st.plotly_chart(fig2, use_container_width=True, key="subplot_breakdown_chart_2")

df_tariffe=pd.read_csv("data/aste_tariffe_medie_risultanti.csv")

# Create figure with 2 rows
fig3= make_subplots(
    rows=2, cols=1,
    shared_xaxes=False,
    subplot_titles=("Aste - AGRICOLO", "Aste - FORSU")
)

# Filter for AGRICOLO
df_agricolo = df_tariffe.query("DIETA == 'AGRICOLO'")
fig3.add_trace(
    go.Bar(
        x=df_agricolo["ASTA"],
        y=df_agricolo["TARIFFA_PARTENZA"], 
        name="Partenza (AGRICOLO)", 
        marker_color=palette_blue[2],
        text=df_agricolo["TARIFFA_PARTENZA"],
        textposition="auto"),
    row=1, col=1
)
fig3.add_trace(
    go.Bar(
        x=df_agricolo["ASTA"],
        y=df_agricolo["MEDIA_TARIFFA"], 
        name="Media (AGRICOLO)", 
        marker_color=palette_green[2],
        text=df_agricolo["MEDIA_TARIFFA"],
        textposition="auto"),
    row=1, col=1
)

# Filter for FORSU
df_forsu = df_tariffe.query("DIETA == 'FORSU'")
fig3.add_trace(
    go.Bar(
        x=df_forsu["ASTA"], 
        y=df_forsu["TARIFFA_PARTENZA"], 
        name="Partenza (FORSU)", 
        text=df_forsu["TARIFFA_PARTENZA"],
        textposition="auto",
        marker_color=palette_blue[4]),
    row=2, col=1
)
fig3.add_trace(
    go.Bar(
        x=df_forsu["ASTA"], 
        y=df_forsu["MEDIA_TARIFFA"], 
        name="Media (FORSU)", 
        marker_color=palette_green[4],
        text=df_forsu["MEDIA_TARIFFA"],
        textposition="auto",),
    row=2, col=1
)

# Layout settings
fig3.update_layout(
    height=700,
    title="📊 Aste e Tariffe – AGRICOLO vs FORSU",
    showlegend=True,
    barmode="group"
)

# Show in Streamlit
st.plotly_chart(fig3, use_container_width=True)