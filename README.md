# Stable Penguin Bot

Link pre-moderation bot for StableUnit telegram chat

Runs on Python 3.5, install all dependencies by executing:
```sh
pip3 install -r requirements.txt
```

### Installation and setup
* Search for @BotFather in Telegram and start it
* Create a new bot by sending command `/newbot`
* Type and send your new bot's public name (`StablePenguinBot` for example)
* Type and send your new bot's user name (`StablePenguinBot` for example)
* BotFather will reply with a token like `XXXXXXXXX:XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX`
* Paste that token in your `.bashrc` like so:
```sh
export PINGUINO_BOT_TOKEN="PASTE:THETOKENHERE"
```
and restart bash
* Alternatively, you can paste it raw in `tokens.py` on your local machine
* Run the bot in debug mode: `python3 bot.py --debug` and add it to your chat
* Send the `/start` command, bot will reply with your chat's ID
* Paste it (with `-`!) to `chat_id` variable in `config.py`
* Restart the bot in normal mode.

### List of features
* If a user joins this chat for the first time, the bot greets him/her and suggests to follow the rules
* If a user comes back to the chat, the bots welcomes him/her back
* If a user posts message with a link for the first time, the bot blocks it and sends to chat's admins for pre-moderation.
_Please note, that the bot must have admin rights in order to function properly._

### Admins can
* accept user\'s message and add him to a whitelist;
* decline user\'s message for this particular link if the user is not whitelisted;
* add the user to a blacklist (permanently disable the user\'s ability to post any links to the chat);
* permanently ban the user.

### List of commands
* `/start`: outputs id of a current chat
* `/wl_add` \* (in reply to a user\'s message): adds the user to the whitelist
* `/wl_del` \* (in reply to a user\'s message): removes the user from the whitelist, so his future links will require pre-moderation
* `/bl_add` \* (in reply to a user\'s message): adds the user to the blacklist
* `/bl_del` \* (in reply to a user\'s message): removes the user from the blacklist, so his future links will require pre-moderation
* `/uid` \* (in reply to user\'s message): outputs the user\'s Telegram id number
* `/db_stat` \*: outputs the current state of a database of chat members, whitelisted and blacklisted members
* `/db_flush 'parameter` \*: flushes any of the database\'s storages (`'members'/'admins'/'whitelist'/'blacklist'`) or the entire database (`'all'`)
* `/kek`: outputs text and other memes
* `/kek_add` \* (in reply to a user\'s message): adds user\'s message (if it\'s a text, a sticker, a photo, an audio or a voice file) to list of available keks
* `/help`: outputs help.

_\* = command is for chat\'s admins only._



### Contributors
[![](https://img.shields.io/badge/Artemy_Gevorkov-%40arv__ego-blue.svg?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAYAAACNiR0NAAAEbklEQVQ4y62US2xUdRjFf%2F%2F%2FfUynnXaGKW15FHnVKm8SRCFB3ZhYRVQSISHKBhKjK2JiTIyuXJC40oUrY%2BJGTZSABomiC0kUFYEIFRWrQi1tmXb6mE7be%2BfOvf%2F7%2F1z0Ydh71t93vpPz5RxlUoujFSOB4dxQQGKFUs2AFRIr9%2FRVzdO%2FVZNVvqPsjqL31%2BYl3icNjh4dDAyNrsPzm%2FL4riZOhRbfwWUeAohAe9ZhrG6af6mYF27X0gPVRHZ6jsYquDxpGAjSJ7rz3om2jHqv2VOLuwtQCwpHA8NvExEXx6JnTg6Eb0%2FU7UpPK3Kewp3bI05hOrEIkHPV1aPduRePbStesAKhseQ8B63V3HRHk8t3o9HLx3unTlRju7KjQVPwFM68chHwNLRlNB0NmtlEtr%2FZO%2FXjlwNBj1aKxM4rjJKUjKv5ZijY2%2FPF8JmuvE%2Fe%2B29gAVqBo6CeCkOBoT3rkFgo14y8%2B%2FCy9bs6sv2rci66HCZcG69lX%2Fq%2B%2FEGrr2lxFbERxAoiggY0Qjk0XB6NGJpN2NORZU3Oo8lRiBX14Z%2FVjypROnc46zqcvRUe7avEhVVNLnVjAcHVEBnL9cmIa%2BMRSzzNqzuWcvrxTk49tpINBZ8%2FKnW6WjzOl2q7LowEewDci6Nh57nh4Lmcq0itRaMYDQ3DMwltjR777sqxv6uFA13Nd1jQOx6R1aAEYmO5Ol5%2FFjjvfnZz5sDgdPJAq68RC4OzCe1ZhyP3t3Ho7jwbij4ApUrITJKybmmOSpRyqxpT8B2SVCj6Dr3j9e0A7ve3wy6FwtOKG1N1jm1v5Y3d7YtKarHhymCVfKPHpuUtAFwZrzMwk7A%2B72OskPcUlZopzHnoaJOKYK2lkHG4NBJy%2FKcxfh2LCGoxlwerrCg0LJIB9FfrRIkFmXtcnFpEJAXQPaubfnQgmK6nFD3FlXLEa%2BdK7Pn4Jt%2FerLCxNcua1qY7%2FLtYqqERsIISYSwwrGh0RwD00c3Fk1taM1%2BVZhJiKyzJaDYub6CaCH8HQjBW4cyv5TsIf5%2BIaHQUqVhEhGpk6Mr75wF0aTZJugv%2Bu1YEY4XUWlIrNHmKn8s1zo7E7Ds1yJMn%2BxcJ%2ByYjChmNFZiqGVobHJ5Y1%2Fw%2BgDsaGnrWNn91qRRe%2BLp%2Feld3a5bEWFY0aM4N1zg9AJ3LGvm8b4pHT9xkdYsHVshqhSPC7Yk6h7YW3%2BlZ2zwAoH4ph6xo9vhhKOg8cmbgulEq197kYUWI5%2BPna%2FAcRX81JjLChmIGC%2FSVa%2BzszPV9un%2FNFoRkZbOHrqfCWJiitRp6ZH1%2Bj68YuTFVJ04FX4GrhNQKUWLpzHl0F3wmaoYbkxH3Lm24%2Bvru9gcLvpPUzHz0FoI%2FW7fE1vYe3lK8b%2B%2FalhNBnFIOEyZDgxXBpEJ5NqE0m5BxVPpQZ%2B6tV3a17xAYGw0NC621WLBKwXQ9pcV3hw9vzh3M%2BWr74ExyMDGy7XaQLHM1srUt2681l5%2Fqyn9shH8mohTf0TgK0vmWVSLC%2F4l%2FAXWxRtaDbtHIAAAAAElFTkSuQmCC)](https://t.me/arv_ego)
