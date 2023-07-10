var express = require('express');
var router = express.Router();
var redis = require('../util/redis.js');

/* GET users listing. */
router.get('/', async function(req, res, next) { 
  // get the recipe id from the request
  const name = req.query.name;
  // get the collection to search
  const collection = req.query.collection;
  // get the recipe from the database
  const params = collection + ':' + name;
  console.log(`params: ${params}`);
  const recipe = await redis.get(params);
  res.send(recipe);
});

module.exports = router;
