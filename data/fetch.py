# imports api key from config
from config import riot_api_key
import time
import requests
from queue import Queue
import json

reqCount = 0


# Creates a session with the api key
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


print("grabbing players")
summonerIdQueue = Queue()
playerJson = apiCall(
    "https://euw1.api.riotgames.com/tft/league/v1/challenger")
for summoner in playerJson.get("entries"):
    summonerIdQueue.put(summoner.get("summonerId"))

# playerJson = apiCall(
#     "https://na1.api.riotgames.com/tft/league/v1/grandmaster")
# for summoner in playerJson.get("entries"):
#     summonerIdQueue.put(summoner.get("summonerId"))

# playerJson = apiCall(
#     "https://na1.api.riotgames.com/tft/league/v1/master")
# for summoner in playerJson.get("entries"):
#     summonerIdQueue.put(summoner.get("summonerId"))

print("getting every puuid")
summonerPuuidQueue = Queue()
while not summonerIdQueue.empty():
    summonerJson = apiCall(
        "https://euw1.api.riotgames.com/tft/summoner/v1/summoners/" + summonerIdQueue.get())
    print(summonerJson.get("puuid"))
    summonerPuuidQueue.put(summonerJson.get("puuid"))

print("getting every match and placing them into a set")
matchSet = set({})
while not summonerPuuidQueue.empty():
    print(f'https://americas.api.riotgames.com/tft/match/v1/matches/by-puuid/{summonerPuuidQueue.get()}/ids?start=0&endTime={int(time.time())}&startTime={int(time.time()  - 86400 )}&count=20')
    matchJson = apiCall(f'https://europe.api.riotgames.com/tft/match/v1/matches/by-puuid/{summonerPuuidQueue.get()}/ids?start=0&endTime={int(time.time())}&startTime={int(time.time() - 86400 )}&count=20')
    print(matchJson)
    print(len(matchJson))
    for matchId in matchJson:
        matchSet.add(matchId)

f = open("matchesEU.json", "w")
f.write(json.dumps(list(matchSet)))
