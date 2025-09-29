import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px 

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

st.title("Biomethane Revenues Comparison")
st.markdown("""
            ### 💵 Biomethane Revenues Analysis 
            
            """)
st.markdown(""" 
            source: WaveTransition 
                        """)

#----------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------
st.divider()  # <--- Streamlit's built-in separator
#----------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------
# --- Shared plant parameters ---
st.subheader("🏭 Plant characteristics")

col1, col2, col3 = st.columns(3)
with col1:
    smc_h = st.number_input("Capacity (Smc/h)", value=500, step=50)
    with col2:
        hours = st.number_input("Operating hours/year", value=8000, step=100)
    with col3:
        share_lng = st.slider("Share of bioLNG (%)", 0, 100, 50, step=5)

# Total Energy production (MWh)
smc_year = smc_h * hours
mwh_year = smc_year * 10.69 / 1000 # PCS 10.69 kWh/Smc


#bioCH4 to GRID
smc_to_grid=smc_year*(1-share_lng / 100)
smc_to_lng=smc_year-smc_to_grid

#For practical use in LCA or energy economics, you might use 13.5–13.8 kWh/kg for real bio-LNG.
mwh_lng = mwh_year * (share_lng / 100)
t_lng=mwh_lng/13.5


mwh_grid = mwh_year - mwh_lng


co2_t = smc_year * 1.96 / 1000 * 0.9 # t/year, 90% capture efficiency

#digestate_t = smc_year * (7.273/100) * 0.9 # rough scaling ~65k m3 for 500 Smc/h
digestate_t = smc_year * 0.016 #parameter to be tuned
#st.write(f"**Total production:** {smc_year:,.0f} Smc/year")
#st.write(f"**Total production:** {mwh_year:,.0f} MWh/year")

operational_output_narrative = f"""
<div style="
    border: 2px solid {palette_green[3]};
    padding: 15px;
    border-radius: 10px;
    background-color: rgba(255, 255, 255, 0.05);
    color: white;
">

<b>📊 Key Operational Parameters </b><br>
<ul>
<li><span style="color:{palette_green[3]}; font-weight:bold;">
bioCH4 production =  {smc_year:,.0f} Smc/year
<li><span style="color:{palette_green[3]}; font-weight:bold;">
bioCH4 production = {mwh_year:,.0f} MWh/y
<li><span style="color:{palette_green[3]}; font-weight:bold;">
bioLNG production = {t_lng:,.0f} t/y
<li><span style="color:{palette_green[3]}; font-weight:bold;">
digestate production = {digestate_t:,.0f} t/y
<li><span style="color:{palette_green[3]}; font-weight:bold;">
bioCO2 production = {co2_t:,.0f} t/y

"""
st.markdown(operational_output_narrative, unsafe_allow_html=True)

#----------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------
st.divider()  # <--- Streamlit's built-in separator
#----------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------
# --- Market price inputs ---
st.subheader("🧮 Market assumptions")


col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    p_gas = st.slider("Gas price (€/MWh)", 10.0, 80.0, 35.0, 1.0)
    with col2:
        p_lng = st.slider("bioLNG price (€/MWh)", 20.0, 100.0, 45.0, 1.0)
    with col3:
        p_go = st.slider("GO price (€/MWh)", 0.0, 5.0, 0.4, 0.1)
    with col4:
        p_co2 = st.slider("merchant CO₂ price (€/t)", 0, 200, 100, 10)
    with col5:
        p_dig = st.slider("Digestate value (€/t)", 0, 20, 7, 1)


# --- Common side revenues ---
# CO2

rev_co2 = co2_t * p_co2

# Digestate
rev_dig = digestate_t * p_dig


# --- DM 2018 calculations ---
# CIC factors
cic_value = 375 # €/CIC
cic_per_mwh = 1 / 5.811 # CIC per MWh advanced


# Grid: -5% eligible, no +20%
#cic_grid = mwh_grid * 0.95 * cic_per_mwh
cic_grid =smc_to_grid /(5)*0.00902  # biometano avanzato!! 1 CIC--> 5 Gcal
cic_lng =(smc_to_lng /(5)*0.00902)*1.2  # biometano avanzato!! 1 CIC--> 5 Gcal

rev_cic_grid = cic_grid * cic_value
rev_gas_grid = mwh_grid * 0.95 * p_gas


# LNG: +20% CIC
cic_lng = mwh_lng * cic_per_mwh * 1.20
rev_cic_lng = cic_lng * cic_value
rev_lng = mwh_lng * p_lng


rev_dm2018 = {
"Gas sales (grid)": rev_gas_grid,
"LNG sales": rev_lng,
"CIC (grid)": rev_cic_grid,
"CIC (LNG +20%)": rev_cic_lng,
"CO₂ sales": rev_co2,
"Digestate": rev_dig
}

#----------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------
st.divider()  # <--- Streamlit's built-in separator
#----------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------
st.subheader("🧮 DM 2018")

