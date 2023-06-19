import json
import re

def config_validator():
    with open('config.json', 'r') as f:
        file = json.load(f)
        config = file['Configuration']

    check = {'Announcers.Twitch.Username':re.match(r'^[a-z0-9_]+$',str(config['Announcers']['Twitch']['Username'])),
     'Announcers.Twitch.DiscordChannelID':re.match(r'^[0-9]{17,19}$',str(config['Announcers']['Twitch']['DiscordChannelID'])),
     'Announcers.YouTube.YouTubeChannelID':re.match(r'^[0-9a-zA-Z_-]+$',str(config['Announcers']['YouTube']['YouTubeChannelID'])),
     'Announcers.YouTube.DiscordChannelID':re.match(r'^[0-9]{17,19}$',str(config['Announcers']['YouTube']['DiscordChannelID'])),
     'Economy.StartBalance': 0 <= config['Economy']['StartBalance'] < 10000000,
     'Economy.Multiplier': 0.1 <= config['Economy']['Multiplier'] <= 10000,
     'Economy.WorkCooldown': 1 <= config['Economy']['WorkCooldown'] <= 100000,
     'Economy.TransferTaxPercentage': 0 <= config['Economy']['TransferTaxPercentage'] <= 100,
     'Leveling.Defaults.StartEXP': 1 <= config['Leveling']['Defaults']['StartEXP'] < 10000000,
     'Leveling.Defaults.LevelUpRequirements': config['Leveling']['Defaults']['StartEXP'] < config['Leveling']['Defaults']['LevelUpRequirements'],
     'Leveling.Messages.BaseEXP': 1 <= config['Leveling']['Messages']['BaseEXP'] < 1000000,
     'Leveling.Messages.RoleBonusEXP.Keys':all([re.match(r'^.{1,127}$',str(value)) for value in config['Leveling']['Messages']['RoleBonusEXP'].keys()]),
     'Leveling.Messages.RoleBonusEXP.Values':all([(1 <= value < 1000000) for value in config['Leveling']['Messages']['RoleBonusEXP'].values()]),
     'Leveling.VoiceCalls.CheckTime': 1 <= config['Leveling']['VoiceCalls']['CheckTime'] < 10000,
     'Leveling.VoiceCalls.BaseEXP': 1 <= config['Leveling']['VoiceCalls']['BaseEXP'] < 1000000,
     'Leveling.VoiceCalls.RoleBonusEXP.Keys':all([re.match(r'^.{1,127}$',str(value)) for value in config['Leveling']['VoiceCalls']['RoleBonusEXP'].keys()]),
     'Leveling.VoiceCalls.RoleBonusEXP.Values':all([(1 <= value < 1000000) for value in config['Leveling']['VoiceCalls']['RoleBonusEXP'].values()]),
     'Loggers.Announcers.JoinChannel':re.match(r'^[0-9]{17,19}$',str(config['Loggers']['Announcers']['JoinChannel'])),
     'Loggers.Announcers.LeaveChannel':re.match(r'^[0-9]{17,19}$',str(config['Loggers']['Announcers']['LeaveChannel'])),
     'Loggers.Announcers.LogChannel':re.match(r'^[0-9]{17,19}$',str(config['Loggers']['Announcers']['LogChannel'])),
     'Loggers.Loggers.LogChannel':re.match(r'^[0-9]{17,19}$',str(config['Loggers']['Loggers']['LogChannel'])),
     'Loggers.Loggers.CmdLogChannel':re.match(r'^[0-9]{17,19}$',str(config['Loggers']['Loggers']['CmdLogChannel'])),
     'Moderation.General.PunishmentsChannel':re.match(r'^[0-9]{17,19}$',str(config['Moderation']['General']['PunishmentsChannel'])),
     'Moderation.Warnings.ExpirationTime': 1 <= config['Moderation']['Warnings']['ExpirationTime'] < 100000,
     'Moderation.Warnings.AutoPunishments.Keys':all([(1 <= key < 100) for key in config['Moderation']['Warnings']['AutoPunishments'].keys()]),
     'Moderation.Warnings.AutoPunishments.Values':all([re.match(r'^(mute|timeout|ban|kick) %member% (?:([1-9]|[1-2][0-9]|3[0-1])(s|m|h|d) (.+))?',str(value)) for value in config['Moderation']['Warnings']['AutoPunishments'].values()]),
     'Moderation.AutoMod.MinimumMessageSize': 1 <= config['Moderation']['AutoMod']['MinimumMessageSize'] < 1000,
     'Moderation.AutoMod.FloodMessageAmount': 1 <= config['Moderation']['AutoMod']['FloodMessageAmount'] < 100,
     'Moderation.AutoMod.MaxMentions': 1 <= config['Moderation']['AutoMod']['MaxMentionsz'] < 100,
     'Profiles.Defaults.Title':re.match(r'^.{1,127}$',str(config['Profiles']['Defaults']['Title'])),
     'Profiles.Defaults.Birthday':re.match(r'^31-02$',str(config['Profiles']['Defaults']['Birthday'])),
     'Profiles.Defaults.Nickname':re.match(r'^.{1,255}$',str(config['Profiles']['Defaults']['Nickname'])),
     'Profiles.Defaults.AboutMe':re.match(r'^.{1,255}$',str(config['Profiles']['Defaults']['AboutMe'])),
     'Profiles.Defaults.Color':re.match(r'^0x[0-9a-f]{6}$',str(config['Profiles']['Defaults']['Color'])),
     'Profiles.Defaults.Image':re.match(r'^\bhttps?:\/\/i\.imgur\.com\/[a-zA-Z0-9]+\.(?:jpg|jpeg|png|gif|bmp)$\b$',str(config['Profiles']['Defaults']['Image'])),
     'Profiles.Defaults.Social':re.match(r'^$',str(config['Profiles']['Defaults']['Social'])),
     'Profiles.Edit.SizeLimits.Title': 128 > config['Profiles']['Edit']['SizeLimits']['Title'][1] > config['Profiles']['Edit']['SizeLimits']['Title'][0] > 0,
     'Profiles.Edit.SizeLimits.Nickname': 256 > config['Profiles']['Edit']['SizeLimits']['Nickname'][1] > config['Profiles']['Edit']['SizeLimits']['Nickname'][0] > 0,
     'Profiles.Edit.SizeLimits.AboutMe': 256 > config['Profiles']['Edit']['SizeLimits']['AboutMe'][1] > config['Profiles']['Edit']['SizeLimits']['AboutMe'][0] > 0,
     'Roles.AutoRole.DefaultRole':re.match(r'^.{1,127}$',str(config['Roles']['AutoRole']['DefaultRole'])),
     'Statistics.TwitchID':re.match(r'^[0-9]+$',str(config['Statistics']['TwitchID'])),
     'Statistics.YouTubeID':re.match(r'^[0-9a-zA-Z_-]+$',str(config['Statistics']['YouTubeID'])),
     'Utits.URLShortenerDelay': 0 <= config['Utils']['URLShortenerDelay'] <= 86400
    }

    for key in check:
        if check[key] is False or check[key] is None:
            print(f'The provided value for {key} is invalid!')
            quit()