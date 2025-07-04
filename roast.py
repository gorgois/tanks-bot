

import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_roast(username, messages):
    prompt = f"""
You are a savage, Tanki-themed AI roast generator. You're reading Discord chat history from a player named {username}. Based on the following messages, write a funny, clever, and Tanki-style roast about them. Make it feel like an in-game taunt, but not mean or personal.

Messages:
{chr(10).join(messages[-5:])}  # Use only last 5 for context

Roast:
"""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{
            "role": "user",
            "content": prompt.strip()
        }],
        max_tokens=100,
        temperature=0.9
    )
    return response.choices[0].message['content'].strip()