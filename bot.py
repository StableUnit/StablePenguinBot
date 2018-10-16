#!/usr/bin/env python3
import os
import shelve
import time

from requests.exceptions import ConnectionError, ReadTimeout
from telebot.apihelper import ApiException

import config
import constants
from commands import welcome, moderate, get_admins, lists_manager, kek
from utils import *


# Handler for greeting a new chat member or several new chat members
# Greets new chat members
# Main chat only
@bot.message_handler(content_types=['new_chat_members'])
def welcoming_task(message):
    if not validate_command(message, check_chat=True):
        return

    welcome.welcome(message)


# Handler for /start
# Sends an info message containing the id of a current chat
# Must be called as a single message
@bot.message_handler(commands=['start'])
def start_msg(message):
    if not validate_command(message, check_length=True):
        return

    chat_id = message.chat.id
    bot.reply_to(message, constants.start_text.format(chat_id))
    logger.info('User {} called /start'.format(get_user(message.from_user)))


# Handler for /help
# Sends a message with explanation of the bot's features and commands
# Must be called as a single message
@bot.message_handler(commands=['help'])
def help_msg(message):
    if not validate_command(message, check_length=True):
        return

    bot.reply_to(message, constants.help_text, parse_mode='HTML')
    logger.info('User {} called /help'.format(get_user(message.from_user)))


# Handler for /get_admins
# Gathers the information about a current chat's administrators and saves it to the database
# Must be called in a supergroup chat
@bot.message_handler(commands=['get_admins'])
def get_my_admins(message):
    get_admins.get_admins(message)
    logger.info('User {} called /get_admins'.format(get_user(message.from_user)))


# Handler for /wl_add
# Adds a user to the whitelist
# Admins only; must be called as a reply
@bot.message_handler(commands=['wl_add'])
def wl_user(message):
    private_mode = False if message.chat.id == config.chat_id else True

    if not validate_command(message, check_rights=True, check_reply=True, check_forward=private_mode):
        return

    lists_manager.wl_add(message, is_forward=private_mode)


# Handler for /wl_del
# Removes a user from the whitelist
# Admins only; must be called as a reply
@bot.message_handler(commands=['wl_del'])
def uwl_user(message):
    private_mode = False if message.chat.id == config.chat_id else True

    if not validate_command(message, check_rights=True, check_reply=True, check_forward=private_mode):
        return

    lists_manager.wl_del(message, is_forward=private_mode)


# Handler for /bl_add
# Adds a user to the blacklist
# Admins only; must be called as a reply
@bot.message_handler(commands=['bl_add'])
def bl_user(message):
    private_mode = False if message.chat.id == config.chat_id else True

    if not validate_command(message, check_rights=True, check_reply=True, check_forward=private_mode):
        return

    lists_manager.bl_add(message, is_forward=private_mode)


# Handler for /bl_del
# Removes a user from the blacklist
# Admins only; must be called as a reply
@bot.message_handler(commands=['bl_del'])
def ubl_user(message):
    private_mode = False if message.chat.id == config.chat_id else True
    if not validate_command(message, check_rights=True, check_reply=True, check_forward=private_mode):
        return

    lists_manager.bl_del(message, is_forward=private_mode)


# Handler fot /uid
# Outputs a user's id
# Admins only; must be called as a reply
@bot.message_handler(commands=['uid'])
def uid_msg(message):
    if not validate_command(message, check_rights=True, check_reply=True):
        return

    bot.reply_to(message, '`{}`'.format(message.reply_to_message.from_user.id), parse_mode="Markdown")
    logger.info('Admin {} called /uid'.format(get_user(message.from_user)))


# Handler for /db_stat
# Outputs a state of the database
# Admins only
@bot.message_handler(commands=['db_stat'])
def stat_msg(message):
    if not validate_command(message, check_rights=True):
        return

    # Collects information from the data file
    with shelve.open(config.data_name, 'c', writeback=True) as data:
        data['admins'] = config.admins_default if not data.get('admins') else data['admins']
        data['members'] = {} if not data.get('members') else data['members']
        data['whitelist'] = {} if not data.get('whitelist') else data['whitelist']
        data['blacklist'] = {} if not data.get('blacklist') else data['blacklist']

        db_statistics = 'Members:\n{0}\nAdmins:\n{3}\nWhitelist:\n{1}\nBlacklist:\n{2}'.format(print_dict(data['members']),\
                                print_dict(data['whitelist'], data), print_dict(data['blacklist'], data), print_dict(data['admins'], data))

    # If the stat is too long for reading as a Telegram message
    # writes it to gen/db.txt and sends it as a file
    # NOTE that there can be up to 4096 symbols in a single Telegram message,
    # so a cut on 700 symbols is done purely for the cosmetic purposes
    if len(db_statistics) > 700:
        # If gen/ doesn't exist
        if not os.path.exists(config.gen_dir):
            os.mkdir(config.gen_dir)
        with open('{}db.txt'.format(config.gen_dir), 'w') as f:
            f.write(db_statistics)
        bot.send_document(message.chat.id, open('{}db.txt'.format(config.gen_dir), 'rb'),\
                    caption='Database is too big. Sending it as a file.',\
                    reply_to_message_id=message.message_id)
        logger.info('Admin {} requested database stats. Sending it as a file'.format(get_user(message.from_user)))
        return

    bot.reply_to(message, db_statistics)
    logger.info('Admin {} requested database stats'.format(get_user(message.from_user)))


