import requests
import json
import time

def get_country_from_llm(text, api_url="http://localhost:1234/v1/chat/completions", model="qwen/qwen3-vl-8b"):
    """
    Queries a local LLM (LM Studio) to extract the country from the given text.
    
    Args:
        text (str): The text description of the victim or sponsor.
        api_url (str): The endpoint for the local LLM.
        model (str): The model identifier to use.
        
    Returns:
        str: The extracted country name or 'Unknown'.
    """
    headers = {
        "Content-Type": "application/json"
    }
    
    # Strict system prompt to ensure clean output
    system_prompt = (
        "You are a data extraction tool. "
        "Analyze the provided text and identify the country it refers to. "
        "Return ONLY the standard English country name. "
        "Do not write sentences. Do not include 'The' at the beginning unless part of the name. "
        "If no country is clearly indicated, return 'Unknown'."
    )
    
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Text: {text}\nCountry:"}
        ],
        "temperature": 0.0, # Deterministic
        "max_tokens": 20,
        "stream": False
    }
    
    try:
        response = requests.post(api_url, headers=headers, data=json.dumps(payload), timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            if 'choices' in result and len(result['choices']) > 0:
                content = result['choices'][0]['message']['content'].strip()
                # Basic cleanup
                content = content.replace(".", "").replace("The ", "")
                return content
        
        print(f"LLM Request failed with status {response.status_code}: {response.text}")
        return "Unknown"
        
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to LM Studio at http://localhost:1234. Is it running?")
        return "ConnectionError"
    except Exception as e:
        print(f"Error querying LLM for '{text}': {e}")
        return "Unknown"
