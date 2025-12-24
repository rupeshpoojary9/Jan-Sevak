import os
import json
import google.generativeai as genai
from django.conf import settings
import openai

class AIProvider:
    def analyze(self, image_path, description, category):
        raise NotImplementedError

class GeminiProvider(AIProvider):
    def configure(self):
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            print("Warning: GEMINI_API_KEY not found.")
            return False
        genai.configure(api_key=api_key)
        return True

    def analyze(self, image_path, description, category):
        if not self.configure():
            return False, "Gemini Not Configured", 0, False

        model = genai.GenerativeModel('gemini-2.0-flash')
        prompt = self._get_prompt(description, category)

        try:
            if image_path and os.path.exists(image_path):
                sample_file = genai.upload_file(path=image_path, display_name="Complaint Image")
                response = model.generate_content([sample_file, prompt])
            else:
                response = model.generate_content(prompt)
            
            return self._parse_response(response.text)
        except Exception as e:
            print(f"Gemini Error: {e}")
            return False, "AI Service Unavailable. Please try again later.", 0, False

    def _get_prompt(self, description, category):
        return f"""
        Analyze this civic complaint.
        Description: {description}
        Reported Category: {category}
        
        Task:
        1. Safety Check: Analyze BOTH the image AND the description. Is the content safe? 
           - REJECT if the description contains profanity, hate speech, or abusive language.
           - REJECT if the image contains nudity, violence, or hate symbols.
        2. Relevance Check: Is this a civic issue? Reject selfies, memes, or unrelated photos.
        3. Determine urgency score (1-10).
        4. Verify category match.
        
        Output format: JSON
        {{
            "is_safe": <bool>,
            "is_civic_issue": <bool>,
            "rejection_reason": <string or null>,
            "urgency_score": <int>,
            "category_matches": <bool>
        }}
        """

    def _parse_response(self, text):
        text = text.strip()
        if text.startswith('```json'):
            text = text[7:]
        if text.endswith('```'):
            text = text[:-3]
            
        try:
            data = json.loads(text)
            is_safe = data.get('is_safe', True)
            is_civic_issue = data.get('is_civic_issue', True)
            rejection_reason = data.get('rejection_reason', None)
            urgency_score = data.get('urgency_score', 0)
            category_matches = data.get('category_matches', False)
            
            is_valid = is_safe and is_civic_issue
            if not is_valid and not rejection_reason:
                rejection_reason = "Content flagged as unsafe or irrelevant."
                
            return is_valid, rejection_reason, urgency_score, category_matches
        except json.JSONDecodeError:
            print("Failed to parse AI JSON response")
            return False, "AI Response Error. Please try again.", 0, False

class GrokProvider(AIProvider):
    def __init__(self):
        self.api_key = os.environ.get("GROK_API_KEY")
        self.client = None
        if self.api_key:
            self.client = openai.OpenAI(
                api_key=self.api_key,
                base_url="https://api.x.ai/v1",
            )

    def analyze(self, image_path, description, category):
        if not self.client:
            print("Warning: GROK_API_KEY not found.")
            return False, "Grok Not Configured", 0, False

        prompt = f"""
        You are an AI assistant for a civic grievance platform.
        Analyze this complaint:
        Description: {description}
        Category: {category}
        
        Output JSON only:
        {{
            "is_safe": boolean,
            "is_civic_issue": boolean,
            "rejection_reason": string|null,
            "urgency_score": int (1-10),
            "category_matches": boolean
        }}
        """

        try:
            # Grok currently supports text-only via OpenAI SDK compatibility
            # Future: Add image support if Grok Vision is available via API
            response = self.client.chat.completions.create(
                model="grok-beta",
                messages=[
                    {"role": "system", "content": "You are a helpful civic assistant. Output valid JSON only."},
                    {"role": "user", "content": prompt}
                ]
            )
            content = response.choices[0].message.content
            print(f"DEBUG: Grok Response: {content}")
            return self._parse_response(content)
        except Exception as e:
            print(f"Grok Error: {e}")
            return False, "AI Service Unavailable. Please try again later.", 0, False

    def _parse_response(self, text):
        # Reuse parsing logic or duplicate if needed. 
        # For simplicity, duplicating basic cleaning
        text = text.strip()
        if text.startswith('```json'):
            text = text[7:]
        if text.endswith('```'):
            text = text[:-3]
        
        try:
            data = json.loads(text)
            is_safe = data.get('is_safe', True)
            is_civic_issue = data.get('is_civic_issue', True)
            rejection_reason = data.get('rejection_reason', None)
            urgency_score = data.get('urgency_score', 0)
            category_matches = data.get('category_matches', False)
            
            is_valid = is_safe and is_civic_issue
            if not is_valid and not rejection_reason:
                rejection_reason = "Content flagged as unsafe or irrelevant."
                
            return is_valid, rejection_reason, urgency_score, category_matches
        except json.JSONDecodeError:
            return False, "AI Response Error. Please try again.", 0, False

