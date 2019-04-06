'use strict';

process.chdir(__dirname);

// Utils
const { logError } = require('./utils/log');

/**
 * @type {Telegraf}
 * Bot
 */
const bot = require('./bot');
var nodemon = require('nodemon');

nodemon({
  script: './bot',
  ext: 'js json'
});

nodemon.on('start', function () {
  console.log('App has started');
}).on('quit', function () {
  console.log('App has quit');
  process.exit();
}).on('restart', function (files) {
  console.log('App restarted due to: ', files);
});
bot.telegram.getMe().then((botInfo) => {
	bot.options.username = botInfo.username;
	bot.context.botInfo = botInfo;
}).then(() => {
});
bot.launch({
  webhook: {
    domain: process.env.APP_URL + process.env.TOKEN,
    port: 3000
  }
})

bot.use(
	require('./handlers/middlewares'),
	require('./handlers/messages'),
	require('./plugins'),
	require('./handlers/commands'),
	require('./handlers/regex'),
	require('./handlers/unmatched'),
);


bot.catch(logError);