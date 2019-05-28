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
from assistant.utils.config import (__msgs, __score_user, __get_message_link)

import logging
import sys
import time

from assistant.utils.helpers import ParamExtractor, Ranges

from assistant.utils.settings import Settings, CheckMessage, CheckUsername



@Assistant.on_message(Filters.command("subscribe"))
def handle_subscribe(bot: Assistant, message: Message) -> None:
            """
            Handle /subscribe command in supergroups. Admin feature.
            Subscribe to specified chat to receive user reports.
            :param message: Message, triggered this event.
            """
            try:
                bot.send_message(
                  message.from_user.id, 
                  __msgs['as_repsub'].format(
                    message.chat.id, 
                    message.chat.title
                  ))
          
                __settings.add_watch(message.from_user.id, message.chat.id)
                __settings.save()
                
                
                bot.send_message(
                          LOGGER_GROUP,
                          __msgs['as_repsblg'].format(
                            message.from_user.first_name, 
                            message.from_user.id,
                            message.chat.id, 
                            message.chat.title
                          ))
                
            except:
                bot.reply_to(message, __msgs['as_replim'])
                

@Assistant.on_message(Filters.command("unsubscribe"))
def handle_unsubscribe(bot: Assistant, message: Message) -> None:
            """
            Handle /unsubscribe command in supergroups. Admin feature.
            Unsubscribe from specified chat.
            :param message: Message, triggered this event.
            """
            try:
                __settings.remove_watch(message.from_user.id, message.chat.id)
                __settings.save()
                
                bot.send_message(
                          LOGGER_GROUP,
                          __msgs['as_repusblg'].format(
                            message.from_user.first_name, 
                            message.from_user.id,
                            message.chat.id, 
                            message.chat.title
                          ))
                    
                
                bot.send_message(
                  message.from_user.id, 
                  __msgs['as_repunsb'].format(
                    message.chat.id, 
                    message.chat.title
                  ))
            except:
                LOGS.error(__msgs['as_admerr'])

                
                
@Assistant.on_message(Filters.command("report"))
def handle_report(bot: Assistant, message: Message) -> None:
            """
            Handle /start command in private chats.
            :param message: Message, triggered this event.
            """
            try:
                if message.reply_to_message:
                    bot.send_message(
            LOGGER_GROUP,
                        __msgs['as_replog'].format(message.from_user.first_name, message.from_user.id,
                                                        message.reply_to_message.from_user.first_name,
                                                        message.reply_to_message.from_user.id, message.chat.id,
                                                        message.chat.title))
                    repreq = ParamExtractor(message.text)
                    reason = repreq.param if repreq.index != -1 else __msgs['as_repnors']
                    for admin in __settings.get_watchers(message.chat.id):
                        try:
                            bot.send_message(admin, __msgs['as_repmsg'].format(message.from_user.first_name,
                                                                                         message.from_user.id, reason,
                                                                                         __get_message_link(
                                                                                             message)),
                                                  parse_mode='Markdown')
                        except:
                            LOGS.warning(__msgs['as_repns'].format(admin))

            except Exception as e:
                LOGS.info(e, __msgs['as_pmex'])

