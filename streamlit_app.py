import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time

# ==============================================================================
# HELPER: AI RESPONSE MOCK
# ==============================================================================
def get_ai_response(user_input):
    user_input = user_input.lower()
    keywords = ['photo', 'search', 'memory', 'date', 'remember', 'vibe', 'find', 'scroll', 'metadata', 'tag', 'location', 'album', 'frustration', 'workaround']
    
    if not any(k in user_input for k in keywords):
        return "🚫 **Out of Scope:** I am unable to answer that. This query is outside the context of this project. I am specifically calibrated to analyze Voice of Customer (VoC) data regarding Google Photos search, memory recall, and retrieval friction."
        
    if 'scroll' in user_input or 'frustration' in user_input:
        return "Users frequently mention 'Chronological Scrubbing' as a major frustration. When semantic search fails, 68% of users resort to endlessly scrolling their timeline, leading to high abandonment rates."
    elif 'tag' in user_input or 'metadata' in user_input:
        return "The VoC data indicates a mismatch in tagging. The system indexes objective metadata (GPS, EXIF dates), but humans recall subjective metadata (vibes, weather, clothing)."
    else:
        return "Based on the 25,450 ingested reviews, users are struggling with 'Vague Semantic Recall'. They remember the episodic context of a photo, but lack the exact keywords the search engine demands."

# ==============================================================================
# 1. PAGE CONFIGURATION & CUSTOM CSS
# ==============================================================================
st.set_page_config(page_title="Discovery Engine", page_icon="🔍", layout="wide")

