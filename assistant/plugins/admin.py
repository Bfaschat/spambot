
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
from assistant.utils.config import (check_restricted_user, __score_message, __check_message_entities, __check_message_spam, __check_message_forward, group_admin_only, __get_actual_username, __get_actual_userid, __msgs, __score_user, __get_message_link, __notify_admin)
 
import logging
import sys
import time

from assistant.utils.helpers import ParamExtractor, Ranges

from assistant.utils.settings import Settings, CheckMessage, CheckUsername

ADMINTITLE = "**Admins in \"{}\"**\n\n"
ADMINCREATOR = (
    '╔ **Creator**\n'
    '╚ `{} `[{}](tg://user?id={})\n\n')
ADMINLISTLASTBOT = '╚ `{} `[{}](tg://user?id={}) `ᴮᴼᵀ`\n'
ADMINLISTLAST = '╚ `{} `[{}](tg://user?id={})\n'
ADMINLISTBOT = '╠ `{} `[{}](tg://user?id={}) `ᴮᴼᵀ`\n'
ADMINLIST = '╠ `{} `[{}](tg://user?id={})\n'

MEMBER_INFO = (
    "╔═════════\n"
    "╠ **{}**\n"
    "╠ Member Count\n"
    "╠═════════\n"
    "╠ Total: `{}`\n"
    "╠═════════\n"
    "╠ Admins: `{}`\n"
    "╠ Members: `{}`\n"
    "╠ Bots: `{}`\n"
    "╠═════════\n"
    "╠ Deleted Accounts: `{}`\n"
    "╚═════════")

CHAT_INFO = (
    "╔═════════\n"
    "║ **Overview Chatlist**\n"
    "║ Total Chats: {}\n"
    "╠═════════\n"
    "║ Private Chats: {}\n"
    "║ Bots: {}\n"
    "║ Groups: {}\n"
    "║ Supergroups: {}\n"
    "║ Channels: {}\n"
    "╠═════════\n"
    "║ Time elapsed: {}\n"
    "╚═════════")

UNREAD_INFO = (
    "╔═════════\n"
    "║ **Unread Messages**\n"
    "║ Total: `{total_msg}` in {total_chats} Chats\n"
    "╠═════════\n"
    "║ Messages from\n"
    "║ `{msg_private}` msg - {chat_private} Users\n"
    "║ `{msg_bots}` msg - {chat_bots} Bots\n"
    "║ `{msg_groups}` msg - {chat_groups} Groups\n"
    "║ `{msg_super}` msg - {chat_super} Supergroups\n"
    "║ `{msg_channel}` msg - {chat_channel} Channels\n"
    "╚═════════")

@Assistant.on_message(Filters.command("mem", "."))
@group_admin_only
def get_members(bot: Assistant, message: Message):
    if message.chat.type == 'private':
        message.delete()

    else:
        total = 0
        admins = 0
        members = 0
        bots = 0
        deleted = 0
        hp =  [x.user.id for x in bot.iter_chat_members(message.chat.id) if x.status in ['restricted']]
        if 197005208 in hp:
          print(True)
        else:
          print(False)
        print(hp)
        for member in bot.iter_chat_members(message.chat.id):
            total += 1
            if member.user.is_bot:
                bots += 1
            elif member.user.is_deleted:
                deleted += 1
            elif member.status in ['creator', 'administrator']:
                admins += 1
            elif not member.user.is_deleted and not member.user.is_bot:
                members += 1

        member_count_text = MEMBER_INFO.format(
            message.chat.title,
            total,
            admins,
            members,
            bots,
            deleted
        )

        message.reply(member_count_text)
        LogMessage(member_count_text)

        
        
@Assistant.on_message(Filters.command(['ban', 'block']))
def handle_banuser(bot: Assistant, message: Message) -> None:
            """
            Handle /ban command in supergroups. Admin feature.
            Remove message replied by this command and permanently ban it's sender.
            :param message: Message, triggered this event.
            """
            try:
                if message.reply_to_message:
                    username = __get_actual_username(message)
                    userid = __get_actual_userid(message)
                    if message.from_user.id != userid:
                        bot.kick_chat_member(
                          message.chat.id, 
                          userid
                        )
                      
                        bot.delete_message(
                          message.chat.id, 
                          message.reply_to_message.message_id
                        )
                        
                        logmsg = __msgs['as_aban'].format(
                          message.from_user.first_name, 
                          message.from_user.id,
                          username, 
                          userid, 
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

                
                
@Assistant.on_message(Filters.command(['restrict', 'mute']))
def handle_muteuser(bot: Assistant, message: Message) -> None:
            """
            Handle /restrict command in supergroups. Admin feature.
            Permanently restrict sender of message replied by this command.
            :param message: Message, triggered this event.
            """
            try:
                if message.reply_to_message:
                    username = __get_actual_username(message)
                    userid = __get_actual_userid(message)
                    if message.from_user.id != userid:
                        mutereq = ParamExtractor(message.text)
                        mutetime = int(time.time()) + (int(mutereq.param) * 86400 if mutereq.index != -1 else 0)
                        
                        bot.restrict_chat_member(
                          message.chat.id, userid, 
                          until_date=mutetime,
                          can_send_messages=False, 
                          can_send_media_messages=False,
                          can_send_other_messages=False, 
                          can_add_web_page_previews=False
                        )
                        
                        logmsg = __msgs['as_amute'].format(
                          message.from_user.first_name, 
                          message.from_user.id,
                          username, 
                          userid, 
                          message.chat.id, 
                          message.chat.title,
                          mutetime if mutereq.index != -1 else 'forever'
                        )
                        
                        bot.send_message(
                      LOGGER_GROUP,
                      logmsg
                    )
                        Notify = __notify_admin(message, logmsg)
                        bot.send_message(Notify, logmsg)
                        
            except Exception as e:
                LOGS.error(e, __msgs['as_admerr'])
                
@Assistant.on_message(Filters.command(['unrestrict', 'un', 'unban']))
def handle_unrestrict(bot: Assistant, message: Message) -> None:
                
            """
            Handle /unrestrict and /unban commands in supergroups. Admin feature.
            Remove all restrictions on sender of message replied by this command
            or specified in mandatory Telegram user ID.
            :param message: Message, triggered this event.
            """
            try:
                if message.reply_to_message:
                    bot.restrict_chat_member(
                      message.chat.id, 
                      message.reply_to_message.from_user.id,
                      can_send_messages=True, 
                      can_send_media_messages=True,
                      can_send_other_messages=True, 
                      can_add_web_page_previews=True
                    )
                
                    logmsg = __msgs['as_aunres'].format(
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
                else:
                    unbanreq = ParamExtractor(message.text)
                    if unbanreq.index != -1:
                        userreq = bot.get_chat_member(
                          message.chat.id, 
                          int(unbanreq.param)
                        )
                        
                        bot.unban_chat_member(message.chat.id, userreq.user.id)
                        logmsg = __msgs['as_aunban'].format(
                          message.from_user.first_name, 
                          message.from_user.id,
                          userreq.user.first_name, 
                          userreq.user.id,
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