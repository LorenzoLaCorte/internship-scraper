import pandas as pd
import configparser
import logging as logger

from jobspy import scrape_jobs

from collections import defaultdict

from jobspy.scrapers.exceptions import IndeedException, LinkedInException

config = configparser.ConfigParser()
config.read('../config.ini')

SCRAPED_LINES_FILE = config.get('RESOURCES', 'SCRAPED_LINES_FILE', fallback='output/scraped_lines.txt')
CITIES = config.get('RESOURCES', 'CITIES', fallback='static/cities.txt')
CITIES_NO_INDEED = config.get('RESOURCES', 'CITIES_NO_INDEED', fallback='static/cities_no_indeed.txt')
DEFAULT_RESULTS = config.getint('RESULTS', 'DEFAULT_RESULTS', fallback=20)

QUERIES_RESULTS = {"software engineering intern": DEFAULT_RESULTS,
                    "software engineer internship": DEFAULT_RESULTS,
                    "software developer internship": DEFAULT_RESULTS,
                    "cloud engineering intern": DEFAULT_RESULTS
                }

query_stats = defaultdict(list[int])
exceptions_stats = defaultdict(int)

def filter_results(jobs):
    return jobs[    ((jobs['title'].str.lower().str.contains('software')) | (jobs['title'].str.lower().str.contains('cloud')))
                &   ((jobs['title'].str.lower().str.contains('engineer')) | (jobs['title'].str.lower().str.contains('engineering')) | (jobs['title'].str.lower().str.contains('developer')) | (jobs['title'].str.lower().str.contains('development')))
                &   ((jobs['title'].str.lower().str.contains('intern')) | (jobs['title'].str.lower().str.contains('internship')))]


def scrape_city(city, country, query, results, no_indeed):
    print(f"Scraping in {city}, {country} with query: {query}")
    try:
        if no_indeed:
            jobs = scrape_jobs(
                site_name=["linkedin"],
                search_term=query,
                location=city,
                results_wanted=results,
            )
        else:
            jobs = scrape_jobs(
                site_name=["linkedin"], #, "indeed"], # Temporary not available
                search_term=query,
                location=city,
                results_wanted=results,
                country_indeed=country,
            )
        
        print(f"Number of results: {len(jobs)}")

        if jobs.empty:
            return jobs

        jobs.to_csv(f'../debug/{city}-{query}.txt', index=False) # DEBUG

        filtered_jobs = filter_results(jobs)
        print(f"Number of results remaining after filtering: {len(filtered_jobs)}")

        # if query has empty locations (always with linkedin), replace them with the city
        filtered_jobs_copy = filtered_jobs.copy() 
        filtered_jobs_copy.loc[filtered_jobs_copy['location'] == '', 'location'] = city + ', ' + country
        filtered_jobs = filtered_jobs_copy

        # stats
        if len(query_stats[query]) == 0:
            query_stats[query].append([len(jobs)])
            query_stats[query].append([len(filtered_jobs)])
        else:
            query_stats[query][0].append(len(jobs))
            query_stats[query][1].append(len(filtered_jobs))

        return filtered_jobs
    
    except Exception as e:
        logger.exception(e)
        exceptions_stats[(city, query, type(e).__name__)] += 1
        print(f"Error while scraping {city}, {country}: {type(e).__name__}: {str(e)}")
        print(f"Failed to scrape {city}, {country}, {query}")

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
                    
                    if company and title and location and job_url:
                        written_lines += 1
                        file.write(f'{company} | {title} | {location} | {job_url}\n')
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


def scrape_cities_file(filename, no_indeed=False):
    rows = pd.DataFrame()
    with open(filename, 'r') as file:
        for line in file:
            country, city = line.strip().split(' | ')
            for query, results in QUERIES_RESULTS.items():
                df = scrape_city(city, country, query, results, no_indeed)
                rows = pd.concat([rows, df], axis=0)
    return rows

def scrape_cities():
    all_rows = pd.DataFrame()

    rows1 = scrape_cities_file(CITIES)
    rows2 = scrape_cities_file(CITIES_NO_INDEED, no_indeed=True)

    all_rows = pd.concat([rows1, rows2], axis=0)

    print_stats()
    write_results(all_rows)