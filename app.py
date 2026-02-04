import streamlit as st
import camelot
import pandas as pd
from io import BytesIO
import os
import time

# --- UI SETTINGS (PERMANENTLY LOCKED) ---
st.set_page_config(page_title="VELO", layout="wide")

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
    [data-testid="stFileUploadDropzone"] div div small { display: none !important; }
    [data-testid="stFileUploadDropzone"]::after {
        content: "VELO PRO | 500MB CAPACITY"; position: absolute; bottom: 20px; left: 50%;
        transform: translateX(-50%); color: #00d2ff !important; font-weight: 800 !important;
        font-size: 18px !important; letter-spacing: 3px; text-shadow: 0 0 15px rgba(0, 210, 255, 0.8);
    }
    .preview-header { font-size: 24px; font-weight: 700; color: #ffffff; margin-top: 40px; border-bottom: 1px solid #1f2937; padding-bottom: 10px; }
    .table-stat-info { color: #00d2ff; font-style: italic; font-size: 14px; margin-bottom: 20px; }
    .stDownloadButton>button {
        width: 100% !important; max-width: 600px; margin: 50px auto !important; display: block;
        background: linear-gradient(135deg, #22c55e 0%, #15803d 100%); padding: 22px !important;
        font-size: 24px !important; font-weight: 800 !important; border-radius: 60px !important;
        box-shadow: 0 15px 40px rgba(22, 101, 52, 0.4);
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
col_logo, col_serv = st.columns([4, 1])
with col_logo: st.markdown('<div class="brand-logo">VELO</div>', unsafe_allow_html=True)
with col_serv:
    st.markdown('<div style="text-align: right; margin-top: 35px;">', unsafe_allow_html=True)
    with st.popover("🌐 OUR SERVICES", use_container_width=True):
        st.write("✅ PDF to Excel Pro")
        st.divider()
        st.write("• VELO Compressor")
    st.markdown('</div>', unsafe_allow_html=True)
st.markdown('<div class="neon-divider"></div>', unsafe_allow_html=True)

# --- LOGIC ---
col_main, col_spacer, col_ad_side = st.columns([4, 0.5, 1])

with col_main:
    st.title("Professional PDF Table Extractor")
    st.markdown("<p style='color: #8b949e; font-size: 22px;'>Elite Precision Data Conversion</p>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("", type="pdf", label_visibility="collapsed")

    if uploaded_file:
        with open("temp.pdf", "wb") as f: f.write(uploaded_file.getbuffer())
        try:
            with st.status("VELO LEGACY ENGINE PROCESSING...", expanded=True):
                time.sleep(1)
                tables = camelot.read_pdf("temp.pdf", pages='all', flavor='lattice', line_scale=40)
            
            if len(tables) > 0:
                st.markdown('<div class="preview-header">Data Preview</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="table-stat-info">Success: {len(tables)} tables identified.</div>', unsafe_allow_html=True)
                
                all_cleaned_dfs = []
                for i, table in enumerate(tables):
                    df = table.df.copy()
                    
                    # --- THE LEGACY CLEANING ALGORITHM ---
                    # 1. Tamamen boş satırları ve sütunları uçur
                    df = df.replace(r'^\s*$', pd.NA, regex=True).dropna(how='all').dropna(axis=1, how='all')
                    
                    # 2. Results karmaşasını çözmek için ilk satırı kontrol et ve temizle
                    if not df.empty:
                        # İlk satırı başlık yap
                        new_header = df.iloc[0] 
                        df = df[1:] 
                        df.columns = new_header
                        
                        # 3. Tekrar index sıfırla ve varsa NaN başlıkları temizle
                        df = df.reset_index(drop=True)
                        df.columns = [str(c).replace('\n', ' ').strip() for c in df.columns]
                    
                    st.markdown(f"**Table {i+1}**")
                    st.dataframe(df, use_container_width=True)
                    all_cleaned_dfs.append(df)
                
                output = BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    for i, df in enumerate(all_cleaned_dfs):
                        df.to_excel(writer, index=False, sheet_name=f'Table_{i+1}')
                
                st.download_button(label="✅ READY TO DOWNLOAD", data=output.getvalue(), file_name="velo_export.xlsx")
            else: st.error("No tables detected.")
        except Exception as e: st.error(f"Error: {e}")
        finally:
            if os.path.exists("temp.pdf"): os.remove("temp.pdf")

with col_ad_side: st.markdown('<div style="height:600px; background:#111827; border:1px solid #1f2937; border-radius:8px; writing-mode:vertical-rl; padding:20px; margin-top:100px; color:#374151; display:flex; align-items:center; justify-content:center;">ADVERTISEMENT</div>', unsafe_allow_html=True)

st.markdown("<div style='text-align: center; color: #1f2937; font-size: 11px; margin-top: 100px;'>VELO GLOBAL • 500MB PRO CAPACITY • 2026</div>", unsafe_allow_html=True)
