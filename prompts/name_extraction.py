import os
import json

from groq import Groq
from dotenv import load_dotenv
from pydantic import BaseModel, ValidationError

from .templates.name_extraction_prompt import TITLE_EXTRACTION_PROMPT

# load environment variables from .env files
load_dotenv()

# get groq api key
groq_api_key = os.getenv("GROQ_API_KEY")

client = Groq()

class GuestName(BaseModel):
    guest: str

def get_name(title_tag: str) -> str:
    assert isinstance(title_tag, str), f"title_tag is of type {type(title_tag)}"

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": TITLE_EXTRACTION_PROMPT
            },
            {
                "role": "user",
                "content": title_tag,
            }
        ],
        model="llama-3.1-8b-instant",
        response_format={"type": "json_object"}
    )

    try:
        response = GuestName.model_validate_json(chat_completion.choices[0].message.content)
        return response.guest
    except ValidationError as e:
        return e.json()


if __name__ == "__main__":
    get_name("<title data-preact-helmet="">Sholto Douglas &amp; Trenton Bricken - How to Build &amp; Understand GPT-7's Mind</title>")

