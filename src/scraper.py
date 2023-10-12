import pandas as pd
import configparser
import time

from JobSpy.src.jobspy import scrape_jobs
from collections import defaultdict

from JobSpy.src.jobspy.scrapers.exceptions import IndeedException, LinkedInException

config = configparser.ConfigParser()
config.read('../config.ini')

SCRAPED_LINES_FILE = config.get('RESOURCES', 'SCRAPED_LINES_FILE', fallback='output/scraped_lines.txt')
CITIES = config.get('RESOURCES', 'CITIES', fallback='static/partial_cities.txt')
DEFAULT_RESULTS = config.getint('RESULTS', 'DEFAULT_RESULTS', fallback=20)
MAX_ATTEMPTS = config.getint('RETRIES', 'MAX_ATTEMPTS', fallback=3)
RETRY_DELAY = config.getint('RETRIES', 'RETRY_DELAY', fallback=3)

QUERIES_RESULTS = {"software engineering intern": DEFAULT_RESULTS,
                    "software engineer intern": DEFAULT_RESULTS, 
                    "software engineering internship": DEFAULT_RESULTS, 
                    "software engineer internship": DEFAULT_RESULTS, 
                    "engineering intern": DEFAULT_RESULTS*2}

query_stats = defaultdict(list[int])
exceptions_stats = defaultdict(int)

def filter_results(jobs):
    return jobs[((jobs['title'].str.lower().str.contains('engineer')) | (jobs['title'].str.lower().str.contains('engineering')) | (jobs['title'].str.lower().str.contains('developer')) | (jobs['title'].str.lower().str.contains('development')))
                & ((jobs['title'].str.lower().str.contains('intern')) | (jobs['title'].str.lower().str.contains('internship')))]


def scrape_city(city, country, query, results, max_attempts, retry_delay):
    print(f"Scraping in {city}, {country} with query: {query}")
    attempts = 0
    while attempts < max_attempts:
        try:
            jobs = scrape_jobs(
                site_name=["linkedin", "indeed"],
                search_term=query,
                location=city,
                results_wanted=results,
                country_indeed=country
            )
            print(f"Number of results: {len(jobs)}")
            jobs.to_csv(f'../debug/{city}-{query}.txt', index=False) # DEBUG

            filtered_jobs = filter_results(jobs)
            print(f"Number of results remaining after filtering: {len(filtered_jobs)}")

            # if query has empty locations, replace them with the city
            filtered_jobs_copy = filtered_jobs.copy()  # Create a copy of the DataFrame
            filtered_jobs_copy.loc[filtered_jobs_copy['location'] == '', 'location'] = city + ', ' + country
            filtered_jobs = filtered_jobs_copy

            if len(query_stats[query]) == 0:
                query_stats[query].append([len(jobs)])
                query_stats[query].append([len(filtered_jobs)])
            else:
                query_stats[query][0].append(len(jobs))
                query_stats[query][1].append(len(filtered_jobs))

            return filtered_jobs
        
        except Exception as e:
            attempts += 1
            exceptions_stats[(city, query, type(e).__name__)] += 1
            print(f"Error while scraping {city}, {country}: {type(e).__name__}: {str(e)}")
            if attempts < max_attempts:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
    
    print(f"Failed to scrape {city}, {country}, {query}, after {max_attempts} attempts.")
    return None


def write_results(all_rows):
    written_lines = 0
    empty_values_rows = 0
    nan_values_rows = 0

    selected_columns = ['company', 'title', 'location', 'job_url']

    try:
        with open(SCRAPED_LINES_FILE, 'a') as file:
            for _, row in all_rows[selected_columns].iterrows():
                if not row.isna().any():
                    company = row["company"] if isinstance(row["company"], str) else row["company"].iloc[0]
                    title = row["title"] if isinstance(row["title"], str) else row["title"].iloc[0]
                    location = row["location"] if isinstance(row["location"], str) else row["location"].iloc[0]
                    job_url = row["job_url"] if isinstance(row["job_url"], str) else row["job_url"].iloc[0]
                    
                    # TODO: if company or title or location aren't present but job_url yes, insert it in contribute_ linkeding or indeed to scrape it
                    if company and title and location and job_url:
                        written_lines += 1
                        file.write(f'{company} | {title} | {location} | {job_url}\n')
                        # print(f"Writing line: {company} | {title} | {location} | {job_url}")
                    else:
                        empty_values_rows += 1
                else:
                    nan_values_rows += 1
        
        print(f"\n📊 Found a total of {written_lines} results scraping")
        print(f"Found {empty_values_rows} filtered results with empty values")
        print(f"Found {nan_values_rows} filtered results with nan values")
    
    except KeyError as e:
        print(f"\nNo results found scraping")


def print_stats():
    for query, stat_lists in query_stats.items():
        print(f"\n📊 Stats for {query}, which had {QUERIES_RESULTS[query]} wanted results")
        print(f"Mean Number of Results: {sum(stat_lists[0])/len(stat_lists[0])}")
        print(f"Mean Number of Filtered Results: {sum(stat_lists[1])/len(stat_lists[1])}")
        print(f"Efficiency of the Query: {sum(stat_lists[1])/sum(stat_lists[0])}")
        print(f"Exception Stats: {exceptions_stats}")


def scrape_cities():
    all_rows = pd.DataFrame()

    with open(CITIES, 'r') as file:
        for line in file:
            country, city = line.strip().split(' | ')
            for query, results in QUERIES_RESULTS.items():
                df = scrape_city(city, country, query, results, MAX_ATTEMPTS, RETRY_DELAY)
                all_rows = pd.concat([all_rows, df], axis=0)
    
    print_stats()
    write_results(all_rows)