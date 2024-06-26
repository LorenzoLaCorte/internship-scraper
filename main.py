import asyncio
import argparse

from internship_scraper.constants import FILTERED_RESULTS_FILE, TABLE_FILE
from internship_scraper.filter import filter_internships
from internship_scraper.scraper import find_internships
from internship_scraper.utils import csv_to_markdown_table

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--job_categories", nargs="+", help="Job categories", type=str)
    parser.add_argument("--job_titles", nargs="+", help="Job titles", type=str)
    parser.add_argument("--job_types", nargs="+", help="Job types", type=str)
    args = parser.parse_args()

    job_categories: list[str] = args.job_categories
    job_titles: list[str] = args.job_titles
    job_types: list[str] = args.job_types

    # try for a maximum of 5 times
    for _ in range(5):
        try:
            asyncio.run(find_internships(job_categories, job_titles, job_types))
            break
        except Exception as e:
            print(f"An error occurred during the scraping phase: {e}")
        
    try:
        filter_internships(job_categories, job_titles, job_types)
        csv_to_markdown_table(FILTERED_RESULTS_FILE, TABLE_FILE)
    except Exception as e:
        print(f"An error occurred during the post processing phase: {e}")
