from time import time

from pyrogram import (CallbackQuery, Emoji, Filters, InlineKeyboardButton,
                      InlineKeyboardMarkup, Message)
from ..assistant import (Assistant, LOGS, LOGGER, LOGGER_GROUP, __schema, __settings, __msgs, __score_user, __get_message_link)
from assistant.utils.callback import pyro_keyboard
from pyrogram import Client, Emoji, Filters
from assistant.utils.settings import Settings, CheckMessage, CheckUsername, LogMessage

TARGET = "bfas237off"  # Target chat. Can also be a list of multiple chat ids/usernames
MENTION = "[{}](tg://user?id={})"  # User mention markup
MESSAGE = "{} Welcome to [Bfas237 offtopic](https://docs.pyrogram.org/)'s group chat {}!"  # Welcome message

# Filter in only new_chat_members updates generated in TARGET chat
@Assistant.on_message(Filters.chat(TARGET) & Filters.new_chat_members)
def welcome(bot: Assistant, message: Message):
  
            """
            Handle join messages in supergroups. Perform some actions
            on newly joined users.
            :param message: Message, triggered this event.
            """
            
            try:
                # Check user profile using our score system
                for new_person in message.new_chat_members:
                    print(new_person.first_name, new_person.last_name, new_person.id)
                    score = __score_user(new_person.first_name, new_person.id)

                    LOGS.info(
                    __msgs['as_alog'].format(new_person.first_name, 
                                             new_person.id,
                                             message.chat.id, 
                                             message.chat.title, 
                                             score
                                            )
                    )
                    try:
                      # If user get score >= 100 - ban him, else - restrict...
                      if score >= __settings.nickgoal:
                          # Delete join message and ban user permanently...
                          bot.delete_message(message.chat.id, message.message_id)
                          
                          bot.kick_chat_member(message.chat.id, new_person.id)
                          # Also ban user who added him...
                          if message.from_user.id != new_person.id:
                            
                              bot.kick_chat_member(message.chat.id, message.from_user.id)
                              
                              LOGS.warning(__msgs['as_banned'].format(
                                new_person.first_name,                           
                                new_person.id, 
                                score, 
                                message.chat.id, 
                                message.chat.title
                              )
                                          )
                                          
        
                      else:
                        # Limit users reached half-goal permanently (in Bot API - 366 days)...
                        limtime = 31622400 if score >= __settings.nickgoal / 2 else __settings.bantime
                        # Restrict all new users for specified in config time...
                        bot.restrict_chat_member(message.chat.id, 
                                                     new_person.id,
                                                      until_date=int(time()) + limtime,
                                                      can_send_messages=False,
                                                     can_send_media_messages=False,
                                                      can_send_other_messages=False,
                                                     can_add_web_page_previews=False)
                        
                        mention = MENTION.format(new_person.first_name, new_person.id)
                        greeting = MESSAGE.format(Emoji.SPARKLES, mention)
                        
                        kb = pyro_keyboard(user_id=new_user.id, confirmed=False)  
                        reply_markups = InlineKeyboardMarkup(kb)
                            
                        message.reply(
                              text=greeting + "\n\nTo be able to participate, please press the button below " + Emoji.DOWN_ARROW,
                              disable_web_page_preview=True,
                              reply_markup=reply_markups

                            )

                  
                    except Exception as e:
                        LOGS.error(e, 
                                   __msgs['as_restex'].format(message.from_user.id,
                                                              message.chat.id,
                                                              message.chat.title
                                                             )
                                  )
            except Exception as e:
                LOGS.error(e, 
                           __msgs['as_joinhex']
                          )
    
        
        

@Assistant.on_callback_query()
def callback_query_pyro(bot: Assistant, cb: CallbackQuery):
    
    data = cb.data.encode('UTF-8') 
    
    user_id = cb.from_user.id 
    
    chat_id = cb.message.chat.id 
    dataid = cb.id
    username = cb.message.chat.username
    data = data.split(b'%') 
    chat_id = str(chat_id)
    action = ''
    confirmed = False
    
    for elem in data:
        name, *args = elem.split(b'=') 
        if name == b'act':
            action = args[0]
        elif name == b'user_id':
            userid = int(args[0])
        elif name == b'cnf':
            confirmed = bool(int(args[0]))
            
    if action == b"unres":
        if user_id == int(userid):
                if not confirmed:
                    bot.restrict_chat_member(
                      chat_id=username,
                      user_id=int(userid),
                      until_date=0,
                      can_send_messages=True,
                      can_send_media_messages=True,
                      can_send_other_messages=True,
                      can_add_web_page_previews=True,
                      can_send_polls=True)
                    
                    cb.answer("Your restriction were lifted, welcome!")
              
                    bot.edit_message_text(
                      chat_id=username,
                      message_id=cb.message.message_id,
                      text=cb.message.text.markdown.split('\n')[0],
                      disable_web_page_preview=True,
                      reply_markup=None)
                    NEW_USER_LOG = (
                      "[{0.reply_to_message.from_user.first_name}](tg://user?id={0.reply_to_message.from_user.id}) "
                      " Just got verified and joined \"[{0.chat.title}](t.me/c/{1}/{2})\".")
                bot.send_message(
            LOGGER_GROUP, NEW_USER_LOG.format(cb.message,
                str(cb.message.chat.id).replace("-100", ""),
                str(cb.message.message_id)))
            
        else:
            cb.answer("😏 That wasn't for you!", show_alert=True)
                


@Assistant.on_message(Filters.chat('bfas237off') & Filters.command("un", "!"))
def unrestrict_members(bot: Assistant, message: Message):
    print(message)
    caller = bot.get_chat_member(message.chat.id, message.from_user.id)
    if caller.status is 'creator' or caller.status is 'administrator' and caller.permissions.can_restrict_members:
        bot.restrict_chat_member(
            chat_id=message.chat.id,
            user_id=message.reply_to_message.from_user.id,
            until_date=0,
            can_send_messages=True,
            can_send_media_messages=True,
            can_send_other_messages=True,
            can_add_web_page_previews=True,
            can_send_polls=True)
        message.reply("Restrictions lifted " + Emoji.OK_HAND)
