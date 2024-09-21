import requests
from bs4 import BeautifulSoup
import csv
import os
import re
import threading
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from urllib.parse import urljoin

# LinkScraper class to handle the web scraping functionality
class LinkScraper:
    @staticmethod
    def scrape_links(url):
        response = requests.get(url)
        if response.status_code != 200:
            if response.status_code == 403:
                raise Exception("Access to the website is forbidden (403 error).")
            else:
                raise Exception(f"Failed to retrieve the page. Status code: {response.status_code}")
        
        soup = BeautifulSoup(response.content, 'html.parser')
        a_tags = soup.find_all('a')
        links = []
        for a in a_tags:
            href = a.get('href')
            if href:
                full_url = urljoin(url, href)
                links.append(full_url)
        return links

    @staticmethod
    def save_links_to_csv(links, filename):
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Link'])
            for link in links:
                writer.writerow([link])

    @staticmethod
    def save_links_to_txt(links, filename):
        with open(filename, 'w', encoding='utf-8') as file:
            for link in links:
                file.write(link + '\n')

# LinkScraperApp class to handle the GUI and user interactions
class LinkScraperApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Link Scraper")
        self.geometry("420x350")
        self.resizable(False, False)

        # Load the Azure theme
        try:
            self.tk.call("source", "azure.tcl")
            self.tk.call("set_theme", "dark")  # You can set 'light' or 'dark'
        except tk.TclError as e:
            print(f"Error loading Azure theme: {e}")
            # Fallback to default theme if the Azure theme fails to load
            self.style = ttk.Style(self)
            self.style.theme_use('clam')

        self.create_widgets()
    def create_widgets(self):
        # URL input
        url_label = ttk.Label(self, text="Enter the URL to scrape links from:")
        url_label.pack(pady=(10, 0))

        url_frame = ttk.Frame(self)
        url_frame.pack(pady=(5, 0))
        self.url_var = tk.StringVar()
        url_entry = ttk.Entry(url_frame, textvariable=self.url_var, width=40)
        url_entry.pack(side=tk.LEFT, padx=(0, 5))
        url_entry.focus()
        clear_button = ttk.Button(url_frame, text="Clear", command=self.clear_input)
        clear_button.pack(side=tk.LEFT)

        # Export format selection
        format_label = ttk.Label(self, text="Select export format:")
        format_label.pack(pady=(10, 0))
        self.format_var = tk.StringVar(value='TXT')
        format_combo = ttk.Combobox(self, textvariable=self.format_var, values=['TXT', 'CSV'], state='readonly')
        format_combo.pack(pady=(5, 0))

        # Overwrite checkbox
        self.overwrite_var = tk.BooleanVar()
        overwrite_check = ttk.Checkbutton(self, text="Overwrite if file exists", variable=self.overwrite_var)
        overwrite_check.pack(pady=(5, 0))

        # Scrape Links button
        scrape_button = ttk.Button(self, text="Scrape Links", command=self.start_scraping)
        scrape_button.pack(pady=(10, 0))

        # Status label
        self.status_var = tk.StringVar()
        status_label = ttk.Label(self, textvariable=self.status_var, wraplength=350)
        status_label.pack(pady=(10, 0))

        # Loading indicator
        self.progress_bar = ttk.Progressbar(self, mode='indeterminate')
        self.progress_bar.pack(pady=(10, 0))
        self.progress_bar.stop()

        # Created by label
        created_by_label = ttk.Label(self, text="Created by DJ_Fox11")
        created_by_label.pack(side=tk.BOTTOM, pady=(0, 10))

    def clear_input(self):
        self.url_var.set("")
        self.status_var.set("")

    def start_scraping(self):
        url = self.url_var.get().strip()
        if not url.startswith("http://") and not url.startswith("https://"):
            if ":" in url:
                self.status_var.set(
                    "Error: Invalid URL. Please enter a valid URL starting with 'http://' or 'https://'.")
                return
            url = "http://" + url

        self.status_var.set("Scraping...")
        self.progress_bar.start()

        # Start scraping in a separate thread
        threading.Thread(target=self.scrape_and_save_links, args=(url,), daemon=True).start()

    def scrape_and_save_links(self, url):
        try:
            links = LinkScraper.scrape_links(url)
            # Schedule the save and GUI updates in the main thread
            self.after(0, self.save_and_update, links, url)
        except Exception as e:
            self.after(0, self.scrape_failed, str(e))

    def save_and_update(self, links, url):
        self.progress_bar.stop()

        sanitized_url = re.sub(r'[^a-zA-Z0-9]', '_', url)
        export_format = self.format_var.get()

        if export_format == "CSV":
            default_filename = f"{sanitized_url}.csv"
            filetypes = [('CSV files', '*.csv')]
            save_function = LinkScraper.save_links_to_csv
        else:
            default_filename = f"{sanitized_url}.txt"
            filetypes = [('Text files', '*.txt')]
            save_function = LinkScraper.save_links_to_txt

        # Ask the user where to save the file
        filename = filedialog.asksaveasfilename(
            defaultextension=filetypes[0][1], filetypes=filetypes, initialfile=default_filename)

        if filename:
            if os.path.exists(filename):
                overwrite = self.overwrite_var.get()
                if not overwrite:
                    self.status_var.set("File not saved: File already exists.")
                    return

            save_function(links, filename)
            self.status_var.set(f"Saved {len(links)} links to {filename}")
        else:
            self.status_var.set("File save cancelled.")

    def scrape_failed(self, error_message):
        self.progress_bar.stop()
        self.status_var.set(f"Error: {error_message}")

if __name__ == "__main__":
    app = LinkScraperApp()
    app.mainloop()
