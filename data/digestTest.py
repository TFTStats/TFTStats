import json
from neo4j import GraphDatabase
from config import neo4j_password



uri = "bolt://localhost:7687"
user = "neo4j"
password = neo4j_password

driver = GraphDatabase.driver(uri, auth=(user, password))

with driver.session() as session:
    results = session.run('''MATCH (patch:PATCH)<-[:ON_THIS_PATCH] - (server:SERVER) <- [:PLAYED_IN_THIS_SERVER] - (league:LEAGUE) <- [:PLAYED_IN_THIS_LEAGUE] - (game:Game) <-[:PLAYED_IN_THIS_MATCH]- (player:PLAYER) - [:HAS_THIS_CHAMPION] -> (champion:CHAMPION) - [:HAS_THIS_ITEM] -> (item:ITEM)
Where champion.character_ID = "TFT8_AurelionSol" and item.item_Name = "TFT_Item_HextechGunblade" and player.placement = 1
RETURN  game,  player , champion , item , league, server,patch''')
    
    d = results.data()
    print (len(d))
    test =[]
    for item in d :
        test.append(item)
        
   
    f = open("test.json", "w")
    f.write(json.dumps(test))
    f.close()
    driver.close()