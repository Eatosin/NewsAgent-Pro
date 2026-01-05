import os
from huggingface_hub import InferenceClient
from src.utils.overlays import add_overlay
from src.schema import AgentState
from io import BytesIO
import base64
from PIL import Image, ImageDraw, ImageFont  # For fallback

# HF Client for FLUX.1-dev (free inference)
hf_client = InferenceClient(
    model="black-forest-labs/FLUX.1-dev",
    token=os.getenv("HF_TOKEN")  # Optional but helps with queue priority
)

def designer_node(state: AgentState):
    hook = state.hook or "Breaking News"
    topic = state.topic or "Latest Developments"
    platform = state.platform.lower()
    
    # Dynamic image prompt based on topic/platform
    image_prompt = (
        f"Premium abstract cover image for a viral {platform} thread about '{topic}'. "
        "Dark futuristic aesthetic, high contrast, geometric patterns, subtle gradients, "
        "professional and modern, wide aspect ratio (16:9), no text or people, "
        "cinematic lighting, highly detailed, inspired by premium social media banners"
    )
    
    subtitle = "Thread 🧵" if "twitter" in platform else "In-Depth Analysis"
    
    try:
        # Generate base image with Flux
        image = hf_client.text_to_image(
            prompt=image_prompt,
            height=512,
            width=1024,
            guidance_scale=7.0,
            num_inference_steps=40  # Balance speed/quality on free tier
        )
        
        buf = BytesIO()
        image.save(buf, format="PNG")
        base_image_bytes = buf.getvalue()
        
        # Apply overlay with perfect text
        overlaid_bytes = add_overlay(
            base_image_bytes=base_image_bytes,
            hook=hook.upper(),
            subtitle=subtitle
        )
        
    except Exception as e:
        print(f"Flux generation failed: {e}. Using fallback image.")
        # Simple dark fallback with text
        img = Image.new("RGB", (1024, 512), color=(15, 15, 35))
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 70)
        except:
            font = ImageFont.load_default()
        draw.text((512, 256), hook.upper(), fill="white", font=font, anchor="mm", stroke_width=3, stroke_fill="black")
        buf = BytesIO()
        img.save(buf, format="PNG")
        overlaid_bytes = buf.getvalue()
    
    # Convert to base64 data URL for Streamlit display
    image_b64 = base64.b64encode(overlaid_bytes).decode("utf-8")
    image_data_url = f"data:image/png;base64,{image_b64}"
    
    return {
        "image_url": image_data_url,
        "image_prompt_used": image_prompt
    }
