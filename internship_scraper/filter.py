import csv

from internship_scraper.constants import (
    JOB_CATEGORIES,
    JOB_TITLES,
    JOB_TYPES,
    RESULTS_FILE,
    EUROPEAN_CITIES,
    EUROPEAN_COUNTRIES
)
from internship_scraper.utils import dump_filtered_results


def filter_internships() -> None:
    with RESULTS_FILE.open("r") as results_file:
        csv_reader = csv.DictReader(results_file, delimiter="|")
        filtered_lines: list[str] = []
        for line in csv_reader:
            title = line["title"]
            city = line["location"].split(", ")[0]
            country = line["location"].split(", ")[-1]
            # print(city, country, (any(city == job_city for job_city in EUROPEAN_CITIES)) or (any(country == job_country for job_country in EUROPEAN_COUNTRIES)))
            if (
                (any(category in title for category in JOB_CATEGORIES))
                and (any(title in title for title in JOB_TITLES))
                and (any(job_type in title for job_type in JOB_TYPES))
                and ((any(city == job_city for job_city in EUROPEAN_CITIES))
                    or (any(country == job_country for job_country in EUROPEAN_COUNTRIES)))
            ):
                filtered_lines.append("|".join(line.values()))
    dump_filtered_results(filtered_lines)