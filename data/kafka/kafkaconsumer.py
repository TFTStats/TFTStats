import json
import pprint
import time
from kafka import KafkaConsumer
import requests
from config import riot_api_key
reqCount = 0
session = requests.Session()
session.headers.update({"X-Riot-Token": riot_api_key})
# calls riot api with a url and returns the json response
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
# To consume latest messages and auto-commit offsets
consumer = KafkaConsumer('quickstart', bootstrap_servers=['localhost:9092'],group_id='my-group',auto_commit_interval_ms=1000)

print(consumer.metrics())

for message in consumer:
    # message value and key are raw bytes -- decode if necessary!
    # e.g., for unicode: `message.value.decode('utf-8')`
    print(message.value.decode('utf-8'),message.offset)
    summonerJson = apiCall(
        "https://na1.api.riotgames.com/tft/summoner/v1/summoners/" + json.loads(message.value.decode('utf-8')))
    print(summonerJson.get("puuid"))
