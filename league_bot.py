import discord
import requests
import pandas as pd
import numpy as np
import random
import datetime
import asyncio

from discord.ext import commands, tasks
from riotwatcher import LolWatcher, ApiError

"""
Próximas funções a serem adicionadas:

random_team        -> retorna um time random com suas posições (DONE)
really_random_team -> retorna um time totalmente aleatório
live_game          -> retorna informação sobre os players de determinada partida (DONE) aaaaaaa
lore               -> retorna lore do champ + algumas caracteristicas úteis 
leaderboard        -> retorna o ranking de challengers de acordo com a região
"""

# Keys:     

riot_key        = 
discord_key     = 


# Vars:

watcher         = LolWatcher(riot_key)
latest          = watcher.data_dragon.versions_for_region('br1')['n']['champion']

champ_list      = watcher.data_dragon.champions(latest, False, 'en_US')
skill_list      = watcher.data_dragon.summoner_spells(latest, 'en_US')

footer_text     = '#BlackLivesMatter ✊🏾\n#Pride 🌈'
client          = commands.Bot(command_prefix='>')


# Dicts:

skill_dict      = {}

for key in skill_list['data']:
    row                         = skill_list['data'][key]
    skill_dict[row['key']]      = row['name']

champion_dict   = {}

for key in champ_list['data']:
    row                         = champ_list['data'][key]
    champion_dict[row['key']]   = row['id']

lanes_dict   = {'Top': ['Aatrox', 'Akali', 'Wukong', 'Volibear',
                        'Tahm Kench' ,'Vladimir', 'Yorick', 'Rumble',
                        'Olaf', 'Nasus', 'Teemo', 'Sylas',
                        'Tryndamere', 'Yasuo', 'Irelia', 'Kennen',
                        'Malphite', 'Maokai', 'Mordekaiser', 'Dr. Mundo',
                        """Cho'Gath""", 'Darius', 'Fiora ', 'Garen ',
                        'Gangplank ', 'Gnar ', 'Swain', 'Shen ',
                        'Illaoi', 'Jax', 'Jayce ', 'Kled',
                        'Ryze', 'Camille ', 'Kayle', 'Renekton',
                        'Riven', 'Sion', 'Singed', 'Quinn',
                        'Vayne', 'Urgot', 'Poppy', 'Pantheon',
                        'Ornn'],

                'Jungle': ['Nautilus','Aatrox','Gragas',
                            'Pantheon','Amumu','Evelynn ',
                            'Elise','Malphite','Sylas',
                            'Volibear','Wukong','Olaf',
                            'Dr. Mundo','Jax','Nocturne',
                            'Nidalee','Shaco','Shyvana',
                            'Sejuani','Rengar',"""Rek'Sai""",
                            'Graves','Hecarim','Jarvan IV',
                            'Kayn','Karthus','Kindred',
                            """Kha'zix""",'Lee Sin','Udyr',
                            'Ivern','Rammus','Vi',
                            'Master Yi','Zac','Warwick',
                            'Trundle','Taliyah','Xin Zhao','Skarner'],

                'Middle': ['Brand','Zyra',"""Kog'Maw""",
                           'Zilean','Taliyah','Tristana',
                           'Aatrox','Fizz','Kassadin',
                           'Heimerdinge','LeBlanc','Katarina',
                           'Cassiopeia','Diana','Corki',
                           'Zed',"""Vel'Koz""",'Lissandra',
                           'Swain','Ziggs','Lux','Neeko',
                           'Malzahar','Qiyana','Veigar',
                           'Xerath','Orianna','Yasuo',
                           'Zoe','Viktor','Talon',
                           'Syndra','Twisted Fate','Ryze',
                           'Pantheon','Akali','Ahri',
                           'Anivia','Annie','Azir',
                           'Aurelion','Ekko','Irelia',
                           'Sylas','Vladimir '],

                'Adcarry': ['Yasuo','Kalista','Jhin',
                            'Xayah','Lucian','Ashe',
                            'Varus','Vayne','Tristana',
                            """Kog'Maw""",'Draven','Sivir',
                            'Jinx','Ezreal','Twitch',
                            'Caitlyn','Miss Fortune',"""Kai'Sa"""],

                'Support': ['Veigar', 'Volibear', 'Morgana',
                            'Blitzcrank', 'Braum', 'Bard',
                            'Alistar', 'Janna', 'Lulu',
                            'Leona','Karma','Xerath',
                            'Nami','Yuumi','Fiddlesticks',
                            'Rakan',"""Vel'Koz""", 'Zilean',
                            'Zyra','Brand', 'Galio',
                            'Lux','Soraka', 'Taric',
                            'Thresh','Malphite','Nautilus',
                            """Tahm Kench""",'Sona','Pyke']}

