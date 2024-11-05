import time
import networkx as nx

from typing import List, Optional

from cdlib import algorithms
from prompts import get_entities
from pyvis.network import Network
from prompts import get_community_summary
from document_processing import merge_chunks

"""
    4. Test the communty summaries +  all of the above in graphrag
    4. Include plotting of graph and writing to some external file
    5. Think about redundancy, esp with LLM calls.
"""

class Graphrag:
    # base graph
    Graph: nx.Graph

    # community
    community_nodes: List[str]
    community_summary: Optional[str] = None
    community_factual_findings: List[str] = None

    # vector database
    # vector_db: FAISS
    # embeddings: HuggingFaceEmbeddings 

    def __init__(self) -> None:
        # TODO: Iterate through all the docs, call merge chunks and save to text_chunks
        self.text_chunks = merge_chunks(0)

        self.create_graph()

        self.detect_communities()

        self.community_factual_findings = []

        self.get_community_summaries()

        # self.vectorize_and_store()

    def create_graph(self) -> None:
        Graph = nx.Graph()

        for idx, chunk in enumerate(self.text_chunks[:2]):
            print(f"Processing chunk {idx}")
            entities, relationships = get_entities(chunk)

            for entity in entities:
                Graph.add_node(entity.name, 
                               type=entity.type, 
                               description=entity.description)
            for relationship in relationships:
                Graph.add_edge(relationship.source, 
                               relationship.target, 
                               relationship=relationship.relationship, 
                               strength=relationship.relationship_strength)
            time.sleep(30)

        self.Graph = Graph


    def detect_communities(self) -> None:
        communities = []
        index = 0
        for component in nx.connected_components(self.Graph):
            print(
                f"Component index {index} of {len(list(nx.connected_components(self.Graph)))}:")
            subgraph = self.Graph.subgraph(component)
            if len(subgraph.nodes) > 1:  # Leiden algorithm requires at least 2 nodes
                try:
                    sub_communities = algorithms.leiden(subgraph)
                    for community in sub_communities.communities:
                        communities.append(list(community))
                except Exception as e:
                    print(f"Error processing community {index}: {e}")
            else:
                communities.append(list(subgraph.nodes))
            index += 1
        # print("Communities from detect_communities:", communities)
        self.community_nodes = communities

    def visualize_graph(self) -> None:
        color_map = None
        # Calculate node sizes based on degree (number of connections)
        # Get the degree of each node
        degrees = dict(self.Graph.degree())
        # Scale the sizes - you can adjust these numbers
        min_size = 20
        max_size = 50
        min_degree = min(degrees.values())
        max_degree = max(degrees.values())

        # Create a Pyvis network object
        net = Network(notebook=True, cdn_resources='remote')

        # Add nodes to Pyvis network with colors and sizes
        for node in self.Graph.nodes():
            # Get node type
            try:
                node_type = self.Graph.nodes[node]['type']
            except Exception as e:
                pass
            # Get color from mapping, default to grey if type not found
            color = color_map.get(node_type, '#999999')
            
            # Calculate scaled node size
            if max_degree > min_degree:  # Prevent division by zero
                size = min_size + (max_size - min_size) * (degrees[node] - min_degree) / (max_degree - min_degree)
            else:
                size = min_size
                
            # Add node with color and size
            try:
                net.add_node(node, 
                            color=color,
                            size=size,
                            title=f"Type: {node_type}\nDegree: {degrees[node]}\nDescription: {G.nodes[node]['description']}")
            except Exception as e:
                net.add_node(node, 
                            size=size,
                            title=f"Degree: {degrees[node]}")

        # Add edges to Pyvis network
        for edge in self.Graph.edges():
            source, target = edge
            edge_data = self.Graph.edges[edge]
            net.add_edge(source, target, 
                        title=f"Relationship: {edge_data['relationship']}\nStrength: {edge_data['strength']}")

        # Configure other visualization options
        net.toggle_physics(True)
        net.show_buttons(filter_=['physics'])

        # Save and show the network
        net.show("network.html")

    def get_community_summaries(self):
        assert self.community_summary is None, "Graph summaries filled already"

        for community_idx in range(len(self.community_nodes)):
            nodes_info = self.get_node_info(community_idx)
            edges_info = self.get_edge_info(community_idx)

            community_report = get_community_summary(nodes_info, edges_info)

            for finding in community_report.findings:
                self.community_factual_findings.append(finding.explanation)

        print("These are community summaries")
        # print(community_report.model_dump_json(indent=3))
        print(self.community_factual_findings)

    def get_node_info(self, idx: int) -> List:
        nodes_context = []

        sub_nodes = self.community_nodes[idx]
        sub_graph = self.Graph.subgraph(sub_nodes)

        for node in sub_graph.nodes():
            info = f"{node},{sub_graph.nodes()[node]['description']}"
            nodes_context.append(info)

        return nodes_context

    def get_edge_info(self, idx: int) -> List:
        edges_context = []

        sub_nodes = self.community_nodes[idx]
        sub_graph = self.Graph.subgraph(sub_nodes)

        for edge in sub_graph.edges():
            info = f"{edge[0]},{edge[1]},{sub_graph.edges()[edge]['relationship']}"
            print(info)

        return edges_context