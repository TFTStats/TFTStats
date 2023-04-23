import json
from neo4j import GraphDatabase
from config import neo4j_password

f = open("matchData.json", "r")

data = json.loads(f.read())
f.close()

uri = "bolt://localhost:7687"
user = "neo4j"
password = neo4j_password

for match in data :
    if(match["info"]["game_version"][12:13] == "."):
        match["info"]["game_version"] = match["info"]["game_version"][:12]
    else:
        match["info"]["game_version"] = match["info"]["game_version"][:13]

driver = GraphDatabase.driver(uri, auth=(user, password))
def ingest_tft_match(session, match_data):
    query = '''
    WITH $matchData AS matchData
    MERGE (p:PATCH {patch_Number: matchData.info.game_version})
    MERGE (s:SERVER {Server_Name :"NA" , patch: matchData.info.game_version})
    MERGE (p)<-[:ON_THIS_PATCH] -(s)
    MERGE (s)<-[:PLAYED_IN_THIS_SERVER] - (L:LEAGUE {rank_Name: "Challenger"})
    with matchData, L
    OPTIONAL MATCH (existing:Game {match_ID: matchData.metadata.match_id})
    with matchData, L, existing
    WHERE existing IS NULL
    CREATE (m:Game {match_ID: matchData.metadata.match_id})
    CREATE (m)-[:PLAYED_IN_THIS_LEAGUE] ->(L)
    WITH  matchData, m
    UNWIND matchData.info.participants AS participant
        CREATE (player:PLAYER {puuid: participant.puuid,  placement: participant.placement,
            level: participant.level}) - [:PLAYED_IN_THIS_MATCH]->(m)     
    WITH  player , participant , matchData
    UNWIND participant.units AS unit
    CREATE (champion:CHAMPION {tier: unit.tier, character_ID: unit.character_id, rarity: unit.rarity , belongs : participant.puuid, match_ID: matchData.metadata.match_id})
    CREATE (player) - [:HAS_THIS_CHAMPION] -> (champion)
    WITH  unit , champion , participant , matchData
    UNWIND unit.itemNames AS item
    CREATE (i:ITEM {item_Name: item , belongs : participant.puuid, match_ID: matchData.metadata.match_id , champion_ID: ID(champion)})
    CREATE (champion) - [:HAS_THIS_ITEM] -> (i)
    
    '''
    print("Executing query with match data:")
    
    result = session.run(query, matchData=match_data)
    
    
    
    

# Replace this with your actual match data JSON object


with driver.session() as session:
    for match_data in data:
        ingest_tft_match(session, match_data)

driver.close()