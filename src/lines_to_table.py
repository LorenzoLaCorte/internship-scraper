import configparser
import pandas as pd

config = configparser.ConfigParser()
config.read('../config.ini')

GITHUB_REPO = config.get('RESOURCES', 'GITHUB_REPO', fallback="")
CONTRIBUTE_LINES_FILE = config.get('RESOURCES', 'CONTRIBUTE_LINES_FILE', fallback="contribute/contribute_lines.txt")
SCRAPED_LINES_FILE = config.get('RESOURCES', 'SCRAPED_LINES_FILE', fallback="output/scraped_lines.txt")
TABLE_FILE = config.get('RESOURCES', 'TABLE_FILE', fallback="output/table.md")


def render_table(data):
    df = pd.DataFrame(data)
    df = df.drop_duplicates(subset=['URL'])
    df.to_markdown(TABLE_FILE, index=False)
    print("DataFrame exported to Table.md successfully.")


def render_file(filename):
    data = []
    try:
        with open(filename, "r") as file:
            for line in file:
                parts = line.strip().split(' | ')
                if len(parts) == 4:
                    company, job_title, place, url = parts
                    print(f"Parsing line: {company} | {job_title} | {place} | {url}")
                    data.append({'Company': company, 'Job Title': job_title, 'Place': place, 'URL': url})
                else:
                    print("Invalid line format:", line)
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return data


def render_lines():
    contribute_lines = render_file(CONTRIBUTE_LINES_FILE)
    scraped_lines = render_file(SCRAPED_LINES_FILE)
    render_table(contribute_lines+scraped_lines)