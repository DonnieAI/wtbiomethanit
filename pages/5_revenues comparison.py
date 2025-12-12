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
            ### 💵 Biomethane Revenues Analysis (only advanced biomethane AGRI - no WASTE) 
            
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
st.subheader("🏭 Operational characteristics")

col1, col2, col3,col4 = st.columns(4)
with col1:
    smc_h = st.number_input("Capacity (Smc/h)", value=500, step=50)
with col2:
        hours = st.number_input("Operating hours/year", value=8500, step=100)
with col3:
        share_lng = st.slider("Share of bioLNG (%)", 0, 100, 0, step=5)
with col4:
    biomethane_advanced = st.checkbox("Biomethane Advanced", value=True)

# k_adv logic
k_adv = 2 if biomethane_advanced else 1


# Total Energy production (MWh)
smc_year = smc_h * hours  #smc/y
mwh_year = smc_year * 9.5 / 1000 #   valore standard GSE: PCS ~ 9.5 kWh/Smc

#bioCH4 to GRID
smc_to_grid=smc_year*(1-share_lng / 100)
smc_to_lng=smc_year-smc_to_grid

#For practical use in LCA or energy economics, you might use 13.5–13.8 kWh/kg for real bio-LNG.
mwh_lng = mwh_year * (share_lng / 100)
t_lng=mwh_lng/13.5
mwh_grid = mwh_year - mwh_lng

co2_t = smc_year * 1.96 / 1000 * 0.9 # t/year, 90% capture efficiency

#digestate_t = smc_year * (7.273/100) * 0.9 # rough scaling ~65k m3 for 500 Smc/h
digestate_t = smc_year * 0.016      #parameter to be tuned

N_go = mwh_year

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
    p_gas = st.slider("Gas price (€/MWh)", 0.0, 200.0, 20.0, 1.0)
with col2:
        p_lng = st.slider("bioLNG price (€/MWh)", 20.0, 100.0, 0.0, 1.0)
with col3:
        p_go = st.slider("GO price (€/MWh)", 0.0, 5.0, 0.0, 0.1)
with col4:
        p_co2 = st.slider("merchant CO₂ price (€/t)", 0, 200, 0, 10)
with col5:
        p_dig = st.slider("Digestate value (€/t)", 0, 80, 20, 1)

#--------------------------------------
# --- Common side revenues --- this revenues are indipendent on the decree
#--------------------------------------
# CO2
rev_co2 = co2_t * p_co2   # biogenic revenue part if bioCO2 is separated and sold
# Digestate
rev_dig = digestate_t * p_dig   #EUR
#

KEY_CO2 = "CO2 sales"
KEY_DIG = "Digestate"

#-----------------------------
# --- DM 2018 calculations ---
#-----------------------------
# CIC factors
cic_value = 375  # €/CIC
cic_grid = (smc_to_grid / 1230) * k_adv 
rev_cic_grid = cic_grid * cic_value


cic_per_mwh = 1 / 5.811 # CIC per MWh advanced
# Grid: -5% eligible, no +20%
#cic_grid = mwh_grid * 0.95 * cic_per_mwh
#cic_grid =smc_to_grid /(5)*0.00902  # biometano avanzato!! 1 CIC--> 5 Gcal
cic_lng =(smc_to_lng /(5)*0.00902)*1.2  # biometano avanzato!! 1 CIC--> 5 Gcal


rev_gas_grid = mwh_grid * 0.95 * p_gas

# LNG: +20% CIC
cic_lng = mwh_lng * cic_per_mwh * 1.20
rev_cic_lng = cic_lng * cic_value
rev_lng = mwh_lng * p_lng

rev_dm2018 = {
                "DM2018 Gas sales PSV (grid)": rev_gas_grid,
                "DM2018 LNG sales": rev_lng,
                "DM2018 CIC (grid)": rev_cic_grid,
                "DM2018 CIC (LNG +20%)": rev_cic_lng,
                KEY_CO2 : rev_co2,
                KEY_DIG: rev_dig
}