class OpenAIProvider(AIProvider):
    def __init__(self):
        self.api_key = os.environ.get("OPENAI_API_KEY")
        self.client = None
        if self.api_key:
            self.client = openai.OpenAI(api_key=self.api_key)

    def analyze(self, image_path, description, category):
        if not self.client:
            print("Warning: OPENAI_API_KEY not found.")
            return False, "OpenAI Not Configured", 0, False

        import base64
        
        # Prepare messages
        messages = [
            {"role": "system", "content": "You are a helpful civic assistant for the Jan Sevak app. Your job is to verify citizen complaints."}
        ]
        
        user_content = [
            {"type": "text", "text": f"""
            Analyze this civic complaint.
            Description: {description}
            Category: {category}

            Your Goal: Verify if this is a valid civic issue.
            
            Rules:
            1. SAFETY: Reject ONLY if it contains nudity, violence, hate speech, or abusive language.
            2. RELEVANCE: 
               - ACCEPT if it shows: Garbage, Trash, Potholes, Broken Roads, Water/Drainage issues, Streetlights, Traffic, or Public Nuisance.
               - ACCEPT even if the image is messy, close-up, or low quality, AS LONG AS it shows a civic problem.
               - REJECT ONLY if it is clearly unrelated (e.g., selfies, memes, screenshots of games/apps).
            
            3. URGENCY: Rate 1-10 based on severity.
            4. CATEGORY: Check if it matches.

            Output JSON only:
            {{
                "is_safe": boolean,
                "is_civic_issue": boolean,
                "rejection_reason": string|null,
                "urgency_score": int,
                "category_matches": boolean
            }}
            """}
        ]

        # Add image if exists
        if image_path and os.path.exists(image_path):
            try:
                file_size = os.path.getsize(image_path)
                print(f"DEBUG: Image found at {image_path}, Size: {file_size} bytes")
                
                with open(image_path, "rb") as image_file:
                    base64_image = base64.b64encode(image_file.read()).decode('utf-8')
                    print(f"DEBUG: Base64 Image Length: {len(base64_image)}")
                    
                    user_content.append({
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    })
            except Exception as e:
                print(f"Error reading image for OpenAI: {e}")
        else:
            print(f"DEBUG: No image found at {image_path}")

        messages.append({"role": "user", "content": user_content})

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                response_format={"type": "json_object"}
            )
            content = response.choices[0].message.content
            print(f"DEBUG: OpenAI Raw Response: {content}")
            return self._parse_response(content)
        except Exception as e:
            print(f"OpenAI Error: {e}")
            return False, "AI Service Unavailable. Please try again later.", 0, False

    def _parse_response(self, text):
        # Reuse parsing logic
        try:
            data = json.loads(text)
            is_safe = data.get('is_safe', True)
            is_civic_issue = data.get('is_civic_issue', True)
            rejection_reason = data.get('rejection_reason', None)
            urgency_score = data.get('urgency_score', 0)
            category_matches = data.get('category_matches', False)
            
            is_valid = is_safe and is_civic_issue
            if not is_valid and not rejection_reason:
                rejection_reason = "Content flagged as unsafe or irrelevant."
                
            return is_valid, rejection_reason, urgency_score, category_matches
        except json.JSONDecodeError:
            return False, "AI Response Error. Please try again.", 0, False

def get_provider():
    provider_name = os.environ.get("AI_PROVIDER", "gemini").lower()
    print(f"Using AI Provider: {provider_name}")
    if provider_name == "grok":
        return GrokProvider()
    elif provider_name == "openai":
        return OpenAIProvider()
    return GeminiProvider()

def analyze_complaint(image_path, description, category):
    provider = get_provider()
    return provider.analyze(image_path, description, category)
