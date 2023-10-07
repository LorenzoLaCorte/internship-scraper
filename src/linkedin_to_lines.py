import configparser
import requests
from bs4 import BeautifulSoup
import re


config = configparser.ConfigParser()
config.read('../config.ini')

LINKEDIN_FILE = config.get('RESOURCES', 'LINKEDIN_FILE')
CONTRIBUTE_LINES_FILE = config.get('RESOURCES', 'CONTRIBUTE_LINES_FILE')


def write_line(company, job_title, place, url):
    with open(CONTRIBUTE_LINES_FILE, "a") as file:
        file.write(f"\n{company} | {job_title} | {place} | {url}")
        # print(f"Writing line: {company} | {job_title} | {place} | {url}") # Debug


def scrape_link(url):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        job_title_element = soup.find('h1', class_='top-card-layout__title')
        job_title = job_title_element.text.strip() if job_title_element else "Job title not found"
        
        company_element = soup.find('a', class_='topcard__org-name-link')
        company = company_element.text.strip() if company_element else "Company not found"
        
        place_element = soup.find('span', class_='topcard__flavor--bullet')
        place = place_element.text.strip() if place_element else "Place not found"
        
        write_line(company, job_title, place, url)
    else:
        print("Failed to retrieve the web page")


def scrape_linkedin_file():
    all_urls = set() # collect all existent urls of contribute_lines
    try:
        with open(CONTRIBUTE_LINES_FILE, "r") as file:
            for line in file:
                parts = line.strip().split(' | ')
                if len(parts) == 4:
                    company, job_title, place, url = parts
                    all_urls.add(url)
                else:
                    print("Invalid line format:", line)
        with open(LINKEDIN_FILE, "r") as file:
            for url in file:
                if not url in all_urls:
                    print(f"Parsing url: {url}")
                    scrape_link(url)
    except Exception as e:
        print(f"An error occurred: {e}")