#----------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------
st.divider()  # <--- Streamlit's built-in separator
#----------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------
st.subheader("📖 DM 2018")

st.markdown(r"""
<div style="
    border: 2px solid #FFD700;
    padding: 12px 14px;
    border-radius: 20px;
    background-color: rgba(255, 255, 255, 0.05);
    color: white;
    line-height: 2.6;
">
📘 <b>DM 2018: Feed-in Premium (CIC)</b>
</div>
""", unsafe_allow_html=True)

st.latex(r"""
            \begin{aligned}
            \text{Revenues}_{2018} &=
            0.95 \, P_{\text{gas}} \, E_{\text{grid}}
            + V_{\text{CIC}} \left( N_{\text{CIC,grid}} + N_{\text{CIC,LNG}} \right) \\
            &\quad + P_{\text{LNG}} \, E_{\text{LNG}}
            + P_{\text{CO}_2} \, Q_{\text{CO}_2}
            + P_{\text{dig}} \, Q_{\text{dig}}
            \end{aligned}
            """)

#st.markdown("Con (coerente con il tuo modello):")

st.latex(r"""
            \begin{aligned}
            N_{\text{CIC,grid}} &= \frac{Q_{\text{grid,Smc}}}{1230}\, k_{\text{adv}} \\
            N_{\text{CIC,LNG}} &= 1.2 \, E_{\text{LNG}} \, \text{CIC}_{\text{per MWh}}
            \end{aligned}
            """)


c_2018_narrative = rf"""
<div style="
    border: 2px solid {palette_green[3]};
    padding: 15px;
    border-radius: 10px;
    background-color: rgba(255, 255, 255, 0.05);
    color: white;
">
<b>📊 DM 2018 - Scheme-specific incentives</b><br>
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
st.divider()  # <--- Streamlit's built-in separator
st.divider()  # <--- Streamlit's built-in separator
#----------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------
st.subheader("📖 DM 2022")


st.markdown(r"""
            <div style="
                border: 2px solid #FFD700;
                padding: 12px 14px;
                border-radius: 20px;
                background-color: rgba(255, 255, 255, 0.05);
                color: white;
                line-height: 2.6;
            ">
            📘 <b>DM 2022: Contract for Difference (two-way CfD)</b>
            </div>
            """, unsafe_allow_html=True)

st.latex(r"""
            \begin{aligned}
            TP &= TR - P_{\text{gas}} - P_{\text{GO}} \\
            \text{Revenues}_{\text{grid}} &=
            E_{\text{grid}} P_{\text{gas}} + E_{\text{grid}} TP + E_{\text{grid}} P_{\text{GO}}
            = E_{\text{grid}} TR
            \end{aligned}
            """)

st.latex(r"""
            \begin{aligned}
            \text{Revenues}_{2022} &=
            E_{\text{grid}} TR
            + P_{\text{LNG}} E_{\text{LNG}}
            + P_{\text{CO}_2} Q_{\text{CO}_2}
            + P_{\text{dig}} Q_{\text{dig}}
            \end{aligned}
            """)

# --- DM 2022 calculations ---
tr = st.slider("Reference Tariff (€/MWh)", 80, 150, 120, 1)  #tariffa riferimento


c_2022_narrative = rf"""
<div style="
    border: 2px solid {palette_green[3]};
    padding: 15px;
    border-radius: 10px;
    background-color: rgba(255, 255, 255, 0.05);
    color: white;
">
<b>📊 DM 2022 - Scheme-specific incentives</b><br>
<ul>

<li><span style="color:{palette_green[3]}; font-weight:bold;">Reference Tariff<sub>€/MWh</sub></span> = {tr:,.0f} </li>
</ul>
<li><span style="color:{palette_green[3]}; font-weight:bold;">N<sub>GO</sub></span> = {N_go:,.0f} </li>
</ul>
<li><span style="color:{palette_green[3]}; font-weight:bold;">P<sub>GO</sub></span> = {p_go:,.1f} EUR </li>

