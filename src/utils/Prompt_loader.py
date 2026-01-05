import os

def load_prompt(filename):
    """
    Reads a prompt file from the src/prompts directory.
    """
    current_dir = os.path.dirname(__file__)
    prompts_dir = os.path.join(os.path.dirname(current_dir), 'prompts')
    file_path = os.path.join(prompts_dir, filename)
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"⚠️ Warning: Prompt file '{filename}' not found.")
        return "You are a helpful AI assistant." # Fallback prompt
