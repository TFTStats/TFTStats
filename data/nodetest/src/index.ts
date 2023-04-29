import axios from "axios";
import kafka from "kafka-node";
import * as dotenv from "dotenv";
dotenv.config();
const client = new kafka.KafkaClient({ kafkaHost: "localhost:9092" });
const producer = new kafka.Producer(client);

producer.on("ready", function () {
  console.log("ready");
});

function getRiotRequestInstance(server: string) {
  const riotRequests = axios.create({
    baseURL: "https://na1.api.riotgames.com/tft",
    headers: {
      "X-Riot-Token": process.env.RIOT_API_KEY,
    },
  });

  return riotRequests;
}
let reqCount = 0;
async function getPlayersFromALeague({
  server,
  league,
}: {
  server: string;
  league: string;
}) {
  const riotRequests = getRiotRequestInstance(server);
  // try {
  //   // const response = await riotRequests.get(`/league/v1/${league}`);
  //   // return response.data;
  // } catch (error) {
  //   console.error(error);
  //   return null;
  // }
  reqCount += 1;
  console.log("request count: " + reqCount);
  let api_limit_reached = true;
  let response: any;

  while (api_limit_reached) {
    try {
      response = await riotRequests.get(`/league/v1/${league}`, {
        validateStatus: function (status) {
          return (status >= 200 && status < 300) || status === 429; // Resolve only if the status is less than 500
        },
      });

      if (response.status === 429) {
        // API limit reached
        console.log("API limit reached. Pausing for 60 seconds...");
        reqCount = 0;
        await new Promise((resolve) => setTimeout(resolve, 60000)); // Pause for 60 seconds
      } else {
        api_limit_reached = false; // Exit the loop
      }
    } catch (error) {
      console.error("Error while making API call:", error);
      break;
    }
  }

  return response.data;
}

async function kafkaProducer(players: { entries: { summonerId: string }[] }) {
  const data = [] as { topic: string; messages: string }[];
  players.entries.forEach((player) => {
    data.push({
      topic: "quickstart",
      messages: JSON.stringify(player.summonerId),
    });
  });
  console.log(data);
  producer.send(data, function (err, data) {
    console.log(data);
  });
}

async function main() {
  const players = (await getPlayersFromALeague({
    server: "NA1",
    league: "challenger",
  })) as {
    entries: { summonerId: string }[];
  };
  if (!players) return;
  kafkaProducer(players);
}

main();
