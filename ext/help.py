import discord
from discord.ext import commands
from tinydb import TinyDB

db = TinyDB('data.json', sort_keys=True, indent=2, separators=(',', ': '))
commands_table = db.table('custom_commands')

CATEGORY_MAPPING: dict[str, list[str]] = {'announcers': ['announcers', 'anuncios', 'announces', 'anuncio'],
                                 'apis': ['apis', 'api'],
                                 'custom': ['custom', 'customs'],
                                 'economy': ['economy', 'economia', 'eco'],
                                 'giveaways': ['giveaways', 'gw', 'giveaway', 'sorteio', 'sorteios'],
                                 'categories': ['categories', 'categorias', 'category'],
                                 'levels': ['levels', 'niveis', 'leveis', 'xp'],
                                 'loggers': ['loggers'],
                                 'moderation': ['moderation', 'moderacao', 'mod', 'punishments'],
                                 'musics': ['musics', 'music', 'musica', 'musicas'],
                                 'profiles': ['profiles', 'perfil', 'perfis', 'profile'],
                                 'roles': ['roles', 'cargos', 'register', 'registro'],
                                 'stats': ['stats', 'statistics', 'estatisticas'],
                                 'tempchannels': ['tempchannels', 'tc', 'tempchannel'],
                                 'tickets': ['tickets', 'ticket'],
                                 'misc': ['misc', 'utils', 'other', 'outros']}

AUTO_PUNISHMENTS = ['2: Castigo de 7 dias',
                    '4: Castigo de 30 dias',
                    '6: Banimento permanente']

