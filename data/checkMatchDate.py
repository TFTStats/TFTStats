import json
import datetime
import time

f = open("matchData.json", "r")

matchData = json.loads(f.read())
f.close()

timeMatch = list([])

for match in matchData:
    timeMatch.append(datetime.datetime.utcfromtimestamp(match.get("info").get("game_datetime")/1000).strftime('%Y-%m-%d %H:%M:%S'))

timeMatch.sort()
f = open("matchTimes.json", "w")
f.write(json.dumps(list(timeMatch)))