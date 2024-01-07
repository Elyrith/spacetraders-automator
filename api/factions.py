import requests
from api.libraries import check_response
import config 

def list_factions(limit=10, page=1):
    request_url = f"{config.base_url}/factions"
    params = {
        "limit": limit,
        "page": page,
    }
    response = requests.get(request_url, headers=config.headers, params=params)
    return check_response(response)

def get_faction(faction_symbol):
    request_url = f"{config.base_url}/agents/{faction_symbol}"
    response = requests.get(request_url, headers=config.headers)
    return check_response(response)

if __name__ == "__main__":
    print("This file is not meant to be run directly.")
