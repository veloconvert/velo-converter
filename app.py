import streamlit as st
import camelot
import pandas as pd
from io import BytesIO
import os
import time

# --- LUXURY CONFIG ---
st.set_page_config(page_title="VELO", layout="wide")

# --- VELO REFINED CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap');
    
    .stApp { background-color: #0b0e14; color: #e2e8f0; font-family: 'Inter', sans-serif; }
    
    /* LOGO: PEARLY METALLIC WHITE */
    .brand-logo {
        font-weight: 800;
        font-size: clamp(28px, 5vw, 36px);
        letter-spacing: 7px;
        background: linear-gradient(135deg, #ffffff 0%, #d1d5db 50%, #ffffff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        filter: drop-shadow(0 0 8px rgba(255,255,255,0.4));
    }

    /* THE ONLY NEON LINE - HEADER DIVIDER */
    .neon-divider {
        height: 2px;
        background: #00d2ff;
        box-shadow: 0 0 15px #00d2ff, 0 0 5px #00d2ff;
        margin: 10px 0 40px 0;
        border: none;
    }

    /* NAVIGATION AREA */
    .nav-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 20px 0 5px 0;
    }

    /* AD SLOTS */
    .ad-box {
        background: #111827;
        border: 1px solid #1f2937;
        border-radius: 4px;
        display: flex;
        justify-content: center;
        align-items: center;
        color: #374151;
        font-size: 10px;
    }

    /* DOWNLOAD BUTTON */
    .stDownloadButton>button {
        width: 100% !important;
        background: linear-gradient(135deg, #22c55e 0%, #15803d 100%);
        color: white !important;
        padding: 15px !important;
        font-size: 18px !important;
        font-weight: 700 !important;
        border-radius: 8px !important;
        border: none !important;
        box-shadow: 0 10px 20px rgba(22, 101, 52, 0.2);
    }

    /* MOBILE FIXES */
    @media (max-width: 768px) {
        .ad-side { display: none; }
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.markdown('<div class="nav-container">', unsafe_allow_html=True)
col_l, col_r = st.columns([1, 1])
with col_l:
    st.markdown('<div class="brand-logo">VELO</div>', unsafe_allow_html=True)
with col_r:
    # Zarif ve kısa servis butonu
    with st.popover("🌐 OUR SERVICES", use_container_width=False):
        st.write("✅ PDF to Excel")
        st.write("• VELO Compressor (Soon)")
st.markdown('</div>', unsafe_allow_html=True)

# THE NEON LINE
st.markdown('<div class="neon-divider"></div>', unsafe_allow_html=True)

# --- ADS TOP ---
st.markdown('<div class="ad-box" style="height:90px; margin-bottom:30px;">ADVERTISEMENT</div>', unsafe_allow_html=True)

# --- CONTENT ---
c_main, c_spacer, c_ad = st.columns([3, 0.1, 1])

with c_main:
    st.title("Professional PDF Table Extractor")
    st.markdown("<p style='color: #6b7280; margin-top:-15px;'>Enterprise Grade Data Conversion</p>", unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("", type="pdf", label_visibility="collapsed")

    if uploaded_file:
        with open("temp.pdf", "wb") as f:
            f.write(uploaded_file.getbuffer())
        try:
            with st.status("Velo Engine Running...", expanded=False):
                time.sleep(1)
                tables = camelot.read_pdf("temp.pdf", pages='all', flavor='lattice')
            
            if len(tables) > 0:
                st.info(f"{len(tables)} tables identified.")
                all_dfs = []
                for table in tables:
                    st.dataframe(table.df, use_container_width=True)
                    all_dfs.append(table.df)
                
                output = BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    for i, df in enumerate(all_dfs):
                        df.to_excel(writer, index=False, header=False, sheet_name=f'Table_{i+1}')
                
                st.download_button(label="✅ READY TO DOWNLOAD", data=output.getvalue(), file_name="velo_data.xlsx")
        except:
            st.error("Error processing PDF.")
        finally:
            if os.path.exists("temp.pdf"): os.remove("temp.pdf")

with c_ad:
    st.markdown('<div class="ad-box ad-side" style="height:600px; writing-mode:vertical-rl;">ADVERTISEMENT</div>', unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("<div style='text-align: center; color: #1f2937; font-size: 10px; margin-top: 50px;'>VELO GLOBAL 2026</div>", unsafe_allow_html=True)
