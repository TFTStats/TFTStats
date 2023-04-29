from config import riot_api_key
import time
import asyncio
import aiohttp
from queue import Queue
import json
from aiohttp import ClientConnectionError
reqCount = 0

# Creates a session with the api key
async def create_session():
    session = aiohttp.ClientSession(headers={"X-Riot-Token": riot_api_key})
    return session

# calls riot api with a url and returns the json response
async def apiCall(session, url: str):
    global reqCount
    reqCount += 1
    print("request count: " + str(reqCount))
    api_limit_reached = True
    while api_limit_reached:
        try:
            async with session.get(url) as response:
                if response.status == 429:  # API limit reached
                    print("API limit reached. Pausing for 60 seconds...")
                    reqCount = 0
                    await asyncio.sleep(60)  # Pause for 60 seconds
                else:
                    api_limit_reached = False  # Exit the loop
                return await response.json()
        except ClientConnectionError as e:
            print(f"Connection error occurred: {e}")
            await asyncio.sleep(5)  # Retry after 5 seconds

    
# Main function to run the async tasks
async def get_summoner_puuids(session, api_url, summoner_puuid_queue):
    summoner_id_queue = Queue()
    player_json = await apiCall(session, api_url)
    for summoner in player_json.get("entries"):
        summoner_id_queue.put(summoner.get("summonerId"))

    while not summoner_id_queue.empty():
        summoner_json = await apiCall(session, "https://euw1.api.riotgames.com/tft/summoner/v1/summoners/" + summoner_id_queue.get())
        print(summoner_json.get("puuid"))
        summoner_puuid_queue.put(summoner_json.get("puuid"))

async def main():
    print("grabbing players")
    summoner_puuid_queue = Queue()
    
    try:
        session = await create_session()

        # Create tasks for each queue
        task1 = get_summoner_puuids(session, "https://euw1.api.riotgames.com/tft/league/v1/challenger", summoner_puuid_queue)
        task2 = get_summoner_puuids(session, "https://na1.api.riotgames.com/tft/league/v1/grandmaster", summoner_puuid_queue)
        task3 = get_summoner_puuids(session, "https://na1.api.riotgames.com/tft/league/v1/master", summoner_puuid_queue)

        # Run tasks concurrently
        await asyncio.gather(task1, task2, task3)

        print("getting every match and placing them into a set")
        match_set = set({})
        while not summoner_puuid_queue.empty():
            match_json = await apiCall(session, f'https://europe.api.riotgames.com/tft/match/v1/matches/by-puuid/{summoner_puuid_queue.get()}/ids?start=0&endTime={int(time.time())}&startTime={int(time.time() - 86400 )}&count=20')
            print(match_json)
            print(len(match_json))
            for match_id in match_json:
                match_set.add(match_id)

        f = open("matchesEU.json", "w")
        f.write(json.dumps(list(match_set)))
    finally:
        await session.close()

# Run the main function with the asyncio event loop
if __name__ == "__main__":
    asyncio.run(main())
