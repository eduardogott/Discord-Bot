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

## Economy

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


## Giveaways

- *!gcreate* - Starts the giveaway creation
- *!gdelete {id}* - Deletes a giveaway based on its message ID 
- *!greroll {id}* - Rerolls a giveaway based on its message ID
- *!gend {id}* - Ends a giveaway prematurely, based on its message ID


## Help
- !help [eco|gw|level|mod|music|profile|roles|tc|tickets|info|misc] - Shows the respective help menu, if none is provided, shows the general help menu


## Leveling

- !level {member} - Shows a member's EXP, if no member is mentioned, shows your EXP
- !rank {member} - Shows a member's place on the leaderboard and info about their EXP, or yours if no member is mentioned
- !leaderboard - Shows top 10 players sorted by EXP
- *!setexp {member} {exp}* - Sets a member EXP
- *!addexp {member} {exp}* - Adds an amount of EXP to a member
- *!removeexp {member} {exp}* - Removes an amount of EXP from a member
- *!resetexp {member}* - Resets a member's EXP


## Moderation - ALL COMMANDS ARE ADMIN COMMANDS

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


## Music

- !play {music} - Adds a music to the queue from a YouTube link or search
- !skip - Skips the current music
- *!clearqueue* - Clears the queue
- !queue - Lists the songs in the queue
- *!remove {index}* - Removes a song from the queue
- *!pause* - Pauses the music player
- *!resume* - Resumes the music player
- !nowplaying - Shows info about the current music
- !replay - Adds the current music to the end of the queue


## Profiles

- !edit (title/birthday/nickname/aboutme/color/image/socialmedia) {value} - Edits your profile
- !profile {member} - Shows member's profile, if no member is mentioned, shows your profile
- !rep {member} - Gives a "+rep" to a player
- !nextbirthdays - Lists the next 10 birthdays
- *!adminedit {member} (title/birthday/nickname/aboutme/color/image/social) {value}* - Edits another member's profile


## Roles

- !register - Starts the user's registration


## TempChannels

- !tempchannel - Starts the creation of a TempChannel
- *!tcdelete {id}* - Deletes a user's TempChannel
- *!tcadd {id} [multiple member mentions]* - Adds the users to the TempChannel
- *!tcremove {id} [multiple member mentions]* - Removes the users from the TempChannel
- *!tctranscript* - Creates a transcript of the current TempChannel
- *!tchelp* - Shows info about the TempChannels commands (same as `!help tc`)
- *!tcadelete* {id} - **ADMIN** - Deletes any TempChannel
- *!tcatranscript {id}* - **ADMIN** - Creates a transcript of any TempChannel


## Tickets

- !ticket - Creates a ticket
- *!tclose* - Closes a ticket
- *!topen* - Reopens a ticket
- *!tdelete* - Deletes a ticket
- *!tadd {member}* - Adds a member to the ticket
- *!tremove {member}* - Removes a member from the ticket
- *!trename {name}* - Renames a ticket channel
- *!ttranscript* - Creates a transcript of the ticket

  
## Utils/Misc

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
## Announcers

- Twitch announcer for livestream on
- YouTube announcer for new videos


## Economy

- Economy system with daily bonus, command !work each two hours, and money transferring, all stored in a json database
- Shop/inventory system, where you spend your money from daily and work, all stored in the database
- Bonus coins and discounts for selected roles
- Leaderboard system, showing the top 10 players by balance
- Admin balance management, like giving or resetting a player's balance


## Giveaways

- Intuitive giveaway creation system, where you provide the channel it'll take part in, the end date, the number of winners, and the prize, one by one, stored in a database
- System of ending giveaways prematurely, canceling giveaways, and rerolling the giveaway


## Help

- Multiple help menus, divided by category, sent in a rich embed


## Leveling

- Leveling system with listeners for messages and time spent in voice calls (default for awarding is each 5 minutes)
- Bonus points for select roles, like booster or Twitch subscriber
- Leaderboard system, showing the top 10 players by EXP
- Admin EXP management, like giving or resetting a player's EXP


## Loggers

- System for announcing when a member joins or leaves
- Logging system for edited profiles, edited messages, pinned messages, deleted messages, and bulk deleted messages (!clear)


## Moderation

