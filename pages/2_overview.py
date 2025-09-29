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
#--------------------------------------------------------------------------------------------

st.title("Biomethane updated figures : overview")
st.markdown("""
            ### 📈 Biomethane production vs capacity 
            
            """)
st.markdown(""" 
            source: GSE. RIE
                        """)

df_1=pd.read_csv("data/produzione_vs_capacita_biometano_italia.csv")

# Convert to long format
df_long_1 = df_1.melt(
    id_vars="YEAR",
    value_vars=["PRODUCTION(bn_scm_y)", "CAPACITY(bn_scm_y)"],
    var_name="Metric",
    value_name="Value"
)



metric_rename = {
    "PRODUCTION(bn_scm_y)": "Production",
    "CAPACITY(bn_scm_y)": "Capacity"
}

df_long_1["Metric_label"] = df_long_1["Metric"].replace(metric_rename)
custom_colors_fig1 = {
    "Production":palette_blue[0],
    "Capacity": palette_green[0]
}
# ---- Step 1: Plot the bar chart ----
fig1 = px.bar(
            df_long_1,
            x="YEAR",
            y="Value",
            color="Metric_label",
            barmode="group",
            color_discrete_map=custom_colors_fig1,
            text_auto=True
)

# ---- Step 2: Format layout ----
fig1.update_layout(
            title="Production vs Capacity over Years [bn smc/y]",
            xaxis_title="Year",
            yaxis_title="Biomethane Quantity [bn smc/y]",
            bargap=0.1,
            xaxis_tickangle=0,
            xaxis=dict(
                tickmode='linear',
                dtick=1  # ensure every year shows
            ),
            height=500
)

# ---- Step 3: Add horizontal PNRR target line ----
PNRR_target = 5.3
years = sorted(df_long_1["YEAR"].unique())
fig1.add_trace(
            go.Scatter(
                x=years,
                y=[PNRR_target] * len(years),
                mode="lines",
                name=f"🎯 PNRR Target",
                line=dict(color=palette_other[0], width=3,dash="longdash"),
            )
        )
DM2018_cap = 1.1  # max mil Smc3/y
fig1.add_trace(
            go.Scatter(
                x=years,
                y=[DM2018_cap] * len(years),
                mode="lines",
                name=f"🎯 DM2018 cap",
                line=dict(color=palette_other[-1], width=4,dash="dashdot"),
            )
        )

# Display in Streamlit
st.plotly_chart(fig1, use_container_width=True, key="subplot_breakdown_chart_1")

st.markdown("""
            ### 🌱 Number of Biomethane Plants
            
            """)
st.markdown(""" 
            source: GSE , RIE
                        """)

df_long_2 = df_1.melt(
    id_vars="YEAR",
    value_vars=["PLANTS", "BIOLNG"],
    var_name="Metric",
    value_name="Value"
)

custom_colors_fig2 = {
    "PLANTS": palette_blue[1],
    "BIOLNG":palette_green[1]
}

fig2 = px.bar(
    df_long_2,
    x="YEAR",
    y="Value",
    color="Metric",
    barmode="group",
    color_discrete_map=custom_colors_fig2,
    text_auto=True
)

fig2.update_layout(
    title="Biomethane Plants Number",
    xaxis_title="Year",
    yaxis_title="Plants [#]",
    bargap=0.1
)

fig2.update_layout(
    xaxis_tickangle=-0
)

fig2.update_layout(
    xaxis=dict(
        tickmode='linear',   # ensures all years show up (if numeric and evenly spaced)
        dtick=1              # show every year (increment = 1)
    )
)

st.plotly_chart(fig2, use_container_width=True, key="subplot_breakdown_chart_33")


#NARRATIVE BOX
# Narrative text with f-string + HTML styling
narrative = f"""
<div style="
    border: 2px solid {palette_green[3]};
    padding: 15px;
    border-radius: 10px;
    background-color: rgba(255, 255, 255, 0.05);
    color: white;
">
<b>📊 Key Insights</b>

- Figures for 2025 and 2026 are based on projections 
- D.M 2018 boosted the production from **{df_1.loc[df_1["YEAR"] == 2018, "PRODUCTION(bn_scm_y)"].values[0]}** to **{df_1.loc[df_1["YEAR"] == 2024, "PRODUCTION(bn_scm_y)"].values[0]}** bsmc from 2018 to 2024
- Current biomethane thoerica capacity : **{df_1.loc[df_1["YEAR"] == 2025, "CAPACITY(bn_scm_y)"].values[0]}** bn Smc/y</span>  
- Target (PNRR): <span style="color:{palette_green[3]}">{PNRR_target} bn Smc/y</span>  
- Gap to close: <span style="color:{palette_green[3]}">{PNRR_target - PNRR_target:.1f} bn Smc/y</span>  

<b>💡 Interpretation:</b>  
- The sector is progressing, but still **below target**.  
- Additional investments or incentives are required to accelerate deployment.  
</div>
"""

