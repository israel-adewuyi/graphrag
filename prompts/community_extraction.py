import os
import sys

from groq import Groq
from typing import List
from dotenv import load_dotenv
from pydantic import BaseModel, Field, ValidationError
from .templates.community_summary_prompt import COMMUNITY_REPORT_SUMMARIZATION_PROMPT

# load environment variables from .env files
load_dotenv()
# get groq api key
groq_api_key = os.getenv("GROQ_API_KEY")

client = Groq()

class Finding(BaseModel):
    explanation: str

class Report(BaseModel):
    title: str
    summary: str
    findings: List[Finding]


def get_community_summary(entity_info: List[str], relationship_info: List[str]):
    query = ["Entity\n"] + entity_info + ["Relationships\n"] + relationship_info

    prompt = COMMUNITY_REPORT_SUMMARIZATION_PROMPT.format(input_text=query)

    response = query_LLM(prompt)

    try:
        community = Report.model_validate_json(response.choices[0].message.content)
        # print(community.model_dump_json(indent=5), type(community))
        return community
    except ValidationError as e:
        print("An error occured")
        print(e.json())


def query_LLM(query: str):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": query,
            }
        ],
        model="gemma2-9b-it",
        response_format={"type": "json_object"}
    )

    return chat_completion


if __name__ == "__main__":
    nodes = ['Trenton,Researcher at Anthropic Lab', 'Dictionary Learning,A technique for solving superposition in LLMs']
    edges = ['Trenton, Dictionary learning,An approach Trenton worked on']

    get_community_summary(nodes, edges)