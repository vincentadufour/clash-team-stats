import csv
import json
import requests
import pandas as pd
from dotenv import load_dotenv
import os
import numpy as np

load_dotenv()

api_key = os.getenv("api_key")

# puuid's by player, variable name only first four letters
arch_puuid = "JIkyz_0k_yLCeRtdeX6TVG58zaY3-iMo_ZD8mt33v39pSBKq6utCRZgIASdJY1xaWsoc14hH62v8uQ"
beef_puuid = "XdL7jreLA-rGz1Evy2aleoPaXfYu4ELwaate5BDTbT-XmNRlBBWN-TVL7D7MDZrFoFsgp7m0z2t-Xg"
mike_puuid = "g1Q2YIIXGBesYlHmTAAuLYDqn7ZRrg_UVLF_DURQwN9jDeOaiG-cMlesehqoWGusRCtF1Nh2Ib45FQ"
moon_puuid = "CbgRckJL3hD1JOBSaIgmfPxw2fMdhHmOLk3SeJlTFT5kYodHIi7EXGULgvyBfyOj5pIFzCkvMNkH8Q"
xios_puuid = "CoIyAMP5-u4Qx1yD3IaJ84AUlC0x9ROFplfTSzhV4taoBO_QItb3sPassmE4cVIhL_0nUlNh4MVa1w"
zate_puuid = "3vNsGPDiUfFu1_jVUx0hv7eUNzyWKsCvgrqmmH6CzJZ07Q8P-fQJuD7o7WnyD1J3I811r9pkcRG8Cg"

all_players = [arch_puuid, beef_puuid, mike_puuid, moon_puuid, xios_puuid, zate_puuid]


########################################## START OF FUNCTIONS ##########################################

def getPlayerInfo(puuid, api_key=api_key):
    # function to retrieve player info by puuid, with api_key with our api key as default value

    # constructing url
    constructed_url = "https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/" + puuid + "?api_key=" + api_key

    # calling API key and storing as json
    player_info = (requests.get(constructed_url)).json()
    return player_info


def getLastXMatches(puuid, x=20, api_key=api_key):
    # function to retrieve last X match ids by puuid defaulted to 20, with api_key with our api key as default value

    # constructing url
    constructed_url = "https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/" + puuid + "/ids?start=0&count=" + str(x) + "&api_key=" + api_key

    # calling api key and storing as json
    match_ids = (requests.get(constructed_url)).json()
    return match_ids


def getMatchDetails(match_id, api_key=api_key):
    # function to retrieve match info by match_id, with api_key with our api key as default value

    # constructing url
    constructed_url = "https://americas.api.riotgames.com/lol/match/v5/matches/" + match_id + "?api_key=" + api_key

    # calling api key and storing as json
    match_details = (requests.get(constructed_url)).json()
    return match_details


def getMatchTimelineDetails(match_id, api_key=api_key):
    # function to retrieve match timeline info by match_id, with api_key with our api key as default value

    # constructing url
    constructed_url = "https://americas.api.riotgames.com/lol/match/v5/matches/" + match_id + "/timeline?api_key=" + api_key

    # calling api key and storing as json
    match_timeline_details = (requests.get(constructed_url)).json()
    return match_timeline_details


def saveToJson(match_id, file_name='recentlySavedJSON.json'):
    # saves json data from api call to .json file

    with open(file_name, "w") as json_file:
        json.dump(match_id, json_file, indent=4)

    print(f'\nMatch Information successfully saved to "{file_name}".')
    return None

