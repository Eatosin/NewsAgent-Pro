import os
import base64
from io import BytesIO
from huggingface_hub import InferenceClient
from PIL import Image, ImageDraw, ImageFont
from src.utils.overlays import add_overlay
from src.schema import AgentState

class HybridState:
    def __init__(self, state):
        data = state.model_dump() if hasattr(state, 'model_dump') else state
        self.__dict__.update(data)
    def get(self, key, default=None):
        return self.__dict__.get(key, default)

# Initialize Client with Schnell for production speed
hf_client = InferenceClient(
    model="black-forest-labs/FLUX.1-schnell",
    token=os.getenv("HF_TOKEN")
)

def designer_node(state: AgentState):
    """
    Designer Agent: Generates viral visual assets using Flux.1 and Pillow.
    """
    state = HybridState(state)
    hook = state.get('hook') or "Latest News"
    topic = state.get('topic') or "Update"
    platform = state.platform.lower() if state.platform else "twitter"
    
    image_prompt = (
        f"Abstract professional cover art for {topic}. "
        "Dark futuristic aesthetic, minimalist geometry, premium texture, "
        "cinematic lighting, wide aspect ratio 16:9, no text."
    )
    
    subtitle = "Thread" if "twitter" in platform else "Analysis"
    
    try:
        # Schnell requires only 4 steps for high quality
        image = hf_client.text_to_image(
            prompt=image_prompt,
            height=512,
            width=1024,
            num_inference_steps=4 
        )
        
        buf = BytesIO()
        image.save(buf, format="PNG")
        base_image_bytes = buf.getvalue()
        
        # Programmatic text overlay
        overlaid_bytes = add_overlay(
            base_image_bytes=base_image_bytes,
            hook=hook.upper(),
            subtitle=subtitle
        )
        
    except Exception as e:
        # Fail-safe: Generate colored background if API fails
        img = Image.new("RGB", (1024, 512), color=(20, 20, 40))
        draw = ImageDraw.Draw(img)
        draw.text((512, 256), hook.upper(), fill="white", anchor="mm")
        buf = BytesIO()
        img.save(buf, format="PNG")
        overlaid_bytes = buf.getvalue()
    
    image_b64 = base64.b64encode(overlaid_bytes).decode("utf-8")
    return {
        "image_url": f"data:image/png;base64,{image_b64}"
    }
