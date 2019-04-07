'use strict';

const Telegraf = require('telegraf');
const config = require('../config');
const bot = new Telegraf(process.env.TOKEN);

const http = require('http');
const token = process.env.TOKEN;

const Bot = require('node-telegram-bot-api');
let bot;

if(process.env.NODE_ENV === 'production') {
  bot.launch({
  webhook: {
    domain: process.env.HEROKU_URL + process.env.TOKEN,
    port: process.env.PORT
  }
})

}
else {
  bot.startPolling();
}

console.log('Your app is listening on port ' + 3000 + ' \u{1F604}');


module.exports = bot;
// cyclic dependency
// bot/index requires context requires actions/warn requires bot/index
Object.assign(bot.context, require('./context'));
