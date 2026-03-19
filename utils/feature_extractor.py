# utils/feature_extractor.py

from agent.llm_handler import ask_llm

def extract_features(user_input):
    prompt = f"""
    Extract structured insurance details from this text:
    "{user_input}"

    Return in JSON format:
    {{
      "incident_type": "",
      "damage_level": "",
      "third_party": ""
    }}
    """
    
    response = ask_llm(prompt)
    return response