import pprint
import requests
pp = pprint.PrettyPrinter(indent=4)
id = "tt0118615"
api_key = "bIr2F5F1XABxaT9SIJ2fBejicWI2yQGKVcepiYXY"
url = f"https://api.watchmode.com/v1/title/{id}/sources/?apiKey={api_key}"
response = requests.get(url)
data = response.json()
pp.pprint(data)
#for item in data:
  #  pp.pprint(item['name'])
