import google.generativeai as genai
import os

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("No API Key found")
    exit(1)

genai.configure(api_key=api_key)

print("Listing available models...")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)
