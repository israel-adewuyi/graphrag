# Reference - https://github.com/microsoft/graphrag/blob/main/graphrag/prompt_tune/prompt/entity_types.py
ENTITY_TYPE_GENERATION_JSON_PROMPT = """
The goal is to study the connections and relations between the entity types and their features in order to understand all available information from the text.
The user's task is to {task}.
The text is a conversation between a bunch of AI scientists, talking about AI safety, AI alignment, what it takes to build super human intelligience, e.t.c.
As part of the analysis, you want to identify the entity types present in the following text.
The entity types must be relevant to the task and the text.
Avoid general entity types such as "other" or "unknown".
This is VERY IMPORTANT: Do not generate redundant or overlapping entity types. For example, if the text contains "company" and "organization" entity types, you should return only one of them.
Don't worry about quantity, always choose quality over quantity. And make sure EVERYTHING in your answer is relevant to the context of entity extraction.
Return the entity types in JSON format with "entities" as the key and the entity types as an array of strings.
=====================================================================
EXAMPLE SECTION: The following section includes example output. These examples **must be excluded from your answer**.

EXAMPLE 1
Task: Determine the connections and organizational hierarchy within the specified community.
Text: Example_Org_A is a company in Sweden. Example_Org_A's director is Example_Individual_B.
JSON RESPONSE:
{{"entity_types": [organization, person] }}
END OF EXAMPLE 1

EXAMPLE 2
Task: Identify the key concepts, principles, and arguments shared among different philosophical schools of thought, and trace the historical or ideological influences they have on each other.
Text: Rationalism, epitomized by thinkers such as René Descartes, holds that reason is the primary source of knowledge. Key concepts within this school include the emphasis on the deductive method of reasoning.
JSON RESPONSE:
{{"entity_types": [concept, person, school of thought] }}
END OF EXAMPLE 2

EXAMPLE 3
Task: Identify the full range of basic forces, factors, and trends that would indirectly shape an issue.
Text: Industry leaders such as Panasonic are vying for supremacy in the battery production sector. They are investing heavily in research and development and are exploring new technologies to gain a competitive edge.
JSON RESPONSE:
{{"entity_types": [organization, technology, sectors, investment strategies] }}
END OF EXAMPLE 3

EXAMPLE 4
Task: Identify the all the main topics of discussion, key people, main ideas and main concepts.
Text: Sholto Douglas 00:06:36
I would take issue with that being the reason that agents haven't taken off. I think that's more about nines of reliability and the model actually successfully doing things. If you can't chain tasks successively with high enough probability, then you won't get something that looks like an agent. And that's why something like an agent might follow more of a step function.
In GPT-4 class models, Gemini Ultra class models, they're not enough. But maybe the next increment on model scale means that you get that extra nine. Even though the loss isn't going down that dramatically, that small amount of extra ability gives you the extra. Obviously you need some amount of context to fit long-horizon tasks, but I don't think that's been the limiting factor up to now.
JSON RESPONSE:
{{"entity_types": [person, AI models, concepts]}}
======================================================================
"""

# ======================================================================
# REAL DATA: The following section is the real data. You should use only this real data to prepare your answer. Generate Entity Types only.
# Task: {task}
# Text: {input_text}
# JSON response:
# {{"entity_types": [<entity_types>] }}
# """