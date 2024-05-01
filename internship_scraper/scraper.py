import asyncio

from jobpilot.scrapers import LinkedInScraper, ScraperInput

from internship_scraper.constants import (
    COMPANIES,
    EUROPEAN_AREA,
    EUROPEAN_CITIES,
    EUROPEAN_COUNTRIES,
    JOB_CATEGORIES,
    JOB_TITLES,
    JOB_TYPES,
)
from internship_scraper.utils import dump_results


async def find_internships() -> None:  # noqa: C901
    scraper = LinkedInScraper()

    keywords: list[str] = []
    extra_keywords: list[str] = []

    for category in JOB_CATEGORIES:
        new_keyword = f"{category} {JOB_TITLES[0]} {JOB_TYPES[0]}"
        extra_keywords += [f"{company} {new_keyword}" for company in COMPANIES]

        for job_type in JOB_TYPES:
            new_keyword = f"{category} {job_type}"
            keywords.append(new_keyword)
            # extra_keywords += [f"{company} {new_keyword}" for company in COMPANIES]

        for title in JOB_TITLES:
            for job_type in JOB_TYPES:
                new_keyword = f"{category} {title} {job_type}"
                keywords.append(new_keyword)
                # extra_keywords += [f"{company} {new_keyword}" for company in COMPANIES]

    for keyword in extra_keywords:
        results = await asyncio.gather(
            *[
                scraper.scrape(
                    ScraperInput(keywords=keyword, location=location, limit=50),
                    concurrent=False,
                    retry_delay=1,
                )
                for location in EUROPEAN_COUNTRIES
            ],
        )

        for result in results:
            dump_results(result)

        results = await asyncio.gather(
            *[
                scraper.scrape(
                    ScraperInput(keywords=keyword, location=location, limit=25),
                    concurrent=False,
                    retry_delay=1,
                )
                for location in EUROPEAN_CITIES
            ],
        )

        for result in results:
            dump_results(result)

        dump_results(
            await scraper.scrape(
                ScraperInput(keywords=keyword, location=EUROPEAN_AREA, limit=1000),
                max_retries=20,
                retry_delay=1,
            ),
        )

    for keyword in keywords:
        for location in EUROPEAN_COUNTRIES:
            dump_results(
                await scraper.scrape(
                    ScraperInput(keywords=keyword, location=location, limit=1000),
                    max_retries=20,
                    retry_delay=1,
                ),
            )
        for location in EUROPEAN_CITIES:
            dump_results(
                await scraper.scrape(
                    ScraperInput(keywords=keyword, location=location, limit=200),
                    max_retries=20,
                    retry_delay=1,
                ),
            )
        dump_results(
            await scraper.scrape(
                ScraperInput(keywords=keyword, location=EUROPEAN_AREA, limit=1000),
                max_retries=20,
                retry_delay=1,
            ),
        )
