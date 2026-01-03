import streamlit as st
import os
import io
import requests
import textwrap
from dotenv import load_dotenv
from tavily import TavilyClient
import google.generativeai as genai
from huggingface_hub import InferenceClient
from PIL import Image, ImageDraw, ImageFont

# Load environment variables
load_dotenv()

# Configuration
PAGE_TITLE = "NewsAgent Pro"
FONT_URL = "https://github.com/google/fonts/raw/main/ofl/anton/Anton-Regular.ttf"
# SWITCHED TO SCHNELL (Faster, Ungated)
IMAGE_MODEL = "black-forest-labs/FLUX.1-schnell" 
LLM_MODEL = "gemini-2.5-flash"

st.set_page_config(page_title=PAGE_TITLE, layout="wide", page_icon="🗞️")

# Initialize Clients
try:
    tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    editor_model = genai.GenerativeModel(LLM_MODEL)
    image_client = InferenceClient(IMAGE_MODEL, token=os.getenv("HF_TOKEN"))
except Exception as e:
    st.error(f"Configuration Error: {e}")
    st.stop()

def get_font(size=80):
    try:
        return ImageFont.truetype("font.ttf", size)
    except OSError:
        response = requests.get(FONT_URL)
        if response.status_code == 200:
            with open("font.ttf", "wb") as f:
                f.write(response.content)
            return ImageFont.truetype("font.ttf", size)
        return ImageFont.load_default()

def research_topic(topic):
    """Retrieves latest news context."""
    try:
        search_result = tavily.search(query=topic, topic="news", days=2)
        results = search_result.get('results', [])
        context = []
        for res in results[:3]:
            context.append(f"Title: {res['title']}\nSummary: {res['content']}")
        return "\n\n".join(context)
    except Exception as e:
        return f"Research failed: {str(e)}"

def generate_content(platform, topic, research_data):
    """Generates text copy."""
    if "Twitter" in platform:
        system_prompt = "You are a Viral Twitter Ghostwriter. Write a Thread. Split tweets with '|||'. Keep under 280 chars."
    else:
        system_prompt = "You are a LinkedIn Top Voice. Write a professional, insightful post."

    user_prompt = f"TOPIC: {topic}\nRESEARCH: {research_data}\nINSTRUCTION: {system_prompt}"
    
    try:
        response = editor_model.generate_content(user_prompt)
        return response.text
    except Exception as e:
        return f"Generation failed: {str(e)}"

def generate_visual_asset(topic, platform):
    """Generates image. Returns (ImageObject, ErrorString)."""
    prompt = f"Abstract 3D render of {topic}, dark gradient background, minimalist, high tech, 8k, no text"
    
    try:
        # Generate Image
        image = image_client.text_to_image(prompt)
        
        # Overlay Logic
        draw = ImageDraw.Draw(image)
        width, height = image.size
        font = get_font(90)
        
        # Text Wrap
        lines = textwrap.wrap(topic.upper(), width=15)
        wrapped_text = "\n".join(lines)
        
        # Draw Box
        bbox = draw.textbbox((0, 0), wrapped_text, font=font)
        text_height = bbox[3] - bbox[1]
        box_height = text_height + 150
        box_y = height - box_height - 50
        
        draw.rectangle([(0, box_y), (width, height)], fill=(0, 0, 0, 240))
        draw.text((50, box_y + 50), wrapped_text, font=font, fill="white")
        
        small_font = get_font(30)
        draw.text((50, height - 60), f"GENERATED FOR {platform.upper()}", font=small_font, fill="#00ff00")
        
        return image, None # Success
    except Exception as e:
        return None, str(e) # Return error message

# --- MAIN UI ---
def main():
    st.title("NewsAgent Pro")
    st.markdown("Autonomous Multi-Modal Content Engine")

    with st.sidebar:
        st.header("Configuration")
        platform_choice = st.selectbox("Target Platform", ["Twitter (Thread)", "LinkedIn (Post)"])
    
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Briefing")
        topic_input = st.text_input("Topic", placeholder="Enter news topic...")
        
        if st.button("Generate Content", type="primary"):
            if not topic_input:
                st.warning("Enter a topic.")
                return

            status = st.status("Initializing Workflow...", expanded=True)
            
            # 1. Research
            status.write("Agent: Researching...")
            research_data = research_topic(topic_input)
            
            # 2. Write
            status.write("Agent: Writing...")
            content_draft = generate_content(platform_choice, topic_input, research_data)
            
            # 3. Design (With Error Catching)
            status.write("Agent: Generating Visuals (Flux Schnell)...")
            visual_asset, visual_error = generate_visual_asset(topic_input, platform_choice)
            
            if visual_error:
                st.error(f"Image Gen Failed: {visual_error}")
            else:
                status.write("✅ Visuals Created.")
            
            status.update(label="Complete", state="complete")
            
            st.session_state['content'] = content_draft
            st.session_state['image'] = visual_asset

    with col2:
        st.subheader("Output")
        
        # Show Image
        if 'image' in st.session_state and st.session_state['image']:
            st.image(st.session_state['image'], caption="Viral Asset", use_column_width=True)
            # Download
            buf = io.BytesIO()
            st.session_state['image'].save(buf, format="PNG")
            st.download_button("Download Image", data=buf.getvalue(), file_name="news.png", mime="image/png")
        
        # Show Text
        if 'content' in st.session_state:
            raw = st.session_state['content']
            if "|||" in raw:
                for i, t in enumerate(raw.split("|||")):
                    st.text_area(f"Tweet {i+1}", t.strip(), height=100)
            else:
                st.text_area("Post", raw, height=400)

if __name__ == "__main__":
    main()
