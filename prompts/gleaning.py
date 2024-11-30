import os
import json

from groq import Groq
from pydantic import BaseModel, ValidationError
from dotenv import load_dotenv
from typing import List, Optional
from .templates.gleaning_prompt import GLEANING_PROMPT
from config import ENTITIES

from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential
)


# load environment variables from .env files
load_dotenv()
# get groq api key
groq_api_key = os.getenv("GROQ_API_KEY")

client = Groq()

# Define Pydantic models
class Entity(BaseModel):
    name: str
    type: str
    description: str

class Relationship(BaseModel):
    source: str
    target: str
    relationship: str

class Response(BaseModel):
    entities: List[Entity]
    relationships: List[Relationship]

@retry(wait=wait_random_exponential(min=10, max=60), stop=stop_after_attempt(6))
def glean_text(entities: List, relationships: List):
    entity_types = ENTITIES

    system_prompt = GLEANING_PROMPT.format(entity_types=entity_types)
    query = f"Here are the entities {entities} \n Here are the relationships {relationships}"

    # print(query)
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": query,
            }
        ],
        model="llama-3.1-70b-versatile",
        response_format={"type": "json_object"}
    )
    
    try:
        response = Response.model_validate_json(chat_completion.choices[0].message.content)
        return response.entities, response.relationships
    except ValidationError as e:
        print("Error in gleaning entity and relationship information. Retrying again ....")
        raise