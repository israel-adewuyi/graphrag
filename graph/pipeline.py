import os
import sys

# Add the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from graphrag import Graphrag

if __name__ == "__main__":
    gr = Graphrag(True)

    docs = gr.query_similarity("Are there any gists on AlphaFold?")
    # print(gr.query_similarity("Where does Trenton work?"))

    for doc in docs:
        print(doc.page_content)
    
    # print(gr.Graph.nodes())