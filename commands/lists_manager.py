#!/usr/bin/env python3
import shelve

from telebot.apihelper import ApiException

import config
from utils import bot, logger, get_user


# Tries to send a message to every admin in the admins list
def send_to_admin(message, text, admins):
    try:
        bot.send_message(message.from_user.id, text.format(get_user(message.reply_to_message.from_user)))
        logger.info(text.format(get_user(message.reply_to_message.from_user)))
    except ApiException as e:
        if str(e.result) == r'<Response [403]>':
            reply_msg = text.format(get_user(message.reply_to_message.from_user)) + '\nI can\'t contact you. Please start a chat with me.'
            bot.reply_to(message, reply_msg)
            logger.error('Admin {} couldn\'t be reached'.format(admins[message.from_user.id]))


# Executes /wl_add
def wl_add(message):
    with shelve.open(config.data_name, 'c', writeback=True) as data:
        data['admins'] = config.admins_default if not data.get('admins') else data['admins']
        data['whitelist'] = {} if not data.get('whitelist') else data['whitelist']
        data['blacklist'] = {} if not data.get('blacklist') else data['blacklist']

        user_id = message.reply_to_message.from_user.id

        # Checks the user's list status and acts accordingly
        if user_id in data['whitelist']:
            send_to_admin(message, 'User {} is already whitelisted.', data['admins'])
            return
        if user_id in data['blacklist']:
            del data['blacklist'][user_id] 
        data['whitelist'][user_id] = [' '.join(get_user(message.reply_to_message.from_user).split(' ')[1:]), message.from_user.id]

        send_to_admin(message, 'User {} has been successfully added to the whitelist.', data['admins'])


# Executes /wl_del
def wl_del(message):
    with shelve.open(config.data_name, 'c', writeback=True) as data:
        data['admins'] = config.admins_default if not data.get('admins') else data['admins']
        data['whitelist'] = {} if not data.get('whitelist') else data['whitelist']

        user_id = message.reply_to_message.from_user.id

        # Checks the user's list status and acts accordingly
        if not (user_id in data['whitelist']):
            send_to_admin(message, 'User {} is already not whitelisted.', data['admins'])
            return 
        del data['whitelist'][user_id]

        send_to_admin(message, 'User {} has been successfully removed from the whitelist.', data['admins'])


# Executes /bl_add
def bl_add(message):
    with shelve.open(config.data_name, 'c', writeback=True) as data:
        data['admins'] = config.admins_default if not data.get('admins') else data['admins']
        data['whitelist'] = {} if not data.get('whitelist') else data['whitelist']
        data['blacklist'] = {} if not data.get('blacklist') else data['blacklist']

        user_id = message.reply_to_message.from_user.id

        # Checks the user's list status and acts accordingly
        if user_id in data['blacklist']:
            send_to_admin(message, 'User {} is already blacklisted.', data['admins'])
            return
        if user_id in data['whitelist']:
            del data['whitelist'][user_id] 
        data['blacklist'][user_id] = [' '.join(get_user(message.reply_to_message.from_user).split(' ')[1:]), message.from_user.id]

        bot.delete_message(chat_id=message.chat.id, message_id=message.reply_to_message.message_id)
        send_to_admin(message, 'User {} has been successfully added to the blacklist.', data['admins'])


# Executes /bl_del
def bl_del(message):
    with shelve.open(config.data_name, 'c', writeback=True) as data:
        data['admins'] = config.admins_default if not data.get('admins') else data['admins']
        data['blacklist'] = {} if not data.get('blacklist') else data['blacklist']

        user_id = message.reply_to_message.from_user.id

        # Checks the user's list status and acts accordingly
        if user_id not in data['blacklist']:
            send_to_admin(message, 'User {} is already not blacklisted.', data['admins'])
            return
        del data['blacklist'][user_id]

        send_to_admin(message, 'User {} has been successfully removed from the blacklist.', data['admins'])