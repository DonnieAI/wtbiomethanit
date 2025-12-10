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
            source: GSE - RIE
                        """)

# download data related to yearly data on bioethane
df_1=pd.read_csv("data/produzione_vs_capacita_biometano_italia.csv")

fig1 = make_subplots(
    rows=2,
    cols=1,
    shared_xaxes=True,
    vertical_spacing=0.12,
    row_heights=[0.6, 0.4],
    subplot_titles=(
        f" Production Growth  [bn Smc3/y] ",
        "Capacity vs Production [bn Smc3/y] "
    )
)


# ---- Step 2: Add the bar chart (cumulative production) ----

fig1.add_trace(
                go.Scatter(
                    x=df_1["YEAR"],
                    y=df_1["CUMULATIVEPRODUCTION(bn_Scm_y)"],
                    mode="lines+markers",  # Add markers to the line
                    name="Cumulative Production (bn Scm/y)",
                    line=dict(
                        color=palette_blue[4],
                        width=3,
                        dash="solid"
                    ),
                    marker=dict(
                        symbol="diamond",      # Marker shape
                        size=8,                # Marker size
                        color=palette_blue[4], # Same color as line (optional)
                        line=dict(
                            width=1,
                            color="white"      # Border around marker (optional)
                        )
                    ),
                    fill="tozeroy",  # <-- This fills the area between the curve and y=0
                    fillcolor="rgba(0, 116, 217, 0.2)"  # Optional: custom transparent fill color
                ),
                row=1,
                col=1
            )


fig1.add_trace(
                go.Bar(
                    x=df_1["YEAR"],
                    y=df_1["CUMULATIVEPRODUCTION(bn_Scm_y)"],
                    name="Cumulative Production",
                    marker=dict(
                        color=palette_blue[4]
                    )
                ),
                row=2,
                col=1
            )

fig1.add_trace(
            go.Bar(
                x=df_1["YEAR"],
                y=df_1["CUMULATIVECAPACITY(bn_Scm_y)"],
                name="Cumulative Capacity",
                marker=dict(
                    color=palette_green[4]
                )
            ),
            row=2,
            col=1
        )

# ---- Step 3: Add horizontal PNRR target line ----
PNRR_target = 5.3  #bn SM3Y
years = sorted(df_1["YEAR"].unique())

fig1.add_trace(
    go.Scatter(
        x=years,
        y=[PNRR_target] * len(years),
        mode="lines",
        name="🎯 PNRR Target",
        line=dict(color=palette_other[0], width=3, dash="longdash"),
    ),
    row=2,
    col=1
)

# ---- Step 4: Add horizontal DM2018 cap line ----
DM2018_cap = 1.1

fig1.add_trace(
                go.Scatter(
                    x=years,
                    y=[DM2018_cap] * len(years),
                    mode="lines",
                    name="🎯 DM2018 cap",
                    line=dict(color=palette_other[-1], width=4, dash="dashdot"),
                ),
                row=2,
                col=1
            )

# ---- Step 5: Update layout (optional, for better visuals) ----
fig1.update_layout(
                    title="Cumulative Production vs. Targets",
                    xaxis_title="Year",
                    yaxis_title="Cumulative Production (bn Scm/y)",
                    barmode="group",
                    template="plotly_white",
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=1.02,
                        xanchor="right",
                        x=1
                    )
                )

fig1.update_xaxes(showticklabels=True, row=1, col=1)
fig1.update_layout(height=1000) 
# Display in Streamlit
st.plotly_chart(fig1, use_container_width=True, key="subplot_breakdown_chart_1")
#---------------------------------
st.divider()
#---------------------------------
#NARRATIVE BOX
# Narrative text with f-string + HTML styling

Prd_value_2025=df_1.loc[df_1["YEAR"] == 2025, "CUMULATIVEPRODUCTION(bn_Scm_y)"].values[0]


narrative = f"""
<div style="
    border: 2px solid {palette_green[3]};
    padding: 15px;
    border-radius: 10px;
    background-color: rgba(255, 255, 255, 0.05);
    color: white;
">
<b>📊 Key Insights</b>

- Figures for 2025 based on projections  
- Current biomethane estimated production in 2025 is <span style="color:{palette_green[3]}">**{Prd_value_2025}** bn Smc/y with **115** plants in operation</span>  
- **{Prd_value_2025}** bn Smc/y are equivalent to {Prd_value_2025*10:.2f} TWh/y  
- D.M 2018 boosted the production from **{df_1.loc[df_1["YEAR"] == 2018, "CUMULATIVEPRODUCTION(bn_Scm_y)"].values[0]}** to **{df_1.loc[df_1["YEAR"] == 2025, "CUMULATIVEPRODUCTION(bn_Scm_y)"].values[0]}** bn Smc from 2018 to 2025  
- Target (PNRR): <span style="color:{palette_green[3]}">{PNRR_target} bn Smc/y</span>  

<b>💡 Interpretation:</b>  
- The sector is progressing, but still **below target**.  
- Additional investments or incentives are required to accelerate deployment.  
</div>
"""

st.markdown(narrative, unsafe_allow_html=True)

#---------------------------------
st.divider()
#---------------------------------


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
                        "OPERATION": palette_blue[0],
                        "QUALIFIED": palette_green[0]
                    }

custom_colors_accesso = {
                        "RETE":palette_blue[1],
                        "BIOLNG": palette_green[1],
                        "ALTRO":palette_other[1]
                    }

custom_colors_dieta = {
                        "FORSU": palette_blue[3],  # Gold
                        "AGRI": palette_green[3],   # Hot pink
                        "MISTO": palette_other[5]  # Medium purple (example if exists)
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
filtered_df = df.query("DECRETO == 'DM2018' and STATO in ['OPERATION', 'QUALIFIED']")
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
                        name=f"Total plants DM2018 = {total_plants_DM2018_int}"
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
filtered_df_2 = df.query("DECRETO == 'DM2022' and STATO in ['OPERATION', 'QUALIFIED']")
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
                        name=f"Total plants DM2022 = {total_plants_DM2022_int}"
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


