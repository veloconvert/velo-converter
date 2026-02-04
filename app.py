import streamlit as st
import camelot
import pandas as pd
from io import BytesIO
import os
import time

# --- SEO & META CONFIG ---
st.set_page_config(page_title="VELO | Pro PDF to Excel", layout="wide", initial_sidebar_state="collapsed")

# --- GOOGLE ANALYTICS INTEGRATION ---
# Sadece bu bölüm eklendi, geri kalan her şey senin gönderdiğin koddur.
st.markdown("""
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-DH8EXJY2DZ"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', 'G-DH8EXJY2DZ');
    </script>
    """, unsafe_allow_html=True)

# --- MASTER CSS (LOCKED & ENHANCED) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap');
    .stApp { background-color: #0b0e14; color: #e2e8f0; font-family: 'Inter', sans-serif; }
    
    /* LOGO & BRANDING */
    .brand-logo {
        font-weight: 800; font-size: clamp(45px, 10vw, 75px); letter-spacing: 15px;
        background: linear-gradient(135deg, #ffffff 0%, #cbd5e1 50%, #ffffff 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        filter: drop-shadow(0 0 20px rgba(255,255,255,0.4));
    }
    .neon-divider { height: 3px; background: #00d2ff; box-shadow: 0 0 20px #00d2ff; margin-bottom: 60px; }
    
    /* UPLOADER OVERRIDE */
    [data-testid="stFileUploader"] {
        max-width: 1000px; margin: 40px auto !important; border: 2px dashed #00d2ff !important;
        background-color: rgba(22, 27, 34, 0.8) !important; border-radius: 24px !important; padding: 50px !important;
        position: relative;
    }
    [data-testid="stFileUploadDropzone"] div div small { display: none !important; }
    [data-testid="stFileUploadDropzone"]::after {
        content: "VELO PRO | 500MB CAPACITY"; position: absolute; bottom: 20px; left: 50%;
        transform: translateX(-50%); color: #00d2ff !important; font-weight: 800 !important;
        font-size: 18px !important; letter-spacing: 3px; text-shadow: 0 0 15px rgba(0, 210, 255, 0.8);
        background-color: #161b22; padding: 5px 20px; z-index: 99;
    }

    /* FOOTER & INFO SECTIONS */
    .info-card {
        background: rgba(17, 24, 39, 0.5); border: 1px solid #1f2937;
        padding: 20px; border-radius: 12px; margin-top: 20px;
    }
    .footer-links { text-align: center; font-size: 12px; color: #4b5563; margin-top: 50px; }
    .footer-links a { color: #00d2ff; text-decoration: none; margin: 0 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
col_logo, col_serv = st.columns([4, 1])
with col_logo: st.markdown('<div class="brand-logo">VELO</div>', unsafe_allow_html=True)
with col_serv:
    st.markdown('<div style="text-align
