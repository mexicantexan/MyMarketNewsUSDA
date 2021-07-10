"""
Made by @Noremax59

grabs reports from USDA website and return the results

Some issues to fix and features that I need to add:
    def dateCheck():
        when the "all dates" argument is passed in to the function the number of individual dates returned is proportional
        to the dicts of the slug_id, need to fix it such that it only returns a date once.

    def timeSeries():
        need to add the ability to splice the data relative to the commodity that is given back automatically.
"""

import requests
from requests.auth import HTTPBasicAuth
import json

class MyMarketNews():

    def __init__(self, API_Key):
        self.API_Key = API_Key

    def slugCheck(self, slug_id):
        """
        Checks to see if a report exists 

        :param slug_id: 
        :return:
        """

        URL = "https://marsapi.ams.usda.gov/services/v1.2/reports/" + slug_id
        API_Key = self.API_Key
        self.response = requests.get(URL, auth=HTTPBasicAuth(username= API_Key, password = "none"))
        key_list = list(self.response.json().keys())

        if key_list[0] == "message":
            result = "A report for " + str(slug_id) + " does not exist"
            return result 

        else:
            result = "A report for " + str( slug_id) + " does exist"
            return result

    def dateCheck(self, slug_id, date_checker):
        """
        Returns either the most recent report_begin_date of the Slug ID provided
        or can provide of full list of report_begin_date's of the Slug ID provided
        :param slug_id:
        :param date_checker:
        :return:
        """
        URL = "https://marsapi.ams.usda.gov/services/v1.2/reports/" + slug_id
        response = requests.get(URL, auth=HTTPBasicAuth(API_Key, "none"))
        data = response.json()

        if date_checker == "recent":
            x = data["results"][0]["report_begin_date"]
            print(x)

        elif date_checker == "all dates":
            x = data["results"]
            for i in range(len(x)):
                print(x[i]["report_begin_date"])

        else:
            print('enter either: "recent" or "all dates"')

    def keyCheck(self, slug_id):
        """
        Returns the keys that can be used to extract data from the reports.
        :param slug_id:
        :return:
        """
        URL = "https://marsapi.ams.usda.gov/services/v1.2/reports/" + slug_id
        API_Key = self.API_Key
        response = requests.get(URL, auth=HTTPBasicAuth(API_Key, "none"))
        data = response.json()

        x = data["results"][2]

        if type(x) is dict:
            zipper = list(x.keys())
            for i in range(len(zipper)):
                print(zipper[i])

        else:
            zipper = list(x)
            for i in range(len(zipper)):
                print(zipper[i])


    def currentReports():
        """
        Doesn't work right now, should be able to call the most recent reports for the day

        :return:
        """
        URL = "https://marsapi.ams.usda.gov/services/public/listPublishedReports"
        response = requests.get(URL, auth=HTTPBasicAuth(API_Key, "none"))
        data = response.json()
        print(data)

    def singleDate(slug_id, begin_date, key):
        """
        Function can be called to get a single data point from a single report

        :param slug_id: The ID of the report being fetched
        :param begin_date: the report date that you want
        :param key:
        :return:
        """
        URL = "https://marsapi.ams.usda.gov/services/v1.2/reports/" + slug_id + "?q=report_begin_date=" + begin_date
        response = requests.get(URL, auth=HTTPBasicAuth(API_Key, "none"))
        data = response.json()

        x = data["results"]

        for i in range(len(x)):
            print(x[i][key])

    def timeSeries(slug_id):
        """
        need to convert the data into a df that can split the data relative to the commodity
        don't know if I can make it generalized or if I need to make it specific to the report
        """

        URL = "https://marsapi.ams.usda.gov/services/v1.2/reports/" + slug_id
        response = requests.get(URL, auth=HTTPBasicAuth(API_Key, "none"))
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
