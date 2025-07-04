import openai
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_roast(username, messages):
    prompt = f"""
You are a savage, Tanki-themed AI roast generator. You're reading Discord chat history from a player named {username}. Based on the following recent messages, write a funny, clever, and Tanki-style roast about them. Make it feel like an in-game taunt, but not mean or personal.

Recent messages:
{chr(10).join(messages[-5:])}

Roast:
"""
    try:
        print(f"DEBUG: Sending prompt to OpenAI:\n{prompt}")
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt.strip()}],
            max_tokens=100,
            temperature=0.9,
        )
        roast_text = response.choices[0].message['content'].strip()
        print(f"DEBUG: Received roast from OpenAI:\n{roast_text}")
        return roast_text
    except Exception as e:
        print(f"ERROR in generate_roast: {e}")
        return "Oops! Something went wrong generating the roast. Try again later."