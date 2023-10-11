import configparser
import pandas as pd

config = configparser.ConfigParser()
config.read('../config.ini')

GITHUB_REPO = config.get('RESOURCES', 'GITHUB_REPO', fallback="")
CONTRIBUTE_LINES_FILE = config.get('RESOURCES', 'CONTRIBUTE_LINES_FILE', fallback="contribute/contribute_lines.txt")
SCRAPED_LINES_FILE = config.get('RESOURCES', 'SCRAPED_LINES_FILE', fallback="output/scraped_lines.txt")
TABLE_FILE = config.get('RESOURCES', 'TABLE_FILE', fallback="output/table.md")
COMPANIES = config.get('RESOURCES', 'COMPANIES', fallback="static/companies.txt")

company_list = []

with open(COMPANIES, 'r') as file:
    for company in file:
        company_list.append(company.lower().strip())


def render_table(data):
    df = pd.DataFrame(data)
    df = df.drop_duplicates(subset=['URL'])
    df['CustomOrder'] = df['Company'].apply(lambda x: company_list.index(x.split(" ")[0].lower()) if x.split(" ")[0].lower() in company_list else None)
    df = df.sort_values(by='CustomOrder')
    df = df.drop(columns=['CustomOrder'])
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
                    # print(f"Parsing line: {company} | {job_title} | {place} | {url}") # Debug
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

render_lines()