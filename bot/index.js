'use strict';

const Telegraf = require('telegraf');
const config = require('../config');
const bot = new Telegraf(process.env.TOKEN);
bot.telegram.setWebhook(`https://${process.env.PROJECT_DOMAIN}.herokuapp.com/webhook`);
const http = require('http');
const express = require('express');
const app = express();
app.get("http://${process.env.PROJECT_DOMAIN}.herokuapp.com/", (request, response) => {
  console.log(Date.now() + " Ping Received");
  response.sendStatus(200);
});
//app.listen(process.env.PORT);
setInterval(() => {
  http.get(`http://${process.env.PROJECT_DOMAIN}.herokuapp.com/`);
}, 280000);

console.log('Your app is listening on port ' + 3000 + ' \u{1F604}');

if (process.env.NODE_ENV === 'development') {
	bot.polling.offset = -1;
}

module.exports = bot;
// cyclic dependency
// bot/index requires context requires actions/warn requires bot/index
Object.assign(bot.context, require('./context'));
