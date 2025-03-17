import requests
import json

url = "https://plant.id/api/v3/kb/plants/name_search?q=Acer ginnala "

payload={}
headers = {
  'Api-Key': 'dEyCrdBfLJ4RWP4BIXEtcwWAHEYdy9uO5pgN6vDP4f7qQ59GdE',
  'Content-Type': 'application/json'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
