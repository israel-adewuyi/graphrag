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
from prompts import get_entities, get_global_response, get_community_summary, glean_text

class Graphrag:
    """
    Graphrag is a class designed to process text chunks, create a graph representation of entities and relationships,
    detect communities within the graph, visualize the graph, store the findings in a vector database for
    similarity search and search over the findings.

    Attributes:
        Graph (nx.Graph): The base graph representing entities and relationships.
        community_nodes (List[str]): List of community nodes detected in the graph.
        community_summary (Optional[str]): Summary of the community findings.
        community_factual_findings (List[str]): List of factual findings for each community.
        vector_db (FAISS): Vector database for storing embeddings.
        embeddings (HuggingFaceEmbeddings): Embeddings model for vectorizing text.
        relationships_no_gleaning (int): Number of relationships without gleaning.
        relationships_with_gleaning (int): Number of relationships with gleaning.
    """
    # base graph
    Graph: nx.Graph

    # community
    community_nodes: List[str]
    community_summary: Optional[str] = None
    community_factual_findings: List[str] = None

    # vector database
    vector_db: FAISS
    embeddings: HuggingFaceEmbeddings 

    # stats
    relationships_no_gleaning: int = 0
    relationships_with_gleaning: int = 0

    def __init__(self, local: bool = False) -> None:
        """
        Initializes the Graphrag class. If `local` is False, it processes text chunks, creates a graph,
        detects communities, visualizes the graph, and stores the findings in a vector database.
        
        If `local` is True, it loads the vector database from the local dir.

        Args:
            local (bool): Flag to indicate whether to load from local dir.
        """
        if not local:
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
        """
        Creates a graph from the text chunks by extracting entities and relationships,
        adding nodes and edges to the graph, and gleaning additional relationships.
        
        See https://arxiv.org/pdf/2404.16130 or https://israel-adewuyi.github.io/blog/2024/replicating-graphrag/ for what gleaning means 
        """
        Graph = nx.Graph()

        for idx, chunk in enumerate(self.text_chunks):
            print(f"Processing chunk {idx}")
            try:
                entities, relationships = get_entities(chunk)

                self.relationships_no_gleaning += len(relationships)

                entities_gleaned, relationships_gleaned = glean_text(entities, relationships)

                self.relationships_with_gleaning += len(relationships_gleaned)
                
                print(f"For index {idx}, {len(relationships_gleaned)} relationships were gleaned.")

                for entity in entities:
                    Graph.add_node(entity.name, 
                                type=entity.type, 
                                description=entity.description)
                
                for relationship in relationships:
                    Graph.add_edge(relationship.source, 
                                relationship.target, 
                                relationship=relationship.relationship)
                
                for relationship in relationships_gleaned:
                    Graph.add_edge(relationship.source, 
                                relationship.target, 
                                relationship=relationship.relationship)
                
                for entity in entities_gleaned:
                    Graph.add_node(entity.name, 
                                type=entity.type, 
                                description=entity.description)
                time.sleep(30)
            except Exception as e:
                print(f"I cannot process chunk at index {idx}")

        print(f"No gleaning - {self.relationships_no_gleaning}, gleaned = {self.relationships_with_gleaning}")
        self.Graph = Graph

    def glean(self, entities: List, relationships: List) -> List:
        pass

    def detect_communities(self) -> None:
        """
        Community detection using the Leiden algorithm.
        """
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
            index += 1
        self.community_nodes = communities

    def visualize_graph(self) -> None:
        """
        Visualizes the graph using Pyvis, with nodes colored and sized based on their type and degree.
        """
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
                        title=f"Relationship: {edge_data['relationship']}")

        net.show("network.html")

    def get_community_summaries(self) -> None:
        """
        Generates summaries for each detected community and stores the factual findings.
        """
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
        """
        Retrieves information about the nodes in a specific community.
        
        The format of the node information is (node, node_description)

        Args:
            idx (int): Index of the community.

        Returns:
            List: List of information about all nodes in the community.
        """
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
        """
        Retrieves information about the edges in a specific community.
        
        The format of the edge information is (edge_node1, edge_node2, relationship between both edge nodes)

        Args:
            idx (int): Index of the community.

        Returns:
            List: List of information about all edges in the community.
        """
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
        """
        Vectorizes the community findings and stores them in the vector database.
        """
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

        print(f"length of document list is {len(documents)}")

        self.vector_db.add_documents(documents=documents, ids=ids)

        self.vector_db.save_local("faiss_index")
        print('--- Completed vectorization')

    def query_similarity(self, query: str) -> str:
        """
        Performs a similarity search on the vector database and returns the response.

        Args:
            query (str): The query string.

        Returns:
            str: The response to the query.
        """
        # 10 is hardcoded as the number of docs to return
        docs1 = self.vector_db.similarity_search_with_score(query, k=10)

        supporting_docs = [(item[0].page_content, item[1]) for item in docs1]

        return self.answer_query(query=query, supporting_docs=supporting_docs)

    def answer_query(self, query: str, supporting_docs: List[str]) -> str:
        """
        Initiate an LLM call to summarize the documents retrieved, in context of the query.

        Args:
            query (str): The query string.
            supporting_docs (List[str]): List of supporting documents.

        Returns:
            str: The response to the query.
        """
        return get_global_response(query=query, supporting_docs=supporting_docs)