#TODO
def getAllGames(puuid, start=0, increment=100, file_name='recentlySavedCSV.csv', api_key=api_key):
    # will need to loop through matchv5 api call to retrieve 0-100, then 101-200, then 201-300, etc
    # will need to have a try: catch to catch when there aren't 100 games left to pull
    # ^ this means the loop needs to have a try: catch as part of the loop since we won't know when we're getting close to the last call
    # we want the json data to be converting to a dataframe instantly after retrieval, to do that, it needs to be normalized as it comes in
    # then we need a better way to store dataframes locally - maybe by saving them as .csv, then we can load from those if we ever need to manually retrieve old data
    # instead of doing it by api calls

    first_time = True   # will be turned off after csv creation
    match_count = 0     # counts how many matches are loaded
    while_loop_count = 1
    skipped_matches = 0 # counts how many matches are skipped
   


    while True:
        print(f'\nStart of while loop {while_loop_count}!')

        # constructing url for retrieving 100 games at a time    
        constructed_url = "https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/" + puuid + "/ids?start=" + str(start) + "&count=" + str(increment) + "&api_key=" + api_key

        # calling api key and storing as json
        matches = (requests.get(constructed_url)).json()

        # stops once there are no more matches to retrieve
        if not matches:
            print(f'Process completed. {match_count-skipped_matches} matches loaded, {skipped_matches} matches skipped.')
            break

        # iterate through each 100 match and append into csv
        for match in matches:
            match_count += 1
            print(f'\n{match_count}: Retrieving {match}.')

            # constructing url for getting match data
            match_details = getMatchDetails(match)

            # check if match details exists
            if match_details:
                print(f'Match details retrieved successfully. Converting to DataFrame..')
            elif not match_details or not isinstance(match_details, dict):      # if match data is corrupted, skip match
                print(f'Skipping match {match} due to invalid data.')
                skipped_matches += 1
                continue

            # convert to DataFrame
            match_dataframe = convertToDataframe(match_details)
            print(f'Match DataFrame created successfully. Appending to csv..')

            # create new csv with first submission to keep headers
            if first_time:
                match_dataframe.to_csv(file_name, mode='w', index=False)
                first_time = False
            else:
                match_dataframe.to_csv(file_name, mode='a', header=False, index=False)

            print(f'Appending step done.')

        print(f"\nI'm about to increase the counter by {increment}.")
        
        # gets next 100 games
        start += increment
        while_loop_count += 1

    return None


