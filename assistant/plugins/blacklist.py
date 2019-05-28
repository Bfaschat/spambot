
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


        
@Assistant.on_message(Filters.command("sw_add"))
def handle_swadd(bot: Assistant, message: Message) -> None:
            """
            Handle /sw_add command in private chats. Allow admins to ask add a new
            stopword to the list of restricted words for new users. Restricted command.
            :param message: Message, triggered this event.
            """
            try:
                swreq = ParamExtractor(message.text)
                if swreq.index != -1:
                    try:
                        bot.send_message(
                          LOGGER_GROUP,
                          __msgs['as_swadd'].format(
                            message.from_user.first_name, 
                            message.from_user.id,
                            swreq.param
                    ))
                        __settings.add_stopword(swreq.param)
                        __settings.save()
                        
                        bot.send_message(
                          message.chat.id,
                          __msgs['as_swuadd'].format(
                            swreq.param
                                         ))
                        
                    except:
                        bot.send_message(message.chat.id, __msgs['as_swerr'])
                else:
                    bot.send_message(message.chat.id, __msgs['as_swpm'])
            except:
                LOGS.error(__msgs['as_pmex'])
                

                
                
@Assistant.on_message(Filters.command("sw_remove"))
def handle_swremove(bot: Assistant, message: Message) -> None:
            """
            Handle /sw_remove command in private chats. Allow admins to ask remove
            stopword from the list of restricted words for new users. Restricted command.
            :param message: Message, triggered this event.
            """
            try:
                swreq = ParamExtractor(message.text)
                if swreq.index != -1:
                    try:
                        bot.send_message(
                          LOGGER_GROUP, 
                          __msgs['as_swrem'].format(
                            message.from_user.first_name, 
                            message.from_user.id,
                            swreq.param
                          ))
                    
                        __settings.remove_stopword(swreq.param)
                        __settings.save()
                        
                        bot.send_message(
                          message.chat.id, 
                          __msgs['as_swurem'].format(
                            swreq.param
                          ))
                        
                    except:
                        bot.send_message(message.chat.id, __msgs['as_swerr'])
                else:
                    bot.send_message(message.chat.id, __msgs['as_swpm'])
            except:
                LOGS.error(__msgs['as_pmex'])

                 
                
                
@Assistant.on_message(Filters.command("sw_list"))
def handle_swlist(bot: Assistant, message: Message) -> None:
            """
            Handle /sw_list command in private chats. Allow admins get full list
            of restricted words for new users. Restricted command.
            :param message: Message, triggered this event.
            """
            try:
                if message.from_user.id in __settings.admins:
                    try:
                        bot.send_message(
                          LOGGER_GROUP, 
                          __msgs['as_swlist'].format(
                            message.from_user.first_name,
                            message.from_user.id
                          ))
                  
                        bot.send_message(
                          message.chat.id,
                          __msgs['as_swulist'].format(', '.join(
                            __settings.stopwords
                          ) ))
                    
                    except:
                        bot.send_message(message.chat.id, __msgs['as_swerr'])
                else:
                    bot.send_message(message.chat.id, __msgs['as_unath'])
            except:
                LOGS.error(__msgs['as_pmex'])