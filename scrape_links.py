import requests
from bs4 import BeautifulSoup
import csv
import itertools
import threading
import time
import os
import re

def scrape_links(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return []
    
    soup = BeautifulSoup(response.content, 'html.parser')
    a_tags = soup.find_all('a')
    links = [a.get('href') for a in a_tags if a.get('href')]
    return links

def save_links_to_csv(links, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Link'])
        for link in links:
            writer.writerow([link])

def display_spinner():
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if not spinning:
            break
        print(f'\rScraping links... {c}', end='', flush=True)
        time.sleep(0.1)

def sanitize_filename(url):
    return re.sub(r'[^a-zA-Z0-9]', '_', url)

if __name__ == '__main__':
    url = input('Enter the URL to scrape links from: ')
    
    spinning = True
    spinner_thread = threading.Thread(target=display_spinner)
    spinner_thread.start()
    
    links = scrape_links(url)
    
    spinning = False
    spinner_thread.join()
    print('\rScraping complete.         ')
    
    sanitized_url = sanitize_filename(url)
    filename = f"{sanitized_url}.csv"
    
    if os.path.exists(filename):
        overwrite = input(f"The file {filename} already exists. Do you want to overwrite it? (yes/no): ")
        if overwrite.lower() != 'yes':
            print("File not saved.")
            exit()


    save_links_to_csv(links, filename)
    print(f"Saved {len(links)} links to {filename}")
    time.sleep(3)
