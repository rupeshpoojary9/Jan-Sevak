import os
import google.generativeai as genai
from complaints.ai_service import analyze_complaint

# Mock Django settings if needed, or just run standalone
# Mock Django settings if needed, or just run standalone
os.environ.setdefault("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY", ""))

def test_profanity():
    description = "This is a test with the word asshole in it."
    category = "OTHERS"
    image_path = None # Test text-only first

    print(f"Testing description: '{description}'")
    is_valid, reason, score, matches = analyze_complaint(image_path, description, category)
    
    print(f"Result: Valid={is_valid}, Reason={reason}, Score={score}")

if __name__ == "__main__":
    test_profanity()
