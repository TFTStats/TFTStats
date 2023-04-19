async function test() {
  const arr = [];
  for (let i = 0; i < 31; i++) {
    arr.push(
      await fetch(`https://euw1.api.riotgames.com/tft/league/v1/challenger`, {
        headers: {
          "X-Riot-Token": "123",
        },
      }).then((res) => res.json())
    );
  }
  console.log(arr);
  console.log(arr.length);
}

test();
