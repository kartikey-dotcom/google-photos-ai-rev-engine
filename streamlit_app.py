import streamlit as st
import streamlit.components.v1 as components
import os

# Configure the Streamlit page
st.set_page_config(
    page_title="Google Photos VoC Intelligence",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Hide Streamlit's default UI elements to make it look like a standalone app
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            header {visibility: hidden;}
            footer {visibility: hidden;}
            .block-container {padding-top: 0rem; padding-bottom: 0rem;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

st.warning("⚠️ **Note:** This application was built as a pure Frontend (HTML/CSS/JS) app. While this Streamlit wrapper allows it to deploy here, for the best performance and functionality (especially with local Javascript modules), we highly recommend deploying directly to **GitHub Pages**, **Vercel**, or **Netlify**.")

# Note: Streamlit's components.html isolates the HTML in an iframe. 
# Relative links to CSS and JS files in the repo often fail to load in Streamlit Cloud 
# because they aren't served by the Streamlit backend automatically. 
# If the UI looks broken, it's because Streamlit is blocking the local CSS/JS files.
try:
    with open("streamlit_index.html", "r", encoding="utf-8") as f:
        html_code = f.read()
        
    # Bridge Streamlit Secrets (TOML) to the Frontend
    if "GEMINI_API_KEY" in st.secrets:
        injected_key = st.secrets["GEMINI_API_KEY"]
        injection_script = f'<script>window.STREAMLIT_INJECTED_KEY = "{injected_key}";</script>'
        html_code = html_code.replace('<head>', f'<head>\n{injection_script}')

    components.html(html_code, height=900, scrolling=True)
except Exception as e:
    st.error(f"Failed to load frontend: {e}")
