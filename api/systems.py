import logging

import config
import requests
from api.libraries import check_response, load_cache_data, save_cache_data

log = logging.getLogger()

def list_systems(limit=10, page=1):
    request_url = f"{config.base_url}/systems"
    payload = {
        "limit": limit,
        "page": page,
    }
    response = requests.get(request_url, headers=config.headers, json=payload)
    return check_response(response)

def get_system(system_symbol):
    cache_filename = (f"_cache/systems_{system_symbol}.json")

    # Use cache data if we have it
    cache_data = load_cache_data(cache_filename)
    if cache_data:
        log.info(f"Using cache data for {system_symbol}")
        return cache_data
    else:
        request_url = f"{config.base_url}/systems/{system_symbol}"
        response = requests.get(request_url, headers=config.headers)
        save_cache_data(response.json(), cache_filename)

    return check_response(response)

def list_waypoints_in_system(system_symbol, limit=10, page=1, traits="", type= ""):
    request_url = f"{config.base_url}/systems/{system_symbol}/waypoints"
    params = {
        "limit": limit,
        "page": page,
        "traits": traits.upper(),
        "type": type.upper(),
    }
    # Delete the "traits" key if its value is an empty string
    if params["traits"] == "":
        del params["traits"]
    # Delete the "type" key if its value is an empty string
    if params["type"] == "":
        del params["type"]

    response = requests.get(request_url, headers=config.headers, params=params)
    return check_response(response)

def get_waypoint(system_symbol, waypoint_symbol):
    request_url = f"{config.base_url}/systems/{system_symbol}/waypoints/{waypoint_symbol}"
    response = requests.get(request_url, headers=config.headers)
    return check_response(response)

def get_market(system_symbol, waypoint_symbol):
    # 2023-11-21 valid waypoint_types are: market, shipyard, jump-gate, construction
    request_url = f"{config.base_url}/systems/{system_symbol}/waypoints/{waypoint_symbol}/market"
    response = requests.get(request_url, headers=config.headers)
    return check_response(response)

def get_shipyard(system_symbol, waypoint_symbol):
    # 2023-11-21 valid waypoint_types are: market, shipyard, jump-gate, construction
    request_url = f"{config.base_url}/systems/{system_symbol}/waypoints/{waypoint_symbol}/shipyard"
    response = requests.get(request_url, headers=config.headers)
    return check_response(response)

def get_jump_gate(system_symbol, waypoint_symbol):
    # 2023-11-21 valid waypoint_types are: market, shipyard, jump-gate, construction
    request_url = f"{config.base_url}/systems/{system_symbol}/waypoints/{waypoint_symbol}/jump-gate"
    response = requests.get(request_url, headers=config.headers)
    return check_response(response)

def get_construction_site(system_symbol, waypoint_symbol):
    # 2023-11-21 valid waypoint_types are: market, shipyard, jump-gate, construction
    request_url = f"{config.base_url}/systems/{system_symbol}/waypoints/{waypoint_symbol}/construction"
    response = requests.get(request_url, headers=config.headers)
    return check_response(response)

def supply_construction_site(system_symbol, waypoint_symbol, ship_symbol, trade_symbol, units):
    request_url = f"{config.base_url}/systems/{system_symbol}/waypoints/{waypoint_symbol}/construction/supply"
    payload = {
        "shipSymbol": ship_symbol,
        "tradeSymbol": trade_symbol,
        "units": units,
    }
    response = requests.post(request_url, headers=config.headers, json=payload)
    return check_response(response)

if __name__ == "__main__":
    print("This file is not meant to be run directly.")
