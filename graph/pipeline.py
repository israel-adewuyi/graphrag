import os
import sys

# Add the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from graphrag import Graphrag

if __name__ == "__main__":
    gr = Graphrag()

    print(gr.query_similarity("Who is Trenton?"))
    
    # print(gr.Graph.nodes())