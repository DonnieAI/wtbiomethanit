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

     #### 💡Note: The **GSE** plays a central role in managing incentives, verifying compliance, and facilitating market integration of biomethane.
    ---

    ## 🧾 DM 2018 – First Incentive Scheme
    - **Full name:** Ministerial Decree of March 2, 2018.
    - **Objective:** Support the production of biomethane for transport and advanced biofuels.
    - **Key measures:**
    - Guaranteed purchase of biomethane by the Gestore dei Servizi Energetici (**GSE**) at incentivized tariffs.
    - Support for plants converting biogas to biomethane.
    - Priority for **advanced biomethane** from waste and agricultural residues.
    - Incentives valid for a maximum of **20 years** from commissioning.
"""
)


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


st.markdown(
"""

    ---

    ## 🔄 DM 2022 – New Support Framework
    - **Full name:** Ministerial Decree of September 15, 2022.
    - **Objective:** Accelerate biomethane development in line with the **Italian National Recovery and Resilience Plan (PNRR)**.
    - **Key measures:**
    - Dedicated funding of **€1.92 billion** from the PNRR for new plants and conversions.
    - Capital grants covering up to **40% of investment costs**.
    - Updated feed-in tariffs for injected biomethane.
    - Strong focus on sustainability and reduction of greenhouse gas emissions.

    ---


    """
)

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

