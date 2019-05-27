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
logging.debug('Silently Initializing.')
logging.getLogger("pyrogram").setLevel(logging.WARN)
LOGS = logging.getLogger(__name__)
known_sessions_file = os.path.join(os.path.dirname(__file__), 'logtest')
# Set up dual logging and tell duallog where to store the logfiles.
duallog.setup(known_sessions_file)
from assistant.utils.helpers import ParamExtractor, Ranges

from assistant.utils.settings import Settings, CheckMessage, CheckUsername
#os.remove("{}/*.session".format(os.getcwd
LOGGER = os.environ.get("LOGGER")
__schema = 8 
__settings = Settings(__schema)
LOGGER_GROUP = int(os.environ.get("LOGGER_GROUP"))

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
