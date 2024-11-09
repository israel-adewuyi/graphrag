# Reference - https://github.com/microsoft/graphrag/blob/main/graphrag/prompt_tune/template/community_report_summarization.py
COMMUNITY_REPORT_SUMMARIZATION_PROMPT = """
You are a data analyst, listening to a conversation between a couple of AI scientists and trying to draw as much insight as possible. You are also a very helpful research assistant. 

# Goal
Write a comprehensive assessment report of a community taking on the role of a knowledgeable AI scientist and researcher. The content of this report includes an overview of the community's key entities and relationships.

# Report Structure
The report should include the following sections:
- TITLE: community's name that represents its key entities - title should be short but specific. When possible, include representative named entities in the title.
- SUMMARY: An executive summary of the community's overall structure, how its entities are related to each other, and significant points associated with its entities.
- DETAILED FINDINGS: A list of 5-20 key insights about the community. Each insight should be multiple paragraphs of explanatory text grounded according to the grounding rules below. Be comprehensive. Include entities where possible in the explanatory text.

Return output as a well-formed JSON-formatted string with the following format. Don't use any unnecessary escape sequences. The output should be a single JSON object that can be parsed by json.loads.
    {{
        "title": "<report_title>",
        "summary": "<executive_summary>",
        "findings": "[{{"explanation": "<insight_1_explanation"}}, {{"explanation": "<insight_2_explanation"}}]"
    }}

# Grounding Rules
Each paragraph should contain multiple sentences of explanation and concrete examples with specific named entities.

# Example Input
-----------
Text:

Entities

entity,description
ABILA CITY PARK,Abila City Park is the location of the POK rally

Relationships

source,target,description
ABILA CITY PARK,POK RALLY,Abila City Park is the location of the POK rally
ABILA CITY PARK,POK,POK is holding a rally in Abila City Park
ABILA CITY PARK,POKRALLY,The POKRally is taking place at Abila City Park
ABILA CITY PARK,CENTRAL BULLETIN,Central Bulletin is reporting on the POK rally taking place in Abila City Park

Output:
{{
    "title": "Abila City Park and POK Rally",
    "summary": "The community revolves around the Abila City Park, which is the location of the POK rally. The park has relationships with POK, POKRALLY, and Central Bulletin, all
of which are associated with the rally event.",
    "findings": [
        {{
            "explanation": "Abila City Park is the central entity in this community, serving as the location for the POK rally. This park is the common link between all other
entities, suggesting its significance in the community. The park's association with the rally could potentially lead to issues such as public disorder or conflict, depending on the
nature of the rally and the reactions it provokes."
        }},
        {{
            "explanation": "POK is another key entity in this community, being the organizer of the rally at Abila City Park. The nature of POK and its rally could be a potential
source of threat, depending on their objectives and the reactions they provoke. The relationship between POK and the park is crucial in understanding the dynamics of this community."
        }},
        {{
            "explanation": "The POKRALLY is a significant event taking place at Abila City Park. This event is a key factor in the community's dynamics and could be a potential
source of threat, depending on the nature of the rally and the reactions it provokes. The relationship between the rally and the park is crucial in understanding the dynamics of this
community."
        }},
        {{
            "explanation": "Central Bulletin is reporting on the POK rally taking place in Abila City Park. This suggests that the event has attracted media attention, which could
amplify its impact on the community. The role of Central Bulletin could be significant in shaping public perception of the event and the entities involved."
        }}
    ]
}}

# Real Data

Use the following text for your answer. Do not make anything up in your answer.

Text:
{input_text}
Output:"""