regions_dict = {'br'    :'BR1',
                'eune'  :'EUN1',
                'euw'   :'EUW1',
                'jp'    :'JP1',
                'kr'    :'KR',
                'lan'   :'LA1',
                'las'   :'LA2',
                'na'    :'NA1',
                'oce'   :'OC1',
                'tr'    :'TR1',
                'ru'    :'RU'}

emotes = ['🔥',
          '🌞',
          '⚡️',
          '🍀', 
          '🌟',
          '🪐',
          '☣️',
          '☢️',
          '🌈',
          '👾']



# Classes:

class Player:
    nickname    = ''
    level       = ''
    pIcon       = ''
    flex_elo    = 'UNRANKED'
    flex_tier   = ''
    flex_wins   = '0'
    flex_losses = '0'
    solo_elo    = 'UNRAKED'
    solo_tier   = ''
    solo_wins   = '0'
    solo_losses = '0'
    pool        = []
    champ_list  = []
    champs      = ''

    # At champs we have:
    # index:      champions names
    # Maestry:    maestry level
    # Points:     maestry points

    def __init__(self, player_info: list, player_league:list , data:pd.DataFrame):
        self.nickname       = player_info['name']
        self.level          = player_info['summonerLevel']
        self.pIcon          = player_info['profileIconId']
        
        try:
            if player_league[0]['queueType'] == 'RANKED_FLEX_SR':

                self.flex_elo       = player_league[0]['tier']
                self.flex_tier      = player_league[0]['rank']
                self.flex_wins      = player_league[0]['wins']
                self.flex_losses    = player_league[0]['losses']
            else:
                self.solo_elo       = player_league[0]['tier']
                self.solo_tier      = player_league[0]['rank']
                self.solo_wins      = player_league[0]['wins']
                self.solo_losses    = player_league[0]['losses']

        except:
            # print('Player has not played 10 Flex Games yet')
            pass

        try:
            if player_league[1]['queueType'] == 'RANKED_FLEX_SR':
                self.flex_elo       = player_league[1]['tier']
                self.flex_tier      = player_league[1]['rank']
                self.flex_wins      = player_league[1]['wins']
                self.flex_losses    = player_league[1]['losses']
            else:
                self.solo_elo       = player_league[1]['tier']
                self.solo_tier      = player_league[1]['rank']
                self.solo_wins      = player_league[1]['wins']
                self.solo_losses    = player_league[1]['losses']

        except:
            pass
            # print('Player has not played 10 Solo Games yet')

        self.champs         = data
        self.pool           = data.index[:5].tolist()

# Functions:

def find(player_nick, player_region):
    try:
        info                = watcher.summoner.by_name(player_region, player_nick)
        ranked_info         = watcher.league.by_summoner(player_region, info['id'])
        player_mastery      = watcher.champion_mastery.by_summoner(player_region, info['id'])

    except:
        return

    champion_rank       = []

    for row in player_mastery:
        maestry_row                 = {}
        maestry_row['Champion']     = row['championId']
        maestry_row['Maestry']      = row['championLevel']
        maestry_row['Points']       = row['championPoints']
        champion_rank.append(maestry_row)

    for row in champion_rank:
        row['championName']         = champion_dict[str(row['Champion'])]

    df          = pd.DataFrame(champion_rank)
    df.set_index('championName', inplace = True)

    selected_df = df[['Maestry','Points']]


    return (info, ranked_info, selected_df)

