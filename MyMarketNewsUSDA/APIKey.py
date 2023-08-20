"""
Author: Jacob Dallas
"""
import os


class ApiKey:
    """
    This class is used to store the api key for the MyMarketNews USDA API
    """
    def __init__(self, api_key: str = None):
        if api_key is not None:
            if api_key != "MY_API_KEY":
                self.api_key = api_key
                return
        # if the api key is still not set, try to get it from constants.py, then from an environment variable
        try:
            from constants import API_KEY
            if API_KEY == "MY_API_KEY":
                raise ImportError("You must provide an API key, either in constants.py, as an environment variable,"
                                  " or by passing it directly into the script")
            self.api_key = API_KEY
        except ImportError:
            if os.environ.get("API_KEY") is not None:
                self.api_key = os.environ.get("API_KEY")
            else:
                raise ImportError("You must provide an API key, either in constants.py, as an environment variable,"
                                  " or by passing it directly into the script")
