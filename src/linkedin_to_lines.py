import configparser
import requests
from bs4 import BeautifulSoup

config = configparser.ConfigParser()
config.read('config.ini')

LINKEDIN_FILE = config.get('SETTINGS', 'LINKEDIN_FILE')
LINES_FILE = config.get('SETTINGS', 'LINES_FILE')


def write_line(company, job_title, place, url):
    with open(LINES_FILE, "a") as file:
        file.write(f"{company} | {job_title} | {place} | {url}\n")
        print(f"Writing line: {company} | {job_title} | {place} | {url}\n")


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


def parse_file():
    try:
        with open(LINKEDIN_FILE, "r") as file:
            for url in file:
                print(f"Parsing url: {url}")
                scrape_link(url)
    except FileNotFoundError:
        print(f"File '{LINKEDIN_FILE}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

parse_file()