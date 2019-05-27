# MIT License
#
# Copyright (c) 2019 Dan Tès <https://github.com/delivrance>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from configparser import ConfigParser

from pyrogram import Client
import logging
from logging.handlers import RotatingFileHandler
from logging import handlers
import sys, os
# Import the duallog package to set up simultaneous logging to screen and console.
import assistant.utils.duallog as duallog
from assistant.utils.helpers import ParamExtractor, Ranges

from assistant.utils.settings import Settings, CheckMessage, CheckUsername
#os.remove("{}/*.session".format(os.getcwd()))
from os.path import dirname, basename, isfile
import glob
    

mod_paths = glob.glob(dirname(__file__) + "/*")
print(mod_paths)
LOGGER = os.environ.get("LOGGER")
__schema = 8 
__settings = Settings(__schema)
LOGGER_GROUP = int(os.environ.get("LOGGER_GROUP"))
logging.debug('Silently Initializing.')
logging.getLogger("pyrogram").setLevel(logging.WARN)
LOGS = logging.getLogger(__name__)
known_sessions_file = os.path.join(os.path.dirname(__file__), 'logtest')
# Set up dual logging and tell duallog where to store the logfiles.
duallog.setup(known_sessions_file)
        
__msgs = {
            'as_welcome': 'Add me to supergroup and give me admin rights. I will try to block spammers automatically.',
            'as_alog': 'New user {} ({}) has joined chat {} ({}). Score: {}.',
            'as_restex': 'Cannot restrict a new user with ID {} in chat {} ({}) due to missing admin rights.',
            'as_msgex': 'Exception detected while handling spam message from {} in chat {} ({}).',
            'as_notoken': 'No API token found. Cannot proceed. Forward API token using ENV option and try again!',
            'as_joinhex': 'Failed to handle join message.',
            'as_banned': 'Permanently banned user {} ({}) (score: {}) in chat {} ({}).',
            'as_msgrest': 'Removed message from restricted user {} ({}) in chat {} ({}).',
            'as_amsgrm': 'Admin {} ({}) removed message from user {} ({}) in chat {} ({}).',
            'as_amute': 'Admin {} ({}) muted user {} ({}) in chat {} ({}) until {}.',
            'as_aunres': 'Admin {} ({}) removed all restrictions from user {} ({}) in chat {} ({}).',
            'as_aunban': 'Admin {} ({}) unbanned user {} ({}) in chat {} ({}).',
            'as_aban': 'Admin {} ({}) permanently banned user {} ({}) in chat {} ({}).',
            'as_admerr': 'Failed to handle admin command.',
            'as_chkme': 'Checking of account {} successfully completed. Your score is: {}.',
            'as_pmex': 'Failed to handle command in private chat with bot.',
            'as_repmsg': 'You have a new report from user *{}* ({}).\n\nReason: *{}*.\n\nMessage link: {}.',
            'as_repns': 'Cannot send message to admin {} due to Telegram Bot API restrictions.',
            'as_repex': 'Failed to handle report command.',
            'as_repsub': 'Successfully subscribed to reports in chat {} ({}) .',
            'as_replim': 'I cannot send you direct messages due to API restrictions. PM me first, then try again.',
            'as_repsblg': 'Admin {} ({}) subscribed to events in chat {}.',
            'as_repunsb': 'Successfully unsubscribed from reports in chat {} ({}).',
            'as_repusblg': 'Admin {} ({}) unsubscribed from events in chat {} ({}).',
            'as_repnors': 'No reason specified.',
            'as_replog': 'User {} ({}) reported message of another user {} ({}) in chat {} ({}).',
            'as_leaveok': 'Command successfully executed. Leaving chat {} ({}) now.',
            'as_leavepm': 'You must specify chat ID or username to leave from. Fix this and try again.',
            'as_leavelg': 'Admin {} ({}) asked bot to leave chat {} ({}).',
            'as_swadd': 'Admin {} ({}) added new stopword {} to list.',
            'as_swrem': 'Admin {} ({}) removed stopword {} from list.',
            'as_swuadd': 'New stopword {} added to list.',
            'as_swurem': 'Stopword {} removed from list.',
            'as_swulist': 'Currently restricted words: {}.',
            'as_swerr': 'Failed to add/remove stopword. Try again later.',
            'as_swlist': 'Admin {} ({}) fetched list of stopwords.',
            'as_swpm': 'You must specify a stopword to add/remove. Fix this and try again.',
            'as_leaverr': 'Failed to leave chat {} ({}) due to some error.',
            'as_unath': 'You cannot access this command due to missing admin rights. This issue will be reported.',
            'as_unathlg': 'User {} ({}) tried to access restricted bot command. Action was denied.',
            'as_pinmsg': 'Admin {} ({}) pinned message {} in chat {} ({}).',
            'as_unpinmsg': 'Admin {} ({}) removed pinned message in chat {} ({}).',
            'as_wipelg': 'Admin {} ({}) removed {} messages (range {}) in chat {} ({}).',
            'as_wipehg': 'Admin {} ({}) tried to remove {} messages in chat {} ({}). Action was denied.',
            'as_spamdbg': 'Received message from restricted user {} ({}) in chat {} ({}). Check results: '
                          'entitles: {}, spam: {}, forward: {}.\nContents: {}.',
            'as_crashed': 'Bot crashed. Scheduling restart in 30 seconds.'
        }            

        
def __score_user(account, yes):
        """
        Check current user's profile and score him.
        :param account: User ID (from API).
        :return: Score results.
        """

        checker = CheckUsername(account, yes, __settings)
        return checker.score

def __get_message_link(message):
        """
        Generate full URL to specified message.
        :param message: Message to process.
        :return: Full URL.
        """
        return 'https://t.me/{}/{}'.format(message.chat.username, message.reply_to_message.message.id)
    
      
class Assistant(Client):
    def __init__(self):
        name = self.__class__.__name__.lower()
        config_file = "{}.ini".format(name)

        config = ConfigParser()
        config.read(config_file)

        super().__init__(
            name,
            bot_token=config.get(name, "bot_token"),
            config_file=config_file,
            workers=16,
            plugins=dict(root="{}/plugins".format(name))
        )
 
    def start(self):
        super().start()
        print("Pyrogram Assistant started. Hi.")

    def stop(self):
        super().stop()
        print("Pyrogram Assistant stopped. Bye.")
