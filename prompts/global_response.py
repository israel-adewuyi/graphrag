import os

from groq import Groq
from typing import List
from dotenv import load_dotenv
from .templates.global_response_prompt import GLOBAL_RESPONSE_PROMPT

# load environment variables from .env files
load_dotenv()
# get groq api key
groq_api_key = os.getenv("GROQ_API_KEY")

client = Groq()

def get_global_response(query: str, supporting_docs: List[str]) -> str:
    prompt = GLOBAL_RESPONSE_PROMPT.format(query=query, supporting_docs=supporting_docs)

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama-3.1-70b-versatile",
    )

    return chat_completion.choices[0].message.content


if __name__ == "__main__":
    pass
    # get_global_response()