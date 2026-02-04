import streamlit as st
import camelot
import pandas as pd
from io import BytesIO
import os
import time

# --- UI CONFIG (LOCKED) ---
st.set_page_config(
    page_title="VELO | Pro PDF to Excel",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- MASTER UI STYLING ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap');
    
    .stApp { background-color: #0b0e14; color: #e2e8f0; font-family: 'Inter', sans-serif; }
    
    .brand-logo {
        font-weight: 800;
        font-size: clamp(45px, 10vw, 75px);
        letter-spacing: 15px;
        text-align: center;
        background: linear-gradient(135deg, #ffffff 0%, #cbd5e1 50%, #ffffff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-top: 50px;
        filter: drop-shadow(0 0 20px rgba(255,255,255,0.4));
    }
    
    .neon-divider {
        height: 3px;
        background: linear-gradient(90deg, transparent, #00d2ff, transparent);
        box-shadow: 0 0 20px #00d2ff;
        margin: 20px auto 60px auto;
        width: 80%;
    }

    /* Diğer Servisler Butonu (Lüks Gri) */
    .other-btn {
        display: block;
        width: fit-content;
        margin: 0 auto 30px auto;
        padding: 10px 25px;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 30px;
        color: #94a3b8;
        text-decoration: none;
        font-size: 14px;
        letter-spacing: 2px;
        transition: 0.3s;
    }
    .other-btn:hover {
        background: rgba(255, 255, 255, 0.1);
        border-color: #00d2ff;
        color: white;
    }

    [data-testid="stFileUploader"] {
        max-width: 800px;
        margin: 0 auto !important;
        border: 2px dashed #00d2ff !important;
        background-color: rgba(22, 27, 34, 0.8) !important;
        border-radius: 24px !important;
        padding: 40px !important;
    }

    .stDownloadButton>button {
        width: 100% !important;
        max-width: 500px;
        margin: 40px auto !important;
        display: block;
        background: linear-gradient(135deg, #22c55e 0%, #15803d 100%) !important;
        color: white !important;
        border: none !important;
        padding: 20px !important;
        font-size: 22px !important;
        font-weight: 800 !important;
        border-radius: 50px !important;
        text-transform: uppercase;
    }

    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- BRANDING & NAVIGATION ---
st.markdown('<div class="brand-logo">VELO</div>', unsafe_allow_html=True)
st.markdown('<div class="neon-divider"></div>', unsafe_allow_html=True)

# Diğer Servisler Butonu (Geri Getirildi)
st.markdown('<a href="#" class="other-btn">OTHER SERVICES</a>', unsafe_allow_html=True)

# --- ENGINE ---
uploaded_file = st.file_uploader("", type="pdf", label_visibility="collapsed")

if uploaded_file:
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    try:
        # Orange/Amber Status
        with st.status("VELO ENGINE PROCESSING...", expanded=True) as status:
            time.sleep(1.5)
            tables = camelot.read_pdf("temp.pdf", pages='all', flavor='lattice', line_scale=40)
            status.update(label="EXTRACTION COMPLETE", state="complete", expanded=False)
        
        if len(tables) > 0:
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                for i, table in enumerate(tables):
                    table.df.to_excel(writer, index=False, sheet_name=f'Table_{i+1}')
            
            st.download_button(
                label="✅ READY TO DOWNLOAD",
                data=output.getvalue(),
                file_name="velo_export.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    except Exception as e:
        st.error(f"Engine Error: {str(e)}")
    finally:
        if os.path.exists("temp.pdf"):
            os.remove("temp.pdf")

# --- FOOTER ---
st.markdown("<br><br><p style='text-align: center; color: #4b5563; font-size: 10px; letter-spacing: 2px;'>VELO GLOBAL • 2026</p>", unsafe_allow_html=True)
