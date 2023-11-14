from os import walk

lines = 0
chars = 0
files = [x[2] for x in walk('C:\\Users\\Eduardo\\Desktop\\DiscordBot\\ext')][0]
for item in files:
    if item.endswith('.pyc'):
        files.remove(item)

for file in files:
    with open(f'ext\\{file}', 'rb') as f:
        lines += len(f.readlines())

with open('discordbot.py', 'rb') as f:
    lines += len(f.readlines())
for file in files:
    with open(f'ext\\{file}', 'rb') as f:
        chars += len(f.read())

with open('discordbot.py', 'rb') as f:
    chars += len(f.read())

print(f'Total de linhas: {lines}')
print(f'Total de caracteres: {chars}')