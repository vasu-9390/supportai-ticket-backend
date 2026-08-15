import os
import json
import logging

logger = logging.getLogger(__name__)

def generate_gemini_json(prompt: str, system_instruction: str = "") -> dict:
    """
    Calls Google Gemini API using google-genai SDK or fallback.
    Returns parsed JSON dictionary.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    
    if api_key and api_key != "your_gemini_api_key_here":
        try:
            from google import genai
            from google.genai import types
            
            client = genai.Client(api_key=api_key)
            config = types.GenerateContentConfig(
                response_mime_type="application/json",
                system_instruction=system_instruction or "You are an advanced enterprise customer support AI assistant. Output strict JSON only."
            )
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=config
            )
            if response.text:
                return json.loads(response.text)
        except Exception as e:
            logger.warning(f"Gemini API call failed or rate limited: {e}. Falling back to internal NLP analyzer.")

    return None
