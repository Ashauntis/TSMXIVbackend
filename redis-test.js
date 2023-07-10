var { Redis } = require("ioredis");
const fs = require("fs");
var { config } = require("./config.js");

const redis = new Redis({
  host: config.REDIS_HOST,
  port: config.REDIS_PORT,
});

// update all recipes in the database
async function GetRecipe() {
  // const params = crafterClass + ':' + name;
  const params = "Culinarian Recipes:Apple Juice";
  console.log('starting database query');
  const recipe = await redis.get(params);
  console.log(`returning \n${recipe}`);
  return recipe;
}
console.log('starting')
GetRecipe()
  .then((recipe) => {
    console.log(recipe);
    process.exit(0);
  })
  .catch((err) => {
    console.log(err);
  });
