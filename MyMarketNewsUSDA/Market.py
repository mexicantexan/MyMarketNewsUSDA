import requests

# TODO: create class for Market that inherits from ApiBase

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
