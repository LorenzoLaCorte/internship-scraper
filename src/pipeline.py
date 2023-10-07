from scraper import scrape_cities
from linkedin_to_lines import scrape_linkedin_file
from lines_to_table import render_lines

def run():
    print("\U0001F409 Scraper")
    scrape_cities()
    print("\n\U0001F4E1 LinkedIn")
    scrape_linkedin_file()
    # scrape_indeed_file()
    print("\n🚀 Rendering")
    render_lines()
    print("\n✅ Job search completed successfully!")


if __name__ == "__main__":
    run()