st.markdown(narrative, unsafe_allow_html=True)

#---------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------
st.divider()  # <--- Streamlit's built-in separator
#---------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------


st.markdown("""
            ### 🗺️ Yearly incremental capacity [mSm3h]
            
            """)
st.markdown(""" 
            source: GSE , RIE
                        """)

dfB=pd.read_csv("data/capacita_installata.csv")

# Create fig1 separately
fig3 = px.bar(
    dfB,
    x="YEAR",
    y="INSTALLED_CAPACITY(mSm3h)",
    #color="DIETA",
    barmode="group",
    #color_discrete_map=custom_colors
)

fig3.update_layout(
    xaxis_tickangle=-0
)

fig3.update_layout(
    xaxis=dict(
        tickmode='linear',   # ensures all years show up (if numeric and evenly spaced)
        dtick=1              # show every year (increment = 1)
    )
)


# Display in Streamlit
st.plotly_chart(fig3, use_container_width=True, key="subplot_breakdown_chart_2")


#---------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------
st.divider()  # <--- Streamlit's built-in separator
#---------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------

st.title("DM 2018 - Statistics and Analysis ")
st.markdown("""
            ### 🗺️ Figures related to the biomethane projects under the DM 2018
            
            """)
st.markdown(""" 
            source: GSE 
                        """)

#----------- Load data
df = pd.read_csv("data/impianti_biometano_sintesi_aggregata.csv")
#-------------------------------------
custom_colors_stato = {
    "ESERCIZIO": palette_blue[0],
    "COSTRUZIONE": palette_green[0]
 }

custom_colors_accesso = {
    "RETE":palette_blue[1],
    "BIOLNG": palette_green[1],
    "ALTRO":palette_other[1]
}

custom_colors_dieta = {
    "FORSU": palette_blue[2],  # Gold
    "AGRI": palette_green[2],   # Hot pink
    "MISTO": palette_other[2]  # Medium purple (example if exists)
}

# Initialize 3-column subplot (xy for bar, domain for pies)
figDM2018 = make_subplots(
    rows=1, cols=3,
    subplot_titles=("STATUS",
                    "ACCES",
                    "FEEDSTOCK"),
    specs=[[{"type": "xy"}, {"type": "domain"}, {"type": "domain"}]]
)

# Total impianti for horizontal line
total_plants_DM2018 = df.query("DECRETO == 'DM2018'")["NUM_IMPIANTI"].sum()

# Grouped data for bar chart
filtered_df = df.query("DECRETO == 'DM2018' and STATO in ['ESERCIZIO', 'COSTRUZIONE']")
agg_df = filtered_df.groupby(['TIPO', 'STATO'], as_index=False)['NUM_IMPIANTI'].sum()

# ------------------ BAR CHART ------------------
bar_chart_2018 = px.bar(
    agg_df,
    x="TIPO",
    y="NUM_IMPIANTI",
    color="STATO",
    barmode="group",
    color_discrete_map=custom_colors_stato,
    text_auto=True,
)

# Add bar chart traces
for trace in bar_chart_2018.data:
    figDM2018.add_trace(trace, row=1, col=1)


total_plants_DM2018_int = int(total_plants_DM2018)
# Add horizontal reference line to bar chart
figDM2018.add_trace(
    go.Scatter(
        x=agg_df["TIPO"].unique(),
        y=[total_plants_DM2018_int] * len(agg_df["TIPO"].unique()),
        mode="lines",
        line=dict(color="#FFB347", width=5),  # pastel orange + thickness 5
        name=f"Totale impianti DM2018 = {total_plants_DM2018_int}"
    ),
    row=1, col=1
)

# Add annotation directly on the bar chart (row=1, col=1)
figDM2018.add_annotation(
    x=0.12,  # center of chart
    y=total_plants_DM2018_int + (0.05 * total_plants_DM2018_int),  # a bit above the line
    xref="paper",
    yref="y1",
    text=f"<b>TOTAL: {total_plants_DM2018_int}</b>",
    showarrow=False,
    font=dict(color="#FFB347", size=14),
    bgcolor="rgba(255,179,71,0.2)",  # optional pastel background
    bordercolor="#FFB347",
    borderwidth=1
)


