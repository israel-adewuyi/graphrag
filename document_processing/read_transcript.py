import re
import os
import sys
import csv
import requests

# Add the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import PODCAST_LINKS
from prompts import get_name
from bs4 import BeautifulSoup

csv_file_path = "artifacts/links.csv"

def read_name_from_url(link: str) -> str:
    # print("Got to the read_name_from_url function")
    pattern = r'[^/]+'
    match = re.findall(pattern, link)
    
    return match[-1]


def get_transcript_index(transcript_section) -> int:
    pattern = re.compile(r'Transcript:?')

    for idx, section in enumerate(transcript_section):
        for content in section.contents:
            content = str(content)
            if pattern.search(content):
                return idx
    
    return -1


def read_transcript_from_url(url: str, idx: int = -1):
    response = requests.get(url)

    # parse HTML with beautifulsoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # get name of guest
    guest_name = read_name_from_url(url)

    # Find the section containing the transcript
    transcript_section = soup.find_all('h2', class_='header-anchor-post')

    if idx == -1:
        idx = get_transcript_index(transcript_section)

    if idx != -1:
        # Get the next sibling elements after the transcript header
        transcript_content = []
        next_element = transcript_section[idx].find_next_sibling()

        while next_element and next_element.name != 'h2':
            transcript_content.append(next_element.get_text())
            next_element = next_element.find_next_sibling()

        transcript_text = '\n\n'.join(transcript_content)

        with open(f"artifacts/transcripts/{guest_name}.txt", "w", encoding='utf-8') as file:
            file.write(transcript_text)

        with open(f"artifacts/successful_transcripts.txt", 'a') as file:
            file.write(url + '\n')
    else:
        # print(f"Transcript section not found for {guest_name}.")
        with open("artifacts/notranscript.txt", 'a') as file:
            file.write(url + '\n')


def read_transcripts():
    with open(csv_file_path, mode='r', newline='') as file:
        reader = csv.reader(file)
        data = list(reader)

    for i, entry in enumerate(data):
        if entry[1] == "True":
            continue

        read_transcript_from_url(entry[0])

    HARDCODED_LIST = [
        "https://www.dwarkeshpatel.com/p/nadia-asparouhova",
        "https://www.dwarkeshpatel.com/p/byrne-hobart-2",
        "https://www.dwarkeshpatel.com/p/tyler-cowen",
    ]

    for url in HARDCODED_LIST:
        read_transcript_from_url(url, 0)



if __name__ == "__main__":
    read_transcripts()