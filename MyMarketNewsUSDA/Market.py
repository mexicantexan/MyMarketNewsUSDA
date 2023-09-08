import datetime
from typing import Union

import pandas as pd

from MyMarketNewsUSDA.ApiBase import ApiBase
from assets.commodities import COMMODITY_DATA, COMMODITY_CLASSES, COMMODITY_REGIONS, COMPOSITE_COMMODITIES, \
    FRUIT_COMMODITIES, ONIONS_AND_POTATOES_COMMODITIES, VEGETABLES_COMMODITIES, HERBS_COMMODITIES, \
    ORNAMENTALS_COMMODITIES, HEMP_COMMODITIES

# example call that we are trying to mimic
# base_url = "https://mymarketnews.ams.usda.gov/get_external_api/result"
#
# payload = {
#     "MT": "/3/",
#     "CLASS": "Fruit",
#     "REGN": "National",
#     "DATE": [
#         "08/01/2023",
#         "08/20/2023"
#     ],
#     "COMD": [
#         "All"
#     ],
#     "ORGC": "No"
# }
#
# response = requests.post(base_url, json=payload)
# if response.status_code == 200:
#     print(response.json())
# else:
#     response.raise_for_status()


def is_commodity(commodity: str) -> bool:
    """
    Checks if the given commodity is a valid commodity
    :param commodity: The commodity to check
    :return: True if the commodity is valid, False otherwise
    """
    if commodity is None:
        return False
    if commodity in FRUIT_COMMODITIES:
        return True
    elif commodity in ONIONS_AND_POTATOES_COMMODITIES:
        return True
    elif commodity in VEGETABLES_COMMODITIES:
        return True
    elif commodity in HERBS_COMMODITIES:
        return True
    elif commodity in ORNAMENTALS_COMMODITIES:
        return True
    elif commodity in HEMP_COMMODITIES:
        return True
    else:
        return False


def is_commodity_class(commodity_class: str) -> bool:
    """
    Checks if the given commodity class is a valid commodity class
    :param commodity_class: The commodity class to check
    :return: True if the commodity class is valid, False otherwise
    """
    if commodity_class is None:
        return False
    if commodity_class in COMMODITY_CLASSES:
        return True
    return False


def is_commodity_region(commodity_region: str) -> bool:
    """
    Checks if the given commodity region is a valid commodity region
    :param commodity_region: The commodity region to check
    :return: True if the commodity region is valid, False otherwise
    """
    if commodity_region is None:
        return False
    if commodity_region in COMMODITY_REGIONS:
        return True
    return False


class Market(ApiBase):
    """
    This class is used to store the data from a single market and provide methods to manipulate that data
    In general the market class is meant to be used to access data at https://www.marketnews.usda.gov/mnp/fv-home

    :param commodity: The commodity to be set
    :param region: The region to be set
    :param class_: The class to be set
    :param organic: The organic to be set
    :param begin_date: The begin_date to be set
    :param end_date: The end_date to be set

    :return: None
        To access market data use property 'data'
        To refresh/get data run method 'refresh_data'
    """

    def __init__(self, **kwargs):
        super().__init__(api_type="market")
        self.data: pd.DataFrame = pd.DataFrame()
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
        if is_commodity(commodity) is False:
            raise ValueError(
                f"commodity must be one of the following: {sorted(set([x['commodity'] for x in COMMODITY_DATA]))}")
        for x in COMMODITY_DATA:
            if commodity == x['commodity']:
                self.commodity = commodity
                self.class_ = x['class']
                return

    def set_region(self, region: str) -> None:
        """
        Sets the region of the market, then gathers the data for that market
        :param region: The region to be set
        :return: None
        """
        region = region.upper()
        if is_commodity_region(region) is False:
            raise ValueError(f"region must be one of the following: {sorted(COMMODITY_REGIONS)}")

        self.region = region

    def set_class(self, class_: str) -> None:
        """
        Sets the class of the market, then gathers the data for that market
        :param class_: The class to be set
        :return: None
        """
        class_ = str(class_).upper()
        if is_commodity_class(class_) is False:
            raise ValueError(f"class_ must be one of the following: {sorted(COMMODITY_CLASSES)}")
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
        elif isinstance(begin_date, str):
            try:
                datetime.datetime.strptime(begin_date, "%m/%d/%Y")
            except ValueError:
                raise ValueError(f"begin_date must be in the format MM/DD/YYYY, not {begin_date}")
        else:
            raise TypeError(f"begin_date must be of type str, datetime.date, or datetime.datetime,"
                            f" not {type(begin_date)}")

        self.begin_date = begin_date

    def set_end_date(self, end_date: Union[str, datetime.date, datetime.datetime]) -> None:
        """
        Sets the end_date of the market, then gathers the data for that market
        :param end_date: The end_date to be set
        :return: None
        """
        if end_date is None:
            end_date = datetime.date.today().strftime("%m/%d/%Y")
        elif isinstance(end_date, (datetime.date, datetime.datetime)):
            end_date = end_date.strftime("%m/%d/%Y")
        elif isinstance(end_date, str):
            try:
                datetime.datetime.strptime(end_date, "%m/%d/%Y")
            except ValueError:
                raise ValueError(f"begin_date must be in the format MM/DD/YYYY, not {end_date}")
        else:
            raise TypeError(f"begin_date must be of type str, datetime.date, or datetime.datetime,"
                            f" not {type(end_date)}")

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


if __name__ == "__main__":
    pd.set_option('display.max_columns', None)
    a = Market(commodity="LETTUCE, GREEN LEAF", region="National", class_="All", organic="No", begin_date="07/01/2021")
    a.refresh_data()
    print(a.data.head(10))
