import json
from neo4j import GraphDatabase
from config import neo4j_password

f = open('./tft-data/tft-trait.json', 'r')
data = json.loads(f.read())

arrayTraits:list = []

for x, y in data["data"].items():
    arrayTraits.append(y)
    
uri = "bolt://localhost:7687"
user = "neo4j"
password = neo4j_password

driver = GraphDatabase.driver(uri, auth=(user, password))    


def getAmountOfMatches (session):
    query = '''
    match (m:Game) return m
    '''
    result = session.run(query)
    return result

def getTraitStats(session, traitID):
    query = '''
    with $traitID as traitID
    MATCH (game:Game) <-[:PLAYED_IN_THIS_MATCH]- (player:PLAYER) - [:HAS_THIS_CHAMPION] -> (champion:CHAMPION) ,(player:PLAYER) - [:HAS_THIS_TRAIT] -> (trait:TRAIT)    
    WHERE trait.trait_Name = traitID and trait.trait_tier_current > 0
    Return player , trait 
    '''
    result = session.run(query, traitID=traitID)
    return result

amountOfMatches:int
data:list = []
with driver.session() as session:
    amountOfMatches =len(getAmountOfMatches(session).data())
    for item in arrayTraits:
    
        queryResult = getTraitStats(session, item["id"]).data()
        tiersArray = []
        
        for i in range(queryResult[0]["trait"]["trait_tier_total"]):
            tiersArray.append([])
            
        for result in queryResult:
            tiersArray[result["trait"]["trait_tier_current"] - 1].append(result)   
        traitStats:dict = {}
        traitStats["id"] = item["id"]
        for  index , tier in enumerate(tiersArray):
            traitStats["tier" + str(index + 1)] = { "amount" : len(tier) }
            traitStats["tier" + str(index + 1)]["playRate"] = len(tier) / amountOfMatches /8
            placement = 0
            for game in tier:
                placement += game["player"]["placement"]
            traitStats["tier" + str(index + 1)]["averagePlacement"] = placement / len(tier)
                
        data.append(traitStats)
      
n = open("traitStats.json", "w")

n.write(json.dumps(data))  
   