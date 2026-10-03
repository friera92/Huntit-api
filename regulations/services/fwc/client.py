import requests


BASE_URL = "https://myfwc.com"

SEASON_DATES_URL = f"{BASE_URL}/hunting/season-dates/"


class FWCClient:
    def __init__(self, timeout=30):
        self.timeout = timeout

    def get_season_dates_page(self):
        response = requests.get(
            SEASON_DATES_URL,
            timeout=self.timeout,
            headers={
                "User-Agent": "HuntIt/1.0"
            },
        )

        response.raise_for_status()

        return response.text