from __future__ import annotations

from typing import TYPE_CHECKING

from internship_scraper.constants import (
    COMPANIES,
    FILTERED_RESULTS_FILE,
    OUTPUT_DIR,
    RESULTS_FILE,
    RESULTS_HEADER,
)
from internship_scraper.db import create_session, Job as DBJob

if TYPE_CHECKING:
    from pathlib import Path

    from jobpilot.models import Job


def setup_output() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    if not RESULTS_FILE.exists():
        with RESULTS_FILE.open("w") as f:
            f.write(RESULTS_HEADER)
    if not FILTERED_RESULTS_FILE.exists():
        with FILTERED_RESULTS_FILE.open("w") as f:
            f.write(RESULTS_HEADER)


def push_results(jobs: list[Job]) -> None:
    session = create_session()
    for job in jobs:
        db_job = session.query(DBJob).filter_by(link=job.link).first()
        if not db_job:
            new_db_job = DBJob(
                link=job.link,
                title=job.title,
                location=str(job.location),
                company=job.company.name,
                description=job.details.description if job.details else None,
                employment_type=str(job.details.employment_type) if job.details and job.details.employment_type else None,
                seniority_level=job.details.seniority_level if job.details else None,
                job_function=job.details.job_function if job.details else None,
                industries=job.details.industries if job.details else None,
            )
            session.add(new_db_job)
    session.commit()


def dump_results(jobs: list[Job]) -> None:
    push_results(jobs)
    with RESULTS_FILE.open("r+") as f:
        content = f.read()

        for job in jobs:
            line = (
                f"{job.company.name.replace('|', '')}|{job.title.replace('|', '')}|"
                f"{str(job.location).replace('|', '')}|{job.link.replace('|', '')}\n"
            )
            if line not in content and job.link not in content:
                f.write(line)


def dump_filtered_results(lines: list[str]) -> None:
    with FILTERED_RESULTS_FILE.open("r+") as f:
        content = f.read()

        for line in lines:
            if line not in content:
                f.write(f"{line}\n")


def csv_to_markdown_table(csv_file: Path, md_file: Path) -> None:
    header_lines: list[str] = []
    prior_job_lines: list[str] = []
    job_lines: list[str] = []

    with csv_file.open("r") as f:
        lines = f.read().splitlines()

        headers = lines[0]
        columns = len(headers.split("|"))
        header_lines.append(f"|{headers}|")
        header_lines.append(f"|{'|'.join(['---'] * columns)}|")
        if len(lines) > 1:
            for line in lines[1:]:
                if any([word in COMPANIES for word in line.split("|")[0].split(" ")]):
                    prior_job_lines += [f"|{line}|"]
                else:
                    job_lines += [f"|{line}|"]
        
        prior_job_lines.sort()
        job_lines.sort()

    with md_file.open("w") as f:
        f.write("\n".join(header_lines+prior_job_lines+job_lines))