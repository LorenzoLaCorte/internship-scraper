from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent

OUTPUT_DIR = PROJECT_ROOT / "output"
RESULTS_FILE = OUTPUT_DIR / "results.csv"
FILTERED_RESULTS_FILE = OUTPUT_DIR / "filtered_results.csv"
TABLE_FILE = OUTPUT_DIR / "table.md"

RESULTS_HEADER = "company|title|location|link\n"

# TODO: the new strategy is filling these three lists from command line, in order for the github action to call it with different arguments
# TODO: change these to get an input from cmdline
# TODO: create 2 different github actions for intern and new grad
# TODO: eventually expand with github actions for research internships / master thesis, phd positions, junior positions

JOB_CATEGORIES = ["software"]
JOB_TITLES = ["engineer", "engineering", "developer"]
JOB_TYPES = ["intern", "internship"]

COMPANIES = [ 
    "amazon",
    "apple",
    "meta",
    "google",
    "microsoft",
    "netflix",
]

EUROPEAN_AREA = "european economic area"

EUROPEAN_COUNTRIES = [
    "albania",
    "andorra",
    "armenia",
    "austria",
    "azerbaijan",
    "belarus",
    "belgium",
    "bosnia",
    "bulgaria",
    "croatia",
    "cyprus",
    "czech republic",
    "denmark",
    "estonia",
    "finland",
    "france",
    "georgia",
    "germany",
    "greece",
    "hungary",
    "ireland",
    "italy",
    "kazakhstan",
    "kosovo",
    "latvia",
    "liechtenstein",
    "lithuania",
    "luxembourg",
    "malta",
    "moldova",
    "monaco",
    "montenegro",
    "netherlands",
    "macedonia",
    "norway",
    "poland",
    "portugal",
    "romania",
    "russian",
    "san marino",
    "serbia",
    "slovakia",
    "slovenia",
    "spain",
    "sweden",
    "switzerland",
    "turkey",
    "ukraine",
    "united kingdom",
    "uk",
    "vatican",
]

EUROPEAN_CITIES = [
    "aarhus",
    "amsterdam",
    "athens",
    "barcelona",
    "berlin",
    "brussels",
    "bucharest",
    "budapest",
    "copenhagen",
    "cork",
    "cracow",
    "delft",
    "dublin",
    "edinburgh",
    "frankfurt",
    "geneva",
    "gothenburg",
    "hamburg",
    "hannover",
    "helsinki",
    "istanbul",
    "kiev",
    "lisbon",
    "london",
    "luxembourg",
    "lyon",
    "madrid",
    "malmo",
    "manchester",
    "milan",
    "moscow",
    "munich",
    "oslo",
    "paris",
    "prague",
    "riga",
    "rome",
    "rotterdam",
    "sofia",
    "stockholm",
    "tallinn",
    "trondheim",
    "valencia",
    "vienna",
    "warsaw",
    "zurich",
]