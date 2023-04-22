import json


f = open("matchData.json", "r")

data = json.loads(f.read())
f.close()
# Trait names for set 8
traits = list(["Set8_Ace","Set8_Admin","Set8_AnimaSquad","Set8_Duelist","Set8_Corrupted","Set8_Defender","Set8_ExoPrime","Set8_Forecaster","Set8_GenAE","Set8_Deadeye","Set8_Hacker","Set8_Heart","Set8_Channeler","Set8_Mascot","Set8_OxForce","Set8_Brawler","Set8_Prankster","Set8_Renegade","Set8_SpaceCorps","Set8_StarGuardian","Set8_Supers","Set8_Threat","Set8_UndergroundThe","Set8_Aegis","Set8_Pulsefire","Set8_Parallel","Set8_Riftwalker","Set8_GunMage"])
# How many matches are in the data set
length = len(data)
print("Total matches: " + str(length))
# Missing Analysis for tier traits 

# Loop through each trait and find the amount of matches that have that trait
for trait in traits:
    # amount = 0
    # placement = list([]) 
    amount = []
    placement =[]
    top1 =[]
    top4 =[]
    # Loop through each match
    for index,  match in enumerate(data):
        match_info = match.get("info")

        participants = match_info.get("participants")
        # Loop through each participant in the match
        for participant in participants:
            userTraits = participant.get("traits")
            # Loop through each trait the participant has
            for userTrait in userTraits:
                # Check if the trait is the one we are looking for and if the trait is active 0 = not active
                if userTrait.get("name") == trait and userTrait.get("tier_current") != 0  :
                # Create a list for each tier and add the placement of the participant to the list
                    for tiers in range(0, userTrait.get("tier_total")):
                        # Make sure this Code only runs once  per trait 
                        if(len(amount) < userTrait.get("tier_total")  ):
                            amount.append(0)
                            placement.append([])
                            top1.append(0)
                            top4.append(0)
                    
                    # Add the + 1 to the right tier and add the placement to the right tier
                    for tier in range(0, userTrait.get("tier_current")):
                        amount[userTrait.get("tier_current") - 1] += 1
                        placement[userTrait.get("tier_current") - 1] .append(participant.get("placement"))
                        if participant.get("placement") == 1:
                            top1[userTrait.get("tier_current") - 1] += 1
                        if participant.get("placement") <= 4:
                            top4[userTrait.get("tier_current") - 1] += 1
# Print the amount of matches that have the trait and the average placement of the trait for each tier                        
    for i in range(0, len(amount)):
        print("Amount of "+ trait + " matches: " + str(amount[i]/8)+ " out of " + str(length) + " matches" + " for tier " + str(i + 1))
        print("Average placement: " + str(sum(placement[i])/len(placement[i])))
        print("Top 1: " + str((top1[i] / length)* 100) + "%")
        print("Top 4: " + str((top4[i] / length)* 100) + "%")
                        
                        
    # print("Amount of "+ trait + " matches: " + str(amount/8)+ " out of " + str(length) + " matches")
    # print("Average placement: " + str(sum(placement)/len(placement)))
