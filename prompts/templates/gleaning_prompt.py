GLEANING_PROMPT = """
-GOAL-
Given a text document that is potentially relevant to the field of AI generally, a list of entity types, a list of 
preliminary list of entities and a preliminary list of relationships between the entities, identify all entities which
are not included in the original list as well as relationships that have not been included in the original list as well. 

-Steps-
1. Identify all entities not included in the OG list. For each identified entity, extract ALL the following information:
- entity_name: Name of the entity, capitalized
- entity_type: One of the following types: [{entity_types}]
- entity_description: Comprehensive description of the entity's attributes and activities
Format each entity output as a JSON entry with the following format:

{{"name": <entity name>, "type": <type>, "description": <entity description>}}

2. From the entities identified in step 1 and entities in the original list, identify all pairs of (source_entity, target_entity) that are *clearly related* to each other and they are not in the provided list of relationships. For all the entities mentioned, you should include their relationships with other entities as much as posible.
For each pair of related entities, extract the following information:
- source_entity: name of the source entity, as identified in step 1
- target_entity: name of the target entity, as identified in step 1
- relationship_description: explanation as to why you think the source entity and the target entity are related to each other
Format each relationship as a JSON entry with the following format:

{{"source": <source_entity>, "target": <target_entity>, "relationship": <relationship_description>}}

3. DO NOT DUPLICATE either entities or relationships. If some entity or relationship is present already, skip it.

- SOME NOTES - 
1. Every entity should be related to at least one other entity. The idea is to build a knowledge graph from this information.
If there are people/persons in the list of entities, pay attention to the things (other entities) they said/did/worked on or with.
SOME NOTES

2. Individuals like Trenton should be returned as Trenton Bricken, Sholto as Sholto Douglas,  Dwarkesh as Dwarkesh Patel.

"""