# Handler for /db_flush
# Removes requested keys of data from the database
# Admins only; one argument required
@bot.message_handler(commands=['db_flush'])
def flush_msg(message):
    if not validate_command(message, check_rights=True):
        return

    # Erases keys (storages) of data depending on what follows after the command 
    with shelve.open(config.data_name, 'c', writeback=True) as data:
        data['admins'] = config.admins_default if not data.get('admins') else data['admins']
        # Sends the man in case of wrong usage
        if (len(message.text.split(' ')) != 2) or (message.text.split(' ')[1].lower() not in constants.db_storages):
            bot.reply_to(message, constants.man['db_flush'], parse_mode='Markdown')
            logger.info('Admin {} called /db_flush the wrong way'.format(get_user(message.from_user)))
            return

        if message.text.split(' ')[1].lower() != 'all':
            del data[message.text.split(' ')[1].lower()]
            bot.reply_to(message, 'Storage \'{}\' has been successfully flushed from the database.'\
                                    .format(message.text.split(' ')[1].lower()))
            logger.info('Storage {0} has been successfully flushed by admin {1}'\
                                    .format(message.text.split(' ')[1].lower(), get_user(message.from_user)))
        else:
            for item in [*data]:
                del data[item]
            bot.reply_to(message, 'Successfully flushed the entire database.')
            logger.info('Database has been successfully flushed by admin {}'.format(get_user(message.from_user)))


# Handler for /kek
# Sends keks.  'Nuff said
# Must be called as a single message
# Users can call it from the main chat only once in a span of 5 seconds
@bot.message_handler(commands=['kek'])
@command_with_delay(delay=5)
def kek_msg(message):
    if not validate_command(message, check_length=True):
        return

    kek.kek(message)


# Handler for /kek_add
# Adds text or media to kek data
# Admins only; must be called as a reply
@bot.message_handler(commands=['kek_add'])
def kekadd_msg(message):
    private_mode = False if message.chat.id == config.chat_id else True
    if not validate_command(message, check_rights=True, check_reply=True, check_forward=private_mode):
        return

    kek.kek_add(message.reply_to_message)


# Handler for messages with links in the main supergroup chat
# Analyzes the messages for links, triggers the admins on detection
@bot.message_handler(func=lambda message: message.entities and message.chat.id == config.chat_id)
def analyze_msg(message):
    entity_type = ''
    admins_failed_contact = []
    pending_msg_id = 0
    too_long = False

    if message.chat.type == 'private':
        return

    with shelve.open(config.data_name, 'c', writeback=True) as data:
        # Gets/Initializes information from/to the data file
        data['admins'] = config.admins_default if not data.get('admins') else data['admins']
        data['whitelist'] = {} if not data.get('whitelist') else data['whitelist']
        data['blacklist'] = {} if not data.get('blacklist') else data['blacklist']
        data['msg_ids_pending'] = [] if not data.get('msg_ids_pending') else data['msg_ids_pending']

        # If a blacklisted user posts a message that contains a link
        # deletes the user's message from the chat and forwards the message to the admins
        # If can't forward to any of the admins (none of the admins have a chat with the bot opened)
        # sends an error message to the chat
        if message.from_user.id in data['blacklist']:
            for entity in message.entities:
                if entity.type in ['url', 'text_link']:
                    entity_type = entity.type
                    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
                    break
            
            for admin in data['admins']:
                try:
                    if entity_type in ['url', 'text_link']:
                        bot.send_message(admin, 'Blacklisted user {0} attempted to post a message:\n{1}'.format(\
                                            get_user(message.from_user), moderate.normalize_message(message)))
                        logger.info('Blacklisted user {0} tried to post a link in message\n'\
                                    '\'{1}\'\nbut it has been successfully deleted.'\
                                    .format(data['blacklist'][message.from_user.id][0], message.text))
                except ApiException as e:
                    if str(e.result) in [r'<Response [400]>', r'<Response [403]>']:
                        admins_failed_contact.append(admin)
                        logger.exception(str(e.result)[11:14])
                        continue
                    else:
                        logger.exception('ApiException.')
            if admins_failed_contact == [*data['admins']]:
                bot.send_message(config.chat_id, 'ERROR!\nCouldn\'t contact any of the admins.')
            return

        # If a whitelisted user posts message that contains a link
        # do nothing
        if message.from_user.id in data['whitelist']:
            return

        # If a user has one or more entities (such as mentions, links, etc.)
        # scans it for links
        # Marks the message as `pending` and calls require_approval() on a link detection
        for entity in message.entities:
            if entity.type in ['url', 'text_link']:
                logger.info('Alert! User {0} has posted a message that contains a {1}.\n'\
                            'Triggering admins...'.format(get_user(message.from_user), entity.type))

                # Initializes the judgment message
                user_data = get_user(message.from_user)
                user_text = moderate.normalize_message(message)
                require_text = 'User {0} posted a link in the following message ({2}):\n\n{1}'\
                   '\n\nShould I approve it?'.format(user_data, user_text, message.message_id)

                # If the judgment message turns out to be too large to fit in one message
                # (i.e. the judgment message contains more than 4096 symbols)
                # fallbacks to the original message as is and flags 'too_long' for a backup keyboard 
                if len(require_text) > 4096:
                    require_text = message.text
                    pending_msg_id = message.text
                    too_long = True
                else:
                    pending_msg_id = message.message_id
                data['msg_ids_pending'].append(pending_msg_id)
                moderate.require_approval(message, require_text, data['admins'], too_long)
                break


