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
IMAGE_MODEL = "black-forest-labs/FLUX.1-dev"
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
    """
    Retrieves latest news context using Tavily Search API.
    Returns: (Context String, List of Source Links)
    """
    try:
        # Search specifically for NEWS in the last 2 DAYS
        search_result = tavily.search(query=topic, topic="news", days=2)
        results = search_result.get('results', [])
        
        context = []
        sources = []
        
        for res in results[:3]:
            context.append(f"Title: {res['title']}\nSummary: {res['content']}")
            sources.append(f"🔗 [{res['title']}]({res['url']})")
            
        return "\n\n".join(context), sources
    except Exception as e:
        return f"Research failed: {str(e)}", []

def generate_content(platform, topic, research_data):
    if "Twitter" in platform:
        system_prompt = (
            "You are a social media ghostwriter. Write a Twitter thread based on the research provided. "
            "Split tweets using the delimiter '|||'. "
            "Ensure the first tweet is a strong hook and the last is a call to action. "
            "Keep each section under 280 characters."
        )
    else:
        system_prompt = (
            "You are a professional content strategist. Write a LinkedIn post based on the research provided. "
            "Focus on business impact, strategic insights, and professional tone. "
            "Use appropriate line breaks for readability."
        )

    user_prompt = f"""
    TOPIC: {topic}
    RESEARCH DATA: {research_data}
    
    SYSTEM INSTRUCTION: {system_prompt}
    """
    
    try:
        response = editor_model.generate_content(user_prompt)
        return response.text
    except Exception as e:
        return f"Generation failed: {str(e)}"

def generate_visual_asset(topic, platform):
    prompt = (
        f"Abstract 3D render representing {topic}, dark navy and black gradient background, "
        "glass texture, soft studio lighting, minimalist, 8k resolution, negative space, "
        "high definition, no text, no chaotic details"
    )
    
    try:
        image = image_client.text_to_image(prompt)
        
        draw = ImageDraw.Draw(image)
        width, height = image.size
        
        font_size = 90
        font = get_font(font_size)
        
        lines = textwrap.wrap(topic.upper(), width=15)
        wrapped_text = "\n".join(lines)
        
        bbox = draw.textbbox((0, 0), wrapped_text, font=font)
        text_height = bbox[3] - bbox[1]
        
        padding = 50
        box_height = text_height + (padding * 3)
        box_y = height - box_height - 100
        
        draw.rectangle(
            [(0, box_y), (width, height)], 
            fill=(0, 0, 0, 240)
        )
        
        text_y = box_y + padding
        draw.text((padding, text_y), wrapped_text, font=font, fill="white")
        
        small_font = get_font(30)
        draw.text((padding, height - 60), f"GENERATED FOR {platform.upper()}", font=small_font, fill="#00ff00")
        
        return image
    except Exception as e:
        print(f"Visual generation error: {e}")
        return None

def main():
    st.title("NewsAgent Pro")
    st.markdown("Autonomous Multi-Modal Content Engine")

    with st.sidebar:
        st.header("Configuration")
        platform_choice = st.selectbox("Target Platform", ["Twitter (Thread)", "LinkedIn (Post)"])
    
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Briefing")
        topic_input = st.text_input("Topic", placeholder="Enter news topic or keyword...")
        
        if st.button("Generate Content", type="primary"):
            if not topic_input:
                st.warning("Please enter a topic.")
                return

            status = st.status("Initializing Agent Workflow...", expanded=True)
            
            # Step 1: Research
            status.write("Agent: Researching topic...")
            research_data, sources = research_topic(topic_input)
            
            # SHOW SOURCES
            if sources:
                st.markdown("### 📚 Live Sources Found:")
                for s in sources:
                    st.markdown(s)
            
            # Step 2: Content Generation
            status.write("Agent: Drafting copy...")
            content_draft = generate_content(platform_choice, topic_input, research_data)
            
            # Step 3: Visual Generation
            status.write("Agent: Designing assets...")
            visual_asset = generate_visual_asset(topic_input, platform_choice)
            
            status.update(label="Workflow Complete", state="complete")
            
            st.session_state['content'] = content_draft
            st.session_state['image'] = visual_asset

    with col2:
        st.subheader("Production Output")
        
        if 'image' in st.session_state and st.session_state['image']:
            st.image(st.session_state['image'], use_column_width=True, caption="Generated Asset")
            
            buf = io.BytesIO()
            st.session_state['image'].save(buf, format="PNG")
            st.download_button(
                label="Download Image",
                data=buf.getvalue(),
                file_name="news_asset.png",
                mime="image/png"
            )

        if 'content' in st.session_state:
            raw_content = st.session_state['content']
            
            if "|||" in raw_content:
                tweets = raw_content.split("|||")
                for i, tweet in enumerate(tweets):
                    st.text_area(f"Tweet {i+1}", value=tweet.strip(), height=120)
            else:
                st.text_area("Post Content", value=raw_content, height=400)

if __name__ == "__main__":
    main()
