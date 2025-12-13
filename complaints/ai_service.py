import os
import json
import google.generativeai as genai
from django.conf import settings

def configure_genai():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Warning: GEMINI_API_KEY not found in environment variables.")
        return False
    genai.configure(api_key=api_key)
    return True

def analyze_complaint(image_path, description, category):
    """
    Analyzes the complaint using Gemini AI to determine urgency and verify category.
    Returns: (urgency_score, category_matches)
    """
    if not configure_genai():
        return False, "AI Service Not Configured", 0, False

    model = genai.GenerativeModel('gemini-2.0-flash')
    
    prompt = f"""
    Analyze this civic complaint.
    Description: {description}
    Reported Category: {category}
    
    Task:
    1. Safety Check: Analyze BOTH the image AND the description. Is the content safe? 
       - REJECT if the description contains profanity, hate speech, or abusive language (e.g. "asshole", "idiot", etc).
       - REJECT if the image contains nudity, violence, or hate symbols.
    2. Relevance Check: Is this a civic issue (pothole, garbage, street light, drainage, etc)? Reject selfies, memes, or unrelated photos.
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
    
    try:
        if image_path and os.path.exists(image_path):
            sample_file = genai.upload_file(path=image_path, display_name="Complaint Image")
            response = model.generate_content([sample_file, prompt])
        else:
            response = model.generate_content(prompt)
            
        # Parse JSON from response
        text = response.text.strip()
        print(f"DEBUG: AI Response: {text}") # Log raw response
        
        if text.startswith('```json'):
            text = text[7:]
        if text.endswith('```'):
            text = text[:-3]
            
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
        
    except Exception as e:
        print(f"Error analyzing complaint: {e}")
        # Fail Closed: If AI fails (likely due to safety block), we REJECT.
        return False, f"AI Verification Failed: {str(e)}", 0, False
