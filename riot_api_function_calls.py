import csv
import json
import requests
import pandas as pd

# our API key, will need to encrypt this later
api_key = "RGAPI-ffdcafba-fb2c-46fe-9840-92710f9ea538"

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


def getLastXMatches(puuid, x=20, api_key=api_key):
    # function to retrieve last X match ids by puuid defaulted to 20, with api_key with our api key as default value

    # constructing url
    constructed_url = "https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/" + puuid + "/ids?start=0&count=" + str(x) + "&api_key=" + api_key

    # calling api key and storing as json
    match_ids = (requests.get(constructed_url)).json()
    return match_ids


def saveToJson(match_id, file_name="recentlySavedJSON"):
    # saves json data from api call to .json file

    with open(file_name, "w") as json_file:
        json.dump(match_id, json_file, indent=4)

    print(f'Match ID {match_id} successfully saved to "{file_name}"')
    return None

########################################## END OF FUNCTIONS ##########################################



saved = getLastXMatches(zate_puuid, 102)

print(saved)

# game = getMatchDetails("NA1_5079182845")

# saveToJson(game, "nathans_last_game")