def match_analyse(region: str, nickname: str, match: list, i: int) -> dict:
    # Returns the useful information from the match at player_info, more useful information can be added later.
    
    player_list     = []
    match_detail    = watcher.match.by_id(region, match['gameId'])

    for player in match_detail['participantIdentities']:
        player_list.append(player['player']['summonerName'])
    
    cursor          = player_list.index(nickname)

    player_info = {}
    player_info['champion']            = champion_dict[str(match_detail['participants'][cursor]['championId'])]
    player_info['spell1']              = skill_dict[str(match_detail['participants'][cursor]['spell1Id'])]
    player_info['spell2']              = skill_dict[str(match_detail['participants'][cursor]['spell2Id'])]
    player_info['win']                 = match_detail['participants'][cursor]['stats']['win']
    player_info['kills']               = match_detail['participants'][cursor]['stats']['kills']
    player_info['deaths']              = match_detail['participants'][cursor]['stats']['deaths']
    player_info['assists']             = match_detail['participants'][cursor]['stats']['assists']
    player_info['totalDamageDealt']    = match_detail['participants'][cursor]['stats']['totalDamageDealt']
    player_info['goldEarned']          = match_detail['participants'][cursor]['stats']['goldEarned']
    player_info['totalMinionsKilled']  = match_detail['participants'][cursor]['stats']['totalMinionsKilled']
    player_info['largestMultiKill']    = match_detail['participants'][cursor]['stats']['largestMultiKill']
    player_info['lane']                = match_detail['participants'][cursor]['timeline']['lane']
    player_info['gameMode']            = match_detail['gameMode']
    # barons                             = last_match_detail['teams']['baronKills']
    # dragons                            = last_match_detail['teams']['dragonKills']
    player_info['gameNumb']            = int(i + 1)

    return player_info

