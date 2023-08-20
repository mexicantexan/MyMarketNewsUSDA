""" 
Author: Noremax59

Anyone who says bureaucracy moves slow has never had to use the MMN API, they change something every 
week that breaks this package. 
"""
from typing import Union

import requests
from requests.auth import HTTPBasicAuth
from APIKey import API_Key


class MyMarketNews(API_Key):

    def __init__(self, api_key):
        super().__init__(api_key)

    def slug_check(self, slug_id) -> str:
        """
        returns a string detailing if the report, based on the slug id the user wants to fetch, exists. 

        :param slug_id: The id of the report being fetched
        :return: 
        """

        if not isinstance(slug_id, str):
            raise TypeError(f"slug_id must be a string")

        _url: str = "https://marsapi.ams.usda.gov/services/v1.2/reports/"
        _url += slug_id

        _response = requests.get(_url, auth=HTTPBasicAuth(username=self.api_key, password="none"))
        _key_list = list(_response.json().keys())

        if _key_list[1] == "message":
            return f"A report for {slug_id} does not exist"

        elif _key_list[1] == "result":
            return f"A report for {slug_id} does exist"

        else:
            return f"You entered an invalid slug id: {slug_id}"

    def date_check(self, slug_id, date_checker) -> Union[str, list]:
        """
        returns either the most recent report_begin_date of the slug id provided
        or can provide of full list of report_begin_date's of the slug id provided

        :param slug_id: The ID of the report being fetched

        :return: a list that contains either the date of the most recent file or 
                 the dates of every report. If "recent" or "all" is not input
                 by the user a message that these two arguments have to be used is
                 sent 

        I've figure out how to check is the date_checker is correct but I need to implement a check for the slug_id
        which could be similar to slug_check.
        """

        if not isinstance((slug_id or date_checker), str):
            raise TypeError(f"Make sure both {slug_id} and {date_checker} are both strings")

        _url = "https://marsapi.ams.usda.gov/services/v1.2/reports/"
        _url += slug_id

        _response = requests.get(_url, auth=HTTPBasicAuth(username=self.api_key, password="none"))
        _data = _response.json()

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

    def key_check(self, slug_id) -> list:
        """
        :param slug_id: slug_id should be in the form of a string
        :return: a list of the keys that can be used to access data 
        """
        if not isinstance(slug_id, str):
            raise TypeError(f"Make sure {slug_id} is a string")

        _url = "https://marsapi.ams.usda.gov/services/v1.2/reports/"
        _url += slug_id
        _response = requests.get(_url, auth=HTTPBasicAuth(self.api_key, password="none"))
        _data = _response.json()

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

    def description(self, slud_id):
        """
        return a description of a given report 
        """

        if not isinstance(slud_id, str):
            raise TypeError(f"slug_id must be a string")

    def current_reports(self, txt=None) -> list:
        """
        Add functionality that will allow this data to be printed to a writable to a .txt file
        :return: returns the slug_id and published date of every report 
        """
        _url = "https://marsapi.ams.usda.gov/services/v1.2/reports/"
        response = requests.get(_url, auth=HTTPBasicAuth(username=self.api_key, password="none"))
        data = response.json()

        _current_reports = []

        for i in range(len(list(data))):
            _current_reports.append(data[i]["slug_id"] + " " + data[i]["published_date"])

        return _current_reports

    def single_date(self, slug_id, begin_date, key):
        """
        Function can be called to get a single data point from a single report

        :param slug_id: The ID of the report being fetched
        :param begin_date: the report date that you want
        :param key:
        :return:
        """
        URL = "https://marsapi.ams.usda.gov/services/v1.2/reports/" + slug_id + "?q=report_begin_date=" + begin_date
        response = requests.get(URL, auth=HTTPBasicAuth(username=self.api_key, password="none"))
        data = response.json()

        x = data["results"]

        for i in range(len(x)):
            print(x[i][key])

    def time_series(self, slug_id):
        """
        need to convert the data into a df that can split the data relative to the commodity
        don't know if I can make it generalized or if I need to make it specific to the report
        """

        URL = "https://marsapi.ams.usda.gov/services/v1.2/reports/" + slug_id
        response = requests.get(URL, auth=HTTPBasicAuth(self.api_key, "none"))
        data = response.json()

        Butter = []
        Date_Butter = []
        Cheese = []
        Date_Cheese = []

        x = data["results"]

        for i in range(len(x)):
            if x[i]["commodity"] == "Butter":
                Butter.append(x[i]["holdings_current_lbs"])
                Date_Butter.append(x[i]["published_date"])
            else:
                Cheese.append(x[i]["holdings_current_lbs"])
                Date_Cheese.append(x[i]["published_date"])

        print(Butter)
