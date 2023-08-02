var { Redis } = require("ioredis");
var { config } = require("../config.js");
var data = require("./resources/recipe_data.js");
var item_data = require("./resources/item_types.js");

var redis = new Redis(config.redis);

// Loop through each class of recipes (e.g., "Alchemist Recipes," "Culinary Recipes," etc.)
Object.keys(data).forEach((classKey) => {
    const recipes = data[classKey];
    // Loop through the recipes in the current class
    Object.keys(recipes).forEach((recipeName) => {
        const recipe = recipes[recipeName];
        if (item_data[recipe.type] === undefined) {
            item_data[recipe.type] = {
                recipes: [],
            };
        };
        item_data[recipe.type].recipes.push({
            name: recipe.recipe,
            id: recipe.recipe_level,
        });
    });
});

// Convert item_data to a flat object (flatten nested object)
const flattenedItemData = {};
Object.keys(item_data).forEach((type) => {
    flattenedItemData[type] = JSON.stringify(item_data[type]);
});

// Save flattenedItemData as a Redis hash using hmset
redis.hmset("item_data", flattenedItemData, (err, result) => {
    if (err) {
        console.error("Error saving data to Redis:", err);
    } else {
        console.log("Data successfully saved to Redis as a hash.");
    }
});

// test the result with a query
redis.hgetall("item_data", (err, result) => {
    console.log("Result of query:", result);
});
