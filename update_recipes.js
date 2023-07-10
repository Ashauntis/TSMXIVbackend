var { Redis } = require("ioredis");
const fs = require("fs");
var { config } = require("./config.js");

const redis = new Redis({
  host: config.REDIS_HOST,
  port: config.REDIS_PORT,
  // password: config.REDIS_PASSWORD,
});

// update all recipes in the database
async function updateRecipes() {
  // read the json document
  const data = JSON.parse(
    fs.readFileSync("./scraper/crafting_recipes.json", "utf8")
  );
  // for each recipe in crafting_recipes.js
  for (var crafter_class in data) {
    console.log("Starting " + crafter_class);
    // await redis.set(crafter_class, JSON.stringify(data[crafter_class]));

    for (var recipe in data[crafter_class]) {
      var entry = crafter_class + ":" + recipe;
      // set the recipe in redis
        await redis.set(entry, JSON.stringify(data[crafter_class][recipe]));
      console.log("Set " + entry);
    }
  }
  return 0;
}
updateRecipes()
  .then(() => {
    console.log("finished");
    process.exit(0);
  })
  .catch((err) => {
    console.log(err);
  });
