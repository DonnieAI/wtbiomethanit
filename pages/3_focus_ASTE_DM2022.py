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
            ### 🗺️ Plant Breakdown
            
            """)
st.markdown(""" 
            source: GSE. RIE
                        """)

custom_colors_feedstock= {
                    "WASTE": palette_blue[1],  # Soft pastel yellow
                    "AGRI": palette_green[1],   # Powder blue
                
                }

df=pd.read_csv("data/impianti_biometano_sintesi_aggregata.csv")
df = df.rename(columns={"DIETA": "FEEDSTOCK"})
df_filtered = df.query("DECRETO == 'DM2022'")
# Create fig1 separately
fig1 = go.Figure()

# Loop through each feedstock type and add a Bar trace
for feedstock in df_filtered["FEEDSTOCK"].unique():
    df_sub = df_filtered[df_filtered["FEEDSTOCK"] == feedstock]
    fig1.add_trace(
        go.Bar(
            x=df_sub["ASTA"],
            y=df_sub["NUM_IMPIANTI"],
            name=feedstock,
            marker=dict(color=custom_colors_feedstock[feedstock])
        )
    )

# Update layout (optional)
fig1.update_layout(
    barmode="group",
    title="Numero Impianti per ASTA (DM2022)",
    xaxis_title="ASTA",
    yaxis_title="Numero Impianti",
    template="plotly_white"
)

# Display in Streamlit
st.plotly_chart(fig1, use_container_width=True, key="subplot_breakdown_chart_1")

#---------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------
st.divider()  # <--- Streamlit's built-in separator
#---------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------
st.markdown("""
            ### 🗺️ Plant Average Capacity (Smch)
            
            """)
st.markdown(""" 
            source: GSE. RIE
                        """)
# Create fig1 separately
fig2 = px.bar(
            df.query("DECRETO=='DM2022'"),
            y="CAPACITA_MEDIA_Smch",
            x="ASTA",
            color="FEEDSTOCK",
            barmode="group",
            color_discrete_map=custom_colors_feedstock,
            #text_auto=True
        )
# Add fig1 traces to subplot position (row=1, col=1)

# Display in Streamlit
st.plotly_chart(fig2, use_container_width=True, key="subplot_breakdown_chart_2")

#---------------------------------------------------------------------------------------------------------------------------
st.divider()  # <--- Streamlit's built-in separator
#------------------------------------------------------

st.markdown("""
            ### 🗺️ Tarif  (EUR/MWh)
            
            """)
st.markdown(""" 
            source: GSE. RIE
                        """)

df_tariffe=pd.read_csv("data/aste_tariffe_medie_risultanti.csv")

fig3 = make_subplots(
    rows=2, cols=1,
    shared_xaxes=False,
    subplot_titles=("Aste - AGRI", "Aste - WASTE")
)

# =========================
# AGRICOLO
# =========================
df_agricolo = df_tariffe.query("DIETA == 'AGRICOLO'")

fig3.add_trace(
    go.Scatter(
        x=df_agricolo["ASTA"],
        y=df_agricolo["TARIFFA_PARTENZA"],
        mode="lines+markers",
        name="Base (AGRI)",
        line=dict(color=palette_other[4]),
                marker=dict(
            symbol="diamond",      # Marker shape
            size=8),
        text=df_agricolo["TARIFFA_PARTENZA"],
        textposition="top center"
    ),
    row=1, col=1
)

fig3.add_trace(
    go.Scatter(
        x=df_agricolo["ASTA"],
        y=df_agricolo["MEDIA_TARIFFA"],
        mode="lines+markers",
        name="Average (AGRI)",
        line=dict(color=palette_green[4]),
        marker=dict(
            symbol="diamond",      # Marker shape
            size=8),
        
        text=df_agricolo["MEDIA_TARIFFA"],
        textposition="top center"
    ),
    row=1, col=1
)

# =========================
# FORSU
# =========================
df_forsu = df_tariffe.query("DIETA == 'FORSU'")

fig3.add_trace(
    go.Scatter(
        x=df_forsu["ASTA"],
        y=df_forsu["TARIFFA_PARTENZA"],
        mode="lines+markers",
        name="Base (FORSU)",
        line=dict(color=palette_other[3]),
        marker=dict(
            symbol="diamond",      # Marker shape
            size=8),
        text=df_forsu["TARIFFA_PARTENZA"],
        textposition="top center"
    ),
    row=2, col=1
)

fig3.add_trace(
    go.Scatter(
        x=df_forsu["ASTA"],
        y=df_forsu["MEDIA_TARIFFA"],
        mode="lines+markers",
        name="Average (FORSU)",
        line=dict(color=palette_blue[3]),
                marker=dict(
            symbol="diamond",      # Marker shape
            size=8),
        text=df_forsu["MEDIA_TARIFFA"],
        textposition="top center"
    ),
    row=2, col=1
)

# =========================
# Layout
# =========================
fig3.update_layout(
    height=700,
    title="Aste e Tariffe – AGRICOLO vs FORSU",
    showlegend=True
)

fig3.update_layout(
    yaxis_title="Tarif (€/MWh)",
    yaxis2_title="Tarif (€/MWh)"
)

# Show in Streamlit
st.plotly_chart(fig3, use_container_width=True)