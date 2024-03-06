import asyncio

from internship_scraper.constants import FILTERED_RESULTS_FILE, TABLE_FILE
from internship_scraper.filter import filter_internships
from internship_scraper.scraper import find_internships
from internship_scraper.utils import csv_to_markdown_table

if __name__ == "__main__":
    try:
        asyncio.run(find_internships())
    except Exception as e:
        print(f"An error occurred during the scraping phase: {e}")
        
    try:
        filter_internships()
        csv_to_markdown_table(FILTERED_RESULTS_FILE, TABLE_FILE)
    except Exception as e:
        print(f"An error occurred during the post processing phase: {e}")