st.markdown("""
<style>
    /* Hide Streamlit components */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Global Background */
    .stApp {
        background-color: #F8F9FA;
    }
    
    /* Tighter KPI Cards */
    .kpi-card {
        background-color: #FFFFFF;
        border-radius: 8px;
        padding: 12px 16px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        border: 1px solid #E8EAED;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .kpi-label {
        font-size: 12px;
        font-weight: 600;
        color: #5F6368;
        text-transform: uppercase;
        margin-bottom: 4px;
    }
    .kpi-value {
        font-size: 28px;
        font-weight: 700;
        color: #202124;
        margin-bottom: 4px;
    }
    .kpi-trend-up {
        font-size: 12px;
        font-weight: 600;
        color: #137333;
        background-color: #E6F4EA;
        padding: 2px 6px;
        border-radius: 10px;
        align-self: flex-start;
    }
    .kpi-trend-down {
        font-size: 12px;
        font-weight: 600;
        color: #A50E0E;
        background-color: #FCE8E6;
        padding: 2px 6px;
        border-radius: 10px;
        align-self: flex-start;
    }
    
    /* Chart Container Styling */
    .chart-container {
        background-color: #FFFFFF;
        border-radius: 8px;
        padding: 15px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        border: 1px solid #E8EAED;
        margin-bottom: 15px;
    }
    
    /* Premium Chat Bubbles */
    [data-testid="stChatMessage"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E8EAED !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02) !important;
        border-radius: 12px !important;
        padding: 15px !important;
        margin-bottom: 10px !important;
    }
    [data-testid="stChatInput"] {
        border-radius: 24px !important;
        border: 1px solid #E8EAED !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05) !important;
        background-color: #FFFFFF !important;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# SIDEBAR (Filters + Chat Triggers)
# ==============================================================================
with st.sidebar:
    st.title("🔍 Recall Lens")
    st.markdown("---")
    
    st.subheader("Ingestion Sources")
    st.checkbox("r/GooglePhotos (Reddit)", value=True)
    st.checkbox("App Store Reviews", value=True)
    st.checkbox("Google Support Forums", value=True)
    
    st.markdown("---")
    st.subheader("Advanced Filters")
    st.date_input("Time Range", [datetime.today() - timedelta(days=90), datetime.today()])
    st.slider("LLM Confidence Threshold", 0.0, 1.0, 0.75, 0.05)
    st.multiselect("User Cohorts", ["Young Explorers", "Heavy Travelers", "Archivists", "Casual Snappers"], default=["Heavy Travelers", "Archivists"])
    
    st.markdown("---")
    st.subheader("Rubric Execution")
    q1_btn = st.button("What kinds of old photos do users struggle to retrieve?")
    q2_btn = st.button("What information do people actually remember about a photo?")
    q3_btn = st.button("What information have they forgotten?")
    q4_btn = st.button("How do users formulate searches when their memory is incomplete?")
    
    if st.button("🔄 Restart Chat", use_container_width=True):
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I analyze Google Photos retrieval failures. Click a question in the sidebar or ask me anything."}
        ]
        st.rerun()

# ==============================================================================
# HEADER
# ==============================================================================
st.title("Google Photos: Memory Discovery Engine")
st.markdown("Enterprise VoC Analytics & Semantic Search Failure Dashboard")

# ==============================================================================
# 1. CUSTOM TOP NAVIGATION (TABS)
# ==============================================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Query Health", "Index Telemetry", "Retrieval Friction", "Issue Tracker", "🤖 AI Discovery Chat"])

# ==============================================================================
# TAB 1: QUERY HEALTH (Dashboard)
# ==============================================================================
with tab1:
    # 2. TIGHTER KPI CARDS
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-label">Total Vol</div>
            <div class="kpi-value">25,450</div>
            <div class="kpi-trend-up">↑ +12% MoM</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-label">Retrieval Friction</div>
            <div class="kpi-value">68.2%</div>
            <div class="kpi-trend-down">↓ -5.4% MoM</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-label">Abandonment</div>
            <div class="kpi-value">42.1%</div>
            <div class="kpi-trend-down">↓ -1.2% MoM</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-label">Zero-Result Rate</div>
            <div class="kpi-value">12.4%</div>
            <div class="kpi-trend-up">↑ +0.8% MoM</div>
        </div>
        """, unsafe_allow_html=True)

    # 3. 3-COLUMN CHART GRID
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        st.markdown("**Semantic vs. Episodic Gap**")
        df_gap = pd.DataFrame({"Type": ["Semantic (System)", "Episodic (Human)"], "Val": [87.6, 12.4]})
        fig_donut = px.pie(df_gap, values='Val', names='Type', hole=0.75, 
                           color_discrete_sequence=["#1A73E8", "#EA4335"])
        fig_donut.update_layout(height=350, template="plotly_white", margin=dict(l=10, r=10, t=10, b=10),
                                legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5))
        st.plotly_chart(fig_donut, use_container_width=True, config={'displayModeBar': False})
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        st.markdown("**Manual Workarounds by Source**")
        df_work = pd.DataFrame({
            "Source": ["Reddit", "Reddit", "Reddit", "App Store", "App Store", "App Store", "Forums", "Forums", "Forums"],
            "Workaround": ["Person Pivot", "App Hopping", "Date Scrubbing"] * 3,
            "Count": [420, 210, 550, 180, 450, 310, 80, 120, 95]
        })
        fig_bar = px.bar(df_work, x="Source", y="Count", color="Workaround", 
                         color_discrete_sequence=["#1A73E8", "#34A853", "#FBBC04"])
        fig_bar.update_layout(height=350, template="plotly_white", margin=dict(l=10, r=10, t=10, b=10),
                              legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5))
        st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})
        st.markdown("</div>", unsafe_allow_html=True)

    with c3:
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        st.markdown("**Failure Modes**")
        categories = ['Wrong-Type Results', 'Zero-Results', 'Look-alikes', 'Date Misses']
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=[42, 12, 28, 18],
            theta=categories,
            fill='toself',
            name='Failures',
            line_color='#EA4335',
            fillcolor='rgba(234, 67, 53, 0.4)'
        ))
        fig_radar.update_layout(
            height=350, 
            polar=dict(radialaxis=dict(visible=True, range=[0, 50])),
            showlegend=False,
            template="plotly_white",
            margin=dict(l=30, r=30, t=20, b=20)
        )
        st.plotly_chart(fig_radar, use_container_width=True, config={'displayModeBar': False})
        st.markdown("</div>", unsafe_allow_html=True)

    # 4. 2-COLUMN CHART GRID
    st.markdown("<div style='height: 5px;'></div>", unsafe_allow_html=True)
    c4, c5 = st.columns([2, 1])
    
    with c4:
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        st.markdown("**Retrieval Friction Trend (Last 90 Days)**")
        dates = pd.date_range(start=datetime.today()-timedelta(days=90), periods=90)
        np.random.seed(42)
        friction = np.linspace(80, 60, 90) + np.random.normal(0, 3, 90)
        df_area = pd.DataFrame({'Date': dates, 'Friction Score': friction})
        
        fig_area = go.Figure()
        fig_area.add_trace(go.Scatter(x=df_area['Date'], y=df_area['Friction Score'], fill='tozeroy', mode='lines', 
                                      line=dict(color='#1A73E8', width=3), fillcolor='rgba(26, 115, 232, 0.2)'))
        fig_area.update_layout(
            height=350,
            template="plotly_white",
            margin=dict(l=10, r=10, t=10, b=10),
            yaxis=dict(title='Friction Index')
        )
        st.plotly_chart(fig_area, use_container_width=True, config={'displayModeBar': False})
        st.markdown("</div>", unsafe_allow_html=True)
        
    with c5:
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        st.markdown("**Breakdown of System Errors**")
        df_tree = pd.DataFrame({
            "Root": ["Errors"] * 4,
            "Type": ["Wrong-Type Results", "Look-alikes", "Zero-Results", "Date Misses"],
            "Val": [42, 28, 12, 18]
        })
        fig_tree = px.treemap(df_tree, path=['Root', 'Type'], values='Val',
                              color='Type', color_discrete_sequence=["#4285F4", "#FBBC04", "#34A853", "#EA4335"])
        fig_tree.update_layout(height=350, template="plotly_white", margin=dict(l=0, r=0, t=10, b=0))
        st.plotly_chart(fig_tree, use_container_width=True, config={'displayModeBar': False})
        st.markdown("</div>", unsafe_allow_html=True)

    # 5. RAW DATA TABLE
    st.markdown("### Live Index Telemetry Logs")
    st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
    mock_data = pd.DataFrame({
        "Timestamp": [(datetime.now() - timedelta(minutes=i*12)).strftime("%Y-%m-%d %H:%M:%S") for i in range(6)],
        "Source": ["Reddit", "App Store", "Reddit", "App Store", "Forums", "Reddit"],
        "Vague Query": [
            "dog sleeping on messy desk",
            "purple sunset with two people",
            "pasta in rome wearing red jacket",
            "cozy rainy feeling window",
            "mechanic tire issue text",
            "silly hat cafe 2018"
        ],
        "Detected Anchor": ["Context/Background", "Color/Vibe", "Location/Clothing", "Atmosphere", "System Event", "Clothing/Location"],
        "Status": ["Failed", "Failed", "Passed", "Failed", "Passed", "Failed"]
    })
    st.dataframe(mock_data, use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)

