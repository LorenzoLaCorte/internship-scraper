from importlib.metadata import version

import jobpilot

from internship_scraper.utils import setup_output

__version__ = version("internship-scraper")

jobpilot.enable_logging()

setup_output()
