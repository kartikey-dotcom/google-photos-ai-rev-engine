import streamlit as st
import pandas as pd
import plotly.express as px
import time

st.set_page_config(page_title="Discovery Engine", page_icon="🔍", layout="wide")

# ==============================================================================
# 1. SIDEBAR CLEANUP
# ==============================================================================
st.sidebar.image("logo.svg", width=60)
st.sidebar.title("Google Photos")
st.sidebar.markdown("---")

st.sidebar.subheader("Ingestion Sources")
src_reddit = st.sidebar.checkbox("r/GooglePhotos (Reddit)", value=True)
src_appstore = st.sidebar.checkbox("App Store Reviews", value=True)
src_forums = st.sidebar.checkbox("Google Support Forums", value=True)

st.sidebar.markdown("---")
st.sidebar.subheader("Rubric Execution")
q1_btn = st.sidebar.button("What kinds of old photos do users struggle to retrieve?")
q2_btn = st.sidebar.button("What information do people actually remember about a photo?")
q3_btn = st.sidebar.button("What information have they forgotten?")
q4_btn = st.sidebar.button("How do users formulate searches when their memory is incomplete?")

# ==============================================================================
# 2. INTERACTIVE PYTHON LOGIC & STATE MANAGEMENT
# ==============================================================================
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I have ingested 25,450 user reviews from Reddit, App Stores, and Forums regarding Google Photos search failures. Click a question in the sidebar, or ask me anything."}
    ]

if "current_view" not in st.session_state:
    st.session_state.current_view = "📊 Data Overview"

# Smart Sidebar Logic
if q1_btn or q2_btn or q3_btn or q4_btn:
    st.session_state.current_view = "🤖 AI Discovery Chat"

# 3. REQUIRED PRE-DEFINED AI RESPONSES
if q1_btn:
    st.session_state.messages.append({"role": "user", "content": "What kinds of old photos do users struggle to retrieve?"})
    st.session_state.messages.append({"role": "assistant", "content": """**Utility Screenshots, Vibe/Aesthetic moments, and Incidental background objects** are the most common lost items.\n\n*Simulated Quote:* "I just want to find a photo based on the rainy weather, not the date." """})
elif q2_btn:
    st.session_state.messages.append({"role": "user", "content": "What information do people actually remember about a photo?"})
    st.session_state.messages.append({"role": "assistant", "content": """Users remember **Episodic data** such as:\n- Weather\n- Clothing\n- People present\n- Emotions and vibes\n\n*Simulated Quote:* "I remember the vibe of a purple sunset, why can't I search 'purple sunset with two people'?"""})
elif q3_btn:
    st.session_state.messages.append({"role": "user", "content": "What information have they forgotten?"})
    st.session_state.messages.append({"role": "assistant", "content": """Users almost always forget **Semantic/System data** such as:\n- Absolute dates\n- Exact location names\n- File types\n\n*Simulated Quote:* "Searching is useless if I don't know the exact date. I just know it was 4 years ago." """})
elif q4_btn:
    st.session_state.messages.append({"role": "user", "content": "How do users formulate searches when their memory is incomplete?"})
    st.session_state.messages.append({"role": "assistant", "content": """Users rely on manual workarounds:\n- **The Person Pivot:** Users search for a known friend's face to anchor the timeline, then manually scroll to find a coffee cup.\n\n*Simulated Quote:* "Had to check WhatsApp to find the date I texted my mechanic about a tire issue, just so I could find the photo in Google Photos by date." """})


# ==============================================================================
# MAIN CANVAS - HEADER
# ==============================================================================
st.title("Discovery Engine")
st.markdown("Ingesting, normalizing, and synthesizing unstructured customer feedback to deconstruct human memory retrieval failures.")

st.markdown("<br>", unsafe_allow_html=True)
current_view = st.radio("Select View:", ["📊 Data Overview", "🤖 AI Discovery Chat"], horizontal=True, label_visibility="collapsed", index=0 if st.session_state.current_view == "📊 Data Overview" else 1)

# Update session state if the radio button is clicked manually
if current_view != st.session_state.current_view:
    st.session_state.current_view = current_view
    st.rerun()

st.markdown("---")

# ==============================================================================
# 4. CONDITIONAL FULL-SCREEN RENDERING
# ==============================================================================
if st.session_state.current_view == "📊 Data Overview":
    st.subheader("Data Overview")
    
    # ROW 1 (KPIs)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="Total Vol", value="25,450", delta="+12% MoM")
    with col2:
        st.metric(label="Retrieval Friction", value="68.2%", delta="+5.4%", delta_color="inverse")
    with col3:
        st.metric(label="Abandonment", value="42.1%", delta="-1.2%")
    with col4:
        st.metric(label="Zero-Result Rate", value="12.4%", delta="+0.8%", delta_color="inverse")
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ROW 2 (Charts across full width)
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        st.subheader("Semantic vs. Episodic Gap")
        df_gap = pd.DataFrame({
            "Query Type": ["Exact Date/Loc (System)", "Vibe/Context (Human)"],
            "Success Rate (%)": [85, 12]
        })
        fig_donut = px.pie(df_gap, values="Success Rate (%)", names="Query Type", hole=0.6,
                           color_discrete_sequence=["#4285F4", "#EA4335"])
        fig_donut.update_layout(margin=dict(t=30, b=10, l=10, r=10))
        st.plotly_chart(fig_donut, use_container_width=True)

    with chart_col2:
        st.subheader("Manual Workarounds by Source")
        df_workaround = pd.DataFrame({
            "Source": ["Reddit", "Reddit", "Reddit", "App Store", "App Store", "App Store", "Forums", "Forums", "Forums"],
            "Workaround Type": ["Person Pivot", "App Hopping", "Date Brute-Force", "Person Pivot", "App Hopping", "Date Brute-Force", "Person Pivot", "App Hopping", "Date Brute-Force"],
            "Mentions": [420, 210, 550, 180, 450, 310, 80, 120, 95]
        })
        fig_bar = px.bar(df_workaround, x="Source", y="Mentions", color="Workaround Type", 
                         color_discrete_sequence=["#4285F4", "#34A853", "#FBBC05"])
        fig_bar.update_layout(margin=dict(t=30, b=10, l=10, r=10))
        st.plotly_chart(fig_bar, use_container_width=True)

elif st.session_state.current_view == "🤖 AI Discovery Chat":
    st.subheader("🤖 AI Discovery Chat")
    
    # Show spinner if a sidebar button was just clicked
    if q1_btn or q2_btn or q3_btn or q4_btn:
        with st.spinner("Synthesizing user feedback across sources..."):
            time.sleep(2)
            
    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input (st.chat_input)
    if prompt := st.chat_input("Ask a follow-up question..."):
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            with st.spinner("Analyzing Voice of Customer data..."):
                time.sleep(1.5)
                response = f"Based on the 25,450 records, users frequently express frustration with {prompt.lower()}. This indicates a strong gap between episodic memory triggers and semantic search indexing."
                st.markdown(response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
