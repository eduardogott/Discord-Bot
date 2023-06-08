# BotDaGaby

Este é um bot de Discord que eu criei quando tava no tédio, só funciona para UM servidor por token.

- [Comandos](#comandos----comando--opções---obrigatório---opcional---)
  * [Economia](#economia)
  * [Sorteios](#sorteios)
  * [Níveis](#níveis)
  * [Moderação](#moderação---todos-os-comandos-são-de-admin)
  * [Música](#música)
  * [Perfis](#perfis)
  * [Cargos](#cargos)
  * [Úteis/Miscelânea](#úteis-miscelânea)
- [Sistemas](#sistemas)
  * [Anunciadores](#anunciadores)
  * [Economia](#economia-1)
  * [Sorteios](#sorteios-1)
  * [Níveis](#níveis-1)
  * [Loggers](#loggers)
  * [Moderação](#moderação)
  * [Música](#música-1)
  * [Perfis](#perfis-1)
  * [Cargos](#cargos-1)
  * [Úteis/Miscelânea](#úteis-miscelânea-1)

# Comandos (`!comando (opções) {obrigatório} [opcional]`)

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


## Sorteios

- !gcreate - Inicia a criação de um sorteio
- !gdelete {id} - Apaga um sorteio baseado no ID da mensagem
- !greroll {id} - Refaz o sorteio baseado no ID da mensagem
- !gend {id} - Encerra um sorteio prematuramente baseado no ID da mensagem


## Níveis

- !level {member} - Exibe o nível e EXP de um jogador, se não mencionado, exibe seu nível e EXP
- !rank {member} - Exibe o lugar de um membro na tabela e informações sobre seu nível e EXP, se não mencionado, exibe suas informações
- !leaderboard - Exibe o top 10 jogadores em ordem de EXP
- !setexp {member} {exp} - ADMIN - Define o EXP de um membro
- !addexp {member} {exp} - ADMIN - Adiciona EXP a um membro
- !removeexp {member} {exp} - ADMIN - Remove EXP de um membro
- !resetexp {member} - ADMIN - Reseta o EXP de um membro


## Moderação - TODOS OS COMANDOS SÃO DE ADMIN

- !ban {member} [reason] - Bane um membro por um motivo (opcional)
- !unban {member_id} - Desbane um membro do servidor
- !kick {member} {reason} - Expulsa um membro por um motivo (opcional)
- !timeout {member} {duration(s/m/h/d)} {reason} - Silencia um membro por tempo determinado por um motivo (opcional)
- !untimeout {member} - Remove o silenciamento de um membro
- !clear {quantity} - Limpa a quantidade de mensagens do canal atualn
- !slowmode {time(s/m/h/d)} - Define o 'modo lento' do canal para uma duração (em segundos)
- !setnickname {member} {nickname} - Define o nickname de um membro
- !history {member} - Lista todas as punições de um membro
- !clearhistory {member} - Limpa a lista de punições de um mebro
- !lock - Bloqueia o cargo @everyone de falar no canal atual 
- !unlock - Permite o cargo @everyone de falar no canal atual novamente 
- !warn {member} {reason} - Adverte um membro por um motivo (opcional) 
- !unwarn {member} - Remove uma advertência de um membro
- !warnings {member} - Lista todas as advertências ativas de um membro


## Música

- !play {music} - Adiciona uma música a fila (link ou 'pesquisa' do YouTube)
- !skip - Pula a música atual
- !clearqueue - DJ -Limpa a fila
- !queue - Lista as musicas na fila
- !remove {index} - DJ - Remove uma música da fila
- !pause - Pausa a música atual
- !resume - Resume a música atual
- !nowplaying - Exibe informações da música atual
- !replay - Adiciona a música atual ao final da fila


## Perfis

- !edit (title/birthday/nickname/aboutme/color/image/socialmedia) {value} - Edita seu perfil
- !profile {member} - Exibe o perfil de um membro, se não mencionado, exibe seu perfil
- !rep {member} - Adiciona um '+rep' a um membro, similar à Steam
- !nextbirthdays - Lista os próximos 10 aniversários


## Cargos
- !registrar - Inicia o registro


## Úteis/Miscelânea

- !random {min} {max} - Gera um número aleatório entre min-max
- !dice {max} - Rola um dado do tamanho específico
- !jankenpon (rock/paper/scissors) - Joga pedra papel tesoura contra o bot
- !choice {multiargs} - Escolhe um ítem do 'multiargs', separados por espaço
- !shorten {url} - Encurta uma URL usando a API do TinyURL
- !avatar {member} - Exibe o avatar de um membro, se não mencionado, exibe o seu
- !userbanner {member} - Exibe o banner de um membro, se não mencionado, exibe o seu
- !userinfo {member} - Exibe infomações sobre um membro, se não mencionado, exibe o seu
- !serverbanner - Exibe o banner do servidor atual
- !servericon - Exibe o ícone do servidor atual
- !serverinfo - Exibe informações sobre o servidor atual
- !about - Exibe informações sobre o bot e seu criador
- !say(e/h) {message} - ADMIN - Envia uma mensagem pela conta do bot, e=@everyone, h=@here

---

# Sistemas
## Anunciadores

- Anunciador de live on na Twitch
- Anunciador de vídeo novo no YouTube


## Economia

- Sistema de economia com bônus diário, comando !trabalhar a cada duas horas e transferência de dinheiro, tudo salvo em uma database .json
- Sistema de loja e inventário, onde você pode gastar seus coins, tudo salvo na database
- Coins bônus e descontos para cargos específicos, como Sub ou Booster
- Sistema de tabela de liderança, exibindo os 10 jogadores com mais coins
- Gerenciamento de saldo para Admins, com comandos coom adicionar e resetar coins


## Sorteios

- Sistema intuitivo para criação de sorteios, onde você insere o canal que irá acontecer, a duração, o número de ganhadores e o prêmio um por um, tudo salvo na database
- Sistema para encerrar sorteios prematuramente, cancelar sorteios ou resortear um ganhador


## Níveis

- Sistema de nivelamento com '*listeners*' para mensagens e tempo gasto em canais de voz (tempo padrão para recompensa é a cada 5 minutos)
- Pontos bônus para cargos específicos, como Sub ou Booster
- Sistema de tabela de liderança, exibindo os 10 jogadores com mais EXP
- Gerenciamento de EXP para Admins, com comandos como expadd ou expreset


## Loggers
- Sistema para anunciar quando um membro entra ou sai do servidor
- Sitema de '*logar*' perfis editados, mensagens editadas, mensagens fixadas, mensagens apagadas por membros e mensagens apagadas usando !clear


## Moderação
- Sistema para punições básicas (ban, kick, timeout) e seus comandos respectivos (unban, untimeout)
- Todas as punições ficam salvas na database
- Sistema para gerenciamento do servidor, com comandos como clear, slowmode, (un)lock, (clear)history, para gerenciamento mais facil
- Advertências com durações personalizaveis (padrão 30 dias) e punições customizáveis após 'x' advertências, todas salvas na database
- Sistema de moderação automática com bloqueador de flood/spam, convites de discord e menções em excesso


## Música
- Bot simples e padrão de música no Discord
- Comando lyrics para exibir a letra de uma música (usando API Musixmatch)
- Comando replay, inserindo a música atual no fim da fila
- Cargo DJ para comandos selecionados, como clearqueue ou pause/resume


## Perfis
- Sistema de perfis com titulo, aniversario, apelido, sobremim, cor, imagem e redes sociais, tudo salvo na database
- Edite seu perfil facilmente usando !editar
- Sistema de reputação usando !rep, com cooldown customizável (padrão 1 por dia), tudo salvo na database
- Anunciador de aniversário (todo dia, num horário definido) em um canal customizável
- Comando para exibir os próximos 10 aniversários


## Cargos
- Sistema de registro com gênero e idade, editável e ampliável

## Úteis/Miscelânea
- Vários '*RNGs*', (*lit. geradores aleatórios de número*)
- Jankenpon com aposta de coins
- Encurtador de URL usando a API do TinyURL
- Avatar/ícone, banner e informações sobre um usuário ou o servidor 
- Informações sobre o bot e seu criador
- Comando say para anunciar para o servidor usando a conta do bot, @everyone/@here opcionais
