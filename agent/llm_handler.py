import openai
import os
openai.api_key = os.getenv("OPENAI_API_KEY")


def ask_llm(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an insurance assistant AI."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        return response['choices'][0]['message']['content']
    
    except Exception as e:
        return f"Error: {e}"