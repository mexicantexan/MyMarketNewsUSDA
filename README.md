# MyMarketNewsUSDA Python Wrapper

This is a Python wrapper for the USDA's My Market News API. It is a work in progress and is not yet ready for use.

To use this wrapper, you will need to obtain an API key from the USDA. You can do so by following the instructions at: 
https://mymarketnews.ams.usda.gov/mymarketnews-api/authentication

Once you have your API key, you can use this wrapper to access the USDA's My Market News API by either passing the api 
key as an environment variable (preferred), or by hard-coding it into the `constants.py` file, or by passing it into
the `MyMarketNews` class as an argument.
