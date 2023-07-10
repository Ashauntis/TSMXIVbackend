var { Redis } = require('ioredis');
var { config } = require('../config.js');

const redis = new Redis({
  host: config.REDIS_HOST,
  port: config.REDIS_PORT,
})

module.exports = redis;