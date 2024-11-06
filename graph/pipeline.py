import os
import sys

# Add the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from graphrag import Graphrag

if __name__ == "__main__":
    gr = Graphrag(False)

    docs = gr.query_similarity("What was discussed about Maths Olympiad ?")
    # print(gr.query_similarity("Where does Trenton work?"))

    print(f"Here is response {docs}")