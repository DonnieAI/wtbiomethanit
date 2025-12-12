import streamlit as st

st.set_page_config(page_title="projects", layout="wide")
from utils import apply_style_and_logo
apply_style_and_logo()


st.title("Italian Biomethane Regulatory overview ")
st.markdown("""
            ### 📖 Italian Biomethane Regulatory overview 
            
            """)
st.markdown(""" 
            source: GSE""") 


# Path to your PDF in the "data" folder
#pdf_path = "data/DM Biometano 15-9-2022 - Regole applicative.pdf"

# Read the file in binary mode
#with open(pdf_path, "rb") as pdf_file:
 #   pdf_bytes = pdf_file.read()

def load_pdf(path):
    with open(path, "rb") as f:
        return f.read()


# Create a download button


st.markdown(
"""
    # 🇮🇹 Biomethane Legislation in Italy

    Italy has introduced specific legislation to promote the **production** and **use** of biomethane, particularly in the transport sector and for decarbonization of the gas grid.
    ## 📌 Summary
    - **DM 2018** → Established the first long-term incentive scheme for biomethane, focused mainly on the transport sector.
    - **DM 2022** → Updated and expanded the scheme with **PNRR** funding, aiming to increase production capacity and sustainability.
    - Together, these decrees create a **comprehensive support system** for the Italian biomethane industry.

    ---

     ### 💡Note: The **GSE** plays a central role in managing incentives, verifying compliance, and facilitating market integration of biomethane.
    ---
"""
)

st.markdown("""
## 🧾 DM 2018 (Ministerial Decree 2 March 2018) — CIC-based support (mainly transport)

**What it is**
- A support scheme designed to stimulate biomethane (especially **advanced biomethane**) for the **transport/biofuels obligation** market.
- The incentive is mainly delivered through **CIC (Immission Certificates)** rather than a classic feed-in tariff.

**How revenues are supported**
- **Market revenue:** biomethane is sold at a market gas price (e.g., PSV-linked).
- **Incentive component:** eligible production receives **CIC**, and (for a limited time) a **fixed-value withdrawal/premium** managed by **GSE**.

**Duration & predictability**
- **Fixed CIC value (withdrawal/premium) is granted for up to 10 years**.
- After the 10-year period, the plant may still receive **CIC issuance**, but the fixed-value withdrawal/premium ends (CIC can be sold to market counterparties).

**Key takeaways for investment modelling**
- Partial hedge via CIC, but **exposure to gas price risk (PSV)** remains on the market-sales component.
- Advanced biomethane can receive **uplifts (e.g., double-counting / higher CIC entitlement)** depending on eligibility.

**Institutional role**
- **GSE** manages verification, eligibility checks and operational procedures for incentive recognition.
""")


# --- External link ---

st.markdown("""
            #### 🌍 Web links
            """)
st.markdown("[🔗 Biometano - DM 02/03/2018](https://www.gse.it/servizi-per-te/rinnovabili-per-i-trasporti/biometano) ", unsafe_allow_html=True)

st.markdown("""
            #### 📚 Documents to be downloaded
            """)
# DM 2018 - File 1
pdf_bytes_1 = load_pdf("data/DM2018/D.M. MiSE 2 marzo 2018.pdf")
st.download_button(
    label="🧾 DM Biometano 2 marzo 2018",
    data=pdf_bytes_1,
    file_name="DM_2_marzo_2018.pdf",
    mime="application/pdf"
)

# DM 2018 - File 2
pdf_bytes_2 = load_pdf("data\DM2018\Procedure applicative 7 0 DM 2 marzo 2018.pdf")
st.download_button(
    label="📄 DM Biometano - Procedure Applicative 7.0 6 maggio 2025",
    data=pdf_bytes_2,
    file_name="Procedure_applicative_3_0.pdf",
    mime="application/pdf"
)


st.markdown("""
## 🔄 DM 2022 (Ministerial Decree 15 September 2022) — PNRR-backed framework (Capex + Operating support)

**What it is**
- A new biomethane framework aligned with **PNRR (Mission 2, Component 2, Investment 1.4)** to accelerate new plants and conversions.
- It combines **investment support (capex grant)** with a long-term **operating incentive** for injected biomethane.

**Two-layer support**
- **Capex grant:** up to **40% of eligible investment costs** (one-off, subject to PNRR rules).
- **Operating incentive:** an incentive applied to the **net biomethane injected**.

**Operating mechanism (15-year stability)**
- Incentives are recognized for **15 years from commercial operation date** (net of eligible force-majeure stoppages).
- Two commercial regimes exist:
  - **TO (Tariffa Omnicomprensiva)**: GSE purchases the biomethane and sells it to the market (FiT-like offtake).
  - **TP (Tariffa Premio / CfD-like)**: the producer sells biomethane on the market and GSE pays a premium that regulates revenues towards the awarded tariff.

**Access & timing**
- Access occurs via **competitive auctions** (pay-as-bid discount on the reference tariff).
- Eligible projects must enter operation within the PNRR deadline (e.g., **by 30 June 2026**, per decree conditions).

**Key takeaways for investment modelling**
- Compared to DM 2018, the “gas” revenue line is typically **more predictable** under the CfD/TO logic because the tariff mechanism reduces direct exposure to gas price volatility (especially under TP/CfD logic).
- Stronger emphasis on sustainability requirements (RED II) and PNRR compliance controls, with GSE managing procedures and verification.
""")

st.markdown("""
            #### 🌍 Web links
            """)
st.markdown("[🔗 Biometano - DM 15/09/2022](https://www.gse.it/servizi-per-te/attuazione-misure-pnrr/produzione-di-biometano) ", unsafe_allow_html=True)

st.markdown("""
            #### 📚 Documents to be downloaded
            """)

# DM 2022
pdf_bytes_3 = load_pdf("data/DM2022/Decreto Ministeriale_Biometano_15-9-2022.pdf")
st.download_button(
    label="📄 DM Biometano 15 settembre 2022",
    data=pdf_bytes_3,
    file_name="DM_Biometano_15-9-2022.pdf",
    mime="application/pdf"
)

pdf_bytes_4 = load_pdf("data/DM2022/DM Biometano 15-9-2022 - Regole applicative_Allegati e Appendici_v13_05_2025.pdf")
st.download_button(
    label="📄 DM Biometano 15 settembre 2022 - Regole applicative 13 maggio 2025",
    data=pdf_bytes_4,
    file_name="DM Biometano 15-9-2022 - Regole applicative_Allegati e Appendici_v13_05_2025.pdf",
    mime="application/pdf"
)

