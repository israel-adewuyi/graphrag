import os
import re
import sys
import requests
from typing import List

# Add the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from prompts import get_name
from bs4 import BeautifulSoup
from config import PODCAST_LINKS
from utils import get_token_count

def get_name_from_file(idx: int) -> str:
    url = PODCAST_LINKS[idx]
    response = requests.get(url)

    # parse HTML with beautifulsoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # get name of guest
    guest_name = get_name(str(soup.title))

    return guest_name

def get_text_file(idx: int) -> List:
    guest_name = get_name_from_file(idx)

    print(f"Guest name(s) is(are) {guest_name}")

    file_name = f"transcripts/{guest_name}.txt"

    try:
        with open(file_name, "r", encoding='utf-8') as file:
            transcript_text = file.readlines()
    except FileNotFoundError:
        print(f"The file {file_name} does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

    transcript_text = [line for line in transcript_text if line.strip() != '']

    return transcript_text

def chunk_text(idx: int) -> List:
    # Regular expression pattern to match the generic signature
    pattern = re.compile(r"^(.*?)(?:\((\d{1,2}:\d{2}:\d{2}) - (\d{1,2}:\d{2}:\d{2})\):?|\s(\d{1,2}:\d{2}:\d{2}))")

    transcript_text = get_text_file(idx)

    CHUNKS = []

    current_block = ""

    for line in transcript_text:
        match = pattern.match(line)

        if match:
            # If a new speaker is detected, save the current block and start a new one
            if current_block:
                current_block = current_block.replace('\xa0', ' ').replace('\n', ' ')
                CHUNKS.append(current_block)
                current_block = ""
            
            current_block = current_block + line
        else:
            # Add the line to the current block
            if current_block:
                current_block = current_block + line

    return CHUNKS

def merge_chunks(idx: int) -> List:
    CHUNKS = chunk_text(idx)

    NEW_CHUNKS = []

    current_chunk = ""
    current_size = 0
    for chunk in CHUNKS:
        length = get_token_count(chunk)

        if length > 1000:
            NEW_CHUNKS.append(chunk)
        elif current_size + length <= 1000:
            current_chunk = current_chunk + chunk
            current_size += length
        elif current_size + length > 1000:
            NEW_CHUNKS.append(current_chunk)
            current_chunk = chunk
            current_size = length
    if current_chunk:
        NEW_CHUNKS.append(current_chunk)

    return NEW_CHUNKS


if __name__ == "__main__":
    # testing the chunking function
    CHUNKS = chunk_text(0)

    lengths = []

    for str in CHUNKS:
        lengths.append(len(str))

    assert len(lengths) == len(CHUNKS)

    print(f"There are {len(CHUNKS)} in the document")
    print(f"Average string length is {sum(lengths) / len(lengths)}")

    print(CHUNKS[:10])