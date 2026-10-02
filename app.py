import streamlit as st
import time
import pandas as pd
import plotly.express as px

# 1. Page Config & Custom Styling
st.set_page_config(page_title="Google Photos VoC Engine", layout="wide", page_icon="📸")

st.markdown("""
<style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* Global Typography & Hide defaults */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Material 3 App Background */
    .stApp {
        background: linear-gradient(180deg, #F8F9FA 0%, #E8F0FE 100%);
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #ffffff !important;
        box-shadow: 2px 0 12px rgba(0,0,0,0.05);
        border-right: 1px solid #E8EAED;
    }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h3 {
        color: #1A73E8 !important;
        font-weight: 600;
    }
    
    /* Button Styling (Material 3) */
    div.stButton > button:first-child {
        background-color: #ffffff;
        color: #1A73E8;
        border: 1px solid #DADCE0;
        border-radius: 24px;
        padding: 10px 24px;
        font-weight: 500;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        width: 100%;
        box-shadow: 0 1px 2px 0 rgba(60,64,67,0.3), 0 1px 3px 1px rgba(60,64,67,0.15);
    }
    div.stButton > button:first-child:hover {
        background-color: #F4F8LF;
        box-shadow: 0 1px 3px 0 rgba(60,64,67,0.3), 0 4px 8px 3px rgba(60,64,67,0.15);
        border-color: #1A73E8;
        transform: translateY(-1px);
        color: #174EA6;
    }
    
    /* Metric Card Styling */
    [data-testid="metric-container"] {
        background-color: white;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.04);
        border: 1px solid #E8EAED;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    [data-testid="metric-container"]:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 16px rgba(0,0,0,0.08);
    }
    [data-testid="metric-container"] label {
        color: #5F6368 !important;
        font-size: 14px !important;
        font-weight: 500 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    [data-testid="metric-container"] div[data-testid="stMetricValue"] {
        color: #202124 !important;
        font-size: 32px !important;
        font-weight: 700 !important;
        margin-top: 8px;
    }
    
    /* Info / Success Blocks (Evidence & Opportunities) */
    .stAlert {
        border-radius: 12px;
        border: none;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        padding: 20px;
    }
    
    .stRadio [role="radiogroup"] {
        background: white;
        padding: 8px;
        border-radius: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        display: inline-flex;
    }
    
    /* Header Gradient Text */
    h1 {
        background: -webkit-linear-gradient(45deg, #1A73E8, #8AB4F8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700 !important;
        padding-bottom: 20px;
    }
    
</style>
""", unsafe_allow_html=True)

# 2. The AI Control Panel (st.sidebar)
st.sidebar.markdown("### ⚙️ Discovery Engine v2.0")
st.sidebar.markdown("---")
gemini_key = st.sidebar.text_input("Gemini API Key", type="password", placeholder="Enter your key...")

st.sidebar.markdown("<br>", unsafe_allow_html=True)
st.sidebar.markdown("#### 📥 Ingestion Sources")
src_reddit = st.sidebar.checkbox("Reddit Data", value=True)
src_appstore = st.sidebar.checkbox("App Store Reviews", value=True)
src_forums = st.sidebar.checkbox("Support Forums", value=True)

st.sidebar.markdown("<br>", unsafe_allow_html=True)
st.sidebar.markdown("#### 🧠 Rubric Execution")
btn_categorize = st.sidebar.button("Categorize 'Lost' Photos")
btn_map = st.sidebar.button("Map Episodic vs Semantic Gaps")
btn_extract = st.sidebar.button("Extract Manual Workarounds")
btn_generate = st.sidebar.button("Generate Opportunity Areas")

action_clicked = btn_categorize or btn_map or btn_extract or btn_generate

# 3. Main Canvas Header
st.title("📸 Google Photos: Memory Discovery Engine")

# Simulate navigation tabs
tabs = ["Query Health", "Index Telemetry", "Retrieval Friction (Active)", "Issue Tracker"]
selected_tab = st.radio("Navigation", tabs, horizontal=True, label_visibility="hidden", index=2)

st.markdown("<br>", unsafe_allow_html=True)

# 4. Interactive Processing State
if "workflow_active" not in st.session_state:
    st.session_state.workflow_active = False

if action_clicked:
    st.session_state.workflow_active = True

if not st.session_state.workflow_active:
    st.info("👋 **System Ready.** Please configure data sources and select a workflow from the sidebar to begin analysis.", icon="ℹ️")
