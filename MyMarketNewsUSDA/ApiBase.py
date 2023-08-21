from typing import Any

import requests
from requests.auth import HTTPBasicAuth

from MyMarketNewsUSDA.ApiKey import ApiKey
from constants import REPORT_API_BASE_URL


class ApiBase(ApiKey):
    """
    Base class for all API methods
    """
    def __init__(self, api_key: str = None, api_type: str = "report"):
        super().__init__(api_key)
        self.api_type = api_type

    @staticmethod
    def create_api_url(slug_id: str, begin_date: str = None, end_date: str = None, key: str = None) -> str:
        """
        Creates the URL for the API call

        :param slug_id: The ID of the report being fetched
        :param begin_date: The date of the report being fetched
        :param end_date: The date of the report being fetched
        :param key: The key of the report being fetched
        :return: The URL for the API call
        """
        _url = REPORT_API_BASE_URL + slug_id
        if begin_date is not None:
            _url += f"?q=report_begin_date={begin_date}"
        if end_date is not None:
            _url += f"&report_end_date={end_date}"
        if key is not None:
            _url += f"&key={key}"
        return _url

    def get_data(self, _url: str, payload: dict = None) -> Any:
        """
        Gets the data from the API call
        :param _url:
        :param payload: The payload for the Market API call
        :return:
        """
        if self.api_type == "report":
            _response = requests.get(_url, auth=HTTPBasicAuth(self.api_key, ''))
        elif self.api_type == "market":
            if payload is None:
                payload = {}
            _response = requests.post(_url, json=payload)
        else:
            raise NotImplementedError(f"api_type must be either 'report' or 'market', not {self.api_type}. "
                                      f"This type is not yet implemented")
        if _response.status_code == 200:
            return _response.json()
        else:
            _response.raise_for_status()
