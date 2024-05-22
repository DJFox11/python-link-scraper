import requests
from bs4 import BeautifulSoup
import csv
import threading
import time
import os
import re
import dearpygui.dearpygui as dpg

def scrape_links(url):
    response = requests.get(url)
    if response.status_code != 200:
        if response.status_code == 403:
            raise Exception("Access to the website is forbidden (403 error).")
        else:
            raise Exception(f"Failed to retrieve the page. Status code: {response.status_code}")

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

def save_links_to_txt(links, filename):
    with open(filename, 'w') as file:
        for link in links:
            file.write(link + '\n')

def sanitize_filename(url):
    return re.sub(r'[^a-zA-Z0-9]', '_', url)

def start_scraping(sender, app_data):
    url = dpg.get_value("url_input")
    if not url.startswith("http://") and not url.startswith("https://"):
        dpg.configure_item("status_label", default_value="Error: Invalid URL. Please enter a valid URL starting with 'http://' or 'https://'.")
        return

    try:
        dpg.configure_item("status_label", default_value="Scraping...")
        dpg.configure_item("loading_indicator", show=True)
        links = scrape_links(url)
        dpg.configure_item("status_label", default_value="Scraping complete.")

        sanitized_url = sanitize_filename(url)
        export_format = dpg.get_value("format_selector")

        if export_format == "CSV":
            filename = f"{sanitized_url}.csv"
            save_function = save_links_to_csv
        else:
            filename = f"{sanitized_url}.txt"
            save_function = save_links_to_txt

        if os.path.exists(filename):
            overwrite = dpg.get_value("overwrite_checkbox")
            if not overwrite:
                dpg.configure_item("status_label", default_value="File not saved: File already exists.")
                dpg.configure_item("loading_indicator", show=False)
                return

        save_function(links, filename)
        dpg.configure_item("status_label", default_value=f"Saved {len(links)} links to {filename}")
    except Exception as e:
        dpg.configure_item("status_label", default_value=f"Error: {str(e)}")
    finally:
        dpg.configure_item("loading_indicator", show=False)

def loading_animation():
    spinner_states = ['/', '-', '\\', '|']
    while dpg.get_item_configuration("loading_indicator")['show']:
        for state in spinner_states:
            dpg.configure_item("loading_indicator", default_value=state)
            time.sleep(0.2)

def clear_input(sender, app_data):
    dpg.set_value("url_input", "")
    dpg.configure_item("status_label", default_value="")

# GUI setup
dpg.create_context()

with dpg.window(label="Link Scraper", width=420, height=260, no_close=True):
    dpg.add_text("Enter the URL to scrape links from:")
    with dpg.group(horizontal=True):
        dpg.add_input_text(tag="url_input", width=250)
        dpg.add_button(label="Clear", callback=clear_input)
    dpg.add_text("Select export format:")
    dpg.add_combo(['TXT', 'CSV'], default_value='TXT', tag="format_selector")
    dpg.add_checkbox(label="Overwrite if file exists", tag="overwrite_checkbox")
    dpg.add_button(label="Scrape Links", callback=start_scraping)
    dpg.add_text("", tag="status_label", wrap=350)
    with dpg.group(horizontal=True):
        dpg.add_text("", tag="scraping_text")
        dpg.add_text("", tag="loading_indicator")
    dpg.configure_item("loading_indicator", show=False)
    dpg.add_spacer(height=5)
    dpg.add_text("Created by DJ_Fox11", pos=(10, 230))

dpg.create_viewport(title='Link Scraper', width=420, height=300)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
