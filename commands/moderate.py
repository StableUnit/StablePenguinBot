#!/usr/bin/env python3
from telebot import types
from telebot.apihelper import ApiException

import config
from utils import bot, logger, get_user, mention_replace


# Returns a stripped message of a judged user
# SPECIAL CASE: emojis in the message
def normalize_message(message):
    normalized = ''
    entity_text = ''
    entity_normalized = ''
    offsets = [0]
    lengths = [0]

    # Encodes the judged message to preserve possible emojis
    msg_enc = message.text.encode('utf-16le')

    # Strips the message in chunks: from entity to entity
    for entity in message.entities:
        # Keeps track of the entities position in the message 
        offsets.append(entity.offset)
        lengths.append(entity.length)

        # Decodes a chunk of the message to get contents of an entity
        # NOTE that in the encoded message every symbols comes with a pair, hence doubling the indices
        entity_text = msg_enc[2*offsets[-1]:2*(offsets[-1]+lengths[-1])].decode('utf-16le')

        # Strips the found link and other entities
        # rewrites it in the Markdown-friendly format 
        if entity.type == 'text_link':
            # Detects a hidden link
            entity_normalized = '[{1}]({0})'.format(entity.url, entity_text)
        elif entity.type == 'url':
            # Detects an ordinary link
            entity_normalized = '[{0}]({0})'.format(entity_text)
        elif entity.type == 'email':
            # Detects an email
            entity_normalized = '[{0}](mailto:{0})'.format(entity_text)
        elif entity.type == 'mention':
            # Detects a user/chat mention
            entity_normalized = '[@{0}](https://t.me/{0})'.format(entity_text[1:])
        elif entity.type == 'bold':
            # Detects a bolded text
            entity_normalized = '*{}*'.format(entity_text)
        elif entity.type == 'italic':
            # Detects an italicized text
            entity_normalized = '_{}_'.format(entity_text)
        elif entity.type == 'code':
            # Detects a coded text
            entity_normalized = '`{}`'.format(entity_text)
        elif entity.type == 'pre':
            # Detects a prettified text
            entity_normalized = '```{}```'.format(entity_text)
        else:
            # Detects other entities
            logger.info('Unrecognized entity of type {0}, offset {1} and length {2} detected. '\
                        'Adding as text'.format(entity.type, entity.offset, entity.length))
            entity_normalized = entity_text

        # Adds the stripped chunk to the final string
        normalized += msg_enc[2*(offsets[-2]+lengths[-2]):2*offsets[-1]].decode('utf-16le') + entity_normalized

    # Adds the part after the last entity
    normalized += msg_enc[2*(offsets[-1]+lengths[-1]):].decode('utf-16le')
    return normalized


# Forwards a judged user's message to every admin from admins list
# for pre-moderation.  Sends the according calls to the callback query handler
def require_approval(message, require_text, admins, too_long=False):
    admins_failed_contact = []

    # Tries to delete the original message from the main chat
    try:
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    # If bot hasn't got the rights, or the message has already been deleted
    # Aborts deletion
    except ApiException as e:
        if str(e.result) == r'<Response [400]>':
            bot.send_message(config.chat_id, 'ERROR!\nCan\'t delete the message! Please, grant me '\
                                             'admin rights in your group or make sure that the message has not been already deleted.')
            logger.error('Can\'t delete the message! Admin rights required or the message is already deleted!')
        else:
            print(e.result)
            logger.exception('ApiException.')

    # Initializes the main judgment keyboard
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    button_yes = types.InlineKeyboardButton(text='✅ Yes', callback_data='yes')
    button_no = types.InlineKeyboardButton(text='🚫 No', callback_data='no')
    button_untrusted = types.InlineKeyboardButton(text='❌ Restrict this user from posting any links', callback_data='untrusted')
    button_banned = types.InlineKeyboardButton(text='☠️ Ban this user', callback_data='banned')
    keyboard.add(button_yes, button_no)
    keyboard.add(button_untrusted)
    keyboard.add(button_banned)

    # Initializes the backup judgment keyboard for a case, when it's impossible
    # to get the user's date (message is too large to add anything)
    keyboard_backup = types.InlineKeyboardMarkup(row_width=2)
    button_yes_backup = types.InlineKeyboardButton(text='✅ Yes', callback_data='yes_huge')
    button_no_backup = types.InlineKeyboardButton(text='🚫 No', callback_data='no_huge')
    keyboard_backup.add(button_yes_backup, button_no_backup)

    # Initializes the judgment keyboard
    kb = keyboard_backup if too_long else keyboard

    # Tries to deliver the judgment message to all admins
    for admin in admins:
        try:
            bot.send_message(admin, require_text, reply_markup=kb)
        except ApiException as e:
            if str(e.result) == r'<Response [403]>':
                admins_failed_contact.append(admin)
                logger.error('Admin {} couldn\'t be reached'.format(admins[admin]))
                continue
            else:
                print(e.result)
                logger.exception('ApiException.')

    # If none of the admins were reached
    # sends an error message to the chat
    if admins_failed_contact == [*admins]:
        bot.send_message(config.chat_id, 'ERROR!\nCouldn\'t contact any of the admins.')
