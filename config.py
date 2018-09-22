#!/usr/bin/env python3
import argparse
import os

import tokens


bot_token = tokens.bot    # set your token in .bashrc (see tokens.py)
chat_id = -1001165738284  # insert your chat's id here (see the output of /start)
admins_default = {        # insert default admins in `id: '@username'` or `id: 'name'` format
    207275675: '@arv_ego',
    547598841: '@elpinguinofrio'
}

path_dir = os.path.dirname(os.path.abspath(__file__))
gen_dir = path_dir + '/gen/'
data_name = path_dir + '/data/data'
kek_text_name = path_dir + '/data/kek_text.txt'
kek_ids_name = path_dir + '/data/kek_ids.txt'

# Adds an option of running the bot in debug mode right from a console:
# `$ python3 bot.py --debug`  OR  `$ python3 bot.py -d`
parser = argparse.ArgumentParser()
parser.add_argument('-d', '--debug', help='runs bot in debug mode', action='store_true')
args = parser.parse_args()
if args.debug:
    bot_token = tokens.bot_test  # set your token in .bashrc (see tokens.py)
    chat_id = -1001396588805     # 'Testing ElPinguino's bot' chat's id
    admins_default = {
        207275675: '@arv_ego'
    }

    print('Running bot in debug mode')