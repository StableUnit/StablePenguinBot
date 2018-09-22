#!/usr/bin/env python3
import os


# To set your API tokens via environmental variables 
# add the following lines to your .bashrc and restart bash by running $SHELL:
# export PINGUINO_BOT_TOKEN="XXXXX:XXXXXXXXXXX"
# export PINGUINO_BOT_TEST_TOKEN="XXXXX:XXXXXXXXXXX"

default_bot = ''
bot = os.getenv('PINGUINO_BOT_TOKEN', default_bot)
bot_test = os.getenv('PINGUINO_BOT_TEST_TOKEN', default_bot)