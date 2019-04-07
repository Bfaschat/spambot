'use strict';

process.chdir(__dirname);
const express = require('express');
const app = express();
// Utils
const { logError } = require('./utils/log');
/**
 * @type {Telegraf}
 * Bot
 */
require("dotenv").config();
const bot = require('./bot');
var nodemon = require('nodemon');

nodemon({
  script: './bot',
  ext: 'js json'
});

app.get(process.env.HEROKU_URL + process.env.TOKEN, (request, response) => {
  console.log(Date.now() + " Ping Received");
  response.sendStatus(200);
});
nodemon.on('start', function () {
  console.log('App has started');
}).on('quit', function () {
  console.log('App has quit');
  process.exit();
}).on('restart', function (files) {
  console.log('App restarted due to: ', files);
});

const bodyParser = require('body-parser');
const packageInfo = require('./package.json');


app.use(bodyParser.json());

app.get('/', function (req, res) {
  res.json({ version: packageInfo.version });
});

var server = app.listen(process.env.PORT, "0.0.0.0", () => {
  const host = server.address().address;
  const port = server.address().port;
  console.log('Web server started at http://%s:%s', host, port);
});

module.exports = (bot) => {
  app.post('/' + bot.token, (req, res) => {
    bot.processUpdate(req.body);
    res.sendStatus(200);
  });
};

bot.telegram.getMe().then((botInfo) => {
	bot.options.username = botInfo.username;
	bot.context.botInfo = botInfo;
}).then(() => {
  //bot.startWebhook('/webhook', null, '3000');
	//bot.startPolling();
});



bot.use(
	require('./handlers/middlewares'),
	require('./handlers/messages'),
	require('./plugins'),
	require('./handlers/commands'),
	require('./handlers/regex'),
	require('./handlers/unmatched'),
);


bot.catch(logError);
