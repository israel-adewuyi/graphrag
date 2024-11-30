import os
import sys

from groq import Groq
from typing import List
from dotenv import load_dotenv
from pydantic import BaseModel, Field, ValidationError
from .templates.community_summary_prompt import COMMUNITY_REPORT_SUMMARIZATION_PROMPT

from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential
)

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")

client = Groq()

class Finding(BaseModel):
    explanation: str

class Report(BaseModel):
    title: str
    summary: str
    findings: List[Finding]

@retry(wait=wait_random_exponential(min=10, max=60), stop=stop_after_attempt(6))
def get_community_summary(entity_info: List[str], relationship_info: List[str]):
    query = ["Entity\n"] + entity_info + ["Relationships\n"] + relationship_info

    prompt = COMMUNITY_REPORT_SUMMARIZATION_PROMPT.format(input_text=query)

    response = query_LLM(prompt)

    try:
        community = Report.model_validate_json(response.choices[0].message.content)
        return community
    except ValidationError as e:
        print("An error occured in community summary extraction ... Retrying")
        raise


def query_LLM(query: str):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": query,
            }
        ],
        model="llama-3.1-70b-versatile",
        response_format={"type": "json_object"}
    )

    return chat_completion


if __name__ == "__main__":
    # Testing out the get_community_summary function
    nodes = ['Trenton,Researcher at Anthropic Lab', 'Dictionary Learning,A technique for solving superposition in LLMs']
    edges = ['Trenton, Dictionary learning,An approach Trenton worked on']

    get_community_summary(nodes, edges)