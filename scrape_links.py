import requests
from bs4 import BeautifulSoup
import csv
import threading
import time
import os
import re
import tkinter as tk
from tkinter import messagebox

def scrape_links(url):
    response = requests.get(url)
    if response.status_code != 200:
        messagebox.showerror("Error", f"Failed to retrieve the page. Status code: {response.status_code}")
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

def sanitize_filename(url):
    return re.sub(r'[^a-zA-Z0-9]', '_', url)

def start_scraping():
    url = url_entry.get()
    if not url:
        messagebox.showerror("Error", "Please enter a URL.")
        return
    
    links = scrape_links(url)
    status_label.config(text='Scraping complete.')
    
    sanitized_url = sanitize_filename(url)
    filename = f"{sanitized_url}.csv"
    
    if os.path.exists(filename):
        overwrite = messagebox.askyesno("File Exists", f"The file {filename} already exists. Do you want to overwrite it?")
        if not overwrite:
            messagebox.showinfo("Info", "File not saved.")
            return

    save_links_to_csv(links, filename)
    messagebox.showinfo("Info", f"Saved {len(links)} links to {filename}")

# GUI setup
root = tk.Tk()
root.title("Link Scraper")

url_label = tk.Label(root, text="Enter the URL to scrape links from:")
url_label.pack()

url_entry = tk.Entry(root, width=50)
url_entry.pack()

scrape_button = tk.Button(root, text="Scrape Links", command=start_scraping)
scrape_button.pack()

status_label = tk.Label(root, text="")
status_label.pack()

root.mainloop()
