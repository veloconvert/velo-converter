import streamlit as st
import camelot
import pandas as pd
from io import BytesIO
import os
import time

# --- PURE LUXURY & MOBILE-FIX CONFIG ---
st.set_page_config(page_title="VELO", layout="wide")

# --- VELO REFINED CSS ---
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
        padding-bottom: 10px;
        border-bottom: 1px solid rgba(255,255,255,0.05);
        margin-bottom: 40px;
    }
    
    .brand-logo {
        font-weight: 800;
        font-size: 28px;
        letter-spacing: 5px;
        color: #ffffff;
    }

    /* AD SLOTS - DISCREET */
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

    /* PREVIEW & STATS */
    .stat-tag {
        color: #4b5563;
        font-style: italic;
        font-size: 13px;
        margin-top: 10px;
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
    }

    /* MOBILE ADJUSTMENTS */
    @media (max-width: 768px) {
        .brand-logo { font-size: 20px; }
        .nav-bar { padding: 10px 0; }
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER SECTION ---
col_logo, col_menu = st.columns([1, 1])
with col_logo:
    st.markdown('<div class="brand-logo">VELO</div>', unsafe_allow_html=True)

with col_menu:
    # Zarif dropdown menü butonu
    with st.popover("🌐 VELO NETWORK", use_container_width=True):
        st.markdown("**Active Services**")
        st.write("✅ PDF to Excel (This App)")
        st.divider()
        st.markdown("**Coming Soon**")
        st.write("• VELO Compressor")
        st.write("• VELO Image AI")

# --- AD SLOT TOP ---
st.markdown('<div class="ad-top">ADVERTISEMENT AREA</div>', unsafe_allow_html=True)

# --- MAIN ENGINE ---
col_main, col_spacer, col_ad_side = st.columns([3, 0.2, 1])

with col_main:
    st.title("PDF Table Extractor")
    st.markdown("<p style='color: #6b7280; margin-top:-15px;'>Professional High-Precision Conversion</p>", unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("", type="pdf", label_visibility="collapsed")

    if uploaded_file:
        with open("temp.pdf", "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        try:
            with st.status("Velo Engine Analyzing...", expanded=False) as status:
                time.sleep(1)
                tables = camelot.read_pdf("temp.pdf", pages='all', flavor='lattice')
                status.update(label="Ready", state="complete")
            
            if len(tables) > 0:
                st.markdown(f'<div class="stat-tag">({len(tables)} tables identified)</div>', unsafe_allow_html=True)
                
                all_dfs = []
                for table in tables:
                    st.dataframe(table.df, use_container_
