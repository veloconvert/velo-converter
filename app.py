import streamlit as st
import camelot
import pandas as pd
from io import BytesIO
import os
import time

# --- PURE LUXURY CONFIG ---
st.set_page_config(page_title="VELO", layout="wide")

# --- VELO REFINED MASTER CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap');
    
    .stApp { background-color: #0b0e14; color: #e2e8f0; font-family: 'Inter', sans-serif; }
    
    /* LOGO: MASSIVE PEARLY METALLIC WHITE */
    .brand-logo {
        font-weight: 800;
        font-size: clamp(40px, 8vw, 60px); /* Büyütüldü */
        letter-spacing: 12px;
        background: linear-gradient(135deg, #ffffff 0%, #cbd5e1 50%, #ffffff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        filter: drop-shadow(0 0 15px rgba(255,255,255,0.4));
        margin-bottom: 5px;
    }

    /* THE NEON LINE - FULL WIDTH DIVIDER */
    .neon-divider {
        height: 2px;
        background: #00d2ff;
        box-shadow: 0 0 15px #00d2ff, 0 0 5px #00d2ff;
        margin: 0 0 40px 0;
        border: none;
    }

    /* NAVIGATION AREA */
    .nav-container {
        display: flex;
        justify-content: space-between;
        align-items: flex-end; /* Tabana hizalı */
        padding: 40px 0 10px 0;
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

    /* READY TO DOWNLOAD BUTTON */
    .stDownloadButton>button {
        width: 100% !important;
        background: linear-gradient(135deg, #22c55e 0%, #15803d 100%);
        color: white !important;
        padding: 18px !important;
        font-size: 20px !important;
        font-weight: 800 !important;
        border-radius: 12px !important;
        border: none !important;
        box-shadow: 0 10px 25px rgba(22, 101, 52, 0.3);
        text-transform: uppercase;
    }

    /* MOBILE ADJUSTMENTS */
    @media (max-width: 768px) {
        .brand-logo { font-size: 32px; letter-spacing: 5px; }
        .ad-side { display: none; }
        .nav-container { flex-direction: column; align-items: flex-start; gap: 20px; }
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER SECTION ---
st.markdown('<div class="nav-container">', unsafe_allow_html=True)
col_left, col_right = st.columns([3, 1]) # Butonu sağa itmek için oran artırıldı

with col_left:
    st.markdown('<div class="brand-logo">VELO</div>', unsafe_allow_html=True)

with col_right:
    # Sağa yaslanmış, şık servis butonu
    st.markdown('<div style="text-align: right;">', unsafe_allow_html=True)
    with st.popover("🌐 OUR SERVICES", use_container_width=True):
        st.markdown("**Network Nodes**")
        st.write("✅ PDF Table Extractor")
        st.divider()
        st.write("• VELO Compressor (Soon)")
        st.write("• VELO Image Lab (Soon)")
    st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# THE NEON DIVIDER
st.markdown('<div class="neon-divider"></div>', unsafe_allow_html=True)

# --- TOP AD SLOT ---
st.markdown('<div class="ad-box" style="height:90px; margin-bottom:40px;">ADVERTISEMENT SPACE</div>', unsafe_allow_html=True)

# --- MAIN CONTENT ---
col_content, col_spacer, col_ad_side = st.columns([3, 0.1, 1])

with col_content:
    st.title("Professional PDF Table Extractor")
    st.markdown("<p style='color: #6b7280; font-size: 18px; margin-top:-15px;'>High-Precision Enterprise Data Conversion</p>", unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("", type="pdf", label_visibility="collapsed")

    if uploaded_file:
        with open("temp.pdf", "wb") as f:
            f.write(uploaded_file.getbuffer())
        try:
            with st.status("Velo Engine Initializing...", expanded=False):
                time.sleep(1)
                tables = camelot.read_pdf("temp.pdf", pages='all', flavor='lattice')
            
            if len(tables) > 0:
                st.info(f"{len(tables)} tables identified and parsed successfully.")
                all_dfs = []
                for table in tables:
                    st.dataframe(table.df, use_container_width=True)
                    all_dfs.append(table.df)
                
                output = BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    for i, df in enumerate(all_dfs):
                        df.to_excel(writer, index=False, header=False, sheet_name=f'Table_{i+1}')
                
                st.download_button(label="✅ READY TO DOWNLOAD", data=output.getvalue(), file_name="velo_export.xlsx")
            else:
                st.error("No extractable tables found.")
        except:
            st.error("Engine processing error. Check document encryption.")
        finally:
            if os.path.exists("temp.pdf"): os.remove("temp.pdf")

with col_ad_side:
    st.markdown('<div class="ad-box" style="height:600px; writing-mode:vertical-rl; padding:10px;">ADVERTISEMENT SPACE</div>', unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("<div style='text-align: center; color: #1f2937; font-size: 11px; margin-top: 80px;'>VELO GLOBAL • SECURE DATA PROTOCOLS • 2026</div>", unsafe_allow_html=True)
