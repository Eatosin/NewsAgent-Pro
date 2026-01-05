import streamlit as st
from src.main import graph
from src.schema import AgentState
from langgraph.prebuilt import ToolNode
import base64
from io import BytesIO

st.set_page_config(page_title="NewsAgent Pro v2", page_icon="📰", layout="wide")

st.title("📰 NewsAgent Pro v2")
st.caption("Turn any news topic into viral Twitter threads or LinkedIn posts — with premium visuals. Powered by Groq/Gemini + Flux.")

with st.form("input_form"):
    topic = st.text_input("News Topic", placeholder="e.g., Venezuela oil developments 2026")
    platform = st.selectbox("Platform", ["Twitter/X", "LinkedIn"])
    submitted = st.form_submit_button("Generate Thread")

if submitted and topic:
    with st.spinner("Initializing Agent Swarm..."):
        config = {"configurable": {"thread_id": "1"}}  # For memory
        
        initial_state = AgentState(
            topic=topic,
            platform=platform.lower()
        )
        
        # Stream the graph
        progress = st.progress(0)
        status = st.empty()
        
        # Expected steps for progress bar
        steps = ["planner", "research_tool", "researcher", "writer", "critic", "designer"]
        
        try:
            for event in graph.stream(initial_state, config, stream_mode="updates"):
                for node, values in event.items():
                    # UI Update
                    status.text(f"Running: {node.replace('_', ' ').title()}...")
                    if node in steps:
                        progress.progress((steps.index(node) + 1) / len(steps))
                    
                    # 🛠️ CRITICAL FIX: Skip if values are None (Prevents Crash)
                    if values is None:
                        continue
                    
                    # Update state safely using Pydantic
                    current_data = initial_state.model_dump()
                    current_data.update(values)
                    initial_state = AgentState(**current_data)
            
            st.success("Complete! 🚀")

        except Exception as e:
            st.error(f"Workflow Error: {e}")
            st.stop()
    
    # --- DISPLAY RESULTS ---
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Visual Asset")
        if initial_state.image_url:
            try:
                # Handle Base64 Image
                if "base64" in initial_state.image_url:
                    st.image(initial_state.image_url, caption="Thread Cover", use_column_width=True)
                    
                    # Download Button
                    img_bytes = base64.b64decode(initial_state.image_url.split(",")[1])
                    st.download_button(
                        label="⬇️ Download Image",
                        data=img_bytes,
                        file_name="thread_cover.png",
                        mime="image/png"
                    )
                else:
                    # Handle URL Image (Fallback)
                    st.image(initial_state.image_url, caption="Thread Cover", use_column_width=True)
            except Exception as e:
                st.warning(f"Could not render image: {e}")
        else:
            st.info("No image generated for this run.")

    with col2:
        st.subheader(f"{platform} Output")
        if initial_state.final_thread:
            for i, tweet in enumerate(initial_state.final_thread, 1):
                st.text_area(f"Part {i}", value=tweet.strip(), height=150)
            
            # Download text
            full_text = "\n\n".join(initial_state.final_thread)
            st.download_button(
                label="⬇️ Download Text",
                data=full_text,
                file_name="thread.txt",
                mime="text/plain"
            )
        else:
            st.warning("No text content generated.")
            
    # Sources Footer
    if initial_state.sources:
        st.divider()
        with st.expander("📚 Verified Sources"):
            for src in initial_state.sources:
                st.markdown(f"- {src}")
