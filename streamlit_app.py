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
    src_reddit = st.checkbox("r/GooglePhotos (Reddit)", value=True)
    src_app = st.checkbox("App Store Reviews", value=True)
    src_forum = st.checkbox("Google Support Forums", value=True)
    
    st.markdown("---")
    st.subheader("Advanced Filters")
    conf_thresh = 0.75
    cohorts = st.multiselect("User Cohorts", ["Young Explorers", "Heavy Travelers", "Archivists", "Casual Snappers"], default=["Heavy Travelers", "Archivists"])
    
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
# DYNAMIC DATA CALCULATION BASED ON FILTERS
# ==============================================================================
# Create a multiplier based on the active filters to make the data fully reactive
active_sources = sum([src_reddit, src_app, src_forum])
source_mult = active_sources / 3.0 if active_sources > 0 else 0.05

# Since the default number of cohorts is 2, we divide by 2.0 so the default multiplier is 1.0
cohort_mult = len(cohorts) / 2.0 if len(cohorts) > 0 else 0.1

dyn_mult = max(0.1, source_mult * cohort_mult)

active_src_names = []
if src_reddit: active_src_names.append("Reddit")
if src_app: active_src_names.append("App Store")
if src_forum: active_src_names.append("Forums")

# ==============================================================================
# HEADER
# ==============================================================================
st.title("Google Photos: Memory Discovery Engine")
st.markdown("Enterprise VoC Analytics & Search Failure Dashboard")

# ==============================================================================
# 1. CUSTOM TOP NAVIGATION (TABS)
# ==============================================================================
tab1, tab2 = st.tabs(["DATA OVERVIEW", "🤖 AI Discovery Chat"])

