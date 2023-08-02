var { Redis } = require("ioredis");
const fs = require("fs");
var { config } = require("../config.js");
var recipes = require('./resources/recipe_data.js');

const redis = new Redis({
  host: config.REDIS_HOST,
  port: config.REDIS_PORT,
  // password: config.REDIS_PASSWORD,
});



// update all recipes in the database
async function updateRecipes() {
  const id_map = JSON.parse(
    fs.readFileSync("./resources/id_map.json", "utf8")
  );
  // for each recipe in crafting_recipes.js
  let update_count = 0;
  for (var crafter_class in recipes) {
    console.log("Starting " + crafter_class);
    for (var recipe in recipes[crafter_class]) {
      // load the recipe into r
      let r = recipes[crafter_class][recipe];
      
      // get the recipe id
      const recipe_name = r.recipe.trim();
      const recipe_id = id_map[recipe_name];

      // convert the materials and crystals to objects that include the quantity and id 
      for (var mat in r['materials']) {
        const mat_id = id_map[mat];
        const mat_qty = r['materials'][mat];
        r['materials'][mat] = {id: mat_id, qty: mat_qty};
      }

      for (var cry in r['crystals']) {
        const cry_id = id_map[cry];
        const cry_qty = r['crystals'][cry];
        r['crystals'][cry] = {id: cry_id, qty: cry_qty};
      }
      
      // stringify the nested objects
      r['materials'] = JSON.stringify(r['materials'])
      r['crystals'] = JSON.stringify(r['crystals'])

      // set the recipe in redis
      await redis.hset(recipe_id, r);
      update_count++;
    }
  }
  console.log("Updated " + update_count + " recipes");
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
