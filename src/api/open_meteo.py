from collections.abc import Callable
from datetime import date
from typing import Any
import time

import httpx

from src.config import LocationConfig

RETRYABLE_STATUS_CODES = {
    429,
    500,
    502,
    503,
    504,
}


class OpenMeteoClient:
    def __init__(
        self,
        base_url: str,
        timeout: float = 30.0,
        max_retries: int = 3,
        http_client: httpx.Client | None = None,
        sleep_func: Callable[[float], None] | None = None,
    ) -> None:
        self.base_url = base_url
        self.timeout = timeout
        self.max_retries = max_retries
        self.http_client = http_client
        self.sleep_func = sleep_func or time.sleep

    def _get_retry_delay(self, attempts: int) -> float:
        return 2 ** (attempts - 1)

    def _sleep_before_retry(self, attempts: int) -> None:
        delay = self._get_retry_delay(attempts)
        self.sleep_func(delay)

    def _get(
        self,
        params: dict[str, object],
    ) -> httpx.Response:
        attempts = 0

        while True:
            attempts += 1

            try:
                if self.http_client is not None:
                    response = self.http_client.get(
                        self.base_url,
                        params=params,
                    )
                else:
                    with httpx.Client(timeout=self.timeout) as client:
                        response = client.get(
                            self.base_url,
                            params=params,
                        )

            except (httpx.TimeoutException, httpx.ConnectError):
                if attempts > self.max_retries:
                    raise

                self._sleep_before_retry(attempts)
                continue

            if response.status_code not in RETRYABLE_STATUS_CODES:
                return response

            if attempts > self.max_retries:
                return response

            self._sleep_before_retry(attempts)

    def fetch_air_quality(
        self,
        location: LocationConfig,
        start_date: date,
        end_date: date,
        variables: tuple[str, ...],
    ) -> dict[str, Any]:
        params = {
            "latitude": location.latitude,
            "longitude": location.longitude,
            "hourly": ",".join(variables),
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "timezone": location.timezone,
        }

        response = self._get(params)
        response.raise_for_status()

        return response.json()