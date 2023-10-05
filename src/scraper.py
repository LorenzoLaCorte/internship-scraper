from jobspy import scrape_jobs
import pandas as pd
import configparser
import time

config = configparser.ConfigParser()
config.read('config.ini')

SCAPED_LINES_FILE = config.get('SETTINGS', 'SCAPED_LINES_FILE')
TABLE_FILE = config.get('SETTINGS', 'TABLE_FILE')

def scrape_city(city, country, results=10, max_attempts=3, retry_delay=2):
    attempts = 0

    while attempts < max_attempts:
        try:
            jobs: pd.DataFrame = scrape_jobs(
                site_name=["linkedin", "indeed"],
                search_term="Software engineering intern",
                location=city,
                results_wanted=results,
                country_indeed=country
            )

            print(f"Successfully scraped: {city}, {country}")
            return jobs
        except Exception as e:
            attempts += 1
            print(f"Error while scraping {city}, {country}: {str(e)}")
            if attempts < max_attempts:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
    
    print(f"Failed to scrape {city}, {country} after {max_attempts} attempts.")
    return None


def scrape_cities():
    all_rows = pd.DataFrame()

    with open(TABLE_FILE, 'r') as file:
        for line in file:
            country, city = line.strip().split(' | ')
            df = scrape_city(city, country)
            all_rows = pd.concat([all_rows, df], axis=1)
    
    selected_columns = ['company', 'title', 'location', 'job_url']

    with open(SCAPED_LINES_FILE, 'w') as file:
        for _, row in all_rows[selected_columns].iterrows():
            file.write(f'{row["company"]} | {row["title"]} | {row["location"]} | {row["job_url"].iloc[0]}\n')