import csv

from internship_scraper.constants import (
    RESULTS_FILE,
    EUROPEAN_CITIES,
    EUROPEAN_COUNTRIES
)
from internship_scraper.utils import dump_filtered_results


def filter_internships(job_categories: list[str], job_titles: list[str], job_types: list[str]) -> None:
    with RESULTS_FILE.open("r") as results_file:
        csv_reader = csv.DictReader(results_file, delimiter="|")
        filtered_lines: list[str] = []
        for line in csv_reader:
            try:
                title = line["title"]
                city = line["location"].split(", ")[0]
                country = line["location"].split(", ")[-1]
            except:
                print("Error parsing the line")
                continue
            if (
                (any(category in title for category in job_categories))
                and (any(title in title for title in job_titles))
                and (any(job_type in title for job_type in job_types))
                and ((any(city == job_city for job_city in EUROPEAN_CITIES))
                    or (any(country == job_country for job_country in EUROPEAN_COUNTRIES)))
            ):
                filtered_lines.append("|".join(line.values()))
    dump_filtered_results(filtered_lines)