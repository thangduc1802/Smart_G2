import requests
import json

url = "https://plant.id/api/v3/kb/plants/EXNAeV1qR3AvTUd3SXkBY39JaVliUHpDJEYANA9rYFY-?details=best_soil_type"

payload={}
headers = {
  'Content-Type': 'application/json',
  'Api-Key': 'dEyCrdBfLJ4RWP4BIXEtcwWAHEYdy9uO5pgN6vDP4f7qQ59GdE'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
