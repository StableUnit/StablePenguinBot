#!/usr/bin/env python3
import shelve

import config
from utils import bot, print_dict


# Executes /get_admins
def get_admins(message):
    # Gets all human administrators of a chat
    admins_objects = [admin for admin in bot.get_chat_administrators(message.chat.id) if not admin.user.is_bot]
    # Gets every administrator's id, appends the default admins' ids
    admins_ids = [ad.user.id for ad in admins_objects] + [*config.admins_default]

    # Writes all admins' ids and information to data
    # Removes obsolete admins
    # Sends a message with the output
    with shelve.open(config.data_name, 'c', writeback=True) as data:
        data['admins'] = config.admins_default if not data.get('admins') else data['admins']

        for admin in admins_objects:
            admin_id = admin.user.id
            admin_data = '@'+admin.user.username if admin.user.username else admin.user.first_name
            if admin_id not in data['admins']:
                data['admins'][admin_id] = admin_data

        for admin_id in list(data['admins']):
            if admin_id not in admins_ids:
                del data['admins'][admin_id]

        bot.reply_to(message, 'List of bot\'s admins:\n{}'.format(print_dict(data['admins'])))