# ==============================================================================
# TAB 1: DATA OVERVIEW (Dashboard)
# ==============================================================================
with tab1:
    # 2. TIGHTER KPI CARDS (Now dynamic)
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    
    v_vol = int(25450 * dyn_mult)
    v_fric = min(98.0, 68.2 + (conf_thresh * 10) - (source_mult * 5))
    v_aban = min(95.0, 42.1 * (1.2 - cohort_mult))
    v_zero = min(50.0, 12.4 + (conf_thresh * 5))
    
    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Total Vol</div>
            <div class="kpi-value">{v_vol:,}</div>
            <div class="kpi-trend-up">↑ +12% MoM</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Retrieval Friction</div>
            <div class="kpi-value">{v_fric:.1f}%</div>
            <div class="kpi-trend-down">↓ -5.4% MoM</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Abandonment</div>
            <div class="kpi-value">{v_aban:.1f}%</div>
            <div class="kpi-trend-down">↓ -1.2% MoM</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Zero-Result Rate</div>
            <div class="kpi-value">{v_zero:.1f}%</div>
            <div class="kpi-trend-up">↑ +0.8% MoM</div>
        </div>
        """, unsafe_allow_html=True)

    # 3. 3-COLUMN CHART GRID
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        st.markdown("**Semantic vs. Episodic Gap**")
        gap_sys = max(10, 87.6 - (conf_thresh * 10))
        gap_hum = 100 - gap_sys
        df_gap = pd.DataFrame({"Type": ["Semantic (System)", "Episodic (Human)"], "Val": [gap_sys, gap_hum]})
        fig_donut = px.pie(df_gap, values='Val', names='Type', hole=0.75, 
                           color_discrete_sequence=["#1A73E8", "#EA4335"])
        fig_donut.update_layout(height=350, template="plotly_white", margin=dict(l=10, r=10, t=10, b=10),
                                legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5))
        st.plotly_chart(fig_donut, use_container_width=True, config={'displayModeBar': False})
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        st.markdown("**Manual Workarounds by Source**")
        base_df_work = pd.DataFrame({
            "Source": ["Reddit", "Reddit", "Reddit", "App Store", "App Store", "App Store", "Forums", "Forums", "Forums"],
            "Workaround": ["Person Pivot", "App Hopping", "Date Scrubbing"] * 3,
            "Count": [420, 210, 550, 180, 450, 310, 80, 120, 95]
        })
        # Filter based on sidebar sources
        df_work = base_df_work[base_df_work["Source"].isin(active_src_names)] if active_src_names else base_df_work
        # Apply scaling based on cohorts/confidence
        df_work['Count'] = (df_work['Count'] * cohort_mult * (1.1 - conf_thresh) * 2).astype(int)
        
        if not df_work.empty:
            fig_bar = px.bar(df_work, x="Source", y="Count", color="Workaround", 
                             color_discrete_sequence=["#1A73E8", "#34A853", "#FBBC04"])
            fig_bar.update_layout(height=350, template="plotly_white", margin=dict(l=10, r=10, t=10, b=10),
                                  legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5))
            st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})
        else:
            st.warning("Please select at least one Ingestion Source.")
        st.markdown("</div>", unsafe_allow_html=True)

    with c3:
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        st.markdown("**Failure Modes**")
        categories = ['Wrong-Type Results', 'Zero-Results', 'Look-alikes', 'Date Misses']
        r_vals = np.array([42, 12, 28, 18]) * dyn_mult * 2
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=r_vals,
            theta=categories,
            fill='toself',
            name='Failures',
            line_color='#EA4335',
            fillcolor='rgba(234, 67, 53, 0.4)'
        ))
        fig_radar.update_layout(
            height=350, 
            polar=dict(radialaxis=dict(visible=True, range=[0, max(50, max(r_vals)*1.2)])),
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
        
        # Change random seed based on filter state so chart changes dynamically
        np.random.seed(int(conf_thresh * 100) + len(cohorts) + active_sources)
        friction = np.linspace(80, 60, 90) + np.random.normal(0, 3 + (1-conf_thresh)*5, 90)
        friction = friction * (0.6 + 0.4 * dyn_mult)
        
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
        tree_vals = np.array([42, 28, 12, 18]) * dyn_mult
        df_tree = pd.DataFrame({
            "Root": ["Errors"] * 4,
            "Type": ["Wrong-Type Results", "Look-alikes", "Zero-Results", "Date Misses"],
            "Val": tree_vals
        })
        fig_tree = px.treemap(df_tree, path=['Root', 'Type'], values='Val',
                              color='Type', color_discrete_sequence=["#4285F4", "#FBBC04", "#34A853", "#EA4335"])
        fig_tree.update_layout(height=350, template="plotly_white", margin=dict(l=0, r=0, t=10, b=0))
        st.plotly_chart(fig_tree, use_container_width=True, config={'displayModeBar': False})
        st.markdown("</div>", unsafe_allow_html=True)

    # 5. RAW DATA TABLE
    st.markdown("### Live Index Telemetry Logs")
    st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
    base_mock_data = pd.DataFrame({
        "Timestamp": [(datetime.now() - timedelta(minutes=i*12)).strftime("%Y-%m-%d %H:%M:%S") for i in range(12)],
        "Source": ["Reddit", "App Store", "Reddit", "App Store", "Forums", "Reddit", "App Store", "Forums", "Reddit", "App Store", "Forums", "Reddit"],
        "Vague Query": [
            "dog sleeping on messy desk",
            "purple sunset with two people",
            "pasta in rome wearing red jacket",
            "cozy rainy feeling window",
            "mechanic tire issue text",
            "silly hat cafe 2018",
            "blue house snow",
            "receipt from target 2021",
            "hiking boots mud",
            "airport terminal running",
            "concert lights blurry",
            "cat under blanket"
        ],
        "Detected Anchor": ["Context", "Color", "Location", "Atmosphere", "System Event", "Clothing", "Color", "System Event", "Context", "Location", "Vibe", "Context"],
        "Status": ["Failed", "Failed", "Passed", "Failed", "Passed", "Failed", "Failed", "Passed", "Failed", "Passed", "Failed", "Failed"]
    })
    
    # Filter based on sources
    if active_src_names:
        df_telemetry = base_mock_data[base_mock_data["Source"].isin(active_src_names)]
    else:
        df_telemetry = base_mock_data.head(0) # empty
        
    st.dataframe(df_telemetry.head(6), use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ==============================================================================
# TAB 2: AI DISCOVERY CHAT
# ==============================================================================
with tab2:
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
