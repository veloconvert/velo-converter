import streamlit as st
import camelot
import pandas as pd
from io import BytesIO
import os
import time

# --- PERFORMANCE & LIMIT CONFIG ---
# 500MB Limit tanımlıyoruz (Streamlit Cloud sağlığı için ideal limit)
st.set_page_config(page_title="VELO", layout="wide")

# --- VELO NİHAİ CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap');
    
    .stApp { background-color: #0b0e14; color: #e2e8f0; font-family: 'Inter', sans-serif; }
    
    /* LOGO: MASSIVE PEARLY METALLIC WHITE */
    .brand-logo {
        font-weight: 800;
        font-size: clamp(45px, 10vw, 75px);
        letter-spacing: 15px;
        background: linear-gradient(135deg, #ffffff 0%, #cbd5e1 50%, #ffffff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        filter: drop-shadow(0 0 20px rgba(255,255,255,0.4));
    }

    .neon-divider {
        height: 3px;
        background: #00d2ff;
        box-shadow: 0 0 20px #00d2ff;
        margin-bottom: 50px;
    }

    /* CENTERED BIG UPLOADER WITH CUSTOM TEXT */
    .stFileUploader {
        max-width: 900px;
        margin: 50px auto !important;
        border: 2px dashed #00d2ff !important;
        background-color: rgba(22, 27, 34, 0.7) !important;
        border-radius: 20px !important;
        padding: 40px !important;
    }
    
    /* Hiding the default 200MB limit label and adding our own vibe */
    .stFileUploader section [data-testid="stFileUploadDropzone"] div:nth-child(2) {
        visibility: hidden;
    }
    .stFileUploader section [data-testid="stFileUploadDropzone"]::after {
        content: "VELO PRO LIMIT: 500MB PER FILE";
        color: #00d2ff;
        font-weight: 700;
        font-size: 14px;
        display: block;
        margin-top: -20px;
    }

    .ad-slot {
        background: #111827;
        border: 1px solid #1f2937;
        border-radius: 8px;
        display: flex;
        justify-content: center;
        align-items: center;
        color: #374151;
        font-size: 11px;
    }

    .stDownloadButton>button {
        width: 100% !important;
        max-width: 500px;
        margin: 40px auto !important;
        display: block;
        background: linear-gradient(135deg, #22c55e 0%, #15803d 100%);
        padding: 20px !important;
        font-size: 22px !important;
        font-weight: 800 !important;
        border-radius: 50px !important;
        box-shadow: 0 15px 35px rgba(22, 101, 52, 0.4);
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
col_l, col_r = st.columns([4, 1])
with col_l:
    st.markdown('<div class="brand-logo">VELO</div>', unsafe_allow_html=True)
with col_r:
    st.markdown('<div style="text-align: right; margin-top: 20px;">', unsafe_allow_html=True)
    with st.popover("🌐 OUR SERVICES", use_container_width=True):
        st.write("✅ PDF Table Extractor")
        st.divider()
        st.write("• VELO Compressor")
        st.write("• VELO Security Hub")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="neon-divider"></div>', unsafe_allow_html=True)

# --- CONTENT & ADS ---
col_main, col_spacer, col_ad = st.columns([3.5, 0.5, 1])

with col_main:
    st.markdown('<div class="ad-slot" style="height:90px; margin-bottom:40px;">ADVERTISEMENT AREA</div>', unsafe_allow_html=True)
    
    st.title("Professional PDF Table Extractor")
    st.markdown("<p style='color: #8b949e; font-size: 20px;'>Enterprise-grade extraction. No small limits.</p>", unsafe_allow_html=True)
    
    # 500MB Limit uploader
    uploaded_file = st.file_uploader("", type="pdf", label_visibility="collapsed")

    if uploaded_file:
        if uploaded_file.size > 500 * 1024 * 1024:
            st.error("File too large. Maximum size is 500MB.")
        else:
            with open("temp.pdf", "wb") as f:
                f.write(uploaded_file.getbuffer())
            try:
                with st.status("VELO ENGINE PROCESSING...", expanded=True):
                    time.sleep(1)
                    tables = camelot.read_pdf("temp.pdf", pages='all', flavor='lattice')
                
                if len(tables) > 0:
                    st.success(f"Success: {len(tables)} tables extracted.")
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
                    st.error("No tables detected.")
            except:
                st.error("Engine processing error.")
            finally:
                if os.path.exists("temp.pdf"): os.remove("temp.pdf")

with col_ad:
    st.markdown('<div class="ad-slot" style="height:600px; writing-mode:vertical-rl; padding:20px;">SIDE ADVERTISEMENT</div>', unsafe_allow_html=True)

st.markdown("<div style='text-align: center; color: #1f2937; font-size: 11px; margin-top: 100px;'>VELO GLOBAL • 500MB PRO LIMIT • 2026</div>", unsafe_allow_html=True)
