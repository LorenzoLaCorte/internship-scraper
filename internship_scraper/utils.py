from __future__ import annotations

from typing import TYPE_CHECKING

from internship_scraper.constants import OUTPUT_DIR, RESULTS_FILE

if TYPE_CHECKING:
    from jobpilot.models import Job


def setup_output() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    if not RESULTS_FILE.exists():
        with RESULTS_FILE.open("w") as f:
            f.write("company | title | location | link\n")


def dump_results(jobs: list[Job]) -> None:
    with RESULTS_FILE.open("r+") as f:
        content = f.read()

        for job in jobs:
            line = f"{job.company.name} | {job.title} | {job.location} | {job.link}\n"
            if line not in content:
                f.write(line)