</div>
"""
st.markdown(c_2022_narrative, unsafe_allow_html=True)






#calcolo tariffa premio
tp = tr - (p_gas + p_go)                 # se p_go è prezzo GO medio (€/MWh)
rev_premium_grid_22 = tp * mwh_grid      # solo parte decreto (CfD)
rev_gas_grid_22 = mwh_grid * p_gas
rev_go_22 = mwh_grid * p_go              # ricavo GO del produttore (se lo modelli come sua vendita)
rev_lng_22 = mwh_lng * p_lng



rev_go_22 = mwh_year * p_go

rev_dm2022 = {
            "DM2022 Premium (TR-PSV)": rev_premium_grid_22,      # SOLO decreto 2022 (verde)
            "DM2022 Gas sales PSV (grid)": rev_gas_grid_22,      # comune (mercato)
            "DM2022 GO sales": rev_go_22,                        # comune (non decreto-only)
            "DM2022 LNG sales": rev_lng_22,                      # comune (mercato)
                KEY_CO2 : rev_co2,
                KEY_DIG: rev_dig                             # comune
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


color_map = {
    # --- DM2018-only (BLUE)
    "DM2018 CIC (grid)":            palette_blue[2],
    "DM2018 CIC (LNG +20%)":        palette_blue[3],

    # --- DM2022-only (GREEN)
    "DM2022 Premium (TR-PSV)":      palette_green[2],

    # --- COMMON / MARKET / SIDE (OTHER)
    "DM2018 Gas sales PSV (grid)":  palette_other[0],
    "DM2022 Gas sales PSV (grid)":  palette_other[0],

    "DM2018 LNG sales":             palette_other[1],
    "DM2022 LNG sales":             palette_other[1],

    "DM2022 GO sales":              palette_other[4],   # comune (se la tieni come ricavo)

    "CO₂ sales":                    palette_other[2],
    "Digestate":                    palette_other[3],
}

# Step 1: Prepare melted dataframe
# Dataframe (robusto)
plot_df = pd.DataFrame({"DM 2018": rev_dm2018, "DM 2022": rev_dm2022}).fillna(0)

# 1) Metti SEMPRE i comuni al bottom (ordine fisso)
bottom_common = [KEY_CO2, "Digestate"]   # usa esattamente le tue chiavi

# 2) Poi metti sopra tutto il resto (in un ordine che scegli tu)
rest_order = [
    # mercato (se vuoi tenerlo subito sopra al common)
    "DM2018 Gas sales PSV (grid)",
    "DM2022 Gas sales PSV (grid)",
    "DM2018 LNG sales",
    "DM2022 LNG sales",
    "DM2022 GO sales",

    # decreto-specific
    "DM2018 CIC (grid)",
    "DM2018 CIC (LNG +20%)",
    "DM2022 Premium (TR-PSV)",
]

# Ordine finale: prima common, poi il resto (tenendo solo le voci presenti davvero)
components_order = [c for c in (bottom_common + rest_order) if c in plot_df.index]

fig = go.Figure()

for comp in components_order:
    fig.add_trace(
        go.Bar(
            name=comp,
            x=plot_df.columns,
            y=plot_df.loc[comp].values,
            marker_color=color_map.get(comp, None),
        )
    )

# Totali (diamante)
totals = plot_df.sum(axis=0)
fig.add_trace(
    go.Scatter(
        x=totals.index,
        y=totals.values,
        mode="markers+text",
        marker=dict(symbol="diamond", size=16, color=palette_other[4]),
        text=[f"{v/1e6:,.1f}" for v in totals.values],
        textposition="top center",
        name="Total Revenue (Diamond)",
    )
)

fig.update_layout(
    title="Stacked revenue components – DM 2018 vs DM 2022",
    yaxis_title="Revenue",
    xaxis_title="Scheme",
    legend_title="Revenue Component",
    barmode="relative",              # gestisce anche premium negativo
    legend_traceorder="normal",      # mantiene l'ordine che hai imposto
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




