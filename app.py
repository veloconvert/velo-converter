import streamlit as st
import camelot
import pandas as pd
from io import BytesIO
import os
import time

# --- PURE UI CONFIG ---
st.set_page_config(page_title="VELO | Pro PDF to Excel", layout="wide", initial_sidebar_state="collapsed")

# --- ORIGINAL LUXURY STYLING ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap');
    .stApp { background-color: #0b0e14; color: #e2e8f0; font-family: 'Inter', sans-serif; }
    
    .brand-logo {
        font-weight: 800; font-size: 80px; letter-spacing: 20px; text-align: center;
        background: linear-gradient(135deg, #ffffff 0%, #64748b 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-top: 100px;
    }
    
    .neon-divider {
        height: 2px; background: #00d2ff; box-shadow: 0 0 15px #00d2ff;
        width: 60%; margin: 20px auto 80px auto;
    }

    .other-btn {
        display: block; width: fit-content; margin: 0 auto 50px auto;
        padding: 8px 20px; background: transparent; border: 1px solid #334155;
        border-radius: 5px; color: #64748b; text-decoration: none; font-size: 12px;
        letter-spacing: 3px; transition: 0.3s;
    }
    .other-btn:hover { border-color: #00d2ff; color: white; }

    [data-testid="stFileUploader"] {
        max-width: 700px; margin: 0 auto !important;
        background-color: #161b22 !important; border: 1px solid #30363d !important;
        border-radius: 10px !important; padding: 30px !important;
    }

    .stDownloadButton>button {
        width: 100% !important; max-width: 400px; margin: 50px auto !important;
        display: block; background: #22c55e !important; color: white !important;
        font-weight: 800 !important; border-radius: 4px !important; border: none !important;
    }

    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- LAYOUT ---
st.markdown('<div class="brand-logo">VELO</div>', unsafe_allow_html=True)
st.markdown('<div class="neon-divider"></div>', unsafe_allow_html=True)
st.markdown('<a href="#" class="other-btn">OTHER SERVICES</a>', unsafe_allow_html=True)

# --- ENGINE ---
uploaded_file = st.file_uploader("", type="pdf", label_visibility="collapsed")

if uploaded_file:
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())
    try:
        with st.status("ENGINE PROCESSING...", expanded=True):
            time.sleep(1)
            tables = camelot.read_pdf("temp.pdf", pages='all', flavor='lattice')
        
        if len(tables) > 0:
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                for i, table in enumerate(tables):
                    table.df.to_excel(writer, index=False, sheet_name=f'Table_{i+1}')
            
            st.download_button(label="READY TO DOWNLOAD", data=output.getvalue(), file_name="velo_export.xlsx")
    finally:
        if os.path.exists("temp.pdf"):
            os.remove("temp.pdf")
