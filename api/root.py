import requests
from api.libraries import check_response
import config 

def get_status():
    request_url = config.base_url
    response = requests.get(request_url, headers=config.headers)
    return check_response(response)

def register_new_agent(symbol, email, faction="COSMIC"):
    request_url = f"{config.base_url}/register"
    payload = {
        "faction": faction,
        "symbol": symbol,
        "email": email,
    }
    response = requests.post(request_url, json=payload)
    return check_response(response)

if __name__ == "__main__":
    print("This file is not meant to be run directly.")
