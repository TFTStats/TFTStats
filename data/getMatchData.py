from config import riot_api_key
import time
import requests
from queue import Queue
import json

reqCount = 0
session = requests.Session()
session.headers.update({"X-Riot-Token": riot_api_key})

def apiCall(url: str):
    global reqCount
    reqCount += 1
    print("request count: " + str(reqCount))
    api_limit_reached = True
    while api_limit_reached:
        response = session.get(url)
        if response.status_code == 429:  # API limit reached
            print("API limit reached. Pausing for 60 seconds...")
            reqCount = 0
            time.sleep(60)  # Pause for 60 seconds
        else:
            api_limit_reached = False  # Exit the loop

    return response.json()

f = open("matches.json","r")

matchSet = json.loads(f.read())
f.close()

matchIdQueue = Queue()
for match in matchSet:
    matchIdQueue.put(match)

print("getting every match and placing them into a set")
matchSet = list([])
# Added a limit to the number of matches to get t o prevent the script from running for too long
while not matchIdQueue.empty() and len(matchSet) < 100:
    matchJson = apiCall(
        "https://americas.api.riotgames.com/tft/match/v1/matches/" + matchIdQueue.get())
    matchSet.append(matchJson)
    print(len(matchSet))

f = open("matchData.json", "w")
f.write(json.dumps(list(matchSet)))