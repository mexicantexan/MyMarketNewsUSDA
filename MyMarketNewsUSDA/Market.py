import datetime
from typing import Union

import pandas as pd
import requests

from MyMarketNewsUSDA.ApiBase import ApiBase
from constants import *


base_url = "https://mymarketnews.ams.usda.gov/get_external_api/result"

payload = {
    "MT": "/3/",
    "CLASS": "Fruit",
    "REGN": "National",
    "DATE": [
        "08/01/2023",
        "08/20/2023"
    ],
    "COMD": [
        "All"
    ],
    "ORGC": "No"
}

response = requests.post(base_url, json=payload)
if response.status_code == 200:
    print(response.json())
else:
    response.raise_for_status()


class Market(ApiBase):
    """
      This class is used to store the data from a single market and provide methods to manipulate that data
    """

    def __init__(self, **kwargs):
        super().__init__(api_type="market")
        self.data = None
        self.commodity = None
        self.region = None
        self.class_ = None
        self.organic = None
        self.begin_date = None
        self.end_date = None

        # set the attributes
        self.set_commodity(kwargs.get("commodity", None))
        self.set_region(kwargs.get("region", None))
        self.set_class(kwargs.get("class_", None))
        self.set_organic(kwargs.get("organic", None))
        self.set_begin_date(kwargs.get("begin_date", None))
        self.set_end_date(kwargs.get("end_date", None))

    def set_commodity(self, commodity: str) -> None:
        """
        Sets the commodity of the market, then gathers the data for that market
        :param commodity: The commodity to be set
        :return: None
        """
        commodity = str(commodity).upper()
        if commodity in FRUIT_COMMODITIES:
            self.commodity = commodity.capitalize()
            self.class_ = "Fruit"
        elif commodity in ONIONS_AND_POTATOES_COMMODITIES:
            self.commodity = commodity.capitalize()
            self.class_ = "Onions And Potatoes"
        elif commodity in VEGETABLES_COMMODITIES:
            self.commodity = commodity.capitalize()
            self.class_ = "Vegetables"
        elif commodity in HERBS_COMMODITIES:
            self.commodity = commodity.capitalize()
            self.class_ = "Herbs"
        elif commodity in ORNAMENTALS_COMMODITIES:
            self.commodity = commodity.capitalize()
            self.class_ = "Ornamentals"
        elif commodity in HEMP_COMMODITIES:
            self.commodity = commodity.capitalize()
            self.class_ = "Hemp"
        else:
            raise ValueError(f"commodity must be one of the following: {COMPOSITE_COMMODITIES}")

    def set_region(self, region: str) -> None:
        """
        Sets the region of the market, then gathers the data for that market
        :param region: The region to be set
        :return: None
        """
        if region not in COMMODITY_REGIONS:
            raise ValueError(f"region must be one of the following: {COMMODITY_REGIONS}")

        self.region = region

    def set_class(self, class_: str) -> None:
        """
        Sets the class of the market, then gathers the data for that market
        :param class_: The class to be set
        :return: None
        """
        class_ = str(class_).capitalize()
        if class_ not in COMMODITY_CLASSES:
            raise ValueError(f"class_ must be one of the following: {COMMODITY_CLASSES}")
        self.class_ = class_

    def set_organic(self, organic: Union[str, bool]) -> None:
        """
        Sets the organic of the market, then gathers the data for that market
        :param organic: The organic to be set
        :return: None
        """
        if isinstance(organic, bool):
            self.organic = "Yes" if organic else "No"
        elif isinstance(organic, str):
            organic = organic.capitalize()
            possible_organic_positives = ["Yes", "True", "Y", "T", "1", "All Organic"]
            possible_organic_negatives = ["No", "False", "N", "F", "0", "No Organic"]
            possible_organic_other = ["All"]
            if organic in possible_organic_positives:
                self.organic = "Yes"
            elif organic in possible_organic_negatives:
                self.organic = "No"
            elif organic in possible_organic_other:
                self.organic = "All"
            else:
                raise ValueError(
                    f"organic must be one of the following:"
                    f" {possible_organic_positives + possible_organic_negatives + possible_organic_other}")
        else:
            raise TypeError(f"organic must be of type str or bool, not {type(organic)}")

    def set_begin_date(self, begin_date: Union[str, datetime.date, datetime.datetime]) -> None:
        """
        Sets the begin_date of the market, then gathers the data for that market
        :param begin_date: The begin_date to be set
        :return: None
        """
        if isinstance(begin_date, (datetime.date, datetime.datetime)):
            begin_date = begin_date.strftime("%m/%d/%Y")

        self.begin_date = begin_date

    def set_end_date(self, end_date: Union[str, datetime.date, datetime.datetime]) -> None:
        """
        Sets the end_date of the market, then gathers the data for that market
        :param end_date: The end_date to be set
        :return: None
        """
        if isinstance(end_date, (datetime.date, datetime.datetime)):
            end_date = end_date.strftime("%m/%d/%Y")

        self.end_date = end_date

    def refresh_data(self) -> None:
        """
        Refreshes the data for the given market and stores it in the data attribute as a pandas dataframe
        """
        _url = self.create_api_url()
        _payload = self.create_payload(commodity=self.commodity, region=self.region, class_=self.class_,
                                       organic=self.organic, begin_date=self.begin_date, end_date=self.end_date)
        self.data = self.get_data(_url, _payload)
        self.data = pd.DataFrame(self.data)
