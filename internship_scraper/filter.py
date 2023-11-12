import csv

from internship_scraper.constants import (
    JOB_CATEGORIES,
    JOB_TITLES,
    JOB_TYPES,
    RESULTS_FILE,
)
from internship_scraper.utils import dump_filtered_results


def filter_internships() -> None:
    with RESULTS_FILE.open("r") as results_file:
        csv_reader = csv.DictReader(results_file, delimiter="|")
        filtered_lines: list[str] = []
        for line in csv_reader:
            title = line["title"]
            if (
                (any(category in title for category in JOB_CATEGORIES))
                and (any(title in title for title in JOB_TITLES))
                and (any(job_type in title for job_type in JOB_TYPES))
            ):
                filtered_lines.append("|".join(line.values()))
    dump_filtered_results(filtered_lines)
