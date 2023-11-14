[toc]

# HyperBot

This is a Discord bot I started creating out of boredom, and it turned into an hobby. This thing took several hours of my life.

Currently with *XX* commands.

To run the bot you must have a Discord Bot token, if you don't know how to get one, here(hyperlink) is a tutorial, then you go to discordbot.py(hyperlink) and, in the last line, replace **TOKEN** with the token you got.

## General info

Commands included: [] = Optional, {} = Required, () = Choose one of, required, <> = Choose one of, optional

Commands preceded by @ are Manager only

The default prefixes are `@bot-mention`, `!` and `.` - but you can edit them in discordbot.py(hyperlink)

## Economy

Coins system, with daily and bi-hourly bonus, item shop, with equipable and consumable items.
Item actions currently contain "give-role" and "send-message", but more will be added.
Economy info is all saved in a TinyDB (json) database.

daily - Claims daily bonus
work - Works each two hours to get money
balance [@member] - Display the user's balance
pay {@member} {value} - Transfer money to another member (10% tax)
shop [item name] - Display the shop or info about an item
buy {item name} - Buys an item from the shop
inventory [@member] - Shows a member's inventory
use {item name} - Uses an consumable item
equip {item name} - (Un)equips an equippable item
@eco (give/take/set/reset) {@member} {value} - Changes an member's balance
@giveitem {@member} {item name} - Gives an item to a member
@takeitem {@member} {item name} - Takes an item from a member's inventory
@clearinventory {@member} - Clears a member inventory

## Utils

Reminders are saved in a TinyDB (json) database.

random [min] [max] - Generates a random number, defaults to 1-100, limited to -1000000000-1000000000
dado [size] - Rolls a dice, defaults to 6, max size is 4096
jankenpon (pedra/papel/tesoura) - Plays rock paper scissors vs the bot
escolher {options} - Chooses one of the items in "options", must be more than two items separated by comma
shorten {url} - Shortens a URL using TinyURL's API, cooldown of 60 seconds
remindme {time(s/m/h/d/w/mo/y)} {message} - Creates a reminder to be reminded in an embed after the chosen time
@poll {question} - Creates an embed poll with ✅ and ❌ reactions
ping - Reply the bot's ping (used to test if the bot is online)
avatar [@member] - Shows the member's avatar
userbanner [@member] - Shows the member's banner
serverbanner - Shows the guild's banner
servericon - Shows the guild's icon
userinfo [@member] - Displays informations about an member
serverinfo `<cargos>` - Displays informations about the guild, or the roles if `<cargos>` is used
@say {message} - Sends a message as the bot (placeholders: %e = @everyone, %h = @here, %a = @command_author)
