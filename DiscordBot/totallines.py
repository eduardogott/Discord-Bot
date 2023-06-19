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

with open('discordbot.py', 'rb') as f, open('validator.py', 'rb') as f2, open('config.json', 'rb') as f3:
    lines += len(f.readlines())
    lines += len(f2.readlines())
    json_lines = len(f3.readlines())
        
for file in files:
    with open(f'ext\\{file}', 'rb') as f:
        chars += len(f.read())

with open('discordbot.py', 'rb') as f, open('validator.py', 'rb') as f2, open('config.json', 'rb') as f3:
    chars += len(f.read())
    chars += len(f2.read())
    json_chars = len(f3.read())

print(f'Total de linhas: {lines} + Configuração {json_lines} linhas')
print(f'Total de caracteres: {chars} + Configuração {json_chars} linhas')