# Handler for buttons from require_approval()
# Determines a judged user's fate according to the admins' verdict
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    approved_msg = ''
    # The judged user's ID is the second word of the judging message (call.message)
    # Case of a huge judged messages: 0 since it will not be used
    user_id = int(call.message.text.split(' ')[1]) if call.data not in ['yes_huge', 'no_huge'] else 0
    # The judged message's ID is in parentheses right before a line-break 
    # Similarly to above: in case of a huge judged message just go with 0
    user_msg_id = int(call.message.text.split(' message (')[1].split('\n')[0][:-2]) if\
                    call.data not in ['yes_huge', 'no_huge'] else 0
    # Gets full information about the judged user
    # If there's a username included, mention_replace() rewrites it in the Markdown-friendly format
    user_data_db = ' '.join(call.message.text.split(' posted a link')[0].split(' ')[2:]) if\
                            call.data not in ['yes_huge', 'no_huge'] else ''
    if '@' in user_data_db.split(' ')[-1]:
        user_data = user_data_db.replace(user_data_db.split(' ')[-1], '({})'.format(\
            mention_replace(int(call.message.text.split(' ')[1]), user_data_db.split(' ')[-1])))
    else:
        user_data = user_data_db
    addedbyadmin_id = int(call.message.chat.id)

    # Gets/Initializes information from/to the data file
    with shelve.open(config.data_name, 'c', writeback=True) as data:
        data['whitelist'] = {} if not data.get('whitelist') else data['whitelist']
        data['blacklist'] = {} if not data.get('blacklist') else data['blacklist']
        data['admins'] = config.admins_default if not data.get('admins') else data['admins']
        data['msg_ids_pending'] = [] if not data.get('msg_ids_pending') else data['msg_ids_pending']

        # If an admin clicked 'Yes'
        if call.data == 'yes':
            # Checks that the judged message is still 'pending' and the judged user's list status
            if not is_msg_pending(call, data, user_msg_id, user_id):
                return

            # If the user was added to the whitelist after he/she posted the judged message
            # sends that message
            if user_id in data['whitelist']:
                bot.reply_to(call.message, 'Message has been approved. This user has '\
                                           'already been whitelisted by admin {}.'.format(data['admins'][data['whitelist'][user_id][1]]))
                data['msg_ids_pending'].remove(user_msg_id)
                msg_data = '\n\n'.join(call.message.text.split('\n\n')[1:-1])
                approved_msg = 'User {0} posted:\n{1}'.format(user_data, msg_data)
                bot.send_message(config.chat_id, approved_msg, parse_mode='Markdown')
                logger.info('Message has been approved by the admin.')
                return
            # If the user was added to the blacklist after he/she posted the judged message
            # blocks the approval
            elif user_id in data['blacklist']:
                bot.reply_to(call.message, 'Can\'t approve: this user has '\
                                           'been blacklisted by admin {}.'.format(data['admins'][data['blacklist'][user_id][1]]))
                data['msg_ids_pending'].remove(user_msg_id)
                return
            # Removes the judged message from the 'pending' queue
            data['msg_ids_pending'].remove(user_msg_id)

            # If the judged user is not in any list
            # adds him/her to the whitelist and resends the approved message to the chat
            data['whitelist'][user_id] = [user_data_db, addedbyadmin_id]
            msg_data = '\n\n'.join(call.message.text.split('\n\n')[1:-1])
            approved_msg = 'User {0} posted:\n{1}'.format(user_data, msg_data)
            bot.send_message(config.chat_id, approved_msg, parse_mode='Markdown')
            logger.info('Message has been approved by the admin.')
            bot.reply_to(call.message, '{} has been added to the whitelist.'.format(call.message.text.split(' posted a link')[0]))
            logger.info('User {0} {1} has been successfully added to the whitelist.'.format(user_id, user_data_db))

        # If an admin clicked 'No'
        elif call.data == 'no':
            # Checks that the judged message is still 'pending' and the judged user's list status
            if not is_msg_pending(call, data, user_msg_id, user_id):
                return

            # If the judged message is still 'pending'
            # removes it from the queue and does nothing
            bot.reply_to(call.message, 'Message has been declined.')
            data['msg_ids_pending'].remove(user_msg_id)
            logger.info('Message has been disapproved by the admin.')

        # If an admin clicked 'Restrict'
        elif call.data == 'untrusted':
            # Checks that the judged message is still 'pending' and the judged user's list status
            if not is_msg_pending(call, data, user_msg_id, user_id):
                return

            # If the judged message is still 'pending'
            # checks the judged user status
            if user_id in data['blacklist']:
                bot.reply_to(call.message, '{} has been added to the blacklist.'.format(call.message.text.split(' posted a link')[0]))
                data['msg_ids_pending'].remove(user_msg_id)
                logger.info('User {0} {1} has been successfully added to the blacklist'.format(user_id, user_data_db))
                return
            # If the user is whitelisted
            # aborts the decline
            elif user_id in data['whitelist']:
                bot.reply_to(call.message, 'This user is whitelisted. Call /wl_del command first.')
                data['msg_ids_pending'].remove(user_msg_id)
                logger.info('User {0} {1} has not been added to the blacklist, for he/she is whitelisted'.format(user_id, user_data))
                return

            # Removes the judged message from the queue and adds the judged user to the blacklist 
            data['blacklist'][user_id] = [user_data_db, addedbyadmin_id]
            bot.reply_to(call.message, '{} has been added to the blacklist.'.format(call.message.text.split(' posted a link')[0]))
            logger.info('User {0} {1} has been successfully added to blacklist'.format(user_id, user_data_db))
        
        # If an admin clicked 'Ban'
        elif call.data == 'banned':
            # Checks that the judged message is still 'pending'
            if user_msg_id not in data['msg_ids_pending']:
                bot.reply_to(call.message, 'This user has been already dealt with.')
                return

            # Attempts to ban the judged user.  If the user is an admin or has been already banned
            # or the bot has no admin rights, aborts
            try:
                if user_id in data['admins']:
                    bot.reply_to(call.message, 'This user is an admin. Admins can not be banned.')
                    data['msg_ids_pending'].remove(user_msg_id)
                    return
                bot.restrict_chat_member(chat_id=config.chat_id, user_id=user_id)
                data['msg_ids_pending'].remove(user_msg_id)
                logger.info('User {0} {1} has been successfully banned'.format(user_id, user_data_db))
            except ApiException as e:
                if str(e.result) == r'<Response [400]>':
                    bot.send_message(config.chat_id, 'ERROR!\nCan\'t delete the message! Please, grant me admin rights '\
                                                     'or make sure that the user is not yet banned.')
                    logger.error('Can\'t delete the message! Admin rights required or the user is already banned!')
                else:
                    print(e.result)
                    logger.exception('ApiException.')

        # Two special cases for large messages
        elif call.data == 'yes_huge':
            if call.message.text not in data['msg_ids_pending']:
                bot.reply_to(call.message, 'This message has been already dealt with.')
                return
            data['msg_ids_pending'].remove(call.message.text)
            bot.send_message(config.chat_id, call.message.text)
            bot.reply_to(call.message, 'This huge message has been approved.')
            logger.info('Ridiculously huge message has been approved by admin {}'.format(data['admins'][call.message.chat.id]))

        elif call.data == 'no_huge':
            if call.message.text not in data['msg_ids_pending']:
                bot.reply_to(call.message, 'This message has been already dealt with.')
                return
            data['msg_ids_pending'].remove(call.message.text)
            bot.reply_to(call.message, 'This huge message has been declined.')
            logger.info('Ridiculously huge message has been declined by admin {}'.format(data['admins'][call.message.chat.id]))


while __name__ == '__main__':
    try:
        bot.polling(none_stop=True, interval=1, timeout=60)
    except ConnectionError:
        logger.exception('ConnectionError')
        time.sleep(15)
    except ReadTimeout:
        logger.exception('ReadTimeout')
        time.sleep(10)
    except KeyboardInterrupt:
        logger.info('Bye')
        os._exit(0)
    except Exception as ex:
        logger.exception(ex)
        time.sleep(60)