import os

from neo4j import GraphDatabase
from dataclasses import dataclass
from typing import List, Any
from dotenv import load_dotenv

load_dotenv()

user = os.getenv("neo4j_user")
password = os.getenv("neo4j_password")


@dataclass
class Entity:
    name: str
    type: str
    description: str

@dataclass
class Relationship:
    source: str
    target: str
    relationship: str
    relationship_strength: int

class Neo4jGraphImporter:
    def __init__(self, uri, username, password):
        """
        Initialize Neo4j connection
        
        Args:
            uri: Neo4j database URI (usually bolt://localhost:7687)
            username: Neo4j database username 
            password: Neo4j database password
        """
        self._driver = GraphDatabase.driver(uri, auth=(username, password), database="graphdb")

    def close(self):
        """Close the database connection"""
        self._driver.close()

    def import_graph_data(self, entities: List[Entity], relationships: List[Relationship]):
        """
        Import entities and relationships into Neo4j graph database
        
        Args:
            entities: List of Entity objects
            relationships: List of Relationship objects
        """
        with self._driver.session() as session:
            # First, create all nodes
            for entity in entities:
                session.run(
                    "MERGE (n:Entity {name: $name}) "
                    "SET n.type = $type, n.description = $description",
                    name=entity.name, 
                    type=entity.type, 
                    description=entity.description
                )
            
            # Then, create relationships
            for rel in relationships:
                session.run(
                    "MATCH (a:Entity {name: $source}), (b:Entity {name: $target}) "
                    "MERGE (a)-[r:RELATES_TO {type: $rel_type}]->(b) "
                    "SET r.strength = $strength",
                    source=rel.source, 
                    target=rel.target, 
                    rel_type=rel.relationship, 
                    strength=rel.relationship_strength
                )

def main():
    # Your existing entities and relationships lists
    entities = [
        Entity(name='Dwarkesh Patel', type='person', description='Podcast host'),
        Entity(name='Sholto Douglas', type='person', description="Researcher behind Gemini's success"),
        Entity(name='Trenton Bricken', type='person', description='Researcher at Anthropic who works on mechanistic interpretability'), 
        Entity(name='Noam Brown', type='person', description='Author of the Diplomacy paper, researcher in the AI field'), 
        Entity(name='Anthropic', type='organization', description='Company where Trenton Bricken works'), 
        Entity(name='Artificial Intelligence', type='concept', description='Field of research that the individuals mentioned work in'), 
        Entity(name='Atari Games', type='technologies', description='Video games that the individuals mentioned refer to as a potential area for research'), 
        Entity(name='Perplexity Graphs', type='technologies', description="Visual representations of data, mentioned in the context of Sholto's paper"), 
        Entity(name='Gemini', type='AI models', description='AI model that Sholto was involved in the success of')
        # ... rest of your entities ...
    ]
    
    relationships = [
        Relationship(source='Dwarkesh Patel', target='Sholto Douglas', relationship='Podcast host and guest', relationship_strength=2),
        Relationship(source='Dwarkesh Patel', target='Trenton Bricken', relationship='Podcast host and guest', relationship_strength=2), 
        Relationship(source='Noam Brown', target='Sholto Douglas', relationship='Respected colleague', relationship_strength=3), 
        Relationship(source='Trenton Bricken', target='Anthropic', relationship='Employee', relationship_strength=5), 
        Relationship(source='Sholto Douglas', target='Gemini', relationship='Involved in its success', relationship_strength=6), 
        Relationship(source='Dwarkesh Patel', target='Artificial Intelligence', relationship='Research interest', relationship_strength=3), 
        Relationship(source='Sholto Douglas', target='Artificial Intelligence', relationship='Research interest', relationship_strength=6), 
        Relationship(source='Trenton Bricken', target='Artificial Intelligence', relationship='Research interest', relationship_strength=6), 
        Relationship(source='Noam Brown', target='Artificial Intelligence', relationship='Research interest', relationship_strength=6)
        # ... rest of your relationships ...
    ]

    # Connect to Neo4j
    importer = Neo4jGraphImporter(
        uri="bolt://localhost:7687", 
        username=user, 
        password=password
    )

    try:
        importer.import_graph_data(entities, relationships)
        print("Graph data successfully imported!")
    finally:
        importer.close()

if __name__ == "__main__":
    main()