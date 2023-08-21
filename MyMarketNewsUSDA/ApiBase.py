from typing import Any

import requests
from requests.auth import HTTPBasicAuth

from MyMarketNewsUSDA.ApiKey import ApiKey
from constants import API_BASE_URL


class ApiBase(ApiKey):
    """
    Base class for all API methods
    """
    def __init__(self, api_key: str = None):
        super().__init__(api_key)

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
        _url = API_BASE_URL + slug_id
        if begin_date is not None:
            _url += f"?q=report_begin_date={begin_date}"
        if end_date is not None:
            _url += f"&report_end_date={end_date}"
        if key is not None:
            _url += f"&key={key}"
        return _url

    def get_data(self, _url: str) -> Any:
        """
        Gets the data from the API call
        :param _url:
        :return:
        """
        _response = requests.get(_url, auth=HTTPBasicAuth(self.api_key, ''))
        if _response.status_code == 200:
            return _response.json()
        else:
            _response.raise_for_status()
