import json
from neo4j import GraphDatabase
from config import neo4j_password

f = open("matchData.json", "r")

data = json.loads(f.read())
f.close()

uri = "bolt://localhost:7687"
user = "neo4j"
password = neo4j_password

driver = GraphDatabase.driver(uri, auth=(user, password))
def ingest_tft_match(session, match_data):
    query = '''
    WITH $matchData AS matchData
    MERGE (p:PATCH {patch_Number: matchData.info.game_version})
    MERGE (s:SERVER {Server_Name :"NA"})
    MERGE (p)<-[:ON_THIS_PATCH] -(s)
    MERGE (L:LEAGUE {rank_Name: "Challenger"})
    MERGE (s)<-[:PLAYED_IN_THIS_SERVER] -(L)
    MERGE (m:Game {match_ID: matchData.metadata.match_id})
    MERGE (m)-[:PLAYED_IN_THIS_LEAGUE] ->(L)
    WITH  matchData, m
    UNWIND matchData.info.participants AS participant
        MERGE (player:PLAYER {puuid: participant.puuid,  placement: participant.placement,
            level: participant.level}) - [:PLAYED_IN_THIS_MATCH]->(m) 

    '''
    print("Executing query with match data:")
    
    result = session.run(query, matchData=match_data)
    
    
    
    

# Replace this with your actual match data JSON object


with driver.session() as session:
    for match_data in data:
        ingest_tft_match(session, match_data)

driver.close()