- System for basic punishments (ban, kick, timeout) with their counterparts (unban, untimeout)
- All punishments are stored in the database
- System for managing the guild, with commands like clear, slowmode, (un)lock, (clear)history, for easier management
- Warning system with customisable duration (default 30 days) and punishments after 'x' number of warnings, all warnings are stored in the database
- Auto moderation system, with flood/spam blocker, discord invite blocker, and mass mention blocker
- Ability to ban and unban players from creating [tickets](#tickets-1)


## Music

- Default and simple music bot with queue
- Lyrics command (using the Musixmatch API)
- Replay command, inserting the current music at the end of the queue
- DJ role for selected commands, like !clearqueue or !pause/!resume


## Profiles

- Profile system with title, birthday, nickname, aboutme, color, image, and social media all in the database
- Easily edit your profile using !edit
- Reputation system using +rep, with a set cooldown (default 1 per day), stored in the database
- Birthday announcer (every day, set time) in a specific channel
- Command to see the next 10 birthdays


## Roles

- Registration system with roles for age and gender, expandable


## TempChannels

- Creation of TempChannels, with a limit of one voice and one text chat per member, saved in the database
- Interactive TempChannel creation with just a simple command
- Ability to add and remove members from your TempChannel whenever you want, saved in the database
- Ability to generate transcripts of the text TempChannel messages
- TempChannels expire and get deleted after 7 days of inactivity


## Tickets

- Simple creation of tickets, with a limit of two tickets per member, saved in the database
- Ability to ban and unban players from creating tickets
- Ability to add and remove members from the ticket, saved in the database
- Ability to generate transcripts of the tickets

## Utils/Misc

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

> Key in the JSON - Explanations - Limits, if needed *(to see limits further, go to [validator.py](/discordbot/validator.py))*

- Announcers.Twitch.Username - The Twitch username that'll be used in the Twitch announcer - Twitch username (leave empty to disable)
- Announcers.Twitch.DiscordChannelID - The Discord channel ID in which livestreams will be announced (leave empty or invalid to deactivate Twitch announcers)
- Announcers.YouTube.YouTubeChannelID - The YouTube channel ID that'll be used in the YouTube announcer - YouTube Channel ID, get yours [here](https://commentpicker.com/youtube-channel-id.php) (leave empty to disable)
- Announcers.YouTube.DiscordChannelID - The Discord channel ID in which new videos will be announced - Discord Channel ID (Snowflake Channel ID)
- Economy.StartBalance - Economy system starting balance - Value between 0 and 9999999
- Economy.Multiplier - Economy system multiplier - Value between 0.1 and 10000
- Economy.WorkCooldown - Work cooldown in minutes - Value between 1 and 100000 minutes, or 69 *nice* days
- Economy.TransferTaxPercentage - Percentage deduced from money transfers - Value between 0 and 100, full percentage, not decimal
- Leveling.Defaults.StartEXP - Starting EXP - Value between 1 and 9999999
- Leveling.Defaults.LevelUpRequirements - Requirements to level up, each level will be a multiple of it - Higher than the starting EXP
- Leveling.Messages.BaseEXP - The base EXP given to a user by message - Value between 1 and 999999
- Leveling.Messages.RoleBonusEXP.Keys - The roles that will be awarded bonus EXP - Role name
- Leveling.Messages.RoleBonusEXP.Values - The bonus EXP given to a user by message if it has the role in the keys above - Value between 1 and 999999
- Leveling.VoiceCalls.CheckTime - Interval for checking if a user is still in a voice call, in seconds - Value between 1 and 9999, or around 3 hours
- Leveling.VoiceCalls.BaseEXP - The base EXP given to a user by 'interval' in a voice call - Value between 1 and 999999
- Leveling.VoiceCalls.RoleBonusEXP.Keys - The roles that will be awarded bonus EXP - Role name
- Leveling.VoiceCalls.RoleBonusEXP.Values - The bonus EXP given to a user by 'interval' in a voice call if it has the role in the keys above - Value between 1 and 999999
- Loggers.Announcers.JoinChannel - Channel for sending "user joined" announcements - Discord Channel ID (Snowflake Channel ID)
- Loggers.Announcers.LeaveChannel - Channel for sending "user left" announcements - Discord Channel ID (Snowflake Channel ID)
- Loggers.Announcers.LogChannel - Channel for sending "user joined" and "user left" logs - Discord Channel ID (Snowflake Channel ID)
- Loggers.Loggers.LogChannel - Channel to send all the [logs](#loggers) - Discord Channel ID (Snowflake Channel ID)
- Loggers.Loggers.CmdLogChannel - Channel to send bot commands logs - Discord Channel ID (Snowflake Channel ID)
- Moderation.General.PunishmentsChannel - Channel to announce punishments - Discord Channel ID (Snowflake Channel ID)
- Moderation.Warnings.ExpirationTime - Time for a warning to expire, in hours - Value between 1 and 99999, or over 10 years
- Moderation.Warnings.AutoPunishments.Keys - The amount of warnings that'll lead to the punishment - Value between 1 and 99 warnings
- Moderation.Warnings.AutoPunishments.Values - The punishment that will be applied to that amount of warnigs - mute|timeout|ban|kick %member% [duration] {reason}
- Moderation.AutoMod.MinimumMessageSize - Minimum size of a message to be filtered by the AutoMod - Value between 1 and 999
- Moderation.AutoMod.FloodMessageAmount - Maximum amount of messages before it'll get flagged by the AutoMod - Value between 1 and 99
- Moderation.AutoMod.MaxMentions - Maximum mentions in a message before it'll get flagged by the AutoMod - Value between 1 and 99
- Profiles.Defaults.Title - Default title when generating a profile - Size between 1 and 127 characters
- Profiles.Defaults.Birthday - DO NOT CHANGE THE VALUE - 31-02
- Profiles.Defaults.Nickname - Default nickname when generating a profile - Size between 1 and 255 characters
- Profiles.Defaults.AboutMe - Default about me when generating a profile - Size between 1 and 255 characters
- Profiles.Defaults.Color - Default color when generating a profile - Hex format, with 0x instead of # (0xffffff)
- Profiles.Defaults.Image - Default image when generating a profile - Uploaded to imgur with format like i.imgur.com/*IMAGEID*.(jpg|jpeg|png|gif|bmp)
- Profiles.Defaults.Social - Default social media when generating a profile - LEAVE BLANK FOR NOW
- Profiles.Edit.SizeLimits.Title - Size limits for the title - 128 > MaxSize > MinSize > 0
- Profiles.Edit.SizeLimits.Nickname - Size limits for the nickname - 256 > MaxSize > MinSize > 0
- Profiles.Edit.SizeLimits.AboutMe - Size limits for the about me - 256 > MaxSize > MinSize > 0
- Roles.AutoRole.DefaultRole - Default role as in the role assigned when a member enters - Role name
- Statistics.TwitchID - Twitch ID to be used in the statistics - Twitch channel ID, get it [here](https://streamscharts.com/tools/convert-username)
- Statistics.YouTubeID - YouTube channel ID to be used in the statistics - YouTube ID, get it [here](https://commentpicker.com/youtube-channel-id.php)
- Utits.URLShortenerDelay - Delay to use the URL shortener in seconds - Value between 1 and 86400, or 1 day
