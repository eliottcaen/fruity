import requests
import json

url = "https://api-to-find-grocery-prices.p.rapidapi.com/amazon"
querystring = {"query": "broccolis", "country": "us", "page": "1"}

headers = {
    "x-rapidapi-host": "api-to-find-grocery-prices.p.rapidapi.com",
    "x-rapidapi-key": "64bf2b5510mshf45d3c72715ca7ep1fa095jsn7613ffd147d6"
}

response = requests.get(url, headers=headers, params=querystring)

# Pretty print the response
if response.status_code == 200:
    data = response.json()
    print(json.dumps(data, indent=4))  # Nicely formatted output
else:
    print(f"Error {response.status_code}: {response.text}")
