import os
from dotenv import load_dotenv

def load_env():
    load_dotenv()
    return os.getenv("GEMINI_API_KEY")

def normalize_text(text):
    """Normalize text for consistent comparisons."""
    return text.strip().lower().replace("&", "and")