MESSAGES = {'announcers': ['anunciadores', 
                          ['Esta categoria serve para anunciar diversas coisas',
                           'Como lives na Twitch e postados vídeos no YouTube',
                           'Apenas editável via configuração do bot pelo admin'], {}],
    
            'apis': ['APIs', 
                    ['Esta categoria serve para acessar APIs diferentes, como:',
                     'Obter a Picture of the Day da NASA',
                     'Obter informações sobre países',
                     'etc...'],
                     {'pais': ['Exibe informações sobre um país', 
                              ['Exibe diversas informações sobre um país',
                               'Utilizando a RESTCountries API',
                               'Use: !pais {código ISO-3166}',
                               'Aliases: `country`, `countries`, `paises`']],

                      'apod': ['Exibe a foto astronômica do dia da NASA', 
                              ['Exibe a foto astronômica do dia da NASA',
                               'Acessando a NASA API, limite de 100 usos do comando por dia',
                               'Essa foto altera a cada 24 horas',
                               'Use: !apod',
                               'Aliases: `nasaapod`']]}],

            'custom': ['comandos customizáveis', 
                      ['Esta categoria serve para criar comandos customizados',
                       'Estes comandos podem ser vistos com !cclist',
                       'Salvos em database, portanto podem ser facilmente editados e apagados'], 
                       {'customcommand': ['Cria um comando customizado',
                                         ['Inicia a criação de um comando customizado',
                                          'Criação intuitiva e fácil',
                                          'Use: !customcommand',
                                          'Aliases: `cc`, `cccreate`']],

                        'customcommandsdelete': ['Apaga um comando customizado', 
                                                ['Apaga um comando customizado',
                                                 'Use: !customcommandsdelete {comando}',
                                                 'Aliases: `ccdelete`']],

                        'customcommandslist': ['Lista os comandos customizados', 
                                              ['Lista os comandos customizados',
                                               'Use: !customcommandslist',
                                               'Aliases: `cclist`']]}],

            'economy': ['economia', 
                       ['Este é o sistema de economia do servidor',
                        'Você pode ganhar coins trabalhando e diariamente',
                        'E pode gastá-los por ítens na loja',
                        'Com sistema de inventário, ítens equipáveis e consumíveis',
                        'Salvo em database, portanto o bot pode ser reiniciado normalmente'],
                        {'daily': ['Recebe seus coins diários', 
                                  ['Recebe seus coins diários',
                                   'Pode ser resgatado a cada 24 horas',
                                   'Resgatando todos os dias você ganha um bônus',
                                   'Use: !daily',
                                   'Aliases: `diario`']],
 
                         'work': ['Trabalhe a cada hora', 
                                 ['Trabalha a cada hora', 
                                  'Recebe entre 100 e 200 coins por trabalho',
                                  'Use: !work',
                                  'Aliases: `trabalhar`']],
 
                         'balance': ['Ver o saldo de um membro', 
                                    ['Ver o saldo de um membro',
                                     'Caso não inserir um membro, veja seu próprio saldo',
                                     'Use: !balance [membro]',
                                     'Aliases: `money`, `saldo`, `bal`']],
 
                         'pay': ['Transfere uma quantia a um membro', 
                                ['Transfere uma quantia a um membro',
                                 'Há uma taxa de transferência de 10%',
                                 'Use: !pay {membro} {quantia}',
                                 'Aliases: `pagar`, `transferir`']],

                         'shop': ['Exibe os ítens da loja', 
                                 ['Exibe os ítens da loja',
                                  'Ou informações sobre um ítem',
                                  'Use: !shop [item]',
                                  'Aliases: `loja`']],
 
                         'buy': ['Adquirir um ítem da loja',
                                ['Adquirir um ítem da loja',
                                 'Use: !buy {item}',
                                 'Aliases: `comprar`, `adquirir`']],
 
                         'inventory': ['Exibe um inventário', 
                                      ['Exibe seu inventário',
                                       'Ou mencione um membro para exibir o dele',
                                       'Use: !inventory {membro}',
                                       'Aliases: `inv`, `inventario`']],
 
                         'use': ['Utiliza um ítem do inventário', 
                                ['Utiliza um consumível do inventário',
                                 'Use: !use {item}',
                                 'Aliases: `usar`, `consumir`']],

                         'equip': ['Equipa um ítem do inventário', 
                                  ['Equipa um ítem equipável no inventário',
                                   'Use: !equip {\item}',
                                   'Aliases: `equipar`']],

                         'eco': ['Edita o saldo de um membro', 
                                ['Edita o saldo de um membro',
                                 'Argumentos possíveis: `add`, `take`, `set`, `reset`',
                                 'Uso: !eco (add/take/set/reset) {membro} [valor]']],
 
                         'giveitem': ['Dá um ítem a um membro', 
                                     ['Dá um ítem a um membro',
                                      'Uso: !giveitem {membro} {item}']],
 
                         'item': ['Tira um ítem de um membro', 
                                 ['Tira um ítem de um membro',
                                  'Uso: !takeitem {membro} {item}']],
 
                         'clearinventory': ['Limpa o inventário de um membro', 
                                           ['Limpa o inventário de um membro',
                                            'Uso: !clearinventory {membro}']]}],

            'giveaways': ['sorteios', 
                         ['Este é o sistema de sorteios do servidor',
                          'Sorteios com número de ganhadores customizável',
                          'Pode ser resorteado e encerrado prematuramente',
                          'Salvos em database, caso o bot reinicie os sorteios continuam'], 
                          {'gcreate': ['Inicia a criação de um sorteio',
                                      ['Inicia a criação de um sorteio',
                                       'Criação intuitiva, com perguntas',
                                       'Use: !gcreate',
                                       'Aliases: `sortear`']],

                           'gdelete': ['Apaga um sorteio', 
                                      ['Apaga um sorteio',
                                       'Use: !gdelete {id}',
                                       'Aliases: `delsorteio`']],
 
                           'greroll': ['Resorteia o vencedor de um sorteio',
                                      ['Resorteia o vencedor de um sorteio',
                                       'O vencedor antigo não participa novamente',
                                       'Use: !greroll {id}',
                                       'Aliases: `resortear`']],
 
                           'gend': ['Finaliza um sorteio prematuramente', 
                                   ['Finaliza um sorteio prematuramente',
                                    'Diferente de !gdelete, que apaga o sorteio',
                                    'Use: !gend {id}',
                                    'Aliases: `endsorteio`']]}],

            'categories': ['categorias', 
                          ['Todas as categorias se aplicam para o comando `!sobre`',
                           'As categorias em **negrito** se aplicam para o `!ajuda`',
                           '',
                           'anuncios, **apis**, **custom**, **economia**, **sorteios**, **categorias**',
                           '**niveis**, loggers, **moderacao**, **musica**, **perfil**, **cargos**,',
                           'stats, **tempchannels**, **tickets**, **misc**'], {}],

            'help': ['sobre e ajuda', 
                    ['Esses são os menus de ajuda do servidor',
                     'Pode usar !help {categoria} e !about {categoria}',
                     'Para exibir as categorias, use !help categorias'],
                     {'sobre': ['Exibe informações sobre uma categoria', 
                               ['Exibe informações sobre uma categoria',
                                'Use: !sobre {categoria}']],

                      'ajuda': ['Exibe informações sobre comandos',
                               ['Exibe informações sobre comandos',
                                'Caso inserir uma categoria, lista os comandos da mesma',
                                'Caso inserir um comando, exibe suas informações',
                                'Use: !ajuda {categoria/comando}']]}],

            'levels': ['niveis', 
                      ['Este é o sistema de níveis e EXP do servidor',
                       'Você pode obter EXP conversando no chat e participando de calls',
                       'Futuramente EXP de mensagens e calls serão separados',
                       'Salvo em database, portanto o bot pode ser reinciado normalmente'], 
                       {'level': ['Exibe o nível de um jogador', 
                                 ['Exibe o nível de um jogador',
                                  'Exibe seu nível caso não mencionar nenhum',
                                  'Use: !level [membro]']],
 
                        'rank': ['Exibe o rank de um jogador', 
                                ['Exibe o rank de um jogador',
                                 'Exibe seu rank caso não mencionar nenhum',
                                 'Use: !rank [membro]']],
 
                        'leaderboard': ['Exibe o top 10 de XP', 
                                       ['Exibe o top 10 de XP',
                                        'Pode exibir também o top 10 calls e top 10 mensagens',
                                        'Use: !leaderboard [xp|msg]']],

                        'setexp': ['Define o XP de um membro', 
                                  ['Define o XP de um membro',
                                   'Deve ser superior a 0',
                                   'Use: !setexp {membro} {valor}',
                                   'Aliases: `setxp`']],
 
                        'addexp': ['Adiciona XP a um membro', 
                                  ['Adiciona XP a um membro',
                                   'Deve ser superior a 0',
                                   'Use: !addexp {membro} {valor}',
                                   'Aliases: `addxp`']],
 
                        'takeexp': ['Remove XP de um membro', 
                                   ['Remove XP de um membro',
                                    'Deve ser superior a 0',
                                    'Use: !takeexp {membro} {valor}',
                                    'Aliases: `takexp`']],
 
                        'resetexp': ['Reseta o XP de um membro', 
                                    ['Reseta o XP de um membro',
                                     'Use: !resetexp {membro} {valor}',
                                     'Aliases: `resetxp`']]}],

            'loggers': ['loggers', 
                       ['Salvam diversas ações em canais de texto customizaveis',
                        'Ações como comandos, mensagens editadas e apagadas',
                        'Perfis editados, avatares editados e nomes editados',
                        'Conta também com anúncio de entradas e saídas do servidor'], {}],

            'moderation': ['moderação',
                          ['Sistema de punições e gerenciamento do servidor',
                           'Comandos de punições básicas e warnings',
                           'Warnings com punições automáticas e customizáveis',
                           'Gerenciamento facilitado, com comandos uteis',
                           'Punições e warnings salvos todos em database'], 
                           {'ticketban': ['Bane um membro de criar tickets', 
                                         ['Bane um membro de criar tickets',
                                          'Use: !ticketban {membro} [motivo]']],
 
                            'unticketban': ['Desbane um membro de criar tickets', 
                                           ['Use: !unticketban {membro}']],
 
                            'ban': ['Bane um membro do servidor', 
                                   ['Bane um membro do servidor',
                                    'Apaga as mensagens dos últimos 7 dias',
                                    'Use: !ban {membro} [motivo]']],
 
                            'unban': ['Desbane um membro do servidor', 
                                     ['Desbane um membro do servidor',
                                      'Deve inserir o ID do membro',
                                      'Use: !unban {id}']],
 
                            'kick': ['Expulsa um membro do servidor', 
                                    ['Expulsa um membro do servidor',
                                     'Use: !kick {membro} [motivo]']],
 
                            'timeout': ['Castiga um membro do servidor', 
                                       ['Castiga um membro do servidor',
                                        'A duração deve ser em [tempo(s/m/h/d)]',
                                        '[S]egundos, [m]inutos, [h]oras, [d]ias',
                                        'Use: !timeout {membro} {duração} [motivo]',
                                        'Aliases: `mute`']],
 
                            'untimeout': ['Remove o castigo de um membro', 
                                         ['Remove o castigo de um membro',
                                          'Use: !untimeout {membro}',
                                          'Aliases: `unmute`']],
 
                            'warn': ['Adverte um membro do servidor', 
                                    ['Adverte um membro do servidor',
                                     'Punições automáticas serão aplicadas como abaixo',
                                     '\n'.join(AUTO_PUNISHMENTS),
                                     'Use: !warn {membro} [motivo]']],

                            'unwarn': ['Remove uma advertência de um membro', 
                                      ['Remove a advertência mais recente ativa de um membro',
                                       'Ex: se o membro possuir 5 advertências, ficará com 4',
                                       'Sendo removida apenas a mais recente',
                                       'Use: !unwarn {membro}']],
 
                            'warnings': ['Lista as advertências de um membro', 
                                        ['Lista as advertências ativas de um membro',
                                         'Use: !warnings {membro}']],
 
                            'clear': ['Limpa as mensagens de um chat', 
                                     ['Limpa as mensagens de um chat',
                                      'Pode inserir e limpar apenas as mensagens de um membro',
                                      'Para limpar as do bot, digite "bot" no lugar do membro',
                                      'Use: !clear {quantidade} [membro]']],
 
                            'slowmode': ['Ativa o modo lento em um chat ', 
                                        ['Define o tempo do modo lento de um chat',
                                         'Insira o tempo em segundos',
                                         'Insira `0` para desativá-lo',
                                         'Use: !slowmode {tempo}']],
 
                            'setnickname': ['Altera o nick de um membro', 
                                           ['Altera o nick de um membro',
                                            'Use: !setnickname {membro} {nick}']],
 
                            'history': ['Exibe as punições de um membro', 
                                       ['Lista todas as punições de um membro',
                                        'Até mesmo as removidas e expiradas',
                                        'Use: !history {membro}']],
 
                            'clearhistory': ['Limpa o histório de um membro', 
                                            ['Limpa o histórico de punições de um membro',
                                             'Não é possível voltar atrás',
                                             'As punições são apagadas da database',
                                             'Use: !clearhistory {membro}']],

                            'lock': ['Bloqueia um canal', 
                                    ['Bloqueia o cargo `everyone` de enviar mensagens em um canal',
                                     'Use: !lock']],
 
                            'unlock': ['Desbloqueia um canal', 
                                      ['Permite o cargo `everyone` a enviar mensagens em um canal novamente',
                                       'Use: !unlock']]}],

            'musics': ['música', 
                      ['Sistema de música do servidor com fila',
                       'Pode tocar musicas do YouTube e Spotify',
                       'Conta com diversos comandos para fácil uso',
                       'Sistema de permissões para ações como pular música ou limpar a fila',
                       'Leaderboard com as músicas mais tocadas e os membros que mais ouvem',
                       'Efeitos de áudio como áudio 8D ou bass boost'], 
                       {'join': ['Faz o bot entrar em seu canal de voz', 
                                ['Faz o bot conectar em seu canal de voz',
                                 'Apenas conectará se não estiver em outro canal',
                                 'Use: !join']],

                        'leave': ['Desconecta o bot de seu canal de voz',
                                 ['Desconecta o bot de seu canal de voz',
                                  'Apenas funciona se o bot estiver no mesmo canal de voz que você',
                                  'Use: !leave']],

                        'play': ['Adiciona uma música a fila',
                                ['Adiciona uma música ao final da fila',
                                 'Deve ser um link ou uma pesquisa do YouTube',
                                 'Use: !play {link ou termo de pesquisa}']],

                        'insert': ['Insere uma música como próxima da fila',
                                  ['Insere uma música como próxima da fila',
                                   'Deve ser um link ou uma pesquisa do YouTube',
                                   'Use: !insert {link ou termo de pesquisa}']],

                        'replay': ['Adiciona a música atual ao final da fila',
                                  ['Adiciona a música atual ao final da fila',
                                   'Use: !replay']],

                        'pause': ['Pausa o tocador de música',
                                 ['Pausa o tocador de música',
                                  'Use: !pause']],

                        'resume': ['Resume/despausa o tocador de música',
                                  ['Resume/despausa o tocador de música',
                                   'Use: !resume']],

                        'forward': ['Adianta a música',
                                   ['Adianta a música pelo tempo escolhido',
                                    'Formato do tempo: {número}(s/m)',
                                    'Exemplo: 15s, 40s, 2m',
                                    'Use: !forward {tempo}']],

                        'backwards': ['Volta a música',
                                     ['Volta a música pelo tempo escolhido',
                                      'Formato do tempo: {número}(s/m)',
                                      'Exemplo: 15s, 40s, 2m',
                                      'Use: !backwards {tempo}']],

                        'restart': ['Reinicia a música atual',
                                   ['Reinicia a música atual',
                                    'Use: !restart']],

                        'volume': ['Define o volume da música',
                                  ['Define o volúme da música',
                                   'Aviso: Volume acima de 100 estoura a música',
                                   'Não recomendado volume acima de 200',
                                   'Use: !volume 0-500']],

                        'nowplaying': ['Exibe informações sobre a música atual',
                                      ['Exibe informações sobre a música atual',
                                       'Informações como: título, canal, duração, views e link',
                                       'Use: !nowplaying']],

                        'lasttrack': ['Exibe informações sobre a última música',
                                     ['Exibe informações sobre a última música',
                                      'Informações como: título, canal, duração, views e link',
                                      'Use: !lasttrack']],

                        'nexttrack': ['Exibe informações sobre a próxima música',
                                     ['Exibe informações sobre a próxima música',
                                      'Informações como: título, canal, duração, views e link',
                                      'Use: !nexttrack']],

                        'queue': ['Exibe a fila de músicas',
                                 ['Exibe a fila de músicas',
                                  'Use: !queue']],

                        'trackinfo': ['Exibe informações sobre alguma música da fila',
                                     ['Exibe informações sobre alguma música da fila',
                                      'Use: !trackinfo {número da música}']],

                        'reverse': ['Inverte a fila',
                                   ['Inverte a fila',
                                    'Use: !reverse']],

                        'shuffle': ['Embaralha a fila',
                                   ['Embaralha a fila',
                                    'Use: !shuffle']],

                        'sort': ['Ordena a fila',
                                ['Ordena a fila',
                                 'Critérios possíveis: artist, name, views, length',
                                 'Traduz-se para artista, nome, views e duração',
                                 'Use: !sort {critério}']],

                        'move': ['Troca o lugar de uma música na fila',
                                ['Troca o lugar de uma música na fila',
                                 'Use: !move {lugar inicial} {lugar final}']],

                        'swap': ['Troca duas músicas de lugar',
                                ['Troca duas músicas de lugar',
                                 'Use: !swap {música 1} {música 2}']],

                        'previous': ['Volta para a música anterior',
                                    ['Volta para a música anterior',
                                     'Use: !previous']],

                        'skip': ['Inicia uma votação ou vota para pular a música atual',
                                ['Inicia uma votação ou vota para pular a música atual',
                                 'É necessário que metade dos membros na call votem',
                                 'Use: !skip']],

                        'forceskip': ['Pula a música atual imediatamente',
                                     ['Pula a música atual imediatamente',
                                      'Use: !forceskip']],

                        'restartqueue': ['Reinicia a fila',
                                        ['Reinicia a fila e volta para a 1° música',
                                         'Use: !restartqueue']],

                        'loop': ['Coloca a música atual em loop',
                                ['Coloca a música atual em loop',
                                 'Use: !loop']],

                        'loopqueue': ['Coloca a fila em loop',
                                     ['Coloca a fila em loop',
                                      'Quando terminar a última música, volta para a primeira',
                                      'Use: !loopqueue']],

                        'random': ['Ativa a ordem aleatória',
                                  ['Ativa a ordem aleatória',
                                   'Use: !random']],

                        'clear': ['Limpa a fila',
                                 ['Limpa a fila',
                                  'Use: !clear']],

                        'remove': ['Remove uma música da fila',
                                  ['Remove uma música da fila',
                                   'Use: !remove {número da música}']],

                        'removedupes': ['Remove as músicas duplicadas na fila',
                                       ['Remove as músicas duplicadas na fila',
                                        'Use: !removedupes']],

                        'musicleaderboard': ['Mostra os membros que mais ouviram músicas',
                                            ['Mostra os membros que mais ouviram músicas',
                                             'Use: !musicleaderboard {membro}']],

                        'mostplayedmusics': ['Mostra as músicas mais tocadas',
                                            ['Mostra as músicas mais tocadas',
                                             'Use: !mostplayedmusics']],

                        'musicprofile': ['Mostra o perfil musical de um membro',
                                        ['Mostra o perfil musical de um membro',
                                         'Ou o seu, caso não mencione ninguém',
                                         'Use: !musicprofile [membro]']]}],

            'profiles': ['perfis', 
                        ['Sistema de perfis customizados do servidor',
                         'Podem ser editados fácil e intuitivamente usando `!edit`',
                         'Salvos em database, portanto o bot pode ser reiniciado normalmente'], 
                         {'edit': ['Edita seu perfil',
                                  ['Edita seu perfil',
                                   'Ítens permitidos: titulo, apelido, sobremim, aniversario, cor, imagem',
                                   'Use: !edit {ítem} {valor}']],

                          'profile': ['Exibe o perfil de um membro',
                                     ['Exibe o perfil de um membro',
                                      'Ou o seu, caso não mencione ninguém',
                                      'Use: !profile [membro]']],

                          'rep': ['Dá +rep para um membro',
                                 ['Dá +rep para um membro',
                                  'Semelhante ao +rep da Steam',
                                  'Cooldown de 24 horas',
                                  'Use: !rep {membro}']],

                          'nextbirthdays': ['Exibe os próximos 10 aniversários',
                                           ['Exibe os próximos 10 aniversarios',
                                            'Use: !nextbirthdays']],
 
                          'adminedit': ['Edita o perfil de outro membro (ADMIN)',
                                       ['Edita o perfil de outro membro (ADMIN)',
                                        'Ítens permitidos: titulo, apelido, sobremim, aniversario, cor, imagem',
                                        'Use: !adminedit {membro} {ítem} {valor}']]}],

            'roles': ['cargos', 
                     ['Sistema de cargos do servidor',
                      'Atualmente conta apenas com cargo automático ao entrar',
                      'E também com sistema de `!registro` ampliável'], 
                      {'register': ['Inicia o registro',
                                   ['Inicia o registro',
                                    'Para receber cargos personalizados',
                                    'Cargos como +18/-18, gênero e cor personalizada',
                                    'Use: !register']]}],

            'stats': ['estatísticas', 
                     ['Sistema para exibir as estatísticas do servidor, assim como do YouTube e Twitch',
                      'Exibe essas estatísticas em canais de voz privados, no fim da lista de canais',
                      'Pode ser customizado apenas pelo admin via configuração'], {}],

            'tempchannels': ['canais temporários', 
                            ['Sistema para a criação de canais temporários',
                             'O dono do canal pode adicionar e remover membros assim que necessário',
                             'Possível gerar transcrição do canal, e gerada automaticamente quando apagado',
                             'Canais temporários expiram em uma semana de inatividade',
                             'Um membro pode ter um canal temporário de voz e um de texto simultaneamente',
                             'Salvos em database, para um facil gerenciamento'], 
                             {'tempchannel': ['Inicia a criação de um canal temporário',
                                             ['Inicia a criação de um canal temporário',
                                              'Use: !tempchannel']],

                              'tcdelete': ['Apaga um canal temporário',
                                          ['Apaga um canal temporário',
                                           'Para apagar um canal de texto, execute este comando nele',
                                           'Para apagar um canal de voz, use !tcdelete {@canal}',
                                           'Use: !tcdelete [@canal]']],

                              'tcadd': ['Adiciona membros ao canal temporário',
                                       ['Adiciona membros ao canal temporário',
                                        'Pode mencionar quantos membros quiser',
                                        'Use: !tcadd {menções}']],

                              'tcremove': ['Remove membros do canal temporário',
                                          ['Remove membros do canal temporário',
                                           'Pode mencionar quantos membros quiser',
                                           'Use: !tcremove {menções}']],

                              'tctranscript': ['Gera uma transcrição do canal temporário', 
                                              ['Gera uma transcrição do canal temporário',
                                               'Transcreve TODAS as mensagens do canal de texto',
                                               'Contém o ID de todos os membros da história do canal',
                                               'Deve ser executado dentro do canal a ser transcrito',
                                               'Use: !tctranscript']],

                              'tcadmin': ['Exibe os comandos de admin dos canais temporários',
                                         ['Exibe os comandos de admin dos canais temporários',
                                          'Comando interativo',
                                          'Use: !tcadmin']]}],

            'tickets': ['tickets', 
                       ['Sistema de criação de tickets via comando',
                        'Membros podem ser adicionados assim que necessário',
                        'Limite customizável de 2 tickets por membro',
                        'Possível gerar transcrição do canal, e gerada automaticamente quando apagado',
                        'Tickets criados em categorias persoonalizáveis',
                        'Salvos em database, para um facil gerenciamento'], 
                        {'ticket': ['Inicia a criação de um ticket',
                                   ['Inicia a criação de um ticket',
                                    'Comando interativo',
                                    'Use: !ticket']],

                         'tclose': ['Fecha um ticket',
                                   ['Fecha um ticket',
                                    'O ticket continuará existindo',
                                    'Porém só a equipe poderá vê-lo',
                                    'Use: !tclose']],

                         'topen': ['Reabre um ticket',
                                  ['Reabre um ticket',
                                   'Use: !topen']],

                         'tdelete': ['Apaga um ticket',
                                    ['Apaga um ticket',
                                     'O ticket precisa estar fechado (!close)',
                                     'Use: !tdelete']],

                         'tadd': ['Adiciona um membro ao ticket',
                                 ['Adiciona um membro ao ticket',
                                  'Use: !tadd {membro}']],

                         'tremove': ['Remove um membro do ticket',
                                    ['Remove um membro do ticket',
                                     'Use: !tremove {membro}']],

                         'trename': ['Renomeia um ticket',
                                    ['Renomeia um ticket',
                                     'Use: !trename {novo nome}']],

                         'ttranscript': ['Gera uma transcrição do ticket',
                                       ['Gera uma transcrição do canal temporário',
                                        'Transcreve TODAS as mensagens do ticket',
                                        'Contém o ID de todos os membros da história do ticket',
                                        'Use: !ttranscript']]}],

            'misc': ['miscelânea', 
                    ['Sistemas que não se encaixam em outras categorias',
                     'Como encurtador de URL, "say" para enviar mensagem como o bot',
                     'Geradores de números, informações sobre o servidor e membros, etc',
                     'Conta com sistema de lembretes',
                     'Para ver a lista completa de comandos, use `!help misc`'], 
                     {'random': ['Gera um número aleatório',
                                ['Gera um número aleatório',
                                 'Padrão: número de 0-100',
                                 'Use: !random {min} {max}']],

                      'dado': ['Roda um dado',
                              ['Roda um dado',
                               'Semelhante ao !random, porém o mínimo é sempre 1',
                               'Use: !dado {tamanho}']],

                      'jankenpon': ['Joga pedra papel tesoura',
                                   ['Joga pedra papel tesoura',
                                    'Use: !jankenpon {pedra/papel/tesoura}']],

                      'escolher': ['Escolhe um entre dois ou mais ítens',
                                  ['Escolhe um entre dois ou mais ítens',
                                   'Separe-os por vírgula ou espaço',
                                   'Use: !escolher {ítens}']],

                      'shorten': ['Encurta um link',
                                 ['Encurta um link usando TinyURL',
                                  'Cooldown de 60 segundos',
                                  'Use: !shorten {URL}']],

                      'remindme': ['Cria um lembrete',
                                  ['Cria um lembrete',
                                   'Comando interativo',
                                   'Cooldown de 60 segundos',
                                   'Use: !remindme']],

                      'poll': ['Cria uma enquete',
                              ['Cria uma enquete em embed',
                               'Comando interativo',
                               'Use: !poll']],

                      'ping': ['Exibe a latência atual do bot',
                              ['Exibe a latência atual do bot',
                               'Assim como informações sobre a shard',
                               'Use: !ping']],

                      'avatar': ['Exibe o avatar de um membro',
                                ['Exibe o avatar de um membro',
                                 'Caso não mencionar ninguém, exibe seu avatar',
                                 'Use: !avatar [membro]']],

                      'userbanner': ['Exibe o banner de um membro',
                                    ['Exibe o banner de um membro',
                                     'Caso não mencionar ninguém, exibe seu banner',
                                     'Use: !userbanner [membro]']],

                      'userinfo': ['Exibe as informações de um membro',
                                  ['Exibe as informações de um membro',
                                   'Caso não mencionar ninguém, exibe suas informações',
                                   'Use: !userinfo [membro]']],

                      'serverbanner': ['Exibe o banner do servidor',
                                      ['Exibe o banner do servidor',
                                       'Use: !serverbanner']],

                      'serverinfo': ['Exibe as informações do servidor',
                                    ['Exibe as informações do servidor',
                                     'Use: !serverinfo']],

                      'servericon': ['Exibe o ícone do servidor',
                                    ['Exibe o ícone do servidor',
                                     'Use: !servericon']],

                      'say': ['Envia uma mensagem como o bot',
                             ['Envia uma mensagem pelo usuário do bot',
                              'Para mencionar usuários, use %everyone% ou %here%',
                              'Use: !say {mensagem}']]}]}

