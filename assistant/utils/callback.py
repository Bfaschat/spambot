from pyrogram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove, ForceReply


def pyro_keyboard(user_id, confirmed):  
    data = list()
    data.append('cnf=' + str(int(confirmed)))
    data.append('user_id=' + str(int(user_id)))
    data = '%'.join(data)
    print(data)
    kb = [[
            InlineKeyboardButton(
                text=('🤖' + ' Press this button to participate'),
                callback_data=b'act=unres%' + data.encode('UTF-8')
            )
        ]]
    return kb  
  
  