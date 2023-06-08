# BotDaGaby

This is a Discord bot I started coding out of boredom, it only works for ONE server per token.

[toc]

# Commands

---

## Economy

- !daily - Claim daily bonus
- !work - Work for 2 hours to get coins
- !balance {member} - Get another member's current balance, if no member is mentioned, get your own balance
- !pay {member} {value} - Send a certain value to another member 
- !shop {item} - Shows the shop, if a item is inserted, shows item description and info
- !buy {item} - Buys an item from the shop
- !use {item} - Uses a consumable from your inventory
- !equip {item} - Equips/unequips an item from your inventory
- !eco (give/take/set/reset) {player} [value] - ADMIN COMMAND - Performs the specified action over the balance of a player
- !giveitem {player} {item} - ADMIN COMMAND - Gives an item to a player
- !takeitem {player} {item} - ADMIN COMMAND - Takes an item from a player
- !clearinventory {player} - ADMIN COMMAND - Clears a player inventory

---

## Giveaways

- !gcreate {channel} {number_of_winners} {prize} - Creates a giveaway with the provided info
- !gdelete {id} - Deletes a giveaway based on its message ID 
- !greroll {id} - Rerolls a giveaway based on its message ID

---

## Leveling

- !level {member} - Shows a member's EXP, if no member is mentioned, shows your EXP
- !rank {member} - Shows a member's place on the leaderboard and info about their EXP, or yours if no member is mentioned
- !leaderboard - Shows top 10 players sorted by EXP
- !setexp {member} {exp} - ADMIN COMMAND - Sets a member EXP
- !addexp {member} {exp} - ADMIN COMMAND - Adds an amount of EXP to a member
- !removeexp {member} {exp} - ADMIN COMMAND - Removes an amount of EXP from a member
- !resetexp {member} - ADMIN COMMAND - Resets a member EXP

---

## Moderation - ALL COMMANDS ARE ADMIN COMMANDS

- !ban {member} [reason] - Bans a member for a (optional) reason
- !unban {member_id} - Unban a member from the guild
- !kick {member} {reason} - Kicks a member for a (optional) reason
- !timeout {member} {duration} {reason} - Timeouts a member for a specific time for a (optional) reason
- !untimeout {member} - Removes the timeout of a member
- !clear {quantity} - Clears the amount of message from a channel
- !slowmode {time} - Sets the slowmode of the channel to the specific time
- !setnickname {member} {nickname} - Sets the nickname of a member
- !history {member} - List all of member's punishments
- !clearhistory {member} - Clears member's list of punishments
- !lock - Locks a channel from the @everyone role
- !unlock - Unlocks a channel from the @everyone role
- !warn {member} {reason} - Warns a member for a (optional) reason
- !unwarn {member} - Removes one warn from a member
- !warnings {member} - Lists all of members active warnings

---

## Music

- !play {music} - Adds a music to the queue from a youtube link or search
- !skip - Skips the current music
- !clearqueue - Clears the queue
- !queue - Lists the musics in the queue
- !remove {index} - Removes a music from the queue
- !pause - Pauses the music player
- !resume - Resumes the music player
- !nowplaying - Shows info about the current music
- !replay - Adds the current music to the end of the queue

---

## Profiles

- !edit (title/birthday/nickname/aboutme/color/image/socialmedia) {value} - Edits your profile
- !profile {member} - Shows member's profile, if no member is mentioned, shows your profile
- !rep {member} - Gives a "+rep" to a player
- !nextbirthdays - Lists the next 10 birthdays

---

## Utils/Misc

- !random {min} {max} - Generates a random number between min-max
- !dice {max} - Rolls a dice from the specified size
- !jankenpon (rock/paper/scissors) - Plays rock-paper-scissors against the bot
- !choice {multiargs} - Chooses an item from the multiargs, separated by space
- !shorten {url} - Shortens a URL using TinyURL's API
- !avatar {member} - Shows member's avatar, if no member is mentioned, shows your avatar
- !userbanner {member} - Shows member's banner, if no member is mentioned, shows your banner
- !userinfo {member} - Shows info about a member, if no member is mentioned, shows your info
- !serverbanner - Shows the current guild banner
- !servericon - Shows the current guild icon
- !serverinfo - Shows info about the current guild
- !about - Shows info about the bot
- !say(e/h) {message} - Sends a message through the bots account, e=@everyone, h=@here

