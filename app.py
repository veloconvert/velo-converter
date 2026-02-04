import streamlit as st
import camelot
import pandas as pd
from io import BytesIO
import os
import time

# --- SAFE PAGE CONFIG (Safari Fix) ---
st.set_page_config(page_title="VELO", layout="wide")

# --- MOBILE & DESKTOP OPTIMIZED CSS ---
st.markdown("""
    <style>
    /* Base Background */
    .stApp { background-color: #0e1117; color: #ffffff; }

    /* Custom Header with dynamic font size */
    .brand-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 15px 0;
        border-bottom: 1px solid #1f2937;
        margin-bottom: 25px;
    }
    
    .brand-name {
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        font-size: clamp(20px, 6vw, 30px);
        letter-spacing: 5px;
        color: #ffffff;
    }

    .network-tag {
        color: #4b5563;
        font-size: clamp(10px, 3vw, 13px);
        text-align: right;
        line-height: 1.2;
    }

    /* NEON CONTAINER - Optimized for Mobile Padding */
    .main-box {
        border: 2px solid #00d2ff;
        border-radius: 15px;
        padding: clamp(15px, 4vw, 30px);
        background: rgba(13, 17, 23, 0.9);
        box-shadow: 0 0 20px rgba(0, 210, 255, 0.15);
    }

    /* Hidden Streamlit Header for cleaner look */
    header {visibility: hidden;}
    footer {visibility: hidden;}

    /* Mobile Responsive Buttons */
    .stDownloadButton>button {
        width: 100% !important;
        max-width: 500px;
        margin: 20px auto !important;
        display: block;
        background: linear-gradient(145deg, #22c55e, #166534);
        border: 1px solid rgba(255,255,255,0.2) !important;
        padding: 15px !important;
        font-size: 18px !important;
        border-radius: 50px !important;
        box-shadow: 0 8px 20px rgba(22, 101, 52, 0.3);
    }

    /* Input Field Fix for Mobile */
    .stFileUploader {
        border: 1px dashed #30363d !important;
        border-radius: 12px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER AREA ---
st.markdown("""
    <div class="brand-header">
        <div class="brand-name">VELO</div>
        <div class="network-tag">VELO NETWORK<br>PDF SERVICES</div>
    </div>
    """, unsafe_allow_html=True)

# --- APP TITLE ---
st.title("PDF Table Extractor")
st.markdown("<p style='color: #9ca3af; margin-top: -15px;'>Professional Data Conversion</p>", unsafe_allow_html=True)

# --- MAIN ENGINE ---
uploaded_file = st.file_uploader("Upload PDF", type="pdf")

if uploaded_file:
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    try:
        with st.status("Processing...", expanded=True) as status:
            time.sleep(1) # Visual feedback
            tables = camelot.read_pdf("temp.pdf", pages='all', flavor='lattice')
            status.update(label="Analysis Ready!", state="complete", expanded=False)
        
        if len(tables) > 0:
            st.markdown(f"<p style='color: #4b5563; font-style: italic;'>({len(tables)} tables identified)</p>", unsafe_allow_html=True)
            
            all_dfs = []
            for i, table in enumerate(tables):
                # We use container width to ensure it doesn't break mobile view
                st.dataframe(table.df, use_container_width=True)
                all_dfs.append(table.df)
            
            # Excel Prep
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                for i, df in enumerate(all_dfs):
                    df.to_excel(writer, index=False, header=False, sheet_name=f'Table_{i+1}')
            
            # THE LUXE BUTTON
            st.download_button(
                label="✅ READY TO DOWNLOAD",
                data=output.getvalue(),
                file_name="velo_export.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            
        else:
            st.error("No tables detected.")
    except Exception as e:
        st.error("An error occurred. Check PDF structure.")
    finally:
        if os.path.exists("temp.pdf"): os.remove("temp.pdf")

# --- FOOTER ---
st.markdown("<div style='text-align: center; color: #1f2937; font-size: 10px; margin-top: 40px;'>SECURE • GLOBAL • VELO</div>", unsafe_allow_html=True)
