var express = require('express');
var router = express.Router();

const endpoints = ['recipes', 'prices']; 

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'TSMXIV', endpoints: endpoints });
});

module.exports = router;
