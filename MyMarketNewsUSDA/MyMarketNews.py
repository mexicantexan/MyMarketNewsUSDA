""" 
Author: Jacob Dallas

Anyone who says bureaucracy moves slow has never had to use the MMN API, they change something every 
week that breaks this package. 
"""
from typing import Union

import requests
import pandas as pd
from requests.auth import HTTPBasicAuth
from APIKey import ApiKey
from constants import API_BASE_URL


class MyMarketNews(ApiKey):

    def __init__(self, api_key: str = None):
        super().__init__(api_key)
        self._current_reports = None

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

    def get_data(self, _url: str) -> Union[dict, None]:
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

    def slug_check(self, slug_id: str) -> str:
        """
        returns a string detailing if the report, based on the slug id the user wants to fetch, exists. 

        :param slug_id: The id of the report being fetched
        :return: 
        """

        if not isinstance(slug_id, str):
            raise TypeError(f"slug_id must be a string")

        _url: str = API_BASE_URL + slug_id

        _response = requests.get(_url, auth=HTTPBasicAuth(username=self.api_key, password="none"))
        _key_list = list(_response.json().keys())

        if _key_list[1] == "message":
            return f"A report for {slug_id} does not exist"

        elif _key_list[1] == "result":
            return f"A report for {slug_id} does exist"

        else:
            return f"You entered an invalid slug id: {slug_id}"

    def date_check(self, slug_id: str, date_checker: str) -> Union[str, list]:
        """
        returns either the most recent report_begin_date of the slug id provided
        or can provide of full list of report_begin_date's of the slug id provided

        :param slug_id: The ID of the report being fetched
        :param date_checker: either "recent" or "all"

        :return: a list that contains either the date of the most recent file or 
                 the dates of every report. If "recent" or "all" is not input
                 by the user a message that these two arguments have to be used is
                 sent 

        I've figure out how to check is the date_checker is correct but I need to implement a check for the slug_id
        which could be similar to slug_check.
        """

        if not isinstance((slug_id or date_checker), str):
            raise TypeError(f"Make sure both {slug_id} and {date_checker} are both strings")

        _url = API_BASE_URL + slug_id

        _data = self.get_data(_url)

        date_holder = []

        if date_checker == "recent":
            date_holder.append(_data["results"][0]["report_begin_date"])
            return date_holder

        elif date_checker == "all":

            alldates = _data["results"]

            for i in range(len(alldates)):
                if alldates[i]["report_begin_date"] in date_holder:
                    pass
                else:
                    date_holder.append(alldates[i]["report_begin_date"])

            return date_holder

        else:
            return f"enter either: 'recent' or 'all'"

    def key_check(self, slug_id: str) -> list:
        """
        :param slug_id: The ID of the report being fetched
        :return: a list of all the keys in the data set
        """
        if not isinstance(slug_id, str):
            raise TypeError(f"Make sure {slug_id} is a string")

        _url = API_BASE_URL + slug_id
        _data = self.get_data(_url)

        _data = _data["results"]
        _key_holder = []

        if isinstance(_data, dict):
            for i in range(len(list(_data))):
                _key_holder.append(_data[i].keys())
                return _key_holder

        else:
            for i in range(len(_data)):
                _key_holder.append(_data[i].keys())
                return _key_holder

    def get_report_info(self, slud_id: str, column_names: list = None) -> dict:
        """
        return a description of a given report 
        """

        if not isinstance(slud_id, str):
            raise TypeError(f"slug_id must be a string")

        if self._current_reports is None:
            self.current_reports()

        # filter the dataframe to only include the report we want based on the slug_id
        _report = self._current_reports[self._current_reports["slug_id"] == slud_id]
        if column_names is None:
            return _report.to_dict()
        output = {}
        for key in column_names:
            if key not in _report.columns:
                raise ValueError(f"{key} is not a valid column name of names: {list(_report.columns)}")
            output[key] = _report[key].values[0]
        return output

    def get_report_title(self, slug_id: str) -> str:
        """
        return the title of a given report, if the slug id is not valid, this will return None

        :param slug_id: The ID of the report being fetched
        :return the title of the report
        """
        return self.get_report_info(slug_id, ["title"]).get("title")

    def get_report_slug_name(self, slug_id: str) -> str:
        """
        return the slug name of a given report, if the slug id is not valid, this will return None

        :param slug_id: The ID of the report being fetched
        :return the slug name of the report
        """
        return self.get_report_info(slug_id, ["slug_name"]).get("slug_name")

    def get_report_slug_id(self, slug_id: str) -> str:
        """
        return the slug id of a given report, if the slug id is not valid, this will return None

        :param slug_id: The ID of the report being fetched
        :return the slug id of the report
        """
        return self.get_report_info(slug_id, ["slug_id"]).get("slug_id", None)

    def current_reports(self) -> pd.DataFrame:
        """
        :return: returns every current report
        """
        _url = API_BASE_URL
        data = self.get_data(_url)
        print(data)
        self._current_reports = pd.DataFrame(data)

        return self._current_reports

    def single_date(self, slug_id, begin_date, key):
        """
        Function can be called to get a single data point from a single report

        :param slug_id: The ID of the report being fetched
        :param begin_date: the report date that you want
        :param key:
        :return:
        """
        _url = API_BASE_URL + slug_id + "?q=report_begin_date=" + begin_date
        _data = self.get_data(_url)

        x = _data["results"]

        for i in range(len(x)):
            print(x[i][key])

    def time_series(self, slug_id):
        """
        need to convert the data into a df that can split the data relative to the commodity
        don't know if I can make it generalized or if I need to make it specific to the report
        """

        _url = API_BASE_URL + slug_id
        _data = self.get_data(_url)
        print(f"Data for {slug_id} has been fetched")
        print(f"{_data=}")
        # Butter = []
        # Date_Butter = []
        # Cheese = []
        # Date_Cheese = []
        #
        # x = data["results"]
        #
        # for i in range(len(x)):
        #     if x[i]["commodity"] == "Butter":
        #         Butter.append(x[i]["holdings_current_lbs"])
        #         Date_Butter.append(x[i]["published_date"])
        #     else:
        #         Cheese.append(x[i]["holdings_current_lbs"])
        #         Date_Cheese.append(x[i]["published_date"])
        #
        # print(Butter)


if __name__ == "__main__":
    x = MyMarketNews("MY_API_KEY")
    x.current_reports()