def historic_embed(hist_list: list, player_info: dict, page_number: int):
    # Returns the match embed

    colour1 = 0
    colour2 = 0
    colour3 = 0
    
    if(player_info['win'] == True):
        colour1 = 0
        colour2 = 255
        colour3 = 0

    else:
        colour1 = 255
        colour2 = 0
        colour3 = 0  

    if(player_info['gameMode'] == 'ARAM'):
        pag = discord.Embed(
                title = 'Match {}/10'.format(page_number+1),
                description = str(player_info['gameMode']).capitalize(),
                colour = discord.Color.from_rgb(int(colour1), int(colour2),int(colour3))
            )
        if player_info['win']:
            win = 'Yes 🥳'
        else:
            win = 'No 😓'

        pag.add_field(name = 'Won?', value = win, inline = False)
        pag.add_field(name = 'Champion:', value = '{}'.format(player_info['champion']), inline = False)

        pag.add_field(name = 'Sumonner Spells:', value = '{} and {}'.format(player_info['spell1'],
                                                                            player_info['spell2']), inline = False)

        pag.add_field(name = 'KDA:', value = '{}/{}/{}'.format(player_info['kills'],
                                                               player_info['deaths'],
                                                               player_info['assists']), inline = True)

        pag.add_field(name = 'CS:', value = '{} Minons'.format(player_info['totalMinionsKilled']), inline = True)
        pag.add_field(name = 'Gold earned:', value ='{} Gold'.format(player_info['goldEarned']), inline = True )
        pag.add_field(name = 'Damage dealt:', value ='{} Damage'.format(player_info['totalDamageDealt']), inline = True )
        pag.add_field(name = 'Largest Multikill:', value ='{} kills in a row'.format(player_info['largestMultiKill']), inline = True)
        pag.set_image(url = 'http://ddragon.leagueoflegends.com/cdn/img/champion/splash/' + str(player_info['champion']) + '_0.jpg')
        pag.set_footer(text = footer_text)
        
        hist_list.append(pag)

    else:
        pag = discord.Embed(
                title = 'Match {}/10'.format(page_number+1),
                description = str(player_info['gameMode']).capitalize(),
                colour = discord.Color.from_rgb(int(colour1), int(colour2),int(colour3))
            )
        if player_info['win']:
            win = 'Yes 🥳'
        else:
            win = 'No 😓'

        pag.add_field(name = 'Won?', value = win, inline = False)
        pag.add_field(name = 'Champion:', value = '{}'.format(player_info['champion']), inline = True)
        pag.add_field(name = 'Lane:', value = '{}'.format(str(player_info['lane']).capitalize()), inline = True)

        pag.add_field(name = 'Sumonner Spells:', value = '{} and {}'.format(player_info['spell1'],
                                                                            player_info['spell2']), inline = False)

        pag.add_field(name = 'KDA:', value = '{}/{}/{}'.format(player_info['kills'],
                                                               player_info['deaths'],
                                                               player_info['assists']), inline = True)

        pag.add_field(name = 'CS:', value = '{} Minons'.format(player_info['totalMinionsKilled']), inline = True)
        pag.add_field(name = 'Gold earned:', value ='{} Gold'.format(player_info['goldEarned']), inline = True )
        pag.add_field(name = 'Damage dealt:', value ='{} Damage'.format(player_info['totalDamageDealt']), inline = True )
        pag.add_field(name = 'Largest Multikill:', value ='{} kills in a row'.format(player_info['largestMultiKill']), inline = True)
        pag.set_image(url = 'http://ddragon.leagueoflegends.com/cdn/img/champion/splash/' + str(player_info['champion']) + '_0.jpg')
        pag.set_footer(text = footer_text)
        
        hist_list.append(pag)
    
    return hist_list

def sea_onlist(team_list: list, champ: str):
    for ch in team_list:
        if ch == champ:
            return True
    
    return False

def search_embed(jogador: Player, color = '52,152,219'):
    color1, color2, color3 = color.split(',', 2)
    detail = discord.Embed(
        title = 'Profile',
        description = random.choice(emotes),
        colour = discord.Colour.from_rgb(int(color1), int(color2), int(color3))
    )

    detail.set_author(name = jogador.nickname,
                    #   icon_url= ('http://ddragon.leagueoflegends.com/cdn/img/champion/tiles/' + str(jogador.pool[0]) + '_0.jpg'))
                    icon_url= 'https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/profile-icons/' + str(jogador.pIcon) + '.jpg')
    
    detail.add_field(name   = 'Level',
                     value  = '{}'.format(jogador.level),
                     inline = False)
                     
    detail.add_field(name   = 'Solo/Duo',
                     value  = '{} {} ({}/{})'.format(jogador.solo_elo, jogador.solo_tier, jogador.solo_wins, jogador.solo_losses),
                     inline = True)

    detail.add_field(name   = 'Flex',
                     value  = '{} {} ({}/{})'.format(jogador.flex_elo, jogador.flex_tier, jogador.flex_wins, jogador.flex_losses),
                     inline = True)

    detail.add_field(name   = 'Player Pool Ranking:',
                     value  = '🏊',
                     inline = False)

    detail.set_image(url = 'http://ddragon.leagueoflegends.com/cdn/img/champion/splash/' + str(jogador.pool[0]) + '_0.jpg')
    for champion in jogador.pool[:3]:
        detail.add_field(name  = '{} ({})'.format(champion, jogador.champs.loc[champion]['Maestry']),
                        value  = '{} Pts'.format(jogador.champs.loc[champion]['Points']),
                        inline = True)

    detail.set_footer(text = footer_text)

    return detail

