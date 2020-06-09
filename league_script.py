from riotwatcher import LolWatcher, ApiError
import pandas as pd
import numpy as np

"""
Actualy its a simple python script to check Ranked points and your Top 5 main characters by Maestry.
I wan't to include matchs hist. and live match info, like enemy team ranking, etc.
"""


# Global vars:
api_key     = '' # Your Riot API Key here inside ''
watcher     = LolWatcher(api_key)
my_region   = 'br1'
welcome     = "Nickname:\n"
latest      = watcher.data_dragon.versions_for_region(my_region)['n']['champion']
champ_list  = watcher.data_dragon.champions(latest, False, 'pt_BR')
rotation    = watcher.champion.rotations(my_region)
repeat      = 'yes'

# Code:

def get_info():
    summoner_name   = input(welcome)
    user            = watcher.summoner.by_name(my_region, summoner_name)
    ranked_info     = watcher.league.by_summoner(my_region, user['id'])
    return (summoner_name, user, ranked_info)

def calculate(ranked_info):
    ret_code = 111
    # 111 = common return
    # 101 = No Flex data, media_flex = 0
    # 110 = No Solo/Duo data, media_solo = 0
    # 100 = No ranked data, all media = 0

    try:
        wins_flex   = ranked_info[0]['wins']
        losses_flex = ranked_info[0]['losses']
        media_flex  = wins_flex/(wins_flex + losses_flex)
    except:
        ret_code = 101
        media_flex = 0

    try:
        wins_solo   = ranked_info[1]['wins']
        losses_solo = ranked_info[1]['losses']
        media_solo  = wins_solo/(wins_solo + losses_solo)
    except:
        media_solo = 0

    return(media_flex, media_solo)

def print_maestry(user):
    mains       = watcher.champion_mastery.by_summoner(my_region, user['id'])
    maestry_rank = []
    champ_dictionary = {}

    for row in mains:
        maestry_row = {}
        maestry_row['Champion'] = row['championId']
        maestry_row['Maestry']  = row['championLevel']
        maestry_row['Points']   = row['championPoints']
        maestry_rank.append(maestry_row)

    for key in champ_list['data']:
        row = champ_list['data'][key]
        champ_dictionary[row['key']] = row['id']

    for row in maestry_rank:
        row['championName'] = champ_dictionary[str(row['Champion'])]

    df = pd.DataFrame(maestry_rank)
    df = df.set_index('championName')
    df = df[['Maestry','Points']]

    mains = df.index[:5].tolist()

    print('Your characters ranking:')

    for index, name in enumerate(mains):
        print( '[' + str(index + 1) + ']' + ' ' + str(name))
        print('Points: ' + str(df.loc[name]['Points']))

    return

def print_info(summoner_name, mediaF, mediaS, user, ranked_info):
    print("""
     Hey, {name}!
     Level: {level}""".format(  name    = user['name'],
                                level   = user['summonerLevel']))

    try:
        print(""" Queue: {filaF}
         {elo} {rank}
         Wins {wins} / Losses {losses} ({mediaF:.2f}%)
         """.format(filaF   = 'Flex',
                     elo     = ranked_info[0]['tier'],
                     rank    = ranked_info[0]['rank'],
                     wins    = ranked_info[0]['wins'],
                     losses  = ranked_info[0]['losses'],
                     mediaF  = media_flex * 100))
    except:
        print(""" You didn't played 10 Flex games yet, no Flex data here.""")
    try:
        print(""" Queue: {filaS}
         {elo2} {rank2}
         Wins {wins2} / Losses {losses2} ({mediaS:.2f}%)

        """.format(

                    filaS   = 'Solo/Duo',
                    elo2    = ranked_info[1]['tier'],
                    rank2   = ranked_info[1]['rank'],
                    wins2   = ranked_info[1]['wins'],
                    losses2 = ranked_info[1]['losses'],
                    mediaS  = media_solo * 100))
    except:
        print("""You didn't played 10 Solo/Duo games yet, no Solo/Duo data here.""")

    print_maestry(user)

# DEBUG:

while repeat.lower() == 'yes':
    summoner_name, user, ranked_info = get_info()
    media_flex, media_solo           = calculate(ranked_info)

    print_info(summoner_name, media_flex, media_solo, user, ranked_info)
    repeat = input("""Do you wan't to search for someone else?""")
