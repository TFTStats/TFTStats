const data = async function () {
  const test = await fetch(
    "https://euw1.api.riotgames.com/tft/league/v1/challenger",
    {
      method: "GET",
      headers: {
        "X-Riot-Token": "13",
      },
    }
  );
  const data = await test.json();
  data.entries.forEach(async (element) => {
    const test = await fetch(
      `https://euw1.api.riotgames.com/tft/summoner/v1/summoners/${element.summonerId}}`,
      {
        method: "GET",
        headers: {
          "X-Riot-Token": "123",
        },
      }
    );
    const data1 = await test.json();
    console.log(data1);
  });
};

data();
