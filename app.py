import streamlit as st
import camelot
import pandas as pd
from io import BytesIO
import os
import time

# --- PURE LUXURY & MOBILE-FIX CONFIG ---
st.set_page_config(page_title="VELO", layout="wide")

# --- VELO REFINED MASTER CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap');
    
    .stApp { background-color: #0b0e14; color: #e2e8f0; font-family: 'Inter', sans-serif; }
    
    /* NEON SIGNATURE FRAME */
    .main .block-container {
        border: 1px solid #00d2ff;
        border-radius: 15px;
        padding: clamp(20px, 5vw, 40px);
        margin-top: 10px;
        box-shadow: 0 0 15px rgba(0, 210, 255, 0.1);
        background-color: rgba(13, 17, 23, 0.9);
    }

    /* TOP NAVIGATION REFINED */
    .nav-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 0;
        border-bottom: 1px solid rgba(255,255,255,0.05);
        margin-bottom: 40px;
    }
    
    .brand-logo {
        font-weight: 800;
        font-size: 32px;
        letter-spacing: 6px;
        color: #ffffff;
        text-shadow: 0 0 10px rgba(255,255,255,0.3);
    }

    /* AD SLOTS */
    .ad-top {
        width: 100%;
        height: 90px;
        background: #10141b;
        border: 1px solid #1f2937;
        display: flex;
        justify-content: center;
        align-items: center;
        color: #374151;
        font-size: 10px;
        margin-bottom: 30px;
        border-radius: 4px;
    }

    /* BUTTONS */
    .stDownloadButton>button {
        width: 100% !important;
        background: linear-gradient(135deg, #22c55e 0%, #15803d 100%);
        color: white !important;
        border: none !important;
        padding: 15px !important;
        font-size: 18px !important;
        font-weight: 700 !important;
        border-radius: 8px !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        box-shadow: 0 10px 20px rgba(22, 101, 52, 0.3);
    }

    /* MOBILE ADJUSTMENTS */
    @media (max-width: 768px) {
        .brand-logo { font-size: 24px; letter-spacing: 3px; }
        .nav-bar { padding: 5px 0; }
        .ad-side { display: none; }
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER SECTION ---
st.markdown('<div class="nav-bar">', unsafe_allow_html=True)
col_logo, col_menu = st.columns([2, 1])

with col_logo:
    st.markdown('<div class="brand-logo">VELO</div>', unsafe_allow_html=True)

with col_menu:
    with st.popover("🌐 NETWORK", use_container_width=True):
        st.markdown("**Our Global Services**")
        st.write("✅ PDF to Excel")
        st.divider()
        st.write("• VELO Compressor (Soon)")
        st.write("• VELO Image Tools (Soon)")
st.markdown('</div>', unsafe_allow_html=True)

# --- AD SLOT TOP ---
st.markdown('<div class="ad-top">ADVERTISEMENT SPACE</div>', unsafe_allow_html=True)

# --- MAIN ENGINE ---
col_main, col_spacer, col_ad_side = st.columns([3, 0.2, 1])

with col_main:
    st.title("Professional PDF Table Extractor")
    st.markdown("<p style='color: #6b7280; margin-top:-15px;'>Enterprise Grade Data Conversion</p>", unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("", type="pdf", label_visibility="collapsed")

    if uploaded_file:
        with open("temp.pdf", "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        try:
            with st.status("Velo Engine Analyzing...", expanded=False) as status:
                time.sleep(1)
                tables = camelot.read_pdf("temp.pdf", pages='all', flavor='lattice')
                status.update(label="Analysis Ready", state="complete")
            
            if len(tables) > 0:
                st.markdown(f'<p style="color:#4b5563; font-style:italic;">({len(tables)} tables identified)</p>', unsafe_allow_html=True)
                
                all_dfs = []
                for table in tables:
                    st.dataframe(table.df, use_container_width=True)
                    all_dfs.append(table.df)
                
                output = BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    for i, df in enumerate(all_dfs):
                        df.to_excel(writer, index=False, header=False, sheet_name=f'Table_{i+1}')
                
                st.download_button(
                    label="✅ READY TO DOWNLOAD",
                    data=output.getvalue(),
                    file_name="velo_export.xlsx"
                )
            else:
                st.error("No tables detected.")
        except Exception as e:
            st.error("Processing error. Ensure PDF has valid tables.")
        finally:
            if os.path.exists("temp.pdf"): os.remove("temp.pdf")

with col_ad_side:
    st.markdown('<div class="ad-side" style="height:600px; background:#10141b; border:1px solid #1f2937; color:#374151; display:flex; align-items:center; justify-content:center; border-radius:4px; font-size:10px; writing-mode: vertical-rl;">ADVERTISEMENT SPACE</div>', unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("<div style='text-align: center; color: #1f2937; font-size: 10px; margin-top: 50px;'>SECURE • PRIVATE • VELO GLOBAL 2026</div>", unsafe_allow_html=True)
