import streamlit as st
import camelot
import pandas as pd
from io import BytesIO
import os
import time

# --- PERFORMANCE CONFIG ---
st.set_page_config(page_title="VELO", layout="wide")

# --- VELO NİHAİ CSS (THE PHANTOM MASK) ---
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
        margin-bottom: 5px;
    }

    .neon-divider {
        height: 3px;
        background: #00d2ff;
        box-shadow: 0 0 20px #00d2ff;
        margin-bottom: 60px;
    }

    /* CENTERED MASSIVE UPLOADER AREA */
    [data-testid="stFileUploader"] {
        max-width: 1000px;
        margin: 60px auto !important;
        border: 2px dashed #00d2ff !important;
        background-color: rgba(22, 27, 34, 0.8) !important;
        border-radius: 24px !important;
        padding: 50px !important;
        position: relative;
    }

    /* THE GHOST MASK: Bu kısım 200MB yazısını fiziksel olarak kapatır */
    [data-testid="stFileUploadDropzone"] div div small {
        opacity: 0 !important;
        display: none !important;
    }
    
    /* Yeni ve güçlü 500MB PRO yazısı */
    [data-testid="stFileUploadDropzone"]::after {
        content: "VELO PRO | 500MB CAPACITY";
        position: absolute;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%);
        color: #00d2ff !important;
        font-weight: 800 !important;
        font-size: 18px !important;
        letter-spacing: 3px;
        text-shadow: 0 0 15px rgba(0, 210, 255, 0.8);
        background-color: #161b22; /* Yazının arkasını kapatmak için */
        padding: 5px 20px;
        z-index: 99;
    }

    /* AD SLOTS */
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

    /* BUTTONS */
    .stDownloadButton>button {
        width: 100% !important;
        max-width: 600px;
        margin: 50px auto !important;
        display: block;
        background: linear-gradient(135deg, #22c55e 0%, #15803d 100%);
        padding: 22px !important;
        font-size: 24px !important;
        font-weight: 800 !important;
        border-radius: 60px !important;
        box-shadow: 0 15px 40px rgba(22, 101, 52, 0.4);
    }
    
    @media (max-width: 768px) {
        .brand-logo { font-size: 35px; letter-spacing: 8px; }
        [data-testid="stFileUploadDropzone"]::after { font-size: 14px; bottom: 10px; }
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
col_logo, col_serv = st.columns([4, 1])
with col_logo:
    st.markdown('<div class="brand-logo">VELO</div>', unsafe_allow_html=True)
with col_serv:
    st.markdown('<div style="text-align: right; margin-top: 35px;">', unsafe_allow_html=True)
    with st.popover("🌐 OUR SERVICES", use_container_width=True):
        st.write("✅ PDF to Excel Pro")
        st.divider()
        st.write("• VELO Compressor")
        st.write("• VELO Security Lab")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="neon-divider"></div>', unsafe_allow_html=True)

# --- LAYOUT ---
col_main, col_spacer, col_ad_side = st.columns([4, 0.5, 1])

with col_main:
    st.markdown('<div class="ad-slot" style="height:90px; margin-bottom:50px;">TOP ADVERTISEMENT</div>', unsafe_allow_html=True)
    
    st.title("Professional PDF Table Extractor")
    st.markdown("<p style='color: #8b949e; font-size: 22px;'>Enterprise-Grade Data Hub</p>", unsafe_allow_html=True)
    
    # 500MB Limit tanımlı uploader
    uploaded_file = st.file_uploader("", type="pdf", label_visibility="collapsed")

    if uploaded_file:
        if uploaded_file.size > 500 * 1024 * 1024:
            st.error("File exceeds 500MB VELO PRO limit.")
        else:
            with open("temp.pdf", "wb") as f:
                f.write(uploaded_file.getbuffer())
            try:
                with st.status("VELO ENGINE PROCESSING...", expanded=True):
                    time.sleep(1)
                    tables = camelot.read_pdf("temp.pdf", pages='all', flavor='lattice')
                
                if len(tables) > 0:
                    st.success(f"Extracted {len(tables)} tables.")
                    for table in tables:
                        st.dataframe(table.df, use_container_width=True)
                    
                    output = BytesIO()
                    with pd.ExcelWriter(output, engine='openpyxl') as writer:
                        for i, table in enumerate(tables):
                            table.df.to_excel(writer, index=False, header=False, sheet_name=f'Table_{i+1}')
                    
                    st.download_button(label="✅ READY TO DOWNLOAD", data=output.getvalue(), file_name="velo_export.xlsx")
                else:
                    st.error("No tables found.")
            except:
                st.error("Processing error.")
            finally:
                if os.path.exists("temp.pdf"): os.remove("temp.pdf")

with col_ad_side:
    st.markdown('<div class="ad-slot" style="height:600px; writing-mode:vertical-rl; padding:20px; margin-top:100px;">SIDE ADVERTISEMENT</div>', unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("<div style='text-align: center; color: #1f2937; font-size: 11px; margin-top: 100px;'>VELO GLOBAL • 500MB PRO CAPACITY • 2026</div>", unsafe_allow_html=True)