st.markdown(rf"""
<div style="
    border: 2px solid #FFD700;
    padding: 0rem;
    border-radius: 10px;
    background-color: rgba(255, 255, 255, 0.05);
    color: white;
    line-height: 1.8;
">

📘 <b>DM 2018: Feed-in Premium</b> <br><br>

$ \text{{Revenues}} = P_{{\text{{gas}}}} \cdot Q_{{\text{{rete}}}} \cdot 0.95 + N_{{\text{{CIC}}}} \cdot V_{{\text{{CIC}}}} + P_{{\text{{bioLNG}}}} \cdot Q_{{\text{{bioLNG}}}} + P_{{\text{{CO₂}}}} \cdot Q_{{\text{{CO₂}}}} + P_{{\text{{digestato}}}} \cdot Q_{{\text{{digestato}}}} $ <br><br>
</div>

""", unsafe_allow_html=True)


c_2018_narrative = rf"""
<div style="
    border: 2px solid {palette_green[3]};
    padding: 15px;
    border-radius: 10px;
    background-color: rgba(255, 255, 255, 0.05);
    color: white;
">
<b>📊 Incentive specific to DM 2018</b><br>
<ul>
<li><span style="color:{palette_green[3]}; font-weight:bold;">N<sub>CICgrid</sub></span> = {cic_grid:,.0f} </li>
</ul>
<li><span style="color:{palette_green[3]}; font-weight:bold;">N<sub>CIClng</sub></span> = {cic_lng:,.0f} </li>
</ul>
<li><span style="color:{palette_green[3]}; font-weight:bold;">V<sub>CIC</sub></span> = {cic_value:,.0f} EUR </li>

</div>
"""

st.markdown(c_2018_narrative, unsafe_allow_html=True)


#----------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------
st.divider()  # <--- Streamlit's built-in separator
#----------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------
st.subheader("🧮 DM 2022")


st.markdown(rf"""
<div style="
    border: 2px solid #4CAF50;
    padding: 15px;
    border-radius: 10px;
    background-color: rgba(255, 255, 255, 0.05);
    color: white;
    line-height: 1.8;
">

📘 <b>DM 2022: Contract for Difference</b> <br>
$ \text{{TP}} = TR - P_{{GO}} - P_{{gas}} $
</div>
""", unsafe_allow_html=True)



# --- DM 2022 calculations ---
tr = st.slider("Tariffa di riferimento (€/MWh)", 80, 150, 120, 1)


tp = tr - p_gas - p_go
rev_premium = tp * mwh_year


rev_gas_grid_22 = mwh_grid * p_gas
rev_lng_22 = mwh_lng * p_lng
rev_go_22 = mwh_year * p_go


rev_dm2022 = {
"Gas sales (grid)": rev_gas_grid_22,
"LNG sales": rev_lng_22,
"GO sales": rev_go_22,
"Premium (TP)": rev_premium,
"CO₂ sales": rev_co2,
"Digestate": rev_dig
}

#----------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------
st.divider()  # <--- Streamlit's built-in separator
#----------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------
# --- Visualization stacked bar plot with Plotly ---
st.subheader("💶 Revenue breakdown comparison")


plot_df = pd.DataFrame({
        "DM 2018": rev_dm2018,
        "DM 2022": rev_dm2022
})

plot_df.index.tolist()
color_map = {
    "Gas sales (grid)":      palette_blue[3],   # medium blue
    "LNG sales":             palette_blue[4],   # slightly darker blue
    "CIC (grid)":            palette_green[1],  # light green
    "CIC (LNG +20%)":        palette_green[2],  # brighter green
    "CO₂ sales":             palette_other[2],  # pastel pink
    "Digestate":             palette_other[1],  # pastel yellow
    "GO sales":              palette_other[0],  # pastel orange
    "Premium (TP)":          palette_green[4],  # lime green (distinct, DM 2022-specific)
}

plot_df_reset = plot_df.reset_index().melt(id_vars="index", var_name="Scheme", value_name="Revenue")

plot_df_reset_sorted = (
    plot_df_reset
    .sort_values(["Scheme", "Revenue"], ascending=[True, False])  # sort by Scheme, then by Revenue descending
)

fig = px.bar(
    plot_df_reset_sorted,
    x="Scheme",
    y="Revenue",
    color="index",
    text_auto=".2s",
    title="Stacked revenue components – DM 2018 vs DM 2022",
    labels={"index": "Revenue component"},
    color_discrete_map=color_map
)

st.plotly_chart(fig, use_container_width=True)


#----------------------------------------------------------------------------------------------------------------
st.divider()  # <--- Streamlit's built-in separator
#----------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------

# --- Display results tables ---
st.subheader("Detailed results")


col1, col2 = st.columns(2)
with col1:
    st.markdown("### DM 2018 (Feed-in Premium / CIC)")
df2018 = pd.DataFrame.from_dict(rev_dm2018, orient="index", columns=["€"]).round(0)
df2018.loc["Total"] = df2018.sum()
st.dataframe(df2018.style.format("{:,.0f}"))


with col2:
    st.markdown("### DM 2022 (Contract for Difference)")
df2022 = pd.DataFrame.from_dict(rev_dm2022, orient="index", columns=["€"]).round(0)
df2022.loc["Total"] = df2022.sum()
st.dataframe(df2022.style.format("{:,.0f}"))




