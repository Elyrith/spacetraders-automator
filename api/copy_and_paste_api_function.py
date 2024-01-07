import requests
from api.libraries import check_response
import config

def copy_and_paste_me(limit=10, page=1):
    request_url = f"{config.base_url}/agents"
    params = { # params for response.get
        "limit": limit,
        "page": page,
    }
    response = requests.get(request_url, headers=config.headers, params=params)

    payload = { # payload for response.post
        "limit": limit,
        "page": page,
    }
    if payload["page"] is None:
        del payload["page"]
    
    response = requests.post(request_url, headers=config.headers, json=payload)

    return check_response(response)

if __name__ == "__main__":
    print("This file is not meant to be run directly.")
