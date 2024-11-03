"""
    1. For all chunks in total chunks, get types from all of them
        Store in a set
    2. For all chunks, generate set of entities and rltn and pass to graph.
"""
import os
import sys



# Add the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from document_processing import chunk_text, merge_chunks

def build_graph():
    pass




if __name__ == "__main__":
    do_something()