# ------------------ PIE CHART: ACCESSO ------------------
pie2018_1_df = df.query("DECRETO == 'DM2018'").groupby('ACCESSO', as_index=False)['NUM_IMPIANTI'].sum()

pie1_colors = [custom_colors_accesso.get(a, "#CCCCCC") for a in pie2018_1_df["ACCESSO"]]

figDM2018.add_trace(
    go.Pie(
        labels=pie2018_1_df ["ACCESSO"],
        values=pie2018_1_df ["NUM_IMPIANTI"],
        hole=0.4,
        textinfo='percent+label+value',
        marker=dict(colors=pie1_colors),
        name="Accesso"
    ),
    row=1, col=2
)

# ------------------ PIE CHART: DIETA ------------------
pie2018_2_df = df.query("DECRETO == 'DM2018'").groupby('DIETA', as_index=False)['NUM_IMPIANTI'].sum()

pie2_colors = [custom_colors_dieta.get(d, "#CCCCCC") for d in pie2018_2_df["DIETA"]]

figDM2018.add_trace(
    go.Pie(
        labels=pie2018_2_df["DIETA"],
        values=pie2018_2_df["NUM_IMPIANTI"],
        hole=0.4,
        textinfo='percent+label+value',
        marker=dict(colors=pie2_colors),
        name="Dieta"
    ),
    row=1, col=3
)

# ------------------ Layout ------------------
figDM2018.update_layout(
    height=600,
    width=1200,
    title_text="DM 2018 - Statistics",
    showlegend=True
)

# Display in Streamlit
st.plotly_chart(figDM2018, use_container_width=True)

#NARRATIVE BOX
# Narrative text with f-string + HTML styling
narrative = f"""
<div style="
    border: 2px solid {palette_green[3]};
    padding: 15px;
    border-radius: 10px;
    background-color: rgba(255, 255, 255, 0.05);
    color: white;
">
<b>📊 Key Insights</b>

- Figures for 2025 and 2026 are based on projections 
- D.M 2018 boosted the production from **{df_1.loc[df_1["YEAR"] == 2018, "PRODUCTION(bn_scm_y)"].values[0]}** to **{df_1.loc[df_1["YEAR"] == 2024, "PRODUCTION(bn_scm_y)"].values[0]}** bsmc from 2018 to 2024
- Current biomethane thoerica capacity : **{df_1.loc[df_1["YEAR"] == 2025, "CAPACITY(bn_scm_y)"].values[0]}** bn Smc/y</span>  
- Target (PNRR): <span style="color:{palette_green[3]}">{PNRR_target} bn Smc/y</span>  
- Gap to close: <span style="color:{palette_green[3]}">{PNRR_target - PNRR_target:.1f} bn Smc/y</span>  

<b>💡 Interpretation:</b>  
- The sector is progressing, but still **below target**.  
- Additional investments or incentives are required to accelerate deployment.  
</div>
"""

st.markdown(narrative, unsafe_allow_html=True)

#---------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------
st.divider()  # <--- Streamlit's built-in separator
#---------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------

st.title("DM 2022 - Statistics and Analysis ")
st.markdown("""
            ### 🗺️ Figures related to the biomethane projects under the DM 2022
            
            """)
st.markdown(""" 
            source: GSE 
                        """)

#----------- Load data
df = pd.read_csv("data/impianti_biometano_sintesi_aggregata.csv")
#-------------------------------------
custom_colors_stato = {
    "ESERCIZIO": palette_blue[0],
    "COSTRUZIONE": palette_green[0]
 }

custom_colors_accesso = {
    "RETE":palette_blue[1],
    "BIOLNG": palette_green[1],
    "ALTRO":palette_other[1]
}

custom_colors_dieta = {
    "FORSU": palette_blue[2],  # Gold
    "AGRI": palette_green[2],   # Hot pink
    "MISTO": palette_other[2]  # Medium purple (example if exists)
}

# Initialize 3-column subplot (xy for bar, domain for pies)
figDM2022 = make_subplots(
    rows=1, cols=3,
    subplot_titles=("STATUS",
                    "ACCES",
                    "FEEDSTOCK"),
    specs=[[{"type": "xy"}, {"type": "domain"}, {"type": "domain"}]]
)

# Total impianti for horizontal line
total_plants_DM2022 = df.query("DECRETO == 'DM2022'")["NUM_IMPIANTI"].sum()

# Grouped data for bar chart
filtered_df_2 = df.query("DECRETO == 'DM2022' and STATO in ['ESERCIZIO', 'COSTRUZIONE']")
agg_df_2 = filtered_df_2.groupby(['TIPO', 'STATO'], as_index=False)['NUM_IMPIANTI'].sum()