#try:
#     response = lol_watcher.summoner.by_name(my_region, 'this_is_probably_not_anyones_summoner_name')
# except ApiError as err:
#     if err.response.status_code == 429:
#         print('We should retry in {} seconds.'.format(err.headers['Retry-After']))
#         print('this retry-after is handled by default by the RiotWatcher library')
#         print('future requests wait until the retry-after time passes')
#     elif err.response.status_code == 404:
#         print('Summoner with that ridiculous name not found.')
#     else:
#         raise



# Code:

@client.remove_command('help')

@client.event
async def on_ready():
    horario     = datetime.datetime.now()
    data, hora  = str(horario).split(' ')
    print('Bot started at:\n{} {}'.format(hora[:8], data))
    print()

@client.command(aliases = ['sea'])
async def search(ctx, *, region_nickname):
    # >sea region nickname
    # Return the Level and top 5 maestry champs from selected player

    print('Starting search')
    region, nickname    = region_nickname.split(' ', 1)
    p_region            = regions_dict[region.lower()]
    
    try:
        print('Getting info')
        info, ranked_info, selected_df = find(nickname, p_region)
        print(str(nickname) + ' has been found.')  

    except:
        print('Player not found')
        await ctx.send('Player not found.')
        return


    jogador     = Player(info, ranked_info, selected_df)

    # Embed formatting:

    print('Creating embed')

    detail      = search_embed(jogador)

    print('Command search finished.')

    await ctx.send(embed = detail)
    
@client.command(aliases = ['hs', 'his', 'hi'], pass_context = True)
async def historic(ctx, *, region_nickname):
    # Returns the last match in historic
    # >hs region nickname
    
    region, nickname    = region_nickname.split(' ', 1)
    p_region            = regions_dict[region.lower()]
    flag                = False

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ["◀️", "▶️", "☑️"]

    try:
        info                = watcher.summoner.by_name(p_region, nickname)
        my_matches          = watcher.match.matchlist_by_account(p_region, info['accountId'])
    
    except:
        print('Player not found')
        await ctx.send('Player not found.')

    last_matches        = []
    player_games        = []
    historic_pages      = []
    
    for i in range(10):
        match = my_matches['matches'][i]
        last_matches.append(match)


    message = await ctx.send('Searching...')
    
    time_remaining = 30
    j = 0

    for i, matches in enumerate(last_matches):

        match_dict = match_analyse(p_region, nickname, matches, i)
        player_games.append(match_dict)
        historic_pages = historic_embed(historic_pages, match_dict, i)
        if(i == 0):
            await message.delete()
            message = await ctx.send(embed = historic_pages[0])
            await message.add_reaction("◀️")
            await message.add_reaction("▶️")
            await message.add_reaction("☑️")

        else:
            try:
                reaction, user = await client.wait_for("reaction_add", timeout = time_remaining, check = check)
                
                if str(reaction.emoji) == "▶️" and j != 9:
                    j += 1
                    await message.edit(embed = historic_pages[j])
                    await message.remove_reaction(reaction, user)
                    
                elif str(reaction.emoji) == "◀️" and j >= 1:
                    j -= 1
                    await message.edit(embed = historic_pages[j])
                    await message.remove_reaction(reaction, user)
                
                elif str(reaction.emoji) == "☑️":
                    await message.remove_reaction(reaction, user)
                    await message.delete()
                    flag = True
                    break
                
                else:
                    await message.remove_reaction(reaction, user)
            
            except asyncio.TimeoutError:
                await message.delete()
                break
    
    time_remaining = 30
    i = j

    while flag == False:
        try:
            reaction, user = await client.wait_for("reaction_add", timeout = time_remaining, check = check)
            if str(reaction.emoji) == "▶️" and i != 9:
                i += 1
                await message.edit(embed = historic_pages[i])
                await message.remove_reaction(reaction, user)

            elif str(reaction.emoji) == "◀️" and i > 1:
                i -= 1
                await message.edit(embed = historic_pages[i])
                await message.remove_reaction(reaction, user)
            
            elif str(reaction.emoji) == "☑️":
                    await message.remove_reaction(reaction, user)
                    await message.delete()
                    flag = False
                    break
                
            else:
                await message.remove_reaction(reaction, user)

        except asyncio.TimeoutError:
            await message.delete()
            flag = True
            break

        except:
            pass
            
