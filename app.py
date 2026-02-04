import streamlit as st
import camelot
import pandas as pd
from io import BytesIO
import os
import time

# --- PURE LUXURY & MOBILE-FIX CONFIG ---
st.set_page_config(page_title="VELO | PDF to Excel Pro", layout="wide")

# --- VELO NEON & AD-READY CSS ---
st.markdown("""
    <style>
    /* Base Theme */
    .stApp { background-color: #0b0e14; color: #e2e8f0; }
    
    /* NEON BLUE BORDER - Every site's signature */
    .main .block-container {
        border: 2px solid #00d2ff;
        border-radius: 20px;
        padding: 30px;
        margin-top: 20px;
        box-shadow: 0 0 20px rgba(0, 210, 255, 0.2);
        background-color: rgba(13, 17, 23, 0.8);
    }

    /* METALLIC NAVBAR */
    .velo-navbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 15px 0;
        border-bottom: 2px solid rgba(255,255,255,0.05);
        margin-bottom: 30px;
    }
    
    .brand-logo {
        font-weight: 800;
        font-size: 32px;
        letter-spacing: 6px;
        color: #ffffff;
        text-shadow: 0 0 10px rgba(255,255,255,0.3);
    }

    /* ADVERTISEMENT SLOTS (Professional Placement) */
    .ad-slot-top {
        width: 100%;
        height: 90px;
        background: #161b22;
        border: 1px solid #30363d;
        display: flex;
        justify-content: center;
        align-items: center;
        color: #484f58;
        font-size: 11px;
        margin-bottom: 20px;
        border-radius: 8px;
    }

    .ad-slot-side {
        width: 100%;
        height: 600px;
        background: #161b22;
        border: 1px solid #30363d;
        display: flex;
        justify-content: center;
        align-items: center;
        color: #484f58;
        border-radius: 8px;
        writing-mode: vertical-rl;
        text-orientation: mixed;
    }

    /* PREVIEW STATS - Muted & Italic */
    .preview-info {
        color: #6b7280;
        font-style: italic;
        font-size: 14px;
        margin: 15px 0;
        border-left: 3px solid #00d2ff;
        padding-left: 10px;
    }

    /* READY TO DOWNLOAD BUTTON - LUXE STYLE */
    .stDownloadButton>button {
        width: 100% !important;
        background: linear-gradient(135deg, #22c55e 0%, #166534 100%);
        color: white !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        padding: 18px !important;
        font-size: 20px !important;
        font-weight: 800 !important;
        border-radius: 12px !important;
        box-shadow: 0 10px 25px rgba(22, 101, 52, 0.4);
        text-transform: uppercase;
        letter-spacing: 2px;
    }

    /* Mobile Responsiveness */
    @media (max-width: 768px) {
        .brand-logo { font-size: 24px; letter-spacing: 3px; }
        .ad-slot-side { display: none; }
    }
    </style>
    """, unsafe_allow_html=True)

# --- NAVBAR & OTHER SERVICES ---
st.markdown("""
    <div class="velo-navbar">
        <div class="brand-logo">VELO</div>
        <div style="color: #4b5563; font-weight: 600; font-size: 12px;">VELO NETWORK SERVICES</div>
    </div>
    """, unsafe_allow_html=True)

with st.expander("🌐 OUR GLOBAL SERVICES (CLICK TO EXPLORE)"):
    st.write("• VELO Compressor - *Coming Soon*")
    st.write("• VELO Image Tools - *Coming Soon*")
    st.write("• VELO AI Scanner - *Coming Soon*")

# --- MAIN PAGE WITH AD SLOTS ---
st.markdown('<div class="ad-slot-top">ADVERTISEMENT AREA (728x90)</div>', unsafe_allow_html=True)

col_content, col_spacer, col_ad_side = st.columns([3.5, 0.2, 1])

with col_content:
    st.title("Professional PDF Table Extractor")
    st.markdown("<p style='color: #8b949e; font-size: 18px;'>High-precision data conversion for global enterprises.</p>", unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Drop PDF File", type="pdf")

    if uploaded_file:
        with open("temp.pdf", "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        try:
            with st.status("Velo Engine Analyzing...", expanded=True) as status:
                time.sleep(1.5) # Orange Energy
                tables = camelot.read_pdf("temp.pdf", pages='all', flavor='lattice')
                status.update(label="Process Complete!", state="complete", expanded=False)
            
            if len(tables) > 0:
                st.markdown(f'<div class="preview-info">({len(tables)} tables identified)</div>', unsafe_allow_html=True)
                
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
                    file_name="velo_export.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            else:
                st.error("No tables detected.")
        except Exception as e:
            st.error(f"Processing Error: {e}")
        finally:
            if os.path.exists("temp.pdf"): os.remove("temp.pdf")

with col_ad_side:
    st.markdown('<div class="ad-slot-side">AD SPACE (160x600)</div>', unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("<div style='text-align: center; color: #1f2937; margin-top: 60px; font-size: 10px;'>SECURE PROCESSING • NO DATA STORED • VELO GLOBAL 2026</div>", unsafe_allow_html=True)
