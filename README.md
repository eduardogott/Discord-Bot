# BotDaGaby

This is a Discord bot I started coding out of boredom, it only works for ONE server per token.  

- [Commands](#commands)
  * [Economy](#economy)
  * [Giveaways](#giveaways)
  * [Help](#help)
  * [Leveling](#leveling)
  * [Moderation](#moderation---all-commands-are-admin-commands)
  * [Music](#music)
  * [Profiles](#profiles)
  * [Roles](#roles)
  * [TempChannels](#tempchannels)
  * [Tickets](#tickets)
  * [Utils/Misc](#utilsmisc)
- [Systems](#systems)
  * [Announcers](#announcers)
  * [Economy](#economy-1)
  * [Giveaways](#giveaways-1)
  * [Help](#help-1)
  * [Leveling](#leveling-1)
  * [Loggers](#loggers)
  * [Moderation](#moderation)
  * [Music](#music-1)
  * [Profiles](#profiles-1)
  * [Roles](#roles-1)
  * [TempChannels](#tempchannels-1)
  * [Tickets](#tickets-1)
  * [Utils/Misc](#utilsmisc-1)
- [Configuration](#configuration)

# Commands
> Commands in italics need **Manager** role, **DJ** role for [music](#music) commands, or being the channel creator for non-admin [TempChannels](#tempchannels) commands.

## Economy [^](#botdagaby)

- !daily - Claim daily bonus
- !work - Work for 2 hours to get coins
- !balance {member} - Get another member's current balance, if no member is mentioned, get your own balance
- !pay {member} {value} - Send a certain value to another member 
- !shop {item} - Shows the shop, if an item is inserted it shows item description and info
- !buy {item} - Buys an item from the shop
- !use {item} - Uses a consumable from your inventory
- !equip {item} - Equips/unequips an item from your inventory
- *!eco (give/take/set/reset) {player} [value]* - Performs the specified action over the balance of a player
- *!giveitem {player} {item}* - Gives an item to a player
- *!takeitem {player} {item}* - Takes an item from a player
- *!clearinventory {player}* - Clears a player's inventory


## Giveaways [^](#botdagaby)

- *!gcreate* - Starts the giveaway creation
- *!gdelete {id}* - Deletes a giveaway based on its message ID 
- *!greroll {id}* - Rerolls a giveaway based on its message ID
- *!gend {id}* - Ends a giveaway prematurely, based on its message ID


## Help [^](#botdagaby)
- !help [eco|gw|level|mod|music|profile|roles|tc|tickets|info|misc] - Shows the respective help menu, if none is provided, shows the general help menu


## Leveling [^](#botdagaby)

- !level {member} - Shows a member's EXP, if no member is mentioned, shows your EXP
- !rank {member} - Shows a member's place on the leaderboard and info about their EXP, or yours if no member is mentioned
- !leaderboard - Shows top 10 players sorted by EXP
- *!setexp {member} {exp}* - Sets a member EXP
- *!addexp {member} {exp}* - Adds an amount of EXP to a member
- *!removeexp {member} {exp}* - Removes an amount of EXP from a member
- *!resetexp {member}* - Resets a member's EXP


## Moderation - ALL COMMANDS ARE ADMIN COMMANDS [^](#botdagaby)

- *!ban {member} [reason]* - Bans a member for an (optional) reason
- *!unban {member_id}* - Unban a member from the guild
- *!kick {member} {reason}* - Kicks a member for an (optional) reason
- *!timeout {member} {duration} {reason}* - Timeouts a member for a specific time for an (optional) reason
- *!untimeout {member}* - Removes the timeout of a member
- *!clear {quantity}* - Clears the amount of messages from a channel
- *!slowmode {time}* - Sets the slowmode of the channel to the specific time
- *!setnickname {member} {nickname}* - Sets the nickname of a member
- *!history {member}* - List all the member's punishments
- *!clearhistory {member}* - Clears member's list of punishments
- *!lock* - Locks a channel from the @everyone role
- *!unlock* - Unlocks a channel from the @everyone role
- *!warn {member} {reason}* - Warns a member for an (optional) reason
- *!unwarn {member}* - Removes one warning from a member
- *!warnings {member}* - Lists all of members active warnings
- *!ticketban {member}* - Bans a member from opening tickets
- *!unticketban {member}* - Unbans a player from opening tickets


## Music [^](#botdagaby)

- !play {music} - Adds a music to the queue from a YouTube link or search
- !skip - Skips the current music
- *!clearqueue* - Clears the queue
- !queue - Lists the songs in the queue
- *!remove {index}* - Removes a song from the queue
- *!pause* - Pauses the music player
- *!resume* - Resumes the music player
- !nowplaying - Shows info about the current music
- !replay - Adds the current music to the end of the queue


## Profiles [^](#botdagaby)

- !edit (title/birthday/nickname/aboutme/color/image/socialmedia) {value} - Edits your profile
- !profile {member} - Shows member's profile, if no member is mentioned, shows your profile
- !rep {member} - Gives a "+rep" to a player
- !nextbirthdays - Lists the next 10 birthdays
- *!adminedit {member} (title/birthday/nickname/aboutme/color/image/social) {value}* - Edits another member's profile


## Roles [^](#botdagaby)

- !register - Starts the user's registration


## TempChannels [^](#botdagaby)

- !tempchannel - Starts the creation of a TempChannel
- *!tcdelete {id}* - Deletes a user's TempChannel
- *!tcadd {id} [multiple member mentions]* - Adds the users to the TempChannel
- *!tcremove {id} [multiple member mentions]* - Removes the users from the TempChannel
- *!tctranscript* - Creates a transcript of the current TempChannel
- *!tchelp* - Shows info about the TempChannels commands (same as `!help tc`)
- *!tcadelete* {id} - **ADMIN** - Deletes any TempChannel
- *!tcatranscript {id}* - **ADMIN** - Creates a transcript of any TempChannel


## Tickets [^](#botdagaby)

- !ticket - Creates a ticket
- *!tclose* - Closes a ticket
- *!topen* - Reopens a ticket
- *!tdelete* - Deletes a ticket
- *!tadd {member}* - Adds a member to the ticket
- *!tremove {member}* - Removes a member from the ticket
- *!trename {name}* - Renames a ticket channel
- *!ttranscript* - Creates a transcript of the ticket

  
## Utils/Misc [^](#botdagaby)

- !random {min} {max} - Generates a random number between min-max
- !dice {max} - Rolls a dice from the specified size
- !jankenpon (rock/paper/scissors) - Plays rock-paper-scissors against the bot
- !choice {multiargs} - Chooses an item from the multiargs, separated by space
- !shorten {url} - Shortens a URL using TinyURL's API
- !remindme {time(s/m/h/d)} {message} - Creates a reminder of some text
- *!poll {message}* - Sends a message with ✅ and ⛔ emojis
- !avatar {member} - Shows member's avatar, if no member is mentioned, shows your avatar
- !userbanner {member} - Shows member's banner, if no member is mentioned, shows your banner
- !userinfo {member} - Shows info about a member, if no member is mentioned, shows your info
- !serverbanner - Shows the current guild banner
- !servericon - Shows the current guild icon
- !serverinfo - Shows info about the current guild
- !about - Shows info about the bot
- *!say(e/h) {message}* - Sends a message through the bot's account, e=@everyone, h=@here
- *!sayeveryone {message}* - Sends a message with the bot, but pinging @everyone
- *!sayhere {message}* - Sends a message with the bot, but pinging @here

---

# Systems
## Announcers [^](#botdagaby)

- Twitch announcer for livestream on
- YouTube announcer for new videos


## Economy [^](#botdagaby)

- Economy system with daily bonus, command !work each two hours, and money transferring, all stored in a json database
- Shop/inventory system, where you spend your money from daily and work, all stored in the database
- Bonus coins and discounts for selected roles
- Leaderboard system, showing the top 10 players by balance
- Admin balance management, like giving or resetting a player's balance


## Giveaways [^](#botdagaby)

- Intuitive giveaway creation system, where you provide the channel it'll take part in, the end date, the number of winners, and the prize, one by one, stored in a database
- System of ending giveaways prematurely, canceling giveaways, and rerolling the giveaway


## Help [^](#botdagaby)

- Multiple help menus, divided by category, sent in a rich embed


## Leveling [^](#botdagaby)

- Leveling system with listeners for messages and time spent in voice calls (default for awarding is each 5 minutes)
- Bonus points for select roles, like booster or Twitch subscriber
- Leaderboard system, showing the top 10 players by EXP
- Admin EXP management, like giving or resetting a player's EXP


## Loggers [^](#botdagaby)

- System for announcing when a member joins or leaves
- Logging system for edited profiles, edited messages, pinned messages, deleted messages, and bulk deleted messages (!clear)


## Moderation [^](#botdagaby)

- System for basic punishments (ban, kick, timeout) with their counterparts (unban, untimeout)
- All punishments are stored in the database
- System for managing the guild, with commands like clear, slowmode, (un)lock, (clear)history, for easier management
- Warning system with customisable duration (default 30 days) and punishments after 'x' number of warnings, all warnings are stored in the database
- Auto moderation system, with flood/spam blocker, discord invite blocker, and mass mention blocker
- Ability to ban and unban players from creating [tickets](#tickets-1)


## Music [^](#botdagaby)

- Default and simple music bot with queue
- Lyrics command (using the Musixmatch API)
- Replay command, inserting the current music at the end of the queue
- DJ role for selected commands, like !clearqueue or !pause/!resume


## Profiles [^](#botdagaby)

- Profile system with title, birthday, nickname, aboutme, color, image, and social media all in the database
- Easily edit your profile using !edit
- Reputation system using +rep, with a set cooldown (default 1 per day), stored in the database
- Birthday announcer (every day, set time) in a specific channel
- Command to see the next 10 birthdays


## Roles [^](#botdagaby)

- Registration system with roles for age and gender, expandable


## TempChannels [^](#botdagaby)

- Creation of TempChannels, with a limit of one voice and one text chat per member, saved in the database
- Interactive TempChannel creation with just a simple command
- Ability to add and remove members from your TempChannel whenever you want, saved in the database
- Ability to generate transcripts of the text TempChannel messages
- TempChannels expire and get deleted after 7 days of inactivity


## Tickets [^](#botdagaby)

- Simple creation of tickets, with a limit of two tickets per member, saved in the database
- Ability to ban and unban players from creating tickets
- Ability to add and remove members from the ticket, saved in the database
- Ability to generate transcripts of the tickets

## Utils/Misc [^](#botdagaby)

- Various RNGs
- Jankenpon with coins betting
- Link shortener using the TinyURL API
- Create reminders for the future, saved in the database
- Create polls with just one command
- User and guild avatar/icon, banner, and info 
- Information about the bot
- Say command to announce this to the server, optional @everyone/@here

---

# Configuration
> The configuration is stored in [config.json](/discordbot/config.json)
