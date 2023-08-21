""" 
Author: Jacob Dallas

Anyone who says bureaucracy moves slow has never had to use the MMN API, they change something every 
week that breaks this package. 
"""
import datetime
import pandas as pd

from constants import API_BASE_URL
from MyMarketNewsUSDA.ApiBase import ApiBase


class MyMarketNews(ApiBase):

    def __init__(self, api_key: str = None):
        super().__init__(api_key)
        self._current_reports = None
        self._time_series_columns = ["report_date", "published_date"]

    def slug_check(self, slug_id: str) -> bool:
        """
        returns a string detailing if the report, based on the slug id the user wants to fetch, exists. 

        :param slug_id: The id of the report being fetched
        :return: 
        """

        if not isinstance(slug_id, str):
            raise TypeError(f"slug_id must be a string")

        _url: str = API_BASE_URL + slug_id
        if self.get_data(_url) is None:
            return False
        return True

    def date_check(self, slug_id: str, desired_date: datetime.date, refresh_reports: bool = False,
                   search_type: str = "before") -> bool:
        """
        returns if the desired date exists or not for the report being fetched

        :param search_type: The type of search to be performed, can be "exact", "before", or "after"
        :param refresh_reports: If True, the reports will be refreshed before checking the date
        :param slug_id: The ID of the report being fetched
        :param desired_date: The date of the report being fetched

        :return: whether or not the date exists for the report
        """
        if (not isinstance(slug_id, str)) or (not isinstance(desired_date, datetime.date)):
            raise TypeError(f"Make sure both {slug_id} is of type string and {desired_date} is of type datetime.date")

        if self._current_reports is None or refresh_reports:
            _data = self.get_current_reports()
        else:
            _data = self._current_reports

        # check if the slug_id is valid
        if slug_id not in _data["slug_id"].values:
            return False
        _data_point = _data[_data["slug_id"] == slug_id]
        if search_type == "exact":
            _data_point = _data_point[_data_point["report_date"] == desired_date]
        elif search_type == "before":
            _data_point = _data_point[_data_point["report_date"] >= desired_date]
        elif search_type == "after":
            _data_point = _data_point[_data_point["report_date"] <= desired_date]

        return len(_data_point) > 0

    def get_report_info(self, slud_id: str, column_names: list = None) -> dict:
        """
        return a description of a given report 
        """

        if not isinstance(slud_id, str):
            raise TypeError(f"slug_id must be a string")

        if self._current_reports is None:
            self.get_current_reports()

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

    def get_current_reports(self) -> pd.DataFrame:
        """
        :return: returns every current report as a dataframe
        """
        data = self.get_data(API_BASE_URL)
        self._current_reports = pd.DataFrame(data)

        # convert the time series columns to a datetime objects
        for key in self._time_series_columns:
            self._current_reports[key] = pd.to_datetime(self._current_reports[key])

        return self._current_reports

    def single_date(self, slug_id: str, begin_date, key):
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
    reports = x.get_current_reports()
    print(reports['market_types'])