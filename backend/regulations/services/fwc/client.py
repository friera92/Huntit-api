from dataclasses import dataclass
from datetime import datetime, timezone

import requests

from .sources import FWCSource, get_source


@dataclass
class FWCFetchResult:
    source: FWCSource
    html: str
    retrieved_at: datetime


class FWCClient:
    def __init__(self, timeout=30):
        self.timeout = timeout

        self.headers = {
            "User-Agent": "HuntIt/1.0"
        }

    def fetch(self, source_key):
        source = get_source(source_key)

        response = requests.get(
            source.url,
            timeout=self.timeout,
            headers=self.headers,
        )

        response.raise_for_status()

        return FWCFetchResult(
            source=source,
            html=response.text,
            retrieved_at=datetime.now(
                timezone.utc
            ),
        )