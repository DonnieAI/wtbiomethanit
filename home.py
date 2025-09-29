"""
WTBIOMETHANIT

"""
#cdm
#     projenv\Scripts\activate
#     streamlit run home.py

import streamlit as st
import pandas as pd


# ✅ Must be the first Streamlit call
st.set_page_config(
    page_title="Home",   # Browser tab title
    page_icon="🏠",      # Optional favicon (emoji or path to .png/.ico)
    layout="wide"        # "centered" or "wide"
)


# ── Load user credentials and profiles ────────────────────────
CREDENTIALS = dict(st.secrets["auth"])
PROFILES = st.secrets.get("profile", {})

# ── Login form ────────────────────────────────────────────────
def login():
    st.title("🔐 Login Required")

    user = st.text_input("Username", key="username_input")
    password = st.text_input("Password", type="password", key="password_input")

    if st.button("Login", key="login_button"):
        if user in CREDENTIALS and password == CREDENTIALS[user]:
            st.session_state["authenticated"] = True
            st.session_state["username"] = user
            st.session_state["first_name"] = PROFILES.get(user, {}).get("first_name", user)
        else:
            st.error("❌ Invalid username or password")

# ── Auth state setup ──────────────────────────────────────────
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# ── Login gate ────────────────────────────────────────────────
if not st.session_state["authenticated"]:
    login()
    st.stop()

# ── App begins after login ────────────────────────────────────

# ---------------Sidebar
from utils import apply_style_and_logo

st.sidebar.success(f"Welcome {st.session_state['first_name']}!")
st.sidebar.button("Logout", on_click=lambda: st.session_state.update(authenticated=False))

# Spacer to push the link to the bottom (optional tweak for better placement)
st.sidebar.markdown("<br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>", unsafe_allow_html=True)

# Company website link
st.sidebar.markdown(
    '<p style="text-align:center;">'
    '<a href="https://www.wavetransition.com" target="_blank">🌐 Visit WaveTransition</a>'
    '</p>',
    unsafe_allow_html=True
)
# ---------Main content
st.set_page_config(page_title="Fuel Dashboard", layout="wide")
st.title("**BIOMETHANIT**")
st.markdown("""
## WAVETRANSITION ITALIAN BIOEMETHANE LANDSCAPE ANALYSIS   

This web application is designed to **collect and present updated information on Italian biomethane projects**, providing a quick yet accurate **overview of key players, project locations, and emerging business opportunities**.

It serves as a **preliminary insight tool** for industry stakeholders, enabling a **fast, immediate understanding** of the biomethane market landscape in Italy, with the goal of supporting **further, in-depth analysis**.

---

### 🌱 Coverage: Italian Biomethane Landscape

The data presented in this app focuses on **Italian biomethane initiatives** and offers a **geospatial view** of ongoing and planned projects.  
This includes details such as:

- **Geographical distribution** of biomethane plants and projects
- **Key market players** and their roles in the biomethane value chain
- **Project characteristics**, such as capacity, feedstock, and development stage
- **Potential business opportunities** for suppliers, investors, and technology providers

---

### 🎯 Purpose

The purpose of **BIOMETHANIT** is to provide stakeholders with a **fast, harmonized view** of the Italian biomethane sector.  
By consolidating **project data and location intelligence** into a single interface, the app helps:

- Identify **market hotspots**
- Understand **competitive positioning**
- Spot **investment and partnership opportunities**

---

### 📌 Key Features

- **Interactive map** of biomethane projects across Italy
- **Categorization by project stage** and other key metadata
- **Quick filtering** for specific regions, players, or project attributes
- **Clear visuals** to assist in rapid assessment

---

### ⚠️ Note

This tool is designed for **quick overviews** and **preliminary assessments**.  
For detailed technical, regulatory, or financial analysis, additional sector-specific data sources should be consulted.

---

### 🧭 Start exploring!

Use the navigation and interactive elements to **browse projects, filter by attributes**, and gain a **geospatial perspective** on the Italian biomethane sector.
""")


