import os

def load_prompt(filename):
    """Reads a prompt file from src/prompts."""
    current_dir = os.path.dirname(__file__)
    prompts_dir = os.path.join(os.path.dirname(current_dir), 'prompts')
    file_path = os.path.join(prompts_dir, filename)
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        # Fallback if file is missing
        return f"You are a helpful assistant. Task: {filename}"
