import requests
import json
from datetime import datetime


def scrap_data(country: str = "Malaysia") -> dict:
    url = f"https://disease.sh/v3/covid-19/countries/{country}"
    response = requests.get(url, timeout=10, verify=False)

    if response.status_code != 200:
        raise Exception(f"Error:: {response.status_code}")

    raw = response.json()

    body = {
        "country": raw["country"],
        "today_cases": int(raw["todayCases"]),
        "today_deaths": int(raw["todayDeaths"]),
        "total_cases": int(raw["cases"]),
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    return body


# -------------------
# MAIN PROGRAM (TEST)
# -------------------
if __name__ == "__main__":
    data = scrap_data("Malaysia")
    print(json.dumps(data, indent=2))