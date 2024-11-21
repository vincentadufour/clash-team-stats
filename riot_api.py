import csv
import json
import requests
import pandas as pd

api_key = "RGAPI-ffdcafba-fb2c-46fe-9840-92710f9ea538"

moon_presence_puuid = "CbgRckJL3hD1JOBSaIgmfPxw2fMdhHmOLk3SeJlTFT5kYodHIi7EXGULgvyBfyOj5pIFzCkvMNkH8Q"

# constructed using process defined in Obsidian
moon_url = "https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/CbgRckJL3hD1JOBSaIgmfPxw2fMdhHmOLk3SeJlTFT5kYodHIi7EXGULgvyBfyOj5pIFzCkvMNkH8Q?api_key=RGAPI-ffdcafba-fb2c-46fe-9840-92710f9ea538"

match_id = "NA1_5156735298"
match_details_url = "https://americas.api.riotgames.com/lol/match/v5/matches/" + match_id + "?api_key=" + api_key


# simplified call for Moon player info
moon_info = (requests.get(moon_url)).json()

print("Done")

print(moon_info)

moon_matches = "https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/CbgRckJL3hD1JOBSaIgmfPxw2fMdhHmOLk3SeJlTFT5kYodHIi7EXGULgvyBfyOj5pIFzCkvMNkH8Q/ids?start=0&count=20&api_key=RGAPI-ffdcafba-fb2c-46fe-9840-92710f9ea538"

match_ids = (requests.get(moon_matches)).json()

print(match_ids)


match_details = (requests.get(match_details_url).json())

# Save match_details to a JSON file
with open("match_details.json", "w") as json_file:
    json.dump(match_details, json_file, indent=4)  # indent=4 for pretty formatting

print("Match details saved to match_details.json")

