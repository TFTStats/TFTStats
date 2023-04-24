import json
f = open("matchData.json", "r")

data = json.loads(f.read())
f.close()

for match in data :
    if(match["info"]["game_version"][12:13] == "."):
        match["info"]["game_version"] = match["info"]["game_version"][:12]
    else:
        match["info"]["game_version"] = match["info"]["game_version"][:13]
print (data[0])        