from assistant.utils.helpers import ParamExtractor, Ranges
from ..assistant import (Assistant, __settings)
from assistant.utils.settings import Settings, CheckMessage, CheckUsername
from functools import wraps

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

    def __get_message_link(self, message) -> str:
        """
        Generate full URL to specified message.
        :param message: Message to process.
        :return: Full URL.
        """
        return 'https://t.me/{}/{}'.format(message.chat.username, message.reply_to_message.message_id)

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

    def __score_user(self, account) -> int:
        """
        Check current user's profile and score him.
        :param account: User ID (from API).
        :return: Score results.
        """
        checker = CheckUsername(account, self.__settings)
        return checker.score

    def __score_message(self, message) -> int:
        """
        Check current message and score it.
        :param message: Message to check.
        :return: Score results.
        """
        checker = CheckMessage(message, self.__settings)
        return checker.score


        
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



def __notify_admin(message, logstr) -> None:
        """
        Notify admin about event if subscribed.
        :param admin: Original message, raised event.
        :param logstr: Message with useful information.
        """
        if message.from_user.id in __settings.get_watchers(message.chat.id):
            return message.from_user.id

            
def __score_user(account, yes) -> None:
        """
        Check current user's profile and score him.
        :param account: User ID (from API).
        :return: Score results.
        """

        checker = CheckUsername(account, yes, __settings)
        return checker.score

def __get_message_link(message) -> None:
        """
        Generate full URL to specified message.
        :param message: Message to process.
        :return: Full URL.
        """
        return 'https://t.me/{}/{}'.format(message.chat.username, message.reply_to_message.message.id)
    
import re


def pass_db(chat_only=False, user_only=False):
    def pass_db_real(func):
        @wraps(func)
        def wrapped(bot, update, *args, **kwargs):
            usr = Usr.from_tg_user_object(update.effective_user)
            if not update.effective_chat.type == 'private':
                grp = Grp.from_tg_chat_object(update.effective_chat)
            else:
                grp = None
            if chat_only:
                return func(bot, update, grp, *args, **kwargs)
            if user_only:
                return func(bot, update, usr, *args, **kwargs)
            return func(bot, update, grp, usr, *args, **kwargs)
        return wrapped
    return pass_db_real


def dev_only(func):
    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in DEV:
            update.effective_message.reply_text(_("You are not a developer!"))
            return
        return func(bot, update, *args, **kwargs)
    return wrapped


def group_admin_only(func):
    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        user_id = update.effective_user.id
        chat_id = update.effective_chat.id
        if user_id not in group_admins(bot, chat_id):
            update.effective_message.reply_text(_("You are not an admin in this chat!"))
            return
        return func(bot, update, *args, **kwargs)
    return wrapped


def group_admins(bot, chat_id):
    return [admin.user.id for admin in bot.get_chat_administrators(chat_id)]


def if_group_admin(bot, chat_id, user_id):
    return user_id in group_admins(bot, chat_id)


def groups_only_response(func):
    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        if update.effective_chat.type != 'group' and update.effective_chat.type != 'supergroup':
            update.effective_message.reply_text(_("This command can only be used in groups!"))
            return
        return func(bot, update, *args, **kwargs)
    return wrapped


def pm_only_response(func):
    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        if update.effective_chat.type != 'private':
            update.effective_message.reply_text(_("This command can only be used in PM!"))
            return
        return func(bot, update, *args, **kwargs)
    return wrapped


def check_group_link(link):
    pattern = "^(http:\/\/|https:\/\/)?t(elegram)?\.(me|dog)\/joinchat\/[a-zA-Z0-9-_]{22}$"
    return re.match(pattern, link)


def link_markdown(name, link):
    return "[{}]({})".format(escape_md(name), link)      