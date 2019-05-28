

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

from pyrogram import Filters, Message, InlineKeyboardMarkup, InlineKeyboardButton, Emoji
from pyrogram import Message, User
from pyrogram.api import functions

from ..assistant import (Assistant, LOGS, LOGGER, LOGGER_GROUP, __schema, __settings)
from assistant.utils.config import (check_restricted_user, __score_message, __check_message_entities, __check_message_spam, __check_message_forward, __msgs)

import logging
import sys
import time

from assistant.utils.helpers import ParamExtractor, Ranges

from assistant.utils.settings import Settings, CheckMessage, CheckUsername

@Assistant.on_message(Filters.incoming)
@check_restricted_user
def handle_msg(bot: Assistant, message: Message) -> None:
            """
            Listen and handle all messages in supergroup (including edited events).
            Find and remove messages with restricted entitles sent by restricted users.
            :param message: Message, triggered this event.
            """
            try:
                # Checking received message from restricted member...
                entities = __check_message_entities(message)
                forward = __check_message_forward(message)
                spam = __check_message_spam(message)

                # Writing to log some debug information when needed...
                bot.send_message(
                      LOGGER_GROUP,
                  __msgs['as_spamdbg'].format(
                      message.from_user.first_name, 
                      message.from_user.id,
                      message.chat.id, 
                      message.chat.title,
                      entities, 
                      spam, 
                      forward,
                      message.text
                    ))

                # Removing messages from restricted members...
                if entities or forward or spam:
                    bot.delete_messages(message.chat.id, message.message_id)
                    bot.send_message(
                      LOGGER_GROUP,
                      __msgs['as_msgrest'].format(
                      message.from_user.first_name, 
                      message.from_user.id,
                      message.chat.id, 
                      message.chat.title
                    ))
                    
            except Exception as e:
                bot.send_message(
                  LOGGER_GROUP,
                  __msgs['as_msgex'].format(
                    message.from_user.id, 
                    message.chat.id, 
                    message.chat.title
                  ))
                LOGS.error(e, __msgs['as_admerr'])