with tab2:
    st.info("Index Telemetry visualizations will be rendered here.")
with tab3:
    st.info("Retrieval Friction deep dives will be rendered here.")
with tab4:
    st.info("Issue Tracker integration will be rendered here.")

# ==============================================================================
# TAB 5: AI DISCOVERY CHAT
# ==============================================================================
with tab5:
    st.subheader("🤖 AI Discovery Chat")
    
    # Initialize chat history with the updated requested line
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I analyze Google Photos retrieval failures. Click a question in the sidebar or ask me anything."}
        ]

    # Handle Sidebar Question Button Clicks
    if q1_btn:
        st.session_state.messages.append({"role": "user", "content": "What kinds of old photos do users struggle to retrieve?"})
        st.session_state.messages.append({"role": "assistant", "content": "**Utility Screenshots, Vibe/Aesthetic moments, and Incidental background objects** are the most common lost items.\n\n*Simulated Quote:* \"I just want to find a photo based on the rainy weather, not the date.\" "})
    elif q2_btn:
        st.session_state.messages.append({"role": "user", "content": "What information do people actually remember about a photo?"})
        st.session_state.messages.append({"role": "assistant", "content": "Users remember **Episodic data** such as:\n- Weather\n- Clothing\n- People present\n- Emotions and vibes\n\n*Simulated Quote:* \"I remember the vibe of a purple sunset, why can't I search 'purple sunset with two people'?\""})
    elif q3_btn:
        st.session_state.messages.append({"role": "user", "content": "What information have they forgotten?"})
        st.session_state.messages.append({"role": "assistant", "content": "Users almost always forget **Semantic/System data** such as:\n- Absolute dates\n- Exact location names\n- File types\n\n*Simulated Quote:* \"Searching is useless if I don't know the exact date. I just know it was 4 years ago.\" "})
    elif q4_btn:
        st.session_state.messages.append({"role": "user", "content": "How do users formulate searches when their memory is incomplete?"})
        st.session_state.messages.append({"role": "assistant", "content": "Users rely on manual workarounds:\n- **The Person Pivot:** Users search for a known friend's face to anchor the timeline, then manually scroll to find a coffee cup.\n\n*Simulated Quote:* \"Had to check WhatsApp to find the date I texted my mechanic about a tire issue, just so I could find the photo in Google Photos by date.\" "})

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        avatar = "✨" if message["role"] == "assistant" else "👤"
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("Ask a follow-up question..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)
            
        # Display assistant response in chat message container
        with st.chat_message("assistant", avatar="✨"):
            with st.spinner("Analyzing semantic intent and querying VoC index..."):
                time.sleep(1.0)
                response = get_ai_response(prompt)
                st.markdown(response)
                
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
