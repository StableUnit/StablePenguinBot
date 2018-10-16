#!/usr/bin/env python3
import random

from first import first

from config import kek_text_name, kek_ids_name
from utils import bot, logger, get_user


# Executes /kek
def kek(message):
    your_kek = ''

    # Tries to gather data from the text files
    try:
        with open(kek_text_name, 'r', encoding='utf-8') as kek_text, open(kek_ids_name, 'r', encoding='utf-8') as kek_ids:
            type_of_kek = random.randint(1, 4)
            # 25% chance for a special kek
            if type_of_kek == 1:
                while your_kek in ['', ' ', '\n', ' \n']:
                    your_kek = random.choice(kek_ids.readlines()).strip()
                kek_type = first(['<audio>', '<photo>', '<sticker>', '<voice>'], key=lambda x: x in your_kek)
                file_id = your_kek.split(kek_type)[1].strip()

                # NOTE, media ids are unique for each bot
                if kek_type == '<audio>':
                    bot.send_audio(message.chat.id, file_id, reply_to_message_id=message.message_id)
                elif kek_type == '<photo>':
                    bot.send_photo(message.chat.id, file_id, reply_to_message_id=message.message_id)
                elif kek_type == '<sticker>':
                    bot.send_sticker(message.chat.id, file_id, reply_to_message_id=message.message_id)
                elif kek_type == '<voice>':
                    bot.send_voice(message.chat.id, file_id, reply_to_message_id=message.message_id)
            else:
                while your_kek in ['', ' ', '\n', ' \n']:
                    your_kek = random.choice(kek_text.readlines()).strip()
                bot.reply_to(message, str(your_kek).replace('<br>', '\n'))
            logger.info('User {0} got this kek: {1}'.format(get_user(message.from_user), your_kek))
    # If the text files are empty or non-existent
    except (OSError, IOError) as e:
        bot.reply_to(message, 'Can\'t access the kek files. Please, make sure they are in \'data\' directory and they are non-empty.')
        logger.info(e)
    except Exception as e:
        logger.exception(e)


# Executes /kek_add
def kek_add(message):
    add_text = ''
    add_id = ''

    # Tries to write new data to either a file with text or a file with ids
    try:
        with open(kek_text_name, 'a+', encoding='utf-8') as kek_text, open(kek_ids_name, 'a+', encoding='utf-8') as kek_ids:
            if getattr(message, 'text'):
                add_text = message.text
                kek_text.write('\n'+add_text)
            elif getattr(message, 'sticker'):
                add_id = '<sticker>{}'.format(message.sticker.file_id)
            elif getattr(message, 'audio'):
                add_id = '<audio>{}'.format(message.audio.file_id)
            elif getattr(message, 'voice'):
                add_id = '<voice>{}'.format(message.voice.file_id)
            elif getattr(message, 'photo'):
                add_id = '<photo>{}'.format(message.photo[0].file_id)
            
            if not(add_text or add_id):
                bot.reply_to(message, 'Sorry, couldn\'t add your kek. Only text, photos, stickers, audio and voice files '\
                                      'are supported by now.')
                logger.info('Couldn\'t add a kek')
                return

            kek_ids.write('\n'+add_id)

            logger.info('Admin {0} added this kek: {1}{2}'.format(get_user(message.from_user), add_text, add_id))
    # If the files are nonexistent
    except OSError as e:
        bot.reply_to(message, 'Can\'t access the kek files. Please, make sure that they are in \'data\' directory and they are non-empty.')
        logger.info(e)
    except Exception as e:
        logger.exception(e)