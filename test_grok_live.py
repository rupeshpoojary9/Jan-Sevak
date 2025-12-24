import os
import django
from django.conf import settings
import openai

# Setup Django to load env vars
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jan_sevak.settings')
django.setup()

api_key = os.environ.get("GROK_API_KEY")
print(f"Testing Grok with Key: {api_key[:5]}..." if api_key else "No Key Found")

if not api_key:
    print("❌ GROK_API_KEY is missing in .env")
    exit(1)

client = openai.OpenAI(
    api_key=api_key,
    base_url="https://api.x.ai/v1",
)

try:
    print("Sending request to Grok...")
    response = client.chat.completions.create(
        model="grok-beta",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Say 'Hello from Grok' if you can hear me."}
        ]
    )
    print("Response:", response.choices[0].message.content)
    print("✅ Grok API is working!")
except Exception as e:
    print(f"❌ Grok API Failed: {e}")
