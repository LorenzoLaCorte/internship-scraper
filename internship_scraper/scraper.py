from jobpilot.scrapers import LinkedInScraper, ScraperInput

from internship_scraper.constants import (
    COMPANIES,
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
    extra_keywords: list[str] = []

    for category in JOB_CATEGORIES:
        for job_type in JOB_TYPES:
            new_keyword = f"{category} {job_type}"
            keywords.append(new_keyword)
            extra_keywords += [f"{company} {new_keyword}" for company in COMPANIES]

        for title in JOB_TITLES:
            for job_type in JOB_TYPES:
                new_keyword = f"{category} {title} {job_type}"
                keywords.append(new_keyword)
                extra_keywords += [f"{company} {new_keyword}" for company in COMPANIES]

    for location in EUROPEAN_COUNTRIES:
        for keyword in extra_keywords:
            dump_results(
                await scraper.scrape(
                    ScraperInput(keywords=keyword, location=location, limit=50),
                    max_retries=20,
                    retry_delay=2,
                    concurrent=False,
                ),
            )
        for keyword in keywords:
            dump_results(
                await scraper.scrape(
                    ScraperInput(keywords=keyword, location=location, limit=1000),
                    max_retries=20,
                    retry_delay=3,
                ),
            )

    for location in EUROPEAN_CITIES:
        for keyword in keywords:
            dump_results(
                await scraper.scrape(
                    ScraperInput(keywords=keyword, location=location, limit=200),
                    max_retries=20,
                    retry_delay=3,
                ),
            )