command_names: list = [command for category in MESSAGES.values() for command in category[2]]
command_explanations: list = [category[2][command] for category in MESSAGES.values() for command in category[2]] #type: ignore
commands_dict: dict = {k: v for k, v in zip(command_names, command_explanations)}

class AboutCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.creator_id = 2345678987964352
    
    @commands.command(aliases=['about', 'help'])
    async def sobre(self, ctx, arg = None):
        category: str | None = None
        for key, values in CATEGORY_MAPPING.items():
            if arg in values:
                category = key
                break

        command: str | None = arg if arg in command_names else None

        if category:
            message = '\n'.join(MESSAGES[category][1])

            if MESSAGES[category][2]:
                commands: dict = {item:MESSAGES[category][2][item][0] for item in MESSAGES[category][2]} #type: ignore
                message += '\n\nComandos:\n'
                message += '\n'.join([f'!{command_key} - {commands[command_key]}' for command_key in commands.keys()])
            
            embed = discord.Embed(title=f'Informações de {MESSAGES[category][0]}', description=message)
            await ctx.send(embed=embed)

        elif command:
            message = '\n'.join(commands_dict[command][1])
            embed = discord.Embed(title=f'Ajuda sobre !{command}', description=message)
            embed.set_footer(text=f'Comando enviado por {ctx.author.display_name} ({ctx.author.id}).')
            await ctx.send(embed=embed)

        else:
            creator_user = self.bot.get_user(self.creator_id)
            embed=discord.Embed(title="Bot da Gaby!")
            #embed.set_thumbnail(url="http")
            embed.add_field(name="Minha Twitch!", value="https://twitch.tv/gaby_ballejo", inline=False)
            embed.add_field(name="Criado por", value=f"https://github.com/eduardogott\nDC: {creator_user.name}#{creator_user.discriminator}", inline=False)
            embed.add_field(name="Latência", value=f"{round(self.bot.latency, 0)}ms")
            embed.set_footer(text="Para mais informações digite !about|help {categoria}, ou !about categorias para vê-las")
            await ctx.send(embed=embed)

            
async def setup(bot):
    await bot.add_cog(AboutCommand(bot))