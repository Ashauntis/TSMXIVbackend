var express = require('express');
var router = express.Router();
var redis = require('../util/redis.js');

/* GET users listing. */
router.get('/', async function(req, res, next) { 
  if (!req.query.id) {
    res.send("No id provided");
    return;
  }
  
  // get the recipe id from the request
  const id = req.query.id;
  // get the recipe from the database
  const recipe = await redis.hgetall(id);
  res.send(recipe);
});

module.exports = router;