@client.command(pass_context = True, aliases = ['rotation', 'rotat'])
async def rot(ctx, *, region):
    p_region            = regions_dict[region.lower()]
    rotation            = watcher.champion.rotations(p_region)
    rotation_list       = []
    rotation_lower_list = []

    for ids in rotation['freeChampionIds']:
        rotation_list.append(champion_dict[str(ids)])
    
    for ids in rotation['freeChampionIdsForNewPlayers']:
        rotation_lower_list.append(champion_dict[str(ids)])

    if 'MonkeyKing' in rotation_list:
        __index = rotation_list.index('MonkeyKing')
        rotation_list[__index]  = 'Wukong'
    
    if 'MonkeyKing' in rotation_lower_list:
        __index = rotation_list.index('MonkeyKing')
        rotation_list[__index]  = 'Wukong'

    detail = discord.Embed(
        title = 'Free Week',
        description = random.choice(emotes),
        colour = discord.Colour.dark_gold()
    )

    detail.set_author(name = ctx.message.author.display_name,
                      icon_url= ctx.message.author.avatar_url)

    # https://getemoji.com

    detail.add_field( name   = 'Champions',
                      value  = '\n'.join(rotation_list),
                      inline = True)
                    
    detail.add_field( name   = 'Champions (for Lv 10 or Above)',
                    value  = '\n'.join(rotation_lower_list),
                    inline = True)

    detail.set_footer(text = footer_text)

    # Debug;
    # print(rotation)
    # print(champion_dict)

    await ctx.send(embed = detail)

@client.command(aliases = ['stt'])
async def status(ctx, *, region):
    p_region            = regions_dict[region.lower()]
    status              = watcher.lol_status.shard_data(p_region)
    server_status = []
    
    for row in status['services']:
        new_row = {}
        new_row['Name']         = row['name']
        new_row['status']       = row['status']
        server_status.append(new_row)

    serverStt = discord.Embed(
        title       = 'Server {}'.format(region.upper()),
        description = 'Status',
        colour      = discord.Colour.orange()
    )
    
    status_dict = { 'online':     '🟢',
                    'maintaince': '🟠',
                    'offline':    '🔴'
    }
    
    # Descrição: 🟢 Online 🔴 Offline 🟠 Maintaince

    for i,row in enumerate(server_status):
        serverStt.add_field(name = server_status[i]['Name'], value   = '{} {}'.format(status_dict[server_status[i]['status']], server_status[i]['status'].capitalize()), inline = False)
    
    serverStt.set_footer(text = footer_text)

    await ctx.send(embed = serverStt)

@client.command( pass_context = True, aliases = ['h', '?', 'Help', 'HELP'])
async def help(ctx):
    # Returns an embed with all commands.
    print('Help has triggered.')
    description = discord.Embed(
        title = 'Help',
        description = 'Hello, {}! 🤩'.format(ctx.message.author.display_name),
        color = discord.Color.purple()    
    )
    
    description.set_author(name = 'League bot',
                           icon_url = 'https://www.nicepng.com/png/full/155-1551184_league-of-legends-icon-png-and-vector-league.png')
    
    description.add_field(name = 'Our Team:', value = """We are a group (2) of students that loves (and hate 🥴) League of Legends.\nWe've made this bot for help people like us that don't have a lot of RAM and need be faster searching for our team mates info and etc.\n✔️\n""", inline = False)
    description.add_field(name = '>search region Nickname', value = 'Show the player resumed profile.\n Also can be called using >𝙨𝙚𝙖', inline = False)
    description.add_field(name = '>rotation region', value = 'Show the free champions rotation.\n Also can be called using >𝙧𝙤𝙩 or >𝗿𝗼𝘁𝗮𝘁', inline = False)
    description.add_field(name = '>historic region Nickname', value = 'Displays the latest player historic.\n Also can be called using >𝗵𝘀', inline = False)
    description.add_field(name = '>status region', value = 'Displays the status of specified region server.\n Also can be called using >𝘀𝘁𝘁', inline = False)
    description.set_footer(text = footer_text)
    description.set_thumbnail(url = 'https://www.nicepng.com/png/full/155-1551184_league-of-legends-icon-png-and-vector-league.png')

    await ctx.send(embed = description)

