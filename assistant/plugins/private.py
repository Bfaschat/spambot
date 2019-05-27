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

from ..assistant import (Assistant, LOGS, LOGGER, LOGGER_GROUP, __schema, __settings, __msgs, __score_user, __get_message_link)


import logging
import sys
import time

from assistant.utils.helpers import ParamExtractor, Ranges

from assistant.utils.settings import Settings, CheckMessage, CheckUsername, LogMessage


    
  
  
  
  
    
class Bfasbot:
    def __check_restricted_user(self, message) -> bool:
        """
        Check if message was sent by a restricted user in supergroup.
        :param message: Message to check.
        :return: Check results.
        """
        usr = self.bot.get_chat_member(message.chat.id, message.from_user.id)
        return message.chat.type == 'supergroup' and usr.status == 'restricted'

    def __check_admin_feature(self, message) -> bool:
        """
        Check if message was sent by user with admin rights in supergroup.
        :param message: Message to check.
        :return: Check results.
        """
        usr = self.bot.get_chat_member(message.chat.id, message.from_user.id)
        return message.chat.type == 'supergroup' and (
                    message.from_user.id in self.__settings.admins or usr.status in ['creator', 'administrator'])

    def __check_owner_feature(self, message) -> bool:
        """
        Check if message was sent by bot admin in private chat.
        :param message: Message to check.
        :return: Check results.
        """
        return message.chat.type == 'private' and message.from_user.id in self.__settings.admins

    def __check_private_chat(self, message) -> bool:
        """
        Check if message was sent in private chat.
        :param message: Message to check.
        :return: Check results.
        """
        return message.chat.type == 'private'

    def __get_actual_username(self, message) -> str:
        """
        Get a real username of current message's sender.
        :param message: Message to check.
        :return: Real username.
        """
        return message.reply_to_message.new_chat_member.first_name if message.reply_to_message.new_chat_member else message.reply_to_message.from_user.first_name

    def __get_actual_userid(self, message) -> str:
        """
        Get a real ID of current message's sender.
        :param message: Message to check.
        :return: Real ID.
        """
        return message.reply_to_message.new_chat_member.id if message.reply_to_message.new_chat_member else message.reply_to_message.from_user.id

    def __check_message_forward(self, message) -> bool:
        """
        Check if current message was forwarded from another chat.
        :param message: Message to check.
        :return: Check results.
        """
        return message.forward_from or message.forward_from_chat


    def __check_message_entities(self, message) -> bool:
        """
        Check if current message contains restricted entitles.
        :param message: Message to check.
        :return: Check results.
        """
        if message.entities:
            for entity in message.entities:
                if entity.type in self.__settings.restent:
                    return True
        return False

    def __check_message_spam(self, message) -> bool:
        """
        Check if current message contains spam.
        :param message: Message to check.
        :return: Check results.
        """
        return self.__score_message(message) >= self.__settings.msggoal


    def __score_message(self, message) -> int:
        """
        Check current message and score it.
        :param message: Message to check.
        :return: Score results.
        """
        checker = CheckMessage(message, self.__settings)
        return checker.score

    def __notify_admin(self, message, logstr) -> None:
        """
        Notify admin about event if subscribed.
        :param admin: Original message, raised event.
        :param logstr: Message with useful information.
        """
        if message.from_user.id in self.__settings.get_watchers(message.chat.id):
            self.bot.send_message(message.from_user.id, logstr)


      
      
      
@Assistant.on_message(Filters.private)
def go(bot: Assistant, message: Message):
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

  
@Assistant.on_message(Filters.command("start"))
def gov(bot: Assistant, message: Message):
            """
            Handle /start command in private chats.
            :param message: Message, triggered this event.
            """
            print
            try:
                bot.send_message(message.chat.id, __msgs['as_welcome'])
            except Exception as e:
                LOGS.info(e, __msgs['as_pmex'])
 