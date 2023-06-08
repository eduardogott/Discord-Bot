# BotDaGaby

Este é um bot de Discord que eu criei quando tava no tédio, só funciona para UM servidor por token.

- [Commands](#commands)
  * [Economy](#economy)
  * [Giveaways](#giveaways)
  * [Leveling](#leveling)
  * [Moderation](#moderation---all-commands-are-admin-commands)
  * [Music](#music)
  * [Profiles](#profiles)
  * [Utils/Misc](#utils-misc)
- [Systems](#systems)
  * [Announcers](#announcers)
  * [Economy](#economy-1)
  * [Giveaways](#giveaways-1)
  * [Leveling](#leveling-1)
  * [Loggers](#loggers)
  * [Moderation](#moderation)
  * [Music](#music-1)
  * [Profiles](#profiles-1)
  * [Utils](#utils)

# Comandos

## Economia

- !daily - Reivindicar bônus diário
- !work - Tabalhe por duas horas para receber coins 
- !balance {member} - Exibe o saldo de coins de outro membro, se não mencionado, exibe seu saldo
- !pay {member} {value} - Transfere uma quantidade de dinheiro a outro membro
- !shop {item} - Exibe a loja, caso um item seja inserido, exibe a descrição e informações sobre o ítem
- !buy {item} - Buys an item from the shop
- !use {item} - Usa um consumível de seu inventário
- !equip {item} - Equipa ou desequipa um ítem de seu inventário
- !eco (give/take/set/reset) {player} [value] - ADMIN - Executa a ação no saldo de um membro
- !giveitem {player} {item} - ADMIN - Adiciona um ítem ao inventário de um jogador
- !takeitem {player} {item} - ADMIN - Remove um ítem do inventário de um jogador
- !clearinventory {player} - ADMIN - Limpa o inventário de um jogador


## Giveaways

- !gcreate {channel} {number_of_winners} {prize} - Creates a giveaway with the provided info
- !gdelete {id} - Deletes a giveaway based on its message ID 
- !greroll {id} - Rerolls a giveaway based on its message ID


## Leveling

- !level {member} - Shows a member's EXP, if no member is mentioned, shows your EXP
- !rank {member} - Shows a member's place on the leaderboard and info about their EXP, or yours if no member is mentioned
- !leaderboard - Shows top 10 players sorted by EXP
- !setexp {member} {exp} - ADMIN COMMAND - Sets a member EXP
- !addexp {member} {exp} - ADMIN COMMAND - Adds an amount of EXP to a member
- !removeexp {member} {exp} - ADMIN COMMAND - Removes an amount of EXP from a member
- !resetexp {member} - ADMIN COMMAND - Resets a member EXP


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


## Profiles

- !edit (title/birthday/nickname/aboutme/color/image/socialmedia) {value} - Edits your profile
- !profile {member} - Shows member's profile, if no member is mentioned, shows your profile
- !rep {member} - Gives a "+rep" to a player
- !nextbirthdays - Lists the next 10 birthdays


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
- !say(e/h) {message} - ADMIN COMMAND - Sends a message through the bots account, e=@everyone, h=@here

---

# Systems
## Announcers

- Twitch annoucer for livestream on
- YouTube announcer for new videos


## Economy

- Economy system with daily bonus, command !work each two hours, and money transfering, all stored in a json database
- Shop/inventory system, where you spend your money from daily and working, all stored in the database
- Bonus coins and discounts for selected roles
- Leaderboard system, showing the top 10 players by balance
- Admin balance management, like giving or resetting a player balance


## Giveaways

- Intuitive giveaway creation system, where you provide the channel it'll take part, the end date, the amount of winners and the prize, one by one, stored in a database
- System of ending giveaways prematurely, cancelling giveaways and rerolling the giveaway


## Leveling

- Leveling system with listeners for messages and time spent in voice calls (default for awaring is each 5 minutes)
- Bonus points for select roles, like booster or twitch subscriber
- Leaderboard system, showing the top 10 players by EXP
- Admin EXP management, like giving or resetting a player EXP


## Loggers
- Announcing system for when a member joins or leaves
- Logging system for edited profiles, edited messages, pinned messages, deleted messages and bulk deleted messages (!clear)


## Moderation
- System for basic punishments (ban, kick, timeout) with their counterparts (unban, untimeout)
- All punishments are stored in the database
- System for managing the guild, with commands like clear, slowmode, (un)lock, (clear)history, for easier management
- Warnings system with customisable duration (default 30 days) and punishments after 'x' number of warnings, all warnings are stored in the database
- Auto moderation system, with flood/spam blocker, discord invites blocker and mass mention blocker


## Music
- Default, simple music bot with queue
- Lyrics command (using Musixmatch API)
- Replay command, inserting the current music to the end of the queue
- DJ role for selected commands, like !clearqueue or !pause/!resume


## Profiles
- Profile system with title, birthday, nickname, aboutme, color, image and social media all in the database
- Easily edit your profile using !edit
- Reputation system using +rep, with set cooldown (default 1 per day), stored in the database
- Birthday announcer (every day, set time) in a specific channel
- Command to see the next 10 birthdays


## Utils
- Various RNGs
- Jankenpon with coins betting
- Link shortener using TinyURL API
- User and guild avatar/icon, banner and info 
- Informations about the bot
- Say command to announce this to the server, optional @everyone/@here
