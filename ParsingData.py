import json


f = open("matchData.json", "r")

data = json.loads(f.read())

# Trait names for set 8
traits = list(["Set8_Ace","Set8_Admin","Set8_AnimaSquad","Set8_Duelist","Set8_Corrupted","Set8_Defender","Set8_ExoPrime","Set8_Forecaster","Set8_GenAE","Set8_Deadeye","Set8_Hacker","Set8_Heart","Set8_Channeler","Set8_Mascot","Set8_OxForce","Set8_Brawler","Set8_Prankster","Set8_Renegade","Set8_SpaceCorps","Set8_StarGuardian","Set8_Supers","Set8_Threat","Set8_UndergroundThe","Set8_Aegis","Set8_Pulsefire","Set8_Parallel","Set8_Riftwalker","Set8_GunMage"])
# How many matches are in the data set
length = len(data)
print("Total matches: " + str(length))
# Missing Analysis for tier traits 

# Loop through each trait and find the amount of matches that have that trait
for trait in traits:
    amount = 0
    placement = list([])
    for match in data:
        participants = match.get("info").get("participants")
        for participant in participants:
            userTraits = participant.get("traits")
            for userTrait in userTraits:
                if userTrait.get("name") == trait:
                    amount += 1
                    placement.append(participant.get("placement"))
    print("Amount of "+ trait + " matches: " + str(amount/8)+ " out of " + str(length) + " matches")
    print("Average placement: " + str(sum(placement)/len(placement)))
