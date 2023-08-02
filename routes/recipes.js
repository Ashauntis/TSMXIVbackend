var express = require('express');
var router = express.Router();
var redis = require('../util/redis.js');

/* GET users listing. */
router.get('/', async function(req, res, next) { 
  if (!req.query.id) {
    res.send("No id provided");
    return;
  }
  let response = {}; 
  // get the recipe id from the request
  const id = req.query.id;
  // get the recipe from the database
  const recipe_raw = await redis.hget(id, 'materials');
  const recipe = await JSON.parse(recipe_raw);
  const crystals_raw = await redis.hget(id, 'crystals');
  const crystals = await JSON.parse(crystals_raw);
  const name = await redis.hget(id, 'recipe');
  
  response.materials = recipe;
  response.crystals = crystals;
  response.name = name;

  res.send(response);
});

module.exports = router;
