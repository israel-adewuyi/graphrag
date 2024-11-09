# Reference - https://github.com/microsoft/graphrag/blob/main/graphrag/prompt_tune/template/entity_extraction.py
GRAPH_EXTRACTION_JSON_PROMPT = """
-Goal-
Given a text document that is potentially relevant to the field of AI generally and a list of entity types, identify all entities of those types from the text and all relationships among the identified entities.

-Steps-
1. Identify all entities. For each identified entity, extract ALL the following information:
- entity_name: Name of the entity, capitalized
- entity_type: One of the following types: [{entity_types}]
- entity_description: Comprehensive description of the entity's attributes and activities
Format each entity output as a JSON entry with the following format:

{{"name": <entity name>, "type": <type>, "description": <entity description>}}

2. From the entities identified in step 1, identify all pairs of (source_entity, target_entity) that are *clearly related* to each other. For all the entities mentioned, you should include their relationships with other entities as much as posible.
For each pair of related entities, extract the following information:
- source_entity: name of the source entity, as identified in step 1
- target_entity: name of the target entity, as identified in step 1
- relationship_description: explanation as to why you think the source entity and the target entity are related to each other
Format each relationship as a JSON entry with the following format:

{{"source": <source_entity>, "target": <target_entity>, "relationship": <relationship_description>}}
Every entity should be related to at least one other entity. The idea is to build a knowledge graph from this information.
If there are people/persons in the list of entities, pay attention to the things (other entities) they said/did/worked on.
SOME NOTES
1. Individuals like Trenton should be returned as Trenton Bricken, Sholto as Sholto Douglas,  Dwarkesh as Dwarkesh Patel.
""" 