else:
    if action_clicked:
        with st.spinner("Ingesting 25,450 records and synthesizing behavioral heuristics..."):
            time.sleep(2.5)
        
    # 5. The Dashboard Layout
    # ROW 1 (KPIs)
    col1, col2, col3 = st.columns(3)
    col1.metric("Valid Verbatims Analyzed", "25,450", delta="+12% WoW", delta_color="normal")
    col2.metric("Primary Missing Metadata", "Absolute Dates", delta="- High Impact -", delta_color="off")
    col3.metric("Dominant Friction Pattern", "Vague Semantic Recall", delta="Alert", delta_color="inverse")
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # ROW 2 (Data Viz)
    viz_col1, viz_col2 = st.columns(2)
    
    with viz_col1:
        # Donut Chart
        donut_data = pd.DataFrame({
            "Attribute": ["Weather", "Clothes", "People", "Location", "Date"],
            "Percentage": [35, 25, 20, 15, 5]
        })
        fig_donut = px.pie(donut_data, values="Percentage", names="Attribute", 
                           title="<b>What Users Actually Remember</b>", hole=0.6,
                           color_discrete_sequence=["#1A73E8", "#EA4335", "#FBBC04", "#34A853", "#9AA0A6"])
        fig_donut.update_layout(
            margin=dict(t=40, b=0, l=0, r=0),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", size=14, color="#3C4043"),
            title_font=dict(size=18, color="#202124")
        )
        # Using a container for white card look around the chart
        with st.container():
            st.plotly_chart(fig_donut, use_container_width=True)
        
    with viz_col2:
        # Stacked Bar Chart
        bar_data = pd.DataFrame({
            "Source": ["Reddit", "Reddit", "Reddit", "App Store", "App Store", "App Store", "Forums", "Forums", "Forums"],
            "Workaround": ["Chronological Scrubbing", "Person Pivot", "App Hopping"] * 3,
            "Count": [120, 80, 20, 45, 90, 15, 60, 40, 10] 
        })
        fig_bar = px.bar(bar_data, x="Source", y="Count", color="Workaround", 
                         title="<b>Manual Workarounds by Source</b>", barmode="stack",
                         color_discrete_sequence=["#1A73E8", "#34A853", "#FBBC04"])
        fig_bar.update_layout(
            margin=dict(t=40, b=0, l=0, r=0),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", size=14, color="#3C4043"),
            title_font=dict(size=18, color="#202124"),
            xaxis_title=None,
            yaxis_title=None
        )
        with st.container():
            st.plotly_chart(fig_bar, use_container_width=True)
        
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # ROW 3 (Verbatim Evidence Grid)
    st.markdown("### 📝 Verbatim Evidence")
    
    # 1. Data Structure
    verbatims = [
        {"source": "App Store", "quote": "Searching is useless if I don't know the exact date. I remember the vibe of a purple sunset."},
        {"source": "Reddit", "quote": "I know I was wearing a red jacket, but searching 'red jacket' brings up every picture with red in it."},
        {"source": "Reddit", "quote": "I just scrolled back 4 years because I remembered it rained that day. App hopping didn't help."},
        {"source": "Support Forum", "quote": "Why can't I search for 'that time we got lost in Tokyo'?"},
        {"source": "Reddit", "quote": "I had to find a picture of my dog first, then look at the date to find the photo I actually wanted."},
        {"source": "App Store", "quote": "The semantic search is too literal. It doesn't understand context or events."},
        {"source": "Play Store", "quote": "The app is useless if I can't search for 'that one time at the beach with the green umbrella'. It only shows me generic beach photos."},
        {"source": "Support Forum", "quote": "It keeps tagging my dog as a cat. And when I search for my dog, it brings up photos of my neighbor's cat. Frustrating!"},
        {"source": "Reddit", "quote": "I remember my friend was wearing a silly hat in a cafe. Searched 'silly hat cafe' and got zero results. Had to scroll back to 2018."},
        {"source": "App Store", "quote": "I want to find the photo of the recipe I took a picture of, but searching for the dish name brings up pictures of me eating."}
    ]
    
    # Display in a grid of 3 columns
    if verbatims:
        cols = st.columns(3)
        for i, verbatim in enumerate(verbatims):
            with cols[i % 3]:
                st.info(f'**"{verbatim["quote"]}"**', icon="💬")
        
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # ROW 4 (Strategic Recommendation)
    st.success("""
    #### 💡 Strategic Product Opportunity
    Data indicates **'Vague Semantic Recall'** is the primary retrieval blocker. Build a **'Progressive Contextual Disambiguation'** MVP to allow AI-guided visual filtering.
    """)
