#!/usr/bin/env python3
import random
import shelve

import config
import constants
from utils import bot, logger, get_user


# Sends a greeting to a new user(s)
# The greeting depends on whether a user has joined the chat for the first time or not
def welcome(message):
    new_members_names = []
    # By default assumes that the new user has joined for the first time
    first_joined = True

    # Gets the information about the current chat members in data
    with shelve.open(config.data_name, 'c', writeback=True) as data:
        data['members'] = {} if not data.get('members') else data['members']
        # Checks every new member
        # NOTE, you can invite multiple users at once
        for member in message.new_chat_members:
            # If new member is bot, skips
            if member.is_bot:
                continue

            # If new member has joined for the first time
            # adds him/her to the database
            if not member.id in data['members']:
                data['members'][member.id] = ' '.join(get_user(member).split(' ')[1:])
                logger.info('User {} has joined the chat for the first time and '\
                            'has been successfully added to the database'.format(get_user(member)))
            # Else, sets first_joined flag to False
            else:
                first_joined = False
                logger.info('User {} has rejoined the chat'.format(get_user(member)))
            new_members_names.append(member.first_name)
    # Welcomes every new member
    if new_members_names:
        welcoming_msg = '{0}, {1}!\nPlease consider the chat rules and enjoy your stay.'.format(random.choice(constants.welcome_list),\
                                    ', '.join(new_members_names)) if first_joined else '{0}, {1}.'.format(random.choice(constants.welcomeback_list),\
                                    ', '.join(new_members_names))
        bot.reply_to(message, welcoming_msg)
