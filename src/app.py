import streamlit as st
from src.main import graph
from src.schema import AgentState
from langgraph.prebuilt import ToolNode
import base64
from io import BytesIO

st.title("📰 NewsAgent Pro v2")
st.caption("Turn any news topic into viral Twitter threads or LinkedIn posts — with premium visuals. Powered by Groq/Gemini + Flux.")

with st.form("input_form"):
    topic = st.text_input("News Topic", placeholder="e.g., Venezuela oil developments 2026")
    platform = st.selectbox("Platform", ["Twitter/X", "LinkedIn"])
    submitted = st.form_submit_button("Generate Thread")

if submitted and topic:
    with st.spinner("Planning outline..."):
        config = {"configurable": {"thread_id": "1"}}  # For memory
        
        initial_state = AgentState(
            topic=topic,
            platform=platform.lower()
        )
        
        # Stream the graph
        progress = st.progress(0)
        status = st.empty()
        
        steps = ["planner", "research_tool", "researcher", "writer", "critic", "designer"]
        step_idx = 0
        
        for event in graph.stream(initial_state, config, stream_mode="updates"):
            node = list(event.keys())[0]
            status.text(f"Running: {node.replace('_', ' ').title()}...")
            progress.progress((steps.index(node) + 1) / len(steps) if node in steps else 1.0)
            
            # Update state
            initial_state = AgentState(**{**initial_state.model_dump(), **event[node]})
        
        st.success("Complete! 🚀")
    
    # Display results
    if initial_state.image_url:
        st.image(initial_state.image_url, caption="Thread Cover Image")
        
        # Download image
        img_bytes = base64.b64decode(initial_state.image_url.split(",")[1])
        st.download_button(
            label="Download Cover Image",
            data=img_bytes,
            file_name="thread_cover.png",
            mime="image/png"
        )
    
    st.subheader(f"{platform.title()} Output")
    for i, tweet in enumerate(initial_state.final_thread or [], 1):
        st.markdown(f"**Part {i}:** {tweet.strip()}")
    
    # Download text
    full_text = "\n\n".join(initial_state.final_thread or [])
    st.download_button(
        label="Download Thread Text",
        data=full_text,
        file_name="thread.txt",
        mime="text/plain"
    )
    
    if initial_state.sources:
        with st.expander("Sources"):
            for src in initial_state.sources:
                st.markdown(f"- {src}")
