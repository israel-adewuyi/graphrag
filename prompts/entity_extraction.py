import os
import json


from groq import Groq
from pydantic import BaseModel, ValidationError
from dotenv import load_dotenv
from typing import List, Optional
from templates.entity_extraction_prompt import GRAPH_EXTRACTION_JSON_PROMPT
# TODO: just for testing, should delete
from entity_types_extraction import get_entity_types


# load environment variables from .env files
load_dotenv()
# get groq api key
groq_api_key = os.getenv("GROQ_API_KEY")

client = Groq()

"""
    1. Get entity types
    2. The text for which I want to get the entities

    TODO: Implement gleaning as implemented in the paper.
"""

# Define Pydantic models
class Entity(BaseModel):
    name: str
    type: str
    description: Optional[str] = None

class Relationship(BaseModel):
    source: str
    target: str
    relationship: str
    relationship_strength: int

class Response(BaseModel):
    entities: List[Entity]
    relationships: List[Relationship]

def get_entities(text):
    entity_types = get_entity_types(text)

    print(f"The entities extracted from the text are : {entity_types}")
    system_prompt = GRAPH_EXTRACTION_JSON_PROMPT.format(entity_types=entity_types)
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": text,
            }
        ],
        model="llama-3.1-70b-versatile",
        response_format={"type": "json_object"}
    )
    
    try:
        response = Response.model_validate_json(chat_completion.choices[0].message.content)
        return response.entities, response.relationships
    except ValidationError as e:
        print("Error in parsing entity and relationship information.")
        return e.json()

    print(type(response), response)


if __name__ == "__main__":
    text = """
        Dwarkesh Patel 0:00:00 Okay, today I have the pleasure to talk with two of my good friends, Sholto and Trenton. 
        Noam Brown, who wrote the Diplomacy paper, said this about Sholto: “he's only been in the field for 1.5 years, but people in AI know that he was one of the most important people behind Gemini's success.” And Trenton, who's at Anthropic, works on mechanistic interpretability and it was widely reported that he has solved alignment. 
        So this will be a capabilities only podcast. Alignment is already solved, no need to discuss further. 
        Let's start by talking about context lengths. It seemed to be underhyped, given how important it seems to me, that you can just put a million tokens into context. 
        There's apparently some other news that got pushed to the front for some reason, but tell me about how you see the future of long context lengths and what that implies for these models. 
        Sholto Douglas 00:01:28 So I think it's really underhyped. Until I started working on it, I didn't really appreciate how much of a step up in intelligence it was for the model to have the onboarding problem basically instantly solved. You can see that a bit in the perplexity graphs in the paper where just throwing millions of tokens worth of context about a code base allows it to become dramatically better at predicting the next token in a way that you'd normally associate with huge increments in model scale. But you don't need that. All you need is a new context. So underhyped and buried by some other news. Dwarkesh Patel 00:01:58 In context, are they as sample efficient and smart as humans? Sholto Douglas 00:02:02 I think that's really worth exploring. 
        For example, one of the evals that we did in the paper had it learn a language in context better than a human expert could, over the course of a couple of months. This is only a small demonstration but I'd be really interested to see things like Atari games where you throw in a couple hundred, or a thousand frames, of labeled actions in the same way that you'd show your friend how to play a game and see if it's able to reason through. It might. At the moment, with the infrastructure and stuff, it's still a bit slow at doing that, but I would actually guess that it might just work out of the box in a way that would be pretty mind-blowing. 
        Trenton Bricken 00:02:38 And crucially, I think this language was esoteric enough that it wasn't in the training data. Sholto Douglas 00:02:42 Exactly. If you look at the model before it has that context thrown in, it doesn't know the language at all and it can't get any translations. Dwarkesh Patel 00:02:49 And this is an actual human language? Sholto Douglas 00:02:51 Exactly. An actual human language. Dwarkesh Patel 00:02:53 So if this is true, it seems to me that these models are already in an important sense, superhuman. Not in the sense that they're smarter than us, but I can't keep a million tokens in my context when I'm trying to solve a problem, remembering and integrating all the information, an entire code base. Am I wrong in thinking this is a huge unlock?
        Sholto Douglas 00:03:14 Actually, I generally think that's true. Previously, I've been frustrated when models aren't as smart, when you ask them a question and you want it to be smarter than you or to know things that you don't. This allows them to know things that you don't. It just ingests a huge amount of information in a way you just can't. So it's extremely important.
        """
    
    get_entities(text=text)
    
