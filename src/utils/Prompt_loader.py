import yaml
import os

def load_prompt(file_name: str) -> str:
    path = os.path.join(os.path.dirname(__file__), "../prompts", file_name)
    with open(path, "r") as f:
        data = yaml.safe_load(f)
    return data["system"]
