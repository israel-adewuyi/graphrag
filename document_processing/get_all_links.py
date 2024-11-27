import re
import os
import sys
import csv
import requests

from bs4 import BeautifulSoup
from typing import List

URL = "https://www.dwarkeshpatel.com/podcast"
csv_file_path = "links.csv"

def get_all_links() -> List:
    LINKS = []

    response = requests.get(url=URL)
    # If status code for response is 200

    if response.status_code == 200:
        content = response.content
        # render content as a BS object
        html_soup = BeautifulSoup(content, "html.parser")

        # get the link to the rss feed
        rss_link = html_soup.find('link', {'rel': 'alternate', 'type': 'application/rss+xml'})['href']

        # get response for rss feed link
        response = requests.get(rss_link)

        rss_content = response.content

        # render content as a BS object
        rss_soup = BeautifulSoup(rss_content, 'xml')

        # get links in the data structure by filtering for 'link' tag
        episode_links = rss_soup.find_all("link")

        for link in episode_links:
            if link.string is not None:
                LINKS.append(link.text)

    return LINKS

def isValidLink(link: str) -> bool:
    # Verify if this is a valid podcast link
    pattern = r'/p/.+'

    if re.search(pattern, link):
        return True
    return False

def isPresent(link: str) -> bool:
    with open(csv_file_path, mode='r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if link in row:
                return True
    return False

def write_links_to_csv():
    LINKS = get_all_links()

    assert LINKS is not None, "Zero links was returned is empty"

    with open(csv_file_path, mode="a", newline='') as file:
        writer = csv.writer(file)
        for link in LINKS:
            if isValidLink(link):
                if isPresent(link):
                    print(f"{link} is present in the csv already, so I am skipping.")
                else:
                    entry = [link, "False"]
                    writer.writerow(entry)

#TODO: 
def write_links_to_json():
    pass

if __name__ == "__main__":
    write_links_to_csv()