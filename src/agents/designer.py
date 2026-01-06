import os
import requests
import io
import textwrap
from PIL import Image, ImageDraw, ImageFont
from huggingface_hub import InferenceClient
from src.schema import HybridState, AgentState

# Initialize Flux Schnell (Faster, Apache 2.0)
hf_token = os.getenv("HF_TOKEN")
client = InferenceClient("black-forest-labs/FLUX.1-schnell", token=hf_token)

def designer_node(state: AgentState):
    state_wrapper = HybridState(state)
    topic = state_wrapper.get("topic", "Breaking News")
    platform = state_wrapper.get("platform", "twitter")
    
    prompt = f"Abstract 3D render of {topic}, dark gradient background, minimalist, high tech, 8k resolution, no text"
    
    try:
        # Generate Image
        image = client.text_to_image(prompt)
        
        # Overlay Text
        draw = ImageDraw.Draw(image)
        width, height = image.size
        
        # Font Fallback
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 90)
        except:
            # Download font if missing (Docker environment)
            font_url = "https://github.com/google/fonts/raw/main/ofl/anton/Anton-Regular.ttf"
            r = requests.get(font_url)
            font = ImageFont.truetype(io.BytesIO(r.content), 90)

        # Wrap Text
        lines = textwrap.wrap(topic.upper(), width=15)
        text = "\n".join(lines)
        
        # Draw Box
        bbox = draw.textbbox((0, 0), text, font=font)
        text_height = bbox[3] - bbox[1]
        
        box_y = height - text_height - 150
        draw.rectangle([(0, box_y), (width, height)], fill=(0, 0, 0, 240))
        
        # Draw Text
        draw.text((50, box_y + 50), text, font=font, fill="white")
        
        # Save to buffer
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        
        # Convert to simple path or bytes for UI
        # For Streamlit state, bytes are fine, but saving to /tmp is safer for passing
        save_path = "/tmp/generated_image.png"
        with open(save_path, "wb") as f:
            f.write(img_byte_arr)
            
        return {"image_url": save_path}
        
    except Exception as e:
        print(f"Design failed: {e}")
        return {"image_url": None}
