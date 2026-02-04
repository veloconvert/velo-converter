import streamlit as st
import camelot
import pandas as pd
from io import BytesIO
import os
import time

# --- GITHUB & GOOGLE AUTHORIZATION ---
st.set_page_config(
    page_title="VELO | Pro PDF to Excel",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Google Doğrulaması (Kilitli)
st.markdown('<meta name="google-site-verification" content="7QSo9l_GthJCi86IIW0CLwarA2KK0AtgZO-WN4PnlTE" />', unsafe_allow_html=True)

# --- MASTER UI STYLING (LOCKED) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap');
    .stApp { background-color: #0b0e14; color: #e2e8f0; font-family: 'Inter', sans-serif; }
    .brand-logo {
        font-weight: 800; font-size: clamp(45px, 10vw, 75px); letter-spacing: 15px;
        background: linear-gradient(135deg, #ffffff 0%, #cbd5e1 50%, #ffffff 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        filter: drop-shadow(0 0 20px rgba(255,255,255,0.4));
    }
    .neon-divider { height: 3px; background: #00d2ff; box-shadow: 0 0 20px #00d2ff; margin-bottom: 60px; }
    [data-testid="stFileUploader"] {
        max-width: 1000px; margin: 60px auto !important; border: 2px dashed #00d2ff !important;
        background-color: rgba(22, 27, 34, 0.8) !important; border-radius: 24px !important; padding: 50px !important;
    }
    .stDownloadButton>button {
        width: 100% !important; max-width: 600px; margin: 50px auto !important; display: block;
        background: linear-gradient(135deg, #22c55e 0%, #15803d 100%); padding: 22px !important;
        font-size: 24px !important; font-weight: 800 !important; border-radius: 60px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER AREA ---
st.markdown('<div class="brand-logo">VELO</div>', unsafe_allow_html=True)
st.markdown('<div class="neon-divider"></div>', unsafe_allow_html=True)

# --- MASTER ENGINE ---
st.title("Professional PDF Table Extractor")
uploaded_file = st.file_uploader("", type="pdf", label_visibility="collapsed")

if uploaded_file:
    with open("temp.pdf", "wb") as f: f.write(uploaded_file.getbuffer())
    try:
        with st.status("VELO PRO ENGINE PROCESSING...", expanded=True):
            time.sleep(1)
            tables = camelot.read_pdf("temp.pdf", pages='all', flavor='lattice', line_scale=40)
        
        if len(tables) > 0:
            final_dfs = []
            for i, table in enumerate(tables):
                df = table.df.copy()
                st.markdown(f"**Table {i+1}**")
                st.dataframe(df, use_container_width=True)
                final_dfs.append(df)
            
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                for i, df in enumerate(final_dfs): df.to_excel(writer, index=False, sheet_name=f'Table_{i+1}')
            
            st.download_button(label="✅ READY TO DOWNLOAD", data=output.getvalue(), file_name="velo_export.xlsx")
    finally:
        if os.path.exists("temp.pdf"): os.remove("temp.pdf")

st.markdown("---")
st.markdown("<p style='text-align: center; color: #4b5563;'>VELO GLOBAL • 500MB PRO CAPACITY • 2026</p>", unsafe_allow_html=True)
