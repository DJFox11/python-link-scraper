# Link Web Scraper

This Python script allows you to scrape links from a webpage and save them to a CSV file.

## Installation

Ensure you have Python installed on your system. This script utilises the following Python libraries:

- `requests`: For making HTTP requests
- `beautifulsoup4`: For parsing HTML
- `itertools`: For creating iterators

`pip install requests beautifulsoup4 tqdm`

## Usage

1. Download the latest release from [Releases](https://github.com/DJFox11/python-link-scraper/releases/tag/master).
2. Extract and downloaded .zip file and open the .exe titled `Link_Scraper.exe`.
3. Enter the website from which you would like to scrape the links and click the `Scrape Links` button.
    - When entering the URL, make sure to include `https://` or `http://` respectively.
4. A .csv file will soon be created containing the links from the specified website.

## Planned Features

1. **Error Handling**
    - Enchance error handling to cover network errors and invalid URL cases.
2. **hreading**
    - Implement threading to prevent GUI freezing during scraping.
3. **Progress Indicator**
    - Add a progress indicator to show the scraping progress.
4. **Better File Management**
    - Automatically generate a new filename if the file already exists.
6. **Input Validation**
    - Include basic input validation for the URL format.
8. **Logging**
    - Add logging functionality for extra tracking and debugging.
10. **GUI Improvements**
    - Enhance the GUI with features like a file picker for the output file, as well as customisable scraping options.
