import configparser
import pandas as pd

config = configparser.ConfigParser()
config.read('../config.ini')

GITHUB_REPO = config.get('SETTINGS', 'GITHUB_REPO')
LINES_FILE = config.get('SETTINGS', 'LINES_FILE')
TABLE_FILE = config.get('SETTINGS', 'TABLE_FILE')


def render_table(data):
    df = pd.DataFrame(data)
    df = df.drop_duplicates(subset=['URL'])
    df.to_markdown(TABLE_FILE, index=False)
    print("DataFrame exported to Table.md successfully.")


def render_lines():
    data = []

    try:
        with open(LINES_FILE, "r") as file:
            for line in file:
                parts = line.strip().split(' | ')
                if len(parts) == 4:
                    company, job_title, place, url = parts
                    print(f"Parsing line: {company} | {job_title} | {place} | {url}\n")
                    data.append({'Company': company, 'Job Title': job_title, 'Place': place, 'URL': url})
                else:
                    print("Invalid line format:", line)
        
        render_table(data)
    
    except FileNotFoundError:
        print(f"File '{LINES_FILE}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")