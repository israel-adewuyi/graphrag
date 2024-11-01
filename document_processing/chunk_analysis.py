import os
import sys

# Add the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from document_processing import chunk_text
from document_processing import merge_chunks
from utils import get_token_count
from utils import plot_bar_chart

def do_something():
    # CHUNKS = chunk_text(0)
    CHUNKS = merge_chunks(0)

    print(f"There are {len(CHUNKS)} in the file")

    token_count = [get_token_count(chunk) for chunk in CHUNKS]

    plot_bar_chart(token_count, "Sholto&Trenton_merged")

    print("Finished plotting graph")



if __name__ == "__main__":
    do_something()