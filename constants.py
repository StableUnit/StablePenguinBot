#!/usr/bin/env python3


welcome_list = [
    'Welcome',
    'Hello',
    'Hi',
    'Greetings',
    'Good to have you on board',
    'Aloha',
    'Bonjour',
    'Nice to meet you',
    'Hola',
    'Konnichi wa'
]

welcomeback_list = [
    'Welcome back',
    'Hello again',
    'Cool to have you back',
    'We missed you'
]

start_text = 'This is a test of moderation bot for @elpinguinofrio.\n'\
                'ID of this chat: {} (copy/paste it to config file).\n\n'\
                'Please run /get_admins to get/update a list of this chat\'s admins.\n'\
                'For commands\' usage see /help.'

help_text = '<b>List of features of this bot:</b>\n'\
            ' – If a user joins this chat for the first time, the bot greets him/her and suggests to follow the rules.\n'\
            ' – If a user comes back to the chat, the bots welcomes him/her back.\n'\
            ' – If a user posts a link for the first time, the bot blocks it and sends to chat\'s admins for pre-moderation.\n'\
            ' <i>Please note, that the bot must have admin rights in order to function properly.</i>\n\n'\
            '<b>Admins can:</b>\n'\
            '  • accept user\'s message and add him to a whitelist;\n'\
            '  • decline user\'s message for this particular link if the user is not whitelisted;\n'\
            '  • add the user to a blacklist (permanently disable the user\'s ability to post any links to the chat);\n'\
            '  • permanently ban the user.\n\n'\
            '<b>List of commands:</b>\n'\
            '/start: outputs id of a current chat.\n'\
            '/wl_add * (in reply to a user\'s message): adds the user to the whitelist.\n'\
            '/wl_del * (in reply to a user\'s message): removes the user from the whitelist, so his future links will require pre-moderation.\n'\
            '/bl_add * (in reply to a user\'s message): adds the user to the blacklist.\n'\
            '/bl_del * (in reply to a user\'s message): removes the user from the blacklist, so his future links will require pre-moderation.\n'\
            '/uid * (in reply to user\'s message): outputs the user\'s Telegram id number.\n'\
            '/db_stat *: outputs the current state of a database of chat members, whitelisted and blacklisted members.\n'\
            '/db_flush \'parameter\' *: flushes any of the database\'s storages (\'members\'/\'admins\'/\'whitelist\'/\'blacklist\') or the entire database (\'all\').\n'\
            '/kek: outputs text and other memes.\n'\
            '/kek_add * (in reply to a user\'s message): adds user\'s message (if it\'s a text, a sticker, a photo, an audio or a voice file) to list of available keks.\n'\
            '/help: outputs this message.\n'\
            '<i>* = command is for chat\'s admins only.</i>\n\n\n'\
            'Contact: @arv_ego.'

db_storages = ['members', 'admins', 'whitelist', 'blacklist', 'all']

man = {'wl_add': '`Usage of /wl_add:`\n'\
                    '`    /wl_add  in response to a user\'s message`\n'\
                    '`Adds the user to the whitelist.`',
        'wl_del': '`Usage of /wl_del:`\n'\
                    '`    /wl_del  in response to a user\'s message`\n'\
                    '`Removes the user from the whitelist.`',
        'bl_add': '`Usage of /bl_add:`\n'\
                    '`    /bl_add  in response to a user\'s message`\n'\
                    '`Adds the user to the blacklist.`',
        'bl_del': '`Usage of /bl_del:`\n'\
                    '`    /bl_del  in response to a user\'s message`\n'\
                    '`Removes the user from the blacklist.`',
        'db_flush': '`Usage of /db_flush:`\n'\
                    '`    /db_flush <parameter>`\n'\
                    '`  parameter = {0}`\n\n'\
                    '`Flushes contents of the parameter in the database.`'.format('{'+' | '.join(db_storages)+'}'),
        'uid': '`Usage of /uid:`\n'\
                    '`    /uid  in response to a user\'s message`\n'\
                    '`Outputs the user\'s unique Telegram ID number.`',
        'kek_add': '`Usage of /kek_add:`\n'\
                    '`    /kek_add  in response to a user\'s message containing new kek`\n'\
                    '`Adds user\'s text to kek_texts file, adds user\'s sticker/photo/audio/voice file to kek_ids file.`'}