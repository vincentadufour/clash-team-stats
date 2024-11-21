import requests

api_key = "RGAPI-ffdcafba-fb2c-46fe-9840-92710f9ea538"      # will need to encrypt this later
moon_api_call = "https://na1.api.riotgames.com/fulfillment/v1/summoners/by-puuid/CbgRckJL3hD1JOBSaIgmfPxw2fMdhHmOLk3SeJlTFT5kYodHIi7EXGULgvyBfyOj5pIFzCkvMNkH8Q?api_key=RGAPI-ffdcafba-fb2c-46fe-9840-92710f9ea538"
moon_url = moon_api_call + '?RGAPI-ffdcafba-fb2c-46fe-9840-92710f9ea538' + api_key

resp = requests.get(moon_api_call)
player_info = resp.json()

# requests.get(moon_api_call)

print("Done")

print(player_info)