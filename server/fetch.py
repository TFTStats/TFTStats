# imports api key from config
from config import riot_api_key
import time
import requests
from queue import Queue
import json

reqCount = 0

# calls riot api with a url and returns the json response


def apiCall(url: str):
    global reqCount
    reqCount += 1
    print("request count: " + str(reqCount))
    api_limit_reached = True
    while api_limit_reached:
        response = requests.get(
            url, headers={"X-Riot-Token": riot_api_key})
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

playerJson = apiCall(
    "https://euw1.api.riotgames.com/tft/league/v1/grandmaster")
for summoner in playerJson.get("entries"):
    summonerIdQueue.put(summoner.get("summonerId"))

playerJson = apiCall(
    "https://euw1.api.riotgames.com/tft/league/v1/master")
for summoner in playerJson.get("entries"):
    summonerIdQueue.put(summoner.get("summonerId"))

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
    matchJson = apiCall(
        "https://europe.api.riotgames.com/tft/match/v1/matches/by-puuid/" + summonerPuuidQueue.get() + "/ids?count=20")
    for matchId in matchJson:
        matchSet.add(matchId)

f = open("matches.json", "w")
f.write(json.dumps(list(matchSet)))
matchIdsQueue = Queue()

for matchId in matchSet:
    matchIdsQueue.put(matchId)
matchList = list([])
while not matchIdsQueue.empty():
    matchId = matchIdsQueue.get()
    matchJson = apiCall(
        "https://europe.api.riotgames.com/tft/match/v1/matches/" + matchId)
    matchList.append(matchJson)
    f = open("matches.json", "w")
    f.write(json.dumps(matchList))

   