@client.command( pass_context = True, aliases = ['rand', 'rt'])
async def randomt(ctx):
    team = []
    
    for key in lanes_dict:
        laner = random.choice(lanes_dict[key])

        while sea_onlist(team, laner):
            laner = random.choice(lanes_dict[key])

        team.append(laner)

    rand_team = discord.Embed(
        title = 'Random Team',
        description = random.choice(emotes),
        colour = discord.Colour.purple()
    )

    rand_team.add_field(name = 'Top', value = team[0], inline = False)
    rand_team.add_field(name = 'Jungler', value = team[1], inline = False)
    rand_team.add_field(name = 'Mid', value = team[2], inline = False)
    rand_team.add_field(name = 'ADCarry', value = team[3], inline = False)
    rand_team.add_field(name = 'Support', value = team[4], inline = False)
    rand_team.set_footer(text = footer_text)

    await ctx.send(embed = rand_team)

@client.command( pass_context = True, aliases = ['spec'])
async def spectate(ctx, *, region_nickname):
    
    region, nickname    = region_nickname.split(' ', 1)
    p_region            = regions_dict[region]
    await ctx.channel.purge(limit = 1)
    message = await ctx.send('Searching...')

    try:
        info                = watcher.summoner.by_name(p_region, nickname)
        await message.edit(content = 'Player Found.')
    
    except:
        print('Player not found.')
        await message.edit(content = 'Player not found.')
        return
    
    try:
        cur_game            = watcher.spectator.by_summoner(p_region, info['id'])
        game_mode           = cur_game['gameMode']
        started_at          = cur_game['gameStartTime']
        ban_list            = cur_game['bannedChampions']
        lenght              = cur_game['gameLength']

    
    except:
        print('No match active.')
        await message.edit(content = 'Player are not playing.')
        await message.delete()
        return
    
    await message.delete()

    participants = cur_game['participants']

    match_embed = discord.Embed(title = 'Active Match',
                                description = game_mode.capitalize(),
                                color = discord.Color.from_rgb(153, 51, 255))


    match_embed.add_field(name = 'Team Blue', value = '{} ({})\n{} ({})\n{} ({})\n{} ({})\n{} ({})'.format( participants[0]['summonerName'],
                                                                                                            champion_dict[str(participants[0]['championId'])],
                                                                                                            participants[1]['summonerName'],
                                                                                                            champion_dict[str(participants[1]['championId'])],
                                                                                                            participants[2]['summonerName'],
                                                                                                            champion_dict[str(participants[2]['championId'])],
                                                                                                            participants[3]['summonerName'],
                                                                                                            champion_dict[str(participants[3]['championId'])],
                                                                                                            participants[4]['summonerName'],
                                                                                                            champion_dict[str(participants[4]['championId'])]), inline = True)

    match_embed.add_field(name = 'Blue Team Bans', value = '{}\n{}\n{}\n{}\n{}'.format(champion_dict[str(ban_list[0]['championId'])],
                                                                                       champion_dict[str(ban_list[1]['championId'])],
                                                                                       champion_dict[str(ban_list[2]['championId'])],
                                                                                       champion_dict[str(ban_list[3]['championId'])],
                                                                                       champion_dict[str(ban_list[4]['championId'])]
                                                                                       ), inline = True)

    match_embed.add_field(name = 'Timer', value = '{mins:.0f}:{sec:02d}'.format(mins = (int(lenght)/60), sec = (int(lenght))%60), inline = False)

    match_embed.add_field(name = 'Team Red', value = '{} ({})\n{} ({})\n{} ({})\n{} ({})\n{} ({})'.format( participants[5]['summonerName'],
                                                                                                            champion_dict[str(participants[5]['championId'])],
                                                                                                            participants[6]['summonerName'],
                                                                                                            champion_dict[str(participants[6]['championId'])],
                                                                                                            participants[7]['summonerName'],
                                                                                                            champion_dict[str(participants[7]['championId'])],
                                                                                                            participants[8]['summonerName'],
                                                                                                            champion_dict[str(participants[8]['championId'])],
                                                                                                            participants[9]['summonerName'],
                                                                                                            champion_dict[str(participants[9]['championId'])]), inline = True)


    match_embed.add_field(name = 'Red Team Bans', value = '{}\n{}\n{}\n{}\n{}'.format(champion_dict[str(ban_list[5]['championId'])],
                                                                                      champion_dict[str(ban_list[6]['championId'])],
                                                                                      champion_dict[str(ban_list[7]['championId'])],
                                                                                      champion_dict[str(ban_list[8]['championId'])],
                                                                                      champion_dict[str(ban_list[9]['championId'])]
                                                                                      ), inline = True)


    match_embed.set_footer(text = footer_text)

    match = await ctx.send(embed = match_embed)

    match_profile_list  = []
    time_remaining      = 30
    j                   = 0

    message = await ctx.send('Loading...')
    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ["◀️", "▶️", "☑️", "🟥", "🟦"]

    texto = ''

    for i, row in enumerate(cur_game['participants']):

        texto = texto + '🟩'
        info_player, ranked_info, selected_df = find(row['summonerName'], p_region)
        
        new_player  = Player(info_player, ranked_info, selected_df)
        color       = '0,191,255' if (row['teamId'] == 100) else '255,51,0'
        
        player_embed = search_embed(new_player, color)
        player_embed.set_image(url = 'http://ddragon.leagueoflegends.com/cdn/img/champion/splash/' + str(champion_dict[str(row['championId'])]) + '_0.jpg' )
        match_profile_list.append(player_embed)

        await message.edit(content = 'Loading players\n{} {}0%'.format(texto, i+1))
 
    await message.delete()
    message = await ctx.send(embed = match_profile_list[0])
    await message.add_reaction("◀️")
    await message.add_reaction("▶️")
    await message.add_reaction("🟦")
    await message.add_reaction("🟥")
    await message.add_reaction("☑️")

    while True:
        try:
            reaction, user = await client.wait_for("reaction_add", timeout = time_remaining, check = check)
            if str(reaction.emoji) == "▶️" and j <= 8:
                j += 1
                await message.edit(embed = match_profile_list[j])
                await message.remove_reaction(reaction, user)
                    
            elif str(reaction.emoji) == "◀️" and j >= 1:
                j -= 1
                await message.edit(embed = match_profile_list[j])
                await message.remove_reaction(reaction, user)

            elif str(reaction.emoji) == "🟥":
                j = 5
                await message.edit(embed = match_profile_list[j])
                await message.remove_reaction(reaction, user)
            
            elif str(reaction.emoji) == "🟦":
                j = 0
                await message.edit(embed = match_profile_list[j])
                await message.remove_reaction(reaction, user)
            
            elif str(reaction.emoji) == "☑️":
                await message.remove_reaction(reaction, user)
                await match.delete()
                await message.delete()
                break
                
            else:
                await message.remove_reaction(reaction, user)
            
            
        except asyncio.TimeoutError:
            await match.delete()
            await message.delete()
            break
   
        


client.run(discord_key)
