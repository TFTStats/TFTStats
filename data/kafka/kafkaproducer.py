import json
from kafka import KafkaProducer
from kafka.errors import KafkaError

producer = KafkaProducer(bootstrap_servers=['localhost:9092'])

# Asynchronous by default
f = open("matchDataEU.json", "r")
data = json.loads(f.read())

from config import riot_api_key
import time
import requests
from queue import Queue
import json

reqCount = 0


# Creates a session with the api key
session = requests.Session()
session.headers.update({"X-Riot-Token": riot_api_key})
def  apiCall(url: str):
    global reqCount
    reqCount += 1
    print("request count: " + str(reqCount))
    api_limit_reached = True
    while api_limit_reached:
        response = session.get(
            url)
        if response.status_code == 429:  # API limit reached
            print("API limit reached. Pausing for 60 seconds...")
            reqCount = 0
            time.sleep(60)  # Pause for 60 seconds
        else:
            api_limit_reached = False  # Exit the loop

    return response.json()

playerJson = apiCall(
    "https://euw1.api.riotgames.com/tft/league/v1/challenger")
for item in playerJson.get("entries"):
    future = producer.send('quickstart', json.dumps(item["summonerId"]).encode('utf-8'))
    future.get()

