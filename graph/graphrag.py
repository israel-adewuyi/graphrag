import time
import faiss
import networkx as nx

from uuid import uuid4
from typing import List, Optional
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.docstore.in_memory import InMemoryDocstore

from cdlib import algorithms
from config import COLOR_MAP
from pyvis.network import Network
from document_processing import merge_chunks
from prompts import get_entities, get_global_response, get_community_summary

class Graphrag:
    # base graph
    Graph: nx.Graph

    # community
    community_nodes: List[str]
    community_summary: Optional[str] = None
    community_factual_findings: List[str] = None

    # vector database
    vector_db: FAISS
    embeddings: HuggingFaceEmbeddings 

    def __init__(self, local: bool = False) -> None:
        if not local:
            # TODO: Iterate through all the docs, call merge chunks and save to text_chunks
            self.text_chunks = merge_chunks(0)

            self.create_graph()

            self.detect_communities()

            self.visualize_graph()

            self.community_factual_findings = []

            self.get_community_summaries()

            self.vectorize_and_store()
        else:
            print("Loading from local this time around")
            self.load_index_from_local()

    def create_graph(self) -> None:
        Graph = nx.Graph()

        for idx, chunk in enumerate(self.text_chunks):
            print(f"Processing chunk {idx}")
            try:
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
            except Exception as e:
                print(f"I cannot process chunk at index {idx}")

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
            # else:
            #     communities.append(list(subgraph.nodes))
            index += 1
        # print("Communities from detect_communities:", communities)
        self.community_nodes = communities

    def visualize_graph(self) -> None:
        color_map = COLOR_MAP
        # Get the degree of each node
        degrees = dict(self.Graph.degree())
        # Scale the sizes
        min_size = 10
        max_size = 60
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
            
            color = color_map.get(node_type, '#999999')
            
            # Calculate scaled node size
            if max_degree > min_degree: 
                size = min_size + (max_size - min_size) * (degrees[node] - min_degree) / (max_degree - min_degree)
            else:
                size = min_size
                
            # Add node with color and size
            try:
                net.add_node(node, 
                            color=color,
                            size=size,
                            title=f"Type: {node_type}\nDegree: {degrees[node]}\nDescription: {self.Graph.nodes[node]['description']}")
            except Exception as e:
                net.add_node(node, 
                            size=size,
                            title=f"Degree: {degrees[node]}")

        # Add edges
        for edge in self.Graph.edges():
            source, target = edge
            edge_data = self.Graph.edges[edge]
            net.add_edge(source, target, 
                        title=f"Relationship: {edge_data['relationship']}\nStrength: {edge_data['strength']}")

        net.show("network.html")

    def get_community_summaries(self) -> None:
        assert self.community_summary is None, "Graph summaries filled already"

        with open("findings.txt", 'w', encoding='utf-8') as file:
            for community_idx in range(len(self.community_nodes)):
                nodes_info = self.get_node_info(community_idx)
                edges_info = self.get_edge_info(community_idx)

                community_report = get_community_summary(nodes_info, edges_info)

                for finding in community_report.findings:
                    file.write(f"{finding.explanation}\n\n")
                    self.community_factual_findings.append(finding.explanation)
    
        print("--- Completed community summary generation")

    def get_node_info(self, idx: int) -> List:
        nodes_context = []

        sub_nodes = self.community_nodes[idx]
        sub_graph = self.Graph.subgraph(sub_nodes)

        for node in sub_graph.nodes():
            node_description = sub_graph.nodes()[node].get('description', "no description provided, use your ideas")
            info = f"{node},{node_description}"
            nodes_context.append(info)

        return nodes_context
    
    def load_index_from_local(self) -> None:
        self.embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-mpnet-base-v2')
        self.vector_db = FAISS.load_local("faiss_index", 
                                          embeddings=self.embeddings,
                                          allow_dangerous_deserialization=True)

    def get_edge_info(self, idx: int) -> List:
        edges_context = []

        sub_nodes = self.community_nodes[idx]
        sub_graph = self.Graph.subgraph(sub_nodes)

        for edge in sub_graph.edges():
            info = f"{edge[0]},{edge[1]},{sub_graph.edges()[edge]['relationship']}"
            edges_context.append(info)

        return edges_context

    def get_vector_store_documents(self):
        assert self.community_factual_findings is not None, "There are no community findings"

        documents = [Document(page_content=content) for content in self.community_factual_findings]

        uuids = [str(uuid4()) for _ in range(len(documents))]

        return documents, uuids
    
    def vectorize_and_store(self) -> None:
        self.embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-mpnet-base-v2')

        index = faiss.IndexFlatIP(len(self.embeddings.embed_query("hello world")))

        self.vector_db = FAISS(
            embedding_function=self.embeddings,
            index=index,
            docstore=InMemoryDocstore(),
            index_to_docstore_id={},
            normalize_L2=True
        )
        
        documents, ids = self.get_vector_store_documents()

        self.vector_db.add_documents(documents=documents, ids=ids)

        self.vector_db.save_local("faiss_index")
        print('--- Completed vectorization')

    def query_similarity(self, query: str) -> str:
        docs1 = self.vector_db.similarity_search_with_score(query, k=10)

        supporting_docs = [(item[0].page_content, item[1]) for item in docs1]

        # for item in supporting_docs:
        #     print(item, end='\n')

        return self.answer_query(query=query, supporting_docs=supporting_docs)

    def answer_query(self, query: str, supporting_docs: List[str]) -> str:
        return get_global_response(query=query, supporting_docs=supporting_docs)