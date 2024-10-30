import os
import sys
import requests

# Add the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import PODCAST_LINKS
from bs4 import BeautifulSoup

def read_transcripts():
    url = PODCAST_LINKS[0]
    
    response = requests.get(url)

    # parse HTML with beautifulsoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # print(soup)

    # Find the section containing the transcript
    transcript_section = soup.find('h2', class_='header-anchor-post', string="Timestamps")

    print(transcript_section)

    if transcript_section:
        # Get the next sibling elements after the transcript header
        transcript_content = []
        next_element = transcript_section.find_next_sibling()

        while next_element and next_element.name != 'h2':
            transcript_content.append(next_element.get_text(separator='\n', strip=True))
            next_element = next_element.find_next_sibling()

        # Join the transcript content into a single string
        transcript_text = '\n\n'.join(transcript_content)
        # print(transcript_text)
    else:
        print("Transcript section not found.")

    # with open('transcript.txt', "w", encoding='utf-8') as file:
    #     file.write(response.content.decode(encoding))

if __name__ == "__main__":
    read_transcripts()