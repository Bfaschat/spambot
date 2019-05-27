
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
from assistant.utils.config import (__notify_admin, __msgs, __score_user, __get_message_link)

import logging
import sys
import time

from assistant.utils.helpers import ParamExtractor, Ranges

from assistant.utils.settings import Settings, CheckMessage, CheckUsername, LogMessage


@Assistant.on_message(Filters.command(["remove","rm"]))
def handle_remove(bot: Assistant, message: Message) -> None:
            """
            Handle /remove command in supergroups. Admin feature.
            Remove message replied by this command.
            :param message: Message, triggered this event.
            """
            try:
                # Remove reported message...
                if message.reply_to_message:
                    bot.delete_messages(message.chat.id, message.reply_to_message.message_id)
                    logmsg =__msgs['as_amsgrm'].format(
                            message.from_user.first_name, 
                            message.from_user.id,
                            message.reply_to_message.from_user.first_name,
                            message.reply_to_message.from_user.id, 
                            message.chat.id,
                            message.chat.title
                          )
                    bot.send_message(
                      LOGGER_GROUP,
                      logmsg
                    )
                    Notify = __notify_admin(message, logmsg)
                    bot.send_message(Notify, logmsg)

            except Exception as e:
                LOGS.error(e, __msgs['as_admerr'])
                
