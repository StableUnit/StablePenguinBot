#!/usr/bin/env python3
import logging
import re
import shelve
from datetime import datetime

import telebot

import config
import constants


# Initializes the bot
bot = telebot.TeleBot(config.bot_token, threaded=False)

# Initializes the logger
logger = telebot.logger
telebot.logger.setLevel(logging.INFO)


# Returns a user's info in
# 'ID First_name Last_name (@user_name)' format
# NOTE, that Last_name and user_name parameters are optional in Telegram
def get_user(user):
    user_info = '{0} {1}'.format(user.id, user.first_name)
    if user.last_name:
        user_info += ' {}'.format(user.last_name)
    if user.username:
        user_info += ' (@{})'.format(user.username)
    return user_info


# Returns a user's info in the Markdown-friendly format
def mention_replace(user_id, username):
    mention_md = ''
    user = re.sub(r'[(@)]', '', username)
    mention_md = '[{0}](tg://user?id={1})'.format(user, user_id)
    return mention_md


# Returns data from a dict in
# `key: value` format  OR  `key: value[0] [value[1]]` format if value is a list of length 2
# NOTE: on recent systems a shelve'd database can not be opened twice
def print_dict(dic, data=None):
    printed = ''

    if data:
        data['admins'] = config.admins_default if not data.get('admins') else data['admins']
        for k, v in dic.items():
            printed += '{0}: {1} [added by {2}]\n'.format(k, v[0], data['admins'][v[1]]) if type(v) == list else '{0}: {1}\n'.format(k, v)
    else:
        for k, v in dic.items():
            printed += '{0}: {1}\n'.format(k, v)
    return printed


# Sets a timer for a command that was called in the main chat
def command_with_delay(delay=10):
    def my_decorator(func):
        def wrapped(message):
            if message.chat.type != 'private':
                now = datetime.now().timestamp()
                diff = now - func.last_call if hasattr(func, 'last_call') else now
                if diff < delay:
                    logger.info('User {0} called {1} after {2} sec, delay is {3}'.format(get_user(message.from_user), func.__name__, round(diff), delay))
                    return

                func.last_call = now

            return func(message)

        return wrapped

    return my_decorator


# Checks whether a command was called properly
def validate_command(message, check_private=False, check_chat=False, check_length=False, check_rights=False, check_reply=False,\
                        check_forward=False):
    if check_private and message.chat.type == 'private':
        logger.info('User {0} called {1} in a private chat. Aborting'.format(get_user(message.from_user), message.text.split(' ')[0]))
        return False

    if check_chat and message.chat.id != config.chat_id:
        logger.info('We are not in our chat. Aborting')
        return False

    if check_length and len(message.text.split(' ')) > 1:
        logger.info('User {0} called {1} and something else. Aborting to prevent loophole'\
                    .format(get_user(message.from_user), message.text.split(' ')[0]))
        return False

    if check_rights:
        with shelve.open(config.data_name, 'c', writeback=True) as data:
            data['admins'] = config.admins_default if not data.get('admins') else data['admins']
            if message.from_user.id not in data['admins']:
                logger.info('User {0} called {1}. Access denied'.format(get_user(message.from_user), message.text.split(' ')[0]))
                return False

    if check_reply and getattr(message, 'reply_to_message') is None:
        bot.reply_to(message, constants.man['{}'.format(message.text.split(' ')[0][1:])], parse_mode='Markdown')
        logger.info('Admin {0} called {1} the wrong way'.format(get_user(message.from_user), message.text.split(' ')[0]))
        return False
    elif check_reply:
        if check_forward and getattr(message.reply_to_message, 'forward_from') is None:
            bot.reply_to(message, constants.man['{}'.format(message.text.split(' ')[0][1:])], parse_mode='Markdown')
            logger.info('Admin {0} called {1} the wrong way'.format(get_user(message.from_user), message.text.split(' ')[0]))
            return False

    return True


# Checks whether a judged message is 'pending'
def is_msg_pending(call, data, user_msg_id, user_id):
    if user_msg_id in data['msg_ids_pending']:
        return True

    if user_id in data['whitelist']:
        bot.reply_to(call.message, 'This message has already been reviewed and the user has '\
                                   'already been whitelisted by admin {}.'.format(data['admins'][data['whitelist'][user_id][1]]))
    elif user_id in data['blacklist']:
        bot.reply_to(call.message, 'This message has already been reviewed and the user has '\
                                   'been blacklisted by admin {}.'.format(data['admins'][data['blacklist'][user_id][1]]))
    
    return False


# Returns text in the HTML-friendly format
# OBSOLETE
def char_replace(text, mode='html'):
    if mode == 'html':
        text = text.replace('<', '&lt;')
        text = text.replace('>', '&gt;')
        text = text.replace('&', '&amp;')

    return text