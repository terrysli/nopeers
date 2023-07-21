# Scrape job data from Envision website.

import json
from bs4 import BeautifulSoup
import requests
from pathlib import Path
from selenium import webdriver

from utils import clean_text, save_html, open_html

BASE_URL = 'https://www.envisionphysicianservices.com'
CLINICAL_JOB_SEARCH_PATH = "find-a-career/clinical-job-search"
OUTPUT_FILE_NAME = "envision"
OUTPUT_FOLDER = "raw"
CHROMEDRIVER_PATH = "/usr/local/bin/chromedriver"
CHROME_BINARY_PATH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# def get_urls(page_end):
#     """
#     Get list of urls for each page in format: BASE_URL/num
#     page_end: last page number to scrape on website
#     get_urls(2) => ["babynames.com", "babynames.com/2"]

#     urls = [f"{BASE_URL}/{n}" for n in range(2, page_end + 1)]
#     urls.insert(0, BASE_URL)

#     return urls

def get_and_save_html(url):
    """Get HTML using chromedriver and save html in txt file."""
    try:
        chrome_options = webdriver.ChromeOptions()
        chrome_options._ignore_local_proxy = True
        chrome_options.executable_path = CHROMEDRIVER_PATH
        chrome_options.binary_location = CHROME_BINARY_PATH

        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        save_html(driver.page_source, 'html_content.txt')
        driver.quit()

    except requests.exceptions.RequestException as e:
        print(f"Error getting HTML from url {url}:", e)

def scrape_html(html):
    """
    Scrape HTML doc to extract and return list of job_info dicts.
    """

    soup = BeautifulSoup(html, 'html.parser')

    # Find list of divs containing info for each job
    results_card_divs = soup.find_all('div', class_="search-results__card")
    print("### results_card_divs = ", len(results_card_divs))

    # List to hold jobs info
    jobs_info = []

    for div in results_card_divs:
        title = div.find("div", class_="jobTitle").get_text()
        specialty = div.find("div", class_="jobSpecialty").get_text()
        details = ""
        details_divs = div.find_all("div", class_="details")
        for details_div in details_divs:
           details += details_div.get_text()

        status = div.find("div", class_="jobStatus").get_text()
        position_type = div.find("div", class_="jobPositionType").get_text()

        info = {
            "title": clean_text(title),
            "specialty": clean_text(specialty),
            "details": clean_text(details),
            "status": clean_text(status),
            "position_type": clean_text(position_type)
        }

        jobs_info.append(info)

    return jobs_info

def write_to_txt_file(data, filename, folder):
    """
    Write dictionary data to filename at folder IN parent folder of this module.
    If wanting text file to live in parent folder, pass empty string to path
    output to, if folder given: {parent}/folder/filename.txt: { data }
               if folder = "": {parent}/filename.txt: { data }
    """

    parent_path = Path(__file__).parent
    #TODO: Change filepath to names folder after completing data output

    if (folder == ""):
        output_file_path = f"{parent_path}/{filename}.txt"
    else:
        output_file_path = f"{parent_path}/{folder}/{filename}.txt"

    try:
        f = open(output_file_path, 'w')
        f.write(json.dumps(data, sort_keys=True))
    except Exception as e:
        print("Error while writing to file {0}: {1}".format(output_file_path, e))

def scrape_and_write_to_file():
    """Scrape data from pages 1-15 at BASE_URL and write to txt file."""

    # Dict to hold {name: [fact, ...], ...}
    jobs_info = {}

    url = f"{BASE_URL}/{CLINICAL_JOB_SEARCH_PATH}"
    html_doc = get_html_document(url)
    scraped_data = scrape_html(html_doc)
    jobs_info.update(scraped_data)

    write_to_txt_file(
        data=jobs_info,
        filename=OUTPUT_FILE_NAME,
        folder=OUTPUT_FOLDER
    )

# Only run scrape_and_write_to_file if this module is run directly
# if __name__ == '__main__':
#     scrape_and_write_to_file()
