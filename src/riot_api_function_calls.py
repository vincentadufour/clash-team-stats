import csv
import json
import requests
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("api_key")

# puuid's by player, variable name only first four letters
arch_puuid = "JIkyz_0k_yLCeRtdeX6TVG58zaY3-iMo_ZD8mt33v39pSBKq6utCRZgIASdJY1xaWsoc14hH62v8uQ"
beef_puuid = "XdL7jreLA-rGz1Evy2aleoPaXfYu4ELwaate5BDTbT-XmNRlBBWN-TVL7D7MDZrFoFsgp7m0z2t-Xg"
mike_puuid = "g1Q2YIIXGBesYlHmTAAuLYDqn7ZRrg_UVLF_DURQwN9jDeOaiG-cMlesehqoWGusRCtF1Nh2Ib45FQ"
moon_puuid = "CbgRckJL3hD1JOBSaIgmfPxw2fMdhHmOLk3SeJlTFT5kYodHIi7EXGULgvyBfyOj5pIFzCkvMNkH8Q"
xios_puuid = "CoIyAMP5-u4Qx1yD3IaJ84AUlC0x9ROFplfTSzhV4taoBO_QItb3sPassmE4cVIhL_0nUlNh4MVa1w"
zate_puuid = "3vNsGPDiUfFu1_jVUx0hv7eUNzyWKsCvgrqmmH6CzJZ07Q8P-fQJuD7o7WnyD1J3I811r9pkcRG8Cg"



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


def saveToJson(match_id, file_name="recentlySavedJSON"):
    # saves json data from api call to .json file

    file_name = file_name + ".json"

    with open(file_name, "w") as json_file:
        json.dump(match_id, json_file, indent=4)

    print(f'\nMatch Information successfully saved to "{file_name}".')
    return None


def getAllGames(puuid, api_key=api_key):
    # will need to loop through matchv5 api call to retrieve 0-100, then 101-200, then 201-300, etc
    # will need to have a try: catch to catch when there aren't 100 games left to pull
    # ^ this means the loop needs to have a try: catch as part of the loop since we won't know when we're getting close to the last call
    # we want the json data to be converting to a dataframe instantly after retrieval, to do that, it needs to be normalized as it comes in
    # then we need a better way to store dataframes locally - maybe by saving them as .csv, then we can load from those if we ever need to manually retrieve old data
    # instead of doing it by api calls


    # games data need to be normalized (preferrably immediately)

    # this doesn't work (yet)
    # json_data = json.loads(game)
    # data = pd.json_normalize(json_data, record_path=[
    # ['metadata'],
    # ['info','participants','challenges','missions','perks','styles',],
    # ['info', 'teams', 'bans','objectives','baron','champion','dragon','horde','inhibitor','riftHerald','tower']
    # ])




    return None



########################################## END OF FUNCTIONS ##########################################

# to get last 10 game IDs
last_10_game_IDs = getLastXMatches(mike_puuid, 10)
print(last_10_game_IDs)


# to get specific match details
match = getMatchDetails("NA1_5155731459")


# to save to json with name 'one_of_mikeys_games'
saveToJson(match, "one_of_mikeys_games")
