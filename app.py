import streamlit as st
import camelot
import pandas as pd
from io import BytesIO
import os
import time

# --- PAGE CONFIG ---
st.set_page_config(page_title="VELO | PDF to Excel Pro", layout="wide", page_icon="📊")

# --- CUSTOM CSS (LUXURY & BRANDING) ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    
    /* VELO BRAND SIGNATURE (Top Left) */
    .brand-signature {
        position: absolute;
        top: -60px;
        left: 0;
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        font-size: 24px;
        letter-spacing: 4px;
        color: #ffffff;
        opacity: 0.9;
        text-transform: uppercase;
    }

    /* TABLE COUNTER STYLE */
    .table-counter {
        color: #484f58; /* Muted color */
        font-style: italic;
        font-size: 14px;
        margin-top: -10px;
        margin-bottom: 20px;
    }

    /* LUXURY GREEN DOWNLOAD BUTTON */
    .stDownloadButton>button {
        display: block;
        margin: 40px auto;
        background: linear-gradient(145deg, #2ea44f, #22863a);
        color: white !important;
        border: 1px solid #ffffff33 !important;
        padding: 15px 50px !important;
        font-size: 20px !important;
        font-weight: 700 !important;
        border-radius: 50px !important;
        box-shadow: 0 10px 20px rgba(0,0,0,0.3);
        text-transform: uppercase;
        transition: all 0.3s ease;
    }
    
    /* Other CSS rules remain for top menu and layout... */
    .other-sites-menu { display: flex; justify-content: flex-end; gap: 25px; padding: 15px 0; border-bottom: 1px solid #30363d; margin-bottom: 40px; }
    .other-sites-menu a { color: #8b949e; text-decoration: none; font-size: 14px; }
    </style>
    """, unsafe_allow_html=True)

# --- BRANDING & TOP NAV ---
st.markdown('<div class="brand-signature">VELO</div>', unsafe_allow_html=True)

st.markdown("""
    <div class="other-sites-menu">
        <a href="#">Compress</a> <a href="#">Merge</a> <a href="#">Edit</a> <a href="#">OCR</a>
    </div>
    """, unsafe_allow_html=True)

# --- MAIN HEADER ---
st.title("Professional PDF Table Extractor")
st.markdown("<p style='color: #8b949e;'>Precision-engineered table extraction for global enterprises.</p>", unsafe_allow_html=True)

# --- UPLOAD SECTION ---
uploaded_file = st.file_uploader("Drop your PDF here", type="pdf")

if uploaded_file:
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    try:
        with st.status("Analyzing...", expanded=True) as status:
            time.sleep(1.5) # Orange energy simulation
            tables = camelot.read_pdf("temp.pdf", pages='all', flavor='lattice')
            status.update(label="Complete!", state="complete", expanded=False)
        
        if len(tables) > 0:
            st.markdown("### Data Preview")
            # TABLE COUNTER (LUXURY MUTED ITALIC)
            st.markdown(f'<div class="table-counter">({len(tables)} tables identified)</div>', unsafe_allow_html=True)
            
            all_dfs = []
            for i, table in enumerate(tables):
                df = table.df.copy()
                # (Existing Header Fix Logic Remains Here)
                if df.shape[1] > 5 and df.iloc[0, 4] == "Results":
                    df.iloc[0, 5] = "Results"
                    if df.shape[0] > 1 and (df.iloc[1, 4] != "" or df.iloc[1, 5] != ""):
                        df.iloc[0, 4] = f"Results - {df.iloc[1, 4]}"
                        df.iloc[0, 5] = f"Results - {df.iloc[1, 5]}"
                        df = df.drop(1).reset_index(drop=True)
                
                st.dataframe(df, use_container_width=True)
                all_dfs.append(df)
            
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                for i, df in enumerate(all_dfs):
                    df.to_excel(writer, index=False, header=False, sheet_name=f'Table_{i+1}')
            
            st.download_button(label="✅ READY TO DOWNLOAD", data=output.getvalue(), file_name="velo_export.xlsx")
            
        else:
            st.error("No tables found.")
    except Exception as e:
        st.error(f"Error: {e}")
    finally:
        if os.path.exists("temp.pdf"): os.remove("temp.pdf")