def convertToDataframe(match):
    # converts match json data to a DataFrame

    print("Began process to convert to DataFrame..")
        
    # flattening metadata to add to each row
    metadata_data = pd.json_normalize(match['metadata'])
    data_version = metadata_data.at[0, 'dataVersion']
    match_id = metadata_data.at[0, 'matchId']

    # flattening general info
    general_info_data = pd.json_normalize(match['info'])
    game_creation = general_info_data.at[0, 'gameCreation']
    game_duration = general_info_data.at[0, 'gameDuration']
    game_end_timestamp = general_info_data.at[0, 'gameEndTimestamp']
    game_id = general_info_data.at[0, 'gameId']
    game_mode = general_info_data.at[0, 'gameMode']
    game_name = general_info_data.at[0, 'gameName']
    game_start_timestamp = general_info_data.at[0, 'gameStartTimestamp']
    game_type = general_info_data.at[0, 'gameType']
    game_version = general_info_data.at[0, 'gameVersion']
    map_id = general_info_data.at[0, 'mapId']

    # list to store rows
    rows = []

    # loop through each participant
    for participant in match['info']['participants']:

        # prepare challenges subtree
        challenges = participant.get("challenges", {})

        # put all participant data in rows
        participant_row = {
            # metadata info ###
            'dataVersion': data_version,
            'matchId': match_id,

            # info ###
            'game_creation': game_creation,
            'game_duration': game_duration,
            'game_end_timestamp': game_end_timestamp,
            'game_id': game_id,
            'game_mode': game_mode,
            'game_name': game_name,
            'game_start_timestamp': game_start_timestamp,
            'game_type': game_type,
            'game_version': game_version,
            'map_id': map_id,

            # info-participant ###
            'allInPings': participant.get("allInPings", np.nan),
            'assistMePings': participant.get("assistMePings", np.nan),
            'assists': participant.get("assists", np.nan),
            'baronKills': participant.get("baronKills", np.nan),
            'basicPings': participant.get("basicPings", np.nan),
            'bountyLevel': participant.get("bountyLevel", np.nan),
            'champExperience': participant.get("champExperience", np.nan),
            'champLevel': participant.get("champLevel", np.nan),
            # skipped champID
            'championName': participant.get("championName", None),
            # skipped championTransform
            'commandPings': participant.get("commandPings", np.nan),
            'consumablesPurchased': participant.get("consumablesPurchased", np.nan),
            'damageDealtToBuildings': participant.get("damageDealtToBuildings", np.nan),
            'damageDealtToBuildings': participant.get("damageDealtToBuildings", np.nan),
            'damageDealtToTurrets': participant.get("damageDealtToTurrets", np.nan),
            'damageSelfMitigated': participant.get("damageSelfMitigated", np.nan),
            'dangerPings': participant.get("dangerPings", np.nan),
            'deaths': participant.get("deaths", np.nan),
            'detectorWardsPlaced': participant.get("detectorWardsPlaced", np.nan),
            'doubleKills': participant.get("doubleKills", np.nan),
            'dragonKills': participant.get("dragonKills", np.nan),
            # skipped eligibleForProgression
            'enemyMissingPings': participant.get("enemyMissingPings", np.nan),
            'enemyVisionPings': participant.get("enemyVisionPings", np.nan),
            'firstBloodAssist': participant.get("firstBloodAssist", None),
            'firstBloodKill': participant.get("firstBloodKill", None),
            'firstTowerAssist': participant.get("firstTowerAssist", None),
            'firstTowerKill': participant.get("firstTowerKill", None),
            'gameEndedInEarlySurrender': participant.get("gameEndedInEarlySurrender", None),
            'gameEndedInSurrender': participant.get("gameEndedInSurrender", None),
            'getBackPings': participant.get("getBackPings", np.nan),
            'goldEarned': participant.get("goldEarned", np.nan),
            'goldSpent': participant.get("goldSpent", np.nan),
            'holdPings': participant.get("holdPings", np.nan),
            'individualPosition': participant.get("individualPosition", None),
            'inhibitorKills': participant.get("inhibitorKills", np.nan),
            'inhibitorTakedowns': participant.get("inhibitorTakedowns", np.nan),
            'inhibitorsLost': participant.get("inhibitorsLost", np.nan),
            'item0': participant.get("item0", np.nan),
            'item1': participant.get("item1", np.nan),
            'item2': participant.get("item2", np.nan),
            'item3': participant.get("item3", np.nan),
            'item4': participant.get("item4", np.nan),
            'item5': participant.get("item5", np.nan),
            'item6': participant.get("item6", np.nan),
            'itemsPurchased': participant.get("itemsPurchased", np.nan),
            'killingSprees': participant.get("killingSprees", np.nan),
            'kills': participant.get("kills", np.nan),
            'lane': participant.get("lane", None),
            'largestCriticalStrike': participant.get("largestCriticalStrike", np.nan),
            'largestKillingSpree': participant.get("largestKillingSpree", np.nan),
            'largestMultiKill': participant.get("largestMultiKill", np.nan),
            'longestTimeSpentLiving': participant.get("longestTimeSpentLiving", np.nan),
            'magicDamageDealt': participant.get("magicDamageDealt", np.nan),
            'magicDamageDealtToChampions': participant.get("magicDamageDealtToChampions", np.nan),
            'magicDamageTaken': participant.get("magicDamageTaken", np.nan),
            'needVisionPings': participant.get("needVisionPings", np.nan),
            'neutralMinionsKilled': participant.get("neutralMinionsKilled", np.nan),
            'nexusKills': participant.get("nexusKills", np.nan),
            'nexusLost': participant.get("nexusLost", np.nan),
            'nexusTakedowns': participant.get("nexusTakedowns", np.nan),
            'objectivesStolen': participant.get("objectivesStolen", np.nan),
            'objectivesStolenAssists': participant.get("objectivesStolenAssists", np.nan),
            'onMyWayPings': participant.get("onMyWayPings", np.nan),
            # skipped participant id, can already use summoner name as unique id
            'pentakills': participant.get("pentakills", np.nan),
            'physicalDamageDealt': participant.get("physicalDamageDealt", np.nan),
            'physicalDamageDealtToChampions': participant.get("physicalDamageDealtToChampions", np.nan),
            'physicalDamageTaken': participant.get("physicalDamageTaken", np.nan),
            # skipped placement
            # skipped all playerAugments (6)
            # skipped playerSubteamId
            # skipped profileIcon
            'pushPings': participant.get("pushPings", np.nan),
            'puuid': participant.get("puuid", None),
            'quadraKills': participant.get("quadraKills", np.nan),
            'retreatPings': participant.get("retreatPings", np.nan),
            'riotIdGameName': participant.get("riotIdGameName", None), # may be redundant, but keeping because not available in old games
            'riotIdTagline': participant.get("riotIdTagline", None),  # this is why we're keeping the above
            'role': participant.get("role", None),
            'sightWardsBoughtInGame': participant.get("sightWardsBoughtInGame", np.nan),
            'spell1Casts': participant.get("spell1Casts", np.nan),
            'spell2Casts': participant.get("spell2Casts", np.nan),
            'spell3Casts': participant.get("spell3Casts", np.nan),
            'spell4Casts': participant.get("spell4Casts", np.nan),
            # skipped subteamPlacement
            'summoner1Casts': participant.get("summoner1Casts", np.nan),
            'summoner1Id': participant.get("summoner1Id", np.nan),
            'summoner2Casts': participant.get("summoner2Casts", np.nan),
            'summoner2Id': participant.get("summoner2Id", np.nan),
            'summonerId': participant.get("summonerId", np.nan),
            'summonerLevel': participant.get("summonerLevel", np.nan),
            'summonerName': participant.get("summonerName", None), # keeping because this will be the only way to quickly identify summoners in old games
            'teamEarlySurrendered': participant.get("teamEarlySurrendered", None),
            'teamId': participant.get("teamId", np.nan), # 100 for first team, 200 for second team
            'teamPosition': participant.get("teamPosition", None),
            'timeCCingOthers': participant.get("timeCCingOthers", np.nan),
            'timePlayed': participant.get("timePlayed", np.nan), # might be a way to find RQers
            'totalAllyJungleMinionsKilled': participant.get("totalAllyJungleMinionsKilled", np.nan),
            'totalDamageDealt': participant.get("totalDamageDealt", np.nan),
            'totalDamageDealtToChampions': participant.get("totalDamageDealtToChampions", np.nan),
            'totalDamageShieldedOnTeammates': participant.get("totalDamageShieldedOnTeammates", np.nan),
            'totalDamageTaken': participant.get("totalDamageTaken", np.nan),
            'totalEnemyJungleMinionsKilled': participant.get("totalEnemyJungleMinionsKilled", np.nan),
            'totalHeal': participant.get("totalHeal", np.nan),
            'totalHealsOnTeammates': participant.get("totalHealsOnTeammates", np.nan),
            'totalMinionsKilled': participant.get("totalMinionsKilled", np.nan),
            'totalTimeCCDealt': participant.get("totalTimeCCDealt", np.nan),
            'totalTimeSpentDead': participant.get("totalTimeSpentDead", np.nan),
            'totalUnitsHealed': participant.get("totalUnitsHealed", np.nan),
            'tripleKills': participant.get("tripleKills", np.nan),
            'trueDamageDealt': participant.get("trueDamageDealt", np.nan),
            'trueDamageDealtToChampions': participant.get("trueDamageDealtToChampions", np.nan),
            'trueDamageTaken': participant.get("trueDamageTaken", np.nan),
            'turretKills': participant.get("turretKills", np.nan),
            'turretTakedowns': participant.get("turretTakedowns", np.nan),
            'turretsLost': participant.get("turretsLost", np.nan),
            'unrealKills': participant.get("unrealKills", np.nan), # what is this??
            'visionClearedPings': participant.get("visionClearedPings", np.nan),
            'visionScore': participant.get("visionScore", np.nan),
            'visionWardsBoughtInGame': participant.get("visionWardsBoughtInGame", np.nan),
            'wardsKilled': participant.get("wardsKilled", np.nan),
            'wardsPlaced': participant.get("wardsPlaced", np.nan),
            'win': participant.get("win", None),

            # info-participant-challenges ###
            'challenges.12AssistStreakCount': challenges.get("12AssistStreakCount", np.nan),
            'challenges.HealFromMapSources': challenges.get("HealFromMapSources", np.nan),
            'challenges.InfernalScalePickup': challenges.get("InfernalScalePickup", np.nan),
            # skipped all the SWARM challenges (10)
            'challenges.abilityUses': challenges.get("abilityUses", np.nan),
            'challenges.acesBefore15Minutes': challenges.get("acesBefore15Minutes", np.nan),
            'challenges.alliedJungleMonsterKills': challenges.get("alliedJungleMonsterKills", np.nan),
            'challenges.baronBuffGoldAdvantageOverThreshold': challenges.get("baronBuffGoldAdvantageOverThreshold", np.nan),
            'challenges.baronTakedowns': challenges.get("baronTakedowns", np.nan),
            'challenges.blastConeOppositeOpponentCount': challenges.get("blastConeOppositeOpponentCount", np.nan),
            'challenges.bountyGold': challenges.get("bountyGold", np.nan),
            'challenges.buffsStolen': challenges.get("buffsStolen", np.nan),
            'challenges.completeSupportQuestInTime': challenges.get("completeSupportQuestInTime", np.nan),
            'challenges.controlWardTimeCoverageInRiverOrEnemyHalf': challenges.get("controlWardTimeCoverageInRiverOrEnemyHalf", np.nan),
            'challenges.controlWardsPlaced': challenges.get("controlWardsPlaced", np.nan),
            'challenges.damagePerMinute': challenges.get("damagePerMinute", np.nan),
            'challenges.damageTakenOnTeamPercentage': challenges.get("damageTakenOnTeamPercentage", np.nan),
            'challenges.dancedWithRiftHerald': challenges.get("dancedWithRiftHerald", np.nan),
            'challenges.deathsByEnemyChamps': challenges.get("deathsByEnemyChamps", np.nan),
            'challenges.dodgeSkillShotsSmallWindow': challenges.get("dodgeSkillShotsSmallWindow", np.nan),
            'challenges.doubleAces': challenges.get("doubleAces", np.nan),
            'challenges.dragonTakedowns': challenges.get("dragonTakedowns", np.nan),
            'challenges.earliestBaron': challenges.get("earliestBaron", np.nan),
            'challenges.earliestDragonTakedown': challenges.get("earliestDragonTakedown", np.nan),
            'challenges.earlyLaningPhaseGoldExpAdvantage': challenges.get("earlyLaningPhaseGoldExpAdvantage", np.nan),
            'challenges.effectiveHealAndShielding': challenges.get("effectiveHealAndShielding", np.nan),
            'challenges.elderDragonKillsWithOpposingSoul': challenges.get("elderDragonKillsWithOpposingSoul", np.nan),
            'challenges.elderDragonMultikills': challenges.get("elderDragonMultikills", np.nan),
            'challenges.enemyChampionImmobilizations': challenges.get("enemyChampionImmobilizations", np.nan),
            'challenges.enemyJungleMonsterKills': challenges.get("enemyJungleMonsterKills", np.nan),
            'challenges.epicMonsterKillsNearEnemyJungler': challenges.get("epicMonsterKillsNearEnemyJungler", np.nan),
            'challenges.epicMonsterKillsWithin30SecondsOfSpawn': challenges.get("epicMonsterKillsWithin30SecondsOfSpawn", np.nan),
            'challenges.epicMonsterSteals': challenges.get("epicMonsterSteals", np.nan),
            'challenges.epicMonsterStolenWithoutSmite': challenges.get("epicMonsterStolenWithoutSmite", np.nan),
            'challenges.firstTurretKilled': challenges.get("firstTurretKilled", np.nan),
            'challenges.fistBumpParticipation': challenges.get("fistBumpParticipation", np.nan),
            'challenges.flawlessAces': challenges.get("flawlessAces", np.nan),
            'challenges.fullTeamTakedown': challenges.get("fullTeamTakedown", np.nan),
            'challenges.gameLength': challenges.get("gameLength", np.nan),
            'challenges.getTakedownsInAllLanesEarlyJungleAsLaner': challenges.get("getTakedownsInAllLanesEarlyJungleAsLaner", np.nan),
            'challenges.goldPerMinute': challenges.get("goldPerMinute", np.nan),
            'challenges.hadOpenNexus': challenges.get("hadOpenNexus", np.nan),
            'challenges.highestChampionDamage': challenges.get("highestChampionDamage", np.nan),
            'challenges.immobilizeAndKillWithAlly': challenges.get("immobilizeAndKillWithAlly", np.nan),
            'challenges.initialBuffCount': challenges.get("initialBuffCount", np.nan),
            'challenges.initialCrabCount': challenges.get("initialCrabCount", np.nan),
            'challenges.jungleCsBefore10Minutes': challenges.get("jungleCsBefore10Minutes", np.nan),
            'challenges.junglerTakedownsNearDamagedEpicMonster': challenges.get("junglerTakedownsNearDamagedEpicMonster", np.nan),
            'challenges.kTurretsDestroyedBeforePlatesFall': challenges.get("kTurretsDestroyedBeforePlatesFall", np.nan),
            'challenges.kda': challenges.get("kda", np.nan),
            'challenges.killAfterHiddenWithAlly': challenges.get("killAfterHiddenWithAlly", np.nan),
            'challenges.killParticipation': challenges.get("killParticipation", np.nan),
            'challenges.killedChampTookFullTeamDamageSurvived': challenges.get("killedChampTookFullTeamDamageSurvived", np.nan),
            'challenges.killingSprees': challenges.get("killingSprees", np.nan),
            'challenges.killsNearEnemyTurret': challenges.get("killsNearEnemyTurret", np.nan),
            'challenges.killsOnOtherLanesEarlyJungleAsLaner': challenges.get("killsOnOtherLanesEarlyJungleAsLaner", np.nan),
            'challenges.killsOnRecentlyHealedByAramPack': challenges.get("killsOnRecentlyHealedByAramPack", np.nan),
            'challenges.killsUnderOwnTurret': challenges.get("killsUnderOwnTurret", np.nan),
            'challenges.killsWithHelpFromEpicMonster': challenges.get("killsWithHelpFromEpicMonster", np.nan),
            'challenges.knockEnemyIntoTeamAndKill': challenges.get("knockEnemyIntoTeamAndKill", np.nan),
            'challenges.landSkillShotsEarlyGame': challenges.get("landSkillShotsEarlyGame", np.nan),
            'challenges.laneMinionsFirst10Minutes': challenges.get("laneMinionsFirst10Minutes", np.nan),
            'challenges.laningPhaseGoldExpAdvantage': challenges.get("laningPhaseGoldExpAdvantage", np.nan),
            'challenges.legendaryCount': challenges.get("legendaryCount", np.nan),
            'challenges.legendaryItemUsed': challenges.get("legendaryItemUsed", None),
            'challenges.lostAnInhibitor': challenges.get("lostAnInhibitor", np.nan),
            'challenges.maxCsAdvantageOnLaneOpponent': challenges.get("maxCsAdvantageOnLaneOpponent", np.nan),
            'challenges.maxKillDeficit': challenges.get("maxKillDeficit", np.nan),
            'challenges.maxLevelLeadLaneOpponent': challenges.get("maxLevelLeadLaneOpponent", np.nan),
            'challenges.mejaisFullStackInTime': challenges.get("mejaisFullStackInTime", np.nan),
            'challenges.moreEnemyJungleThanOpponent': challenges.get("moreEnemyJungleThanOpponent", np.nan),
            'challenges.multiKillOneSpell': challenges.get("multiKillOneSpell", np.nan),
            'challenges.multiTurretRiftHeraldCount': challenges.get("multiTurretRiftHeraldCount", np.nan),
            'challenges.multikills': challenges.get("multikills", np.nan),
            'challenges.multikillsAfterAggressiveFlash': challenges.get("multikillsAfterAggressiveFlash", np.nan),
            'challenges.outerTurretExecutesBefore10Minutes': challenges.get("outerTurretExecutesBefore10Minutes", np.nan),
            'challenges.outnumberedKills': challenges.get("outnumberedKills", np.nan),
            'challenges.outnumberedNexusKill': challenges.get("outnumberedNexusKill", np.nan),
            'challenges.perfectDragonSoulsTaken': challenges.get("perfectDragonSoulsTaken", np.nan),
            'challenges.perfectGame': challenges.get("perfectGame", np.nan),
            'challenges.pickKillWithAlly': challenges.get("pickKillWithAlly", np.nan),
            'challenges.playedChampSelectPosition': challenges.get("playedChampSelectPosition", np.nan),
            'challenges.poroExplosions': challenges.get("poroExplosions", np.nan),
            'challenges.quickCleanse': challenges.get("quickCleanse", np.nan),
            'challenges.quickFirstTurret': challenges.get("quickFirstTurret", np.nan),
            'challenges.quickSoloKills': challenges.get("quickSoloKills", np.nan),
            'challenges.riftHeraldTakedowns': challenges.get("riftHeraldTakedowns", np.nan),
            'challenges.saveAllyFromDeath': challenges.get("saveAllyFromDeath", np.nan),
            'challenges.scuttleCrabKills': challenges.get("scuttleCrabKills", np.nan),
            'challenges.shortestTimeToAceFromFirstTakedown': challenges.get("shortestTimeToAceFromFirstTakedown", np.nan),
            'challenges.skillshotsDodged': challenges.get("skillshotsDodged", np.nan),
            'challenges.skillshotsHit': challenges.get("skillshotsHit", np.nan),
            'challenges.snowballsHit': challenges.get("snowballsHit", np.nan),
            'challenges.soloBaronKills': challenges.get("soloBaronKills", np.nan),
            'challenges.soloKills': challenges.get("soloKills", np.nan),
            'challenges.soloTurretsLategame': challenges.get("soloTurretsLategame", np.nan),
            'challenges.stealthWardsPlaced': challenges.get("stealthWardsPlaced", np.nan),
            'challenges.survivedSingleDigitHpCount': challenges.get("survivedSingleDigitHpCount", np.nan),
            'challenges.survivedThreeImmobilizesInFight': challenges.get("survivedThreeImmobilizesInFight", np.nan),
            'challenges.takedownOnFirstTurret': challenges.get("takedownOnFirstTurret", np.nan),
            'challenges.takedowns': challenges.get("takedowns", np.nan),
            'challenges.takedownsAfterGainingLevelAdvantage': challenges.get("takedownsAfterGainingLevelAdvantage", np.nan),
            'challenges.takedownsBeforeJungleMinionSpawn': challenges.get("takedownsBeforeJungleMinionSpawn", np.nan),
            'challenges.takedownsFirstXMinutes': challenges.get("takedownsFirstXMinutes", np.nan),
            'challenges.takedownsInAlcove': challenges.get("takedownsInAlcove", np.nan),
            'challenges.takedownsInEnemyFountain': challenges.get("takedownsInEnemyFountain", np.nan),
            'challenges.teamBaronKills': challenges.get("teamBaronKills", np.nan),
            'challenges.teamDamagePercentage': challenges.get("teamDamagePercentage", np.nan),
            'challenges.teamElderDragonKills': challenges.get("teamElderDragonKills", np.nan),
            'challenges.teamRiftHeraldKills': challenges.get("teamRiftHeraldKills", np.nan),
            'challenges.tookLargeDamageSurvived': challenges.get("tookLargeDamageSurvived", np.nan),
            'challenges.turretPlatesTaken': challenges.get("turretPlatesTaken", np.nan),
            'challenges.turretTakedowns': challenges.get("turretTakedowns", np.nan),
            'challenges.turretsTakenWithRiftHerald': challenges.get("turretsTakenWithRiftHerald", np.nan),
            'challenges.twentyMinionsIn3SecondsCount': challenges.get("twentyMinionsIn3SecondsCount", np.nan),
            'challenges.twoWardsOneSweeperCount': challenges.get("twoWardsOneSweeperCount", np.nan),
            'challenges.unseenRecalls': challenges.get("unseenRecalls", np.nan),
            'challenges.visionScoreAdvantageLaneOpponent': challenges.get("visionScoreAdvantageLaneOpponent", np.nan),
            'challenges.visionScorePerMinute': challenges.get("visionScorePerMinute", np.nan),
            'challenges.voidMonsterKill': challenges.get("voidMonsterKill", np.nan),
            'challenges.wardTakedowns': challenges.get("wardTakedowns", np.nan),
            'challenges.wardTakedownsBefore20M': challenges.get("wardTakedownsBefore20M", np.nan),
            'challenges.wardsGuarded': challenges.get("wardsGuarded", np.nan),
            'challenges.junglerKillsEarlyJungle': challenges.get("junglerKillsEarlyJungle", np.nan),
            'challenges.killsOnLanersEarlyJungleAsJungler': challenges.get("killsOnLanersEarlyJungleAsJungler", np.nan),
            'challenges.highestCrowdControlScore': challenges.get("highestCrowdControlScore", np.nan),
            'challenges.highestWardKills': challenges.get("highestWardKills", np.nan),
            'challenges.firstTurretKilledTime': challenges.get("firstTurretKilledTime", np.nan),


        }
        rows.append(participant_row)

    # create DataFrame from rows
    data = pd.DataFrame(rows)

    return data



########################################## END OF FUNCTIONS ##########################################
# these are commented out to then uncomment to test functions


# # to get last 10 game IDs
# last_10_game_IDs = getLastXMatches(mike_puuid, 10)
# print(last_10_game_IDs)

# # to get specific match details
# match = getMatchDetails("NA1_5155731459")

# # to save to json with name 'one_of_mikeys_games'
# saveToJson(match, "one_of_mikeys_games")

# # turn match json data into dataframe
# game_data = convertToDataframe(match)

# # print(game_data.head(10))

# # Save to CSV or inspect the result
# game_data.to_csv('certain_match.csv')

getAllGames(zate_puuid, 0, 50, 'zatevon_all_games.csv')
