import streamlit as st
import base64
import os
from io import BytesIO
from src.main import graph
from src.schema import AgentState

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="NewsAgent Pro v2", 
    page_icon="🗞️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS ---
st.markdown("""
<style>
    .stButton>button {width: 100%; border-radius: 8px; font-weight: bold;}
    .reportview-container {margin-top: -2em;}
    h1 {color: #FF4B4B;}
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.title("🤖 Agent Command")
    st.info("System Online v2.0")
    st.markdown("### ⚙️ Engine Specs")
    st.markdown("- **Planner:** Llama 3.3 (Groq)")
    st.markdown("- **Writer:** Gemini 2.5 / Groq")
    st.markdown("- **Visuals:** Flux.1 Schnell")
    
    st.markdown("---")
    st.write("Authored by **Lexpertz R&D**")

# --- MAIN INTERFACE ---
st.title("🗞️ NewsAgent Pro")
st.markdown("### Autonomous Multi-Modal Content Engine")
st.caption("Enter a topic. The AI swarm will Research, Plan, Write, and Design assets automatically.")

# Input Section
with st.container():
    col_input, col_btn = st.columns([3, 1])
    with col_input:
        topic = st.text_input("Mission Objective (Topic)", placeholder="e.g. DeepSeek vs OpenAI rivalry")
    with col_btn:
        platform = st.selectbox("Target Platform", ["Twitter", "LinkedIn"])
        run_btn = st.button("🚀 Launch Agents", type="primary")

# --- SESSION STATE INITIALIZATION ---
if "generated_content" not in st.session_state:
    st.session_state.generated_content = None
if "generated_image" not in st.session_state:
    st.session_state.generated_image = None
if "sources" not in st.session_state:
    st.session_state.sources = []

# --- EXECUTION LOGIC ---
if run_btn and topic:
    # Reset State
    st.session_state.generated_content = None
    st.session_state.generated_image = None
    
    status_box = st.status("🚀 Initializing Agent Swarm...", expanded=True)
    
    try:
        # Initialize Pydantic State
        initial_state = AgentState(
            topic=topic,
            platform=platform.lower()
        )
        
        # Run Graph
        curr_state = initial_state
        
        # We iterate through the stream updates
        for event in graph.stream(initial_state):
            for node_name, values in event.items():
                # Skip empty updates
                if not values:
                    continue
                
                # Update status based on active agent
                if node_name == "planner":
                    status_box.write("🧠 **Planner:** Strategy & Hook defined.")
                elif node_name == "researcher":
                    status_box.write(f"🕵️‍♂️ **Researcher:** Gathered data.")
                elif node_name == "writer":
                    status_box.write("✍️ **Writer:** Draft generated.")
                elif node_name == "designer":
                    status_box.write("🎨 **Designer:** Visual asset rendered.")

                # Update local state dict to track progress
                # Note: LangGraph returns the *changes*, so we update our tracker
                # For simplicity in this UI loop, we grab final artifacts at the end
                if "final_thread" in values:
                    st.session_state.generated_content = values["final_thread"]
                if "image_url" in values:
                    st.session_state.generated_image = values["image_url"]
                if "research_data" in values:
                    # Extract sources for display
                    # Assuming research_data is a string in the final state or list of dicts
                    # Adjust based on your researcher.py output
                    pass 

        status_box.update(label="✅ Mission Accomplished", state="complete", expanded=False)

    except Exception as e:
        status_box.update(label="❌ Mission Failed", state="error")
        st.error(f"Agent Logic Error: {str(e)}")

# --- RESULTS DISPLAY ---
if st.session_state.generated_content or st.session_state.generated_image:
    st.divider()
    res_col1, res_col2 = st.columns([1, 1])

    # LEFT: Visuals
    with res_col1:
        st.subheader("🎨 Visual Asset")
        if st.session_state.generated_image:
            img_path = st.session_state.generated_image
            if os.path.exists(img_path):
                st.image(img_path, caption="Viral Cover Image", use_container_width=True)
                
                # Download Button
                with open(img_path, "rb") as file:
                    btn = st.download_button(
                        label="⬇️ Download PNG",
                        data=file,
                        file_name=f"newsagent_{int(time.time())}.png",
                        mime="image/png"
                    )
            else:
                st.warning("Image file missing (Docker ephemeral storage).")
        else:
            st.info("No visual generated for this run.")

    # RIGHT: Copy
    with res_col2:
        st.subheader(f"📝 {platform} Draft")
        content = st.session_state.generated_content
        
        if content:
            if isinstance(content, list): # Twitter Thread
                for i, tweet in enumerate(content):
                    st.text_area(f"Tweet {i+1}", value=tweet, height=120)
            else: # LinkedIn Post
                st.text_area("Post Content", value=content, height=400)
        else:
            st.info("No text content generated.")
