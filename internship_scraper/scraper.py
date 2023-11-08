from jobpilot.scrapers import LinkedInScraper, ScraperInput

from internship_scraper.constants import (
    EUROPEAN_CITIES,
    EUROPEAN_COUNTRIES,
    JOB_CATEGORIES,
    JOB_TITLES,
    JOB_TYPES,
)
from internship_scraper.utils import dump_results


async def find_internships() -> None:
    scraper = LinkedInScraper()

    keywords: list[str] = []

    for category in JOB_CATEGORIES:
        keywords += [f"{category} {job_type}" for job_type in JOB_TYPES]

        for title in JOB_TITLES:
            keywords.append(f"{category} {title}")
            keywords += [f"{category} {title} {job_type}" for job_type in JOB_TYPES]

    for title in JOB_TITLES:
        keywords += [f"{title} {job_type}" for job_type in JOB_TYPES]

    for location in EUROPEAN_CITIES:
        for keyword in keywords:
            dump_results(
                await scraper.scrape(
                    ScraperInput(keywords=keyword, location=location, limit=200),
                ),
            )

    for location in EUROPEAN_COUNTRIES:
        for keyword in keywords:
            dump_results(
                await scraper.scrape(
                    ScraperInput(keywords=keyword, location=location, limit=1000),
                ),
            )
