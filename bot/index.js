'use strict';

const Telegraf = require('telegraf');
const config = require('../config');
const bot = new Telegraf(process.env.TOKEN);

const http = require('http');


if(process.env.NODE_ENV === 'production') {
  bot.telegram.setWebhook(process.env.HEROKU_URL + process.env.TOKEN);
}
else {
  bot.startPolling();
}


//app.listen(process.env.PORT);
setInterval(() => {
  http.get(process.env.HEROKU_URL + process.env.TOKEN);
}, 280000);

console.log('Your app is listening on port ' + 3000 + ' \u{1F604}');



module.exports = bot;
// cyclic dependency
// bot/index requires context requires actions/warn requires bot/index
Object.assign(bot.context, require('./context'));
