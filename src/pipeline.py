from scraper import scrape_cities
from linkedin_to_lines import scrape_linkedin_file
from lines_to_table import render_lines

def run():
    scrape_cities(result_per_city=5, retries=3)
    scrape_linkedin_file()
    # scrape_indeed_file()
    render_lines()

if __name__ == "__main__":
    run()