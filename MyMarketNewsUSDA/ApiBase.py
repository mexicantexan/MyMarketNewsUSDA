import datetime
from typing import Any

import requests
from requests.auth import HTTPBasicAuth

from MyMarketNewsUSDA.ApiKey import ApiKey
from constants import REPORT_API_BASE_URL, MARKET_API_BASE_URL


class ApiBase(ApiKey):
    """
    Base class for all API methods
    """
    def __init__(self, api_key: str = None, api_type: str = "report"):
        super().__init__(api_key)
        self.api_type = api_type

    def create_api_url(self, **kwargs) -> str:
        """
        Creates the URL for the API call

        :param kwargs: The keyword arguments for the Market API call
            can be any of the following if api_type == "report":
                - slug_id
                - begin_date
                - end_date
                - key

            can be any of the following if api_type == "market":
                - commodity
                - region
                - class_
                - organic
                - begin_date
                - end_date

        :return: The URL for the API call
        """
        if self.api_type == "report":
            _url = REPORT_API_BASE_URL + kwargs.get('slug_id', '')
            if kwargs.get('begin_date') is not None:
                begin_date = kwargs.get('begin_date')
                if isinstance(begin_date, datetime.date):
                    begin_date = begin_date.strftime("%m/%d/%Y")
                _url += f"?q=report_begin_date={begin_date}"
            if kwargs.get('end_date') is not None:
                end_date = kwargs.get('end_date')
                if isinstance(end_date, (datetime.date, datetime.datetime)):
                    end_date = end_date.strftime("%m/%d/%Y")
                _url += f"&report_end_date={end_date}"
            if kwargs.get('key') is not None:
                _url += f"&key={kwargs.get('key')}"
        elif self.api_type == "market":
            # since this is a post, the variables are passed through the POST payload
            _url = MARKET_API_BASE_URL
        else:
            raise NotImplementedError(f"api_type must be either 'report' or 'market', not {self.api_type}. "
                                      f"This type is not yet implemented")
        return _url

    def set_api_type(self, api_type: str) -> None:
        """
        Sets the api_type of the ApiBase class
        :param api_type: The api_type to be set
        :return: None
        """
        self.api_type = api_type

    def get_api_type(self) -> str:
        """
        Gets the api_type of the ApiBase class
        :return: The api_type
        """
        return self.api_type

    @staticmethod
    def create_payload(**kwargs) -> dict:
        """
        Creates the payload for the Market API call
        :param kwargs: The keyword arguments for the Market API call
            can be any of the following:
                - commodity
                - region
                - class_
                - organic
                - begin_date
                - end_date
        :return: The payload for the Market API call
        """
        payload = {}
        if kwargs.get('commodity') is not None:
            payload['CLASS'] = kwargs.get('commodity')
        if kwargs.get('region') is not None:
            payload['REGN'] = kwargs.get('region')
        if kwargs.get('class_') is not None:
            payload['COMD'] = kwargs.get('class_')
        if kwargs.get('organic') is not None:
            payload['ORGC'] = kwargs.get('organic')
        if kwargs.get('begin_date') is not None:
            begin_date = kwargs.get('begin_date')
            if isinstance(begin_date, datetime.date):
                begin_date = begin_date.strftime("%m/%d/%Y")
            payload['DATE'] = [begin_date]
        if kwargs.get('end_date') is not None:
            end_date = kwargs.get('end_date')
            if isinstance(end_date, (datetime.date, datetime.datetime)):
                end_date = end_date.strftime("%m/%d/%Y")
            payload['DATE'].append(end_date)
        return payload

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
