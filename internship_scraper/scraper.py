import asyncio

from jobpilot.scrapers import LinkedInScraper, ScraperInput

from internship_scraper.constants import (
    COMPANIES,
    EUROPEAN_AREA,
    EUROPEAN_CITIES,
    EUROPEAN_COUNTRIES,
)
from internship_scraper.utils import dump_results


async def find_internships(job_categories: list[str], job_titles: list[str], job_types: list[str]) -> None:  # noqa: C901
    scraper = LinkedInScraper()

    keywords: list[str] = []
    extra_keywords: list[str] = []

    for category in job_categories:
        new_keyword = f"{category} {job_titles[0]} {job_types[0]}"
        extra_keywords += [f"{company} {new_keyword}" for company in COMPANIES]

        for job_type in job_types:
            new_keyword = f"{category} {job_type}"
            keywords.append(new_keyword)
            # extra_keywords += [f"{company} {new_keyword}" for company in COMPANIES]

        for title in job_titles:
            for job_type in job_types:
                new_keyword = f"{category} {title} {job_type}"
                keywords.append(new_keyword)
                # extra_keywords += [f"{company} {new_keyword}" for company in COMPANIES]

    for keyword in extra_keywords:
        try:
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
        except Exception as e:
            print(f"An error occurred during the scraping phase: {e}, skipping...") # or maybe I can find a way to keep internet results
            continue

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