# ------------------ BAR CHART ------------------
bar_chart_2022 = px.bar(
    agg_df_2,
            x="TIPO",
            y="NUM_IMPIANTI",
            color="STATO",
            barmode="group",
            color_discrete_map=custom_colors_stato,
            text_auto=True,
        )

# Add bar chart traces
for trace in bar_chart_2022.data:
    figDM2022.add_trace(trace, row=1, col=1)


total_plants_DM2022_int = int(total_plants_DM2022)
# Add horizontal reference line to bar chart
figDM2022.add_trace(
    go.Scatter(
        x=agg_df["TIPO"].unique(),
        y=[total_plants_DM2022_int] * len(agg_df["TIPO"].unique()),
        mode="lines",
        line=dict(color="#FFB347", width=5),  # pastel orange + thickness 5
        name=f"Totale impianti DM2022 = {total_plants_DM2022_int}"
    ),
    row=1, col=1
)

# Add annotation directly on the bar chart (row=1, col=1)
figDM2022.add_annotation(
    x=0.12,  # center of chart
    y=total_plants_DM2022_int + (0.05 * total_plants_DM2022_int),  # a bit above the line
    xref="paper",
    yref="y1",
    text=f"<b>TOTAL: {total_plants_DM2022_int}</b>",
    showarrow=False,
    font=dict(color="#FFB347", size=14),
    bgcolor="rgba(255,179,71,0.2)",  # optional pastel background
    bordercolor="#FFB347",
    borderwidth=1
)


# ------------------ PIE CHART: ACCESSO ------------------
pie2022_1_df = df.query("DECRETO == 'DM2022'").groupby('ACCESSO', as_index=False)['NUM_IMPIANTI'].sum()

pie1_colors = [custom_colors_accesso.get(a, "#CCCCCC") for a in pie2022_1_df["ACCESSO"]]

figDM2022.add_trace(
    go.Pie(
        labels=pie2022_1_df ["ACCESSO"],
        values=pie2022_1_df ["NUM_IMPIANTI"],
        hole=0.4,
        textinfo='percent+label+value',
        marker=dict(colors=pie1_colors),
        name="Accesso"
    ),
    row=1, col=2
)

# ------------------ PIE CHART: DIETA ------------------
pie2022_2_df = df.query("DECRETO == 'DM2022'").groupby('DIETA', as_index=False)['NUM_IMPIANTI'].sum()

pie2_colors = [custom_colors_dieta.get(d, "#CCCCCC") for d in pie2022_2_df["DIETA"]]

figDM2022.add_trace(
    go.Pie(
        labels=pie2022_2_df["DIETA"],
        values=pie2022_2_df["NUM_IMPIANTI"],
        hole=0.4,
        textinfo='percent+label+value',
        marker=dict(colors=pie2_colors),
        name="Dieta"
    ),
    row=1, col=3
)

# ------------------ Layout ------------------
figDM2022.update_layout(
    height=600,
    width=1200,
    title_text="DM 2022 - Statistics",
    showlegend=True
)

# Display in Streamlit
st.plotly_chart(figDM2022, use_container_width=True)

#NARRATIVE BOX
# Narrative text with f-string + HTML styling
narrative = f"""
<div style="
    border: 2px solid {palette_green[3]};
    padding: 15px;
    border-radius: 10px;
    background-color: rgba(255, 255, 255, 0.05);
    color: white;
">
<b>📊 Key Insights</b>

- Figures for 2025 and 2026 are based on projections 
- D.M 2018 boosted the production from **{df_1.loc[df_1["YEAR"] == 2018, "PRODUCTION(bn_scm_y)"].values[0]}** to **{df_1.loc[df_1["YEAR"] == 2024, "PRODUCTION(bn_scm_y)"].values[0]}** bsmc from 2018 to 2024
- Current biomethane thoerica capacity : **{df_1.loc[df_1["YEAR"] == 2025, "CAPACITY(bn_scm_y)"].values[0]}** bn Smc/y</span>  
- Target (PNRR): <span style="color:{palette_green[3]}">{PNRR_target} bn Smc/y</span>  
- Gap to close: <span style="color:{palette_green[3]}">{PNRR_target - PNRR_target:.1f} bn Smc/y</span>  

<b>💡 Interpretation:</b>  
- The sector is progressing, but still **below target**.  
- Additional investments or incentives are required to accelerate deployment.  
</div>
"""

st.markdown(narrative, unsafe_allow_html=True)