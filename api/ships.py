import requests

import config
from api.libraries import check_response


def list_ships(limit=10, page=1):
    request_url = f"{config.base_url}/my/ships"
    params = {
        "limit": limit,
        "page": page,
    }
    response = requests.get(request_url, headers=config.headers, params=params)
    return check_response(response)

def purchase_ship(shiptype, waypoint):
    # 2023-11-22 valid shiptypes are: SHIP_PROBE, SHIP_MINING_DRONE, SHIP_SIPHON_DRONE, SHIP_INTERCEPTOR, SHIP_LIGHT_HAULER, SHIP_COMMAND_FRIGATE, SHIP_EXPLORER, SHIP_HEAVY_FREIGHTER, SHIP_LIGHT_SHUTTLE, SHIP_ORE_HOUND, SHIP_REFINING_FREIGHTER, SHIP_SURVEYOR
    request_url = f"{config.base_url}/my/ships"
    params = {
        "shipType": shiptype,
        "waypointSymbol": waypoint,
    }
    response = requests.post(request_url, headers=config.headers, json=params)
    return check_response(response)

def get_ship(ship_symbol):
    request_url = f"{config.base_url}/my/ships/{ship_symbol}"
    response = requests.get(request_url, headers=config.headers)
    return check_response(response)

def get_ship_cargo(ship_symbol):
    request_url = f"{config.base_url}/my/ships/{ship_symbol}/cargo"
    response = requests.get(request_url, headers=config.headers)
    return check_response(response)

def orbit(ship_symbol):
    request_url = f"{config.base_url}/my/ships/{ship_symbol}/orbit"
    response = requests.post(request_url, headers=config.headers)
    return check_response(response)

def ship_refine(ship_symbol, produce):
    # 2023-11-23 - Valid produce values: IRON, COPPER, SILVER, GOLD, ALUMINUM, PLATINUM, URANITE, MERITIUM, FUEL
    request_url = f"{config.base_url}/my/ships/{ship_symbol}/refine"
    payload = {
        "produce": produce,
    }
    response = requests.post(request_url, headers=config.headers, json=payload)
    return check_response(response)

# TODO: create_chart

def get_ship_cooldown(ship_symbol):
    request_url = f"{config.base_url}/my/ships/{ship_symbol}/cooldown"
    response = requests.get(request_url, headers=config.headers)
    return check_response(response)

def dock(ship_symbol):
    request_url = f"{config.base_url}/my/ships/{ship_symbol}/dock"
    response = requests.post(request_url, headers=config.headers)
    return check_response(response)

def create_survey(ship_symbol):
    request_url = f"{config.base_url}/my/ships/{ship_symbol}/survey"
    response = requests.post(request_url, headers=config.headers)
    return check_response(response)

def extract_resources(ship_symbol):
    request_url = f"{config.base_url}/my/ships/{ship_symbol}/extract"
    response = requests.post(request_url, headers=config.headers)
    return check_response(response)

# TODO: siphon_resources

def extract_resources_with_survey(ship_symbol, survey):
    request_url = f"{config.base_url}/my/ships/{ship_symbol}/extract/survey"
    payload = {
        "survey": survey,
    }
    response = requests.post(request_url, headers=config.headers, json=payload)
    return check_response(response)

# TODO: jettison_cargo
def jettison_cargo(ship_symbol, cargo, units):
    request_url = f"{config.base_url}/my/ships/{ship_symbol}/jettison"
    payload = {
        "symbol": cargo,
        "units": units,
    }
    response = requests.post(request_url, headers=config.headers, json=payload)
    return check_response(response)

# TODO: jump_ship

def navigate(ship_symbol, waypoint):
    request_url = f"{config.base_url}/my/ships/{ship_symbol}/navigate"
    payload = {
        "waypointSymbol": waypoint,
    }
    response = requests.post(request_url, headers=config.headers, json=payload)
    return check_response(response)

def patch_ship_nav(ship_symbol, flight_mode="CRUISE"):
    # 2023-11-23 Valid flight_mode values: DRIFT, STEALTH, CRUISE, BURN
    request_url = f"{config.base_url}/my/ships/{ship_symbol}/nav"
    payload = {
        "flightMode": flight_mode,
    }
    response = requests.patch(request_url, headers=config.headers, json=payload)
    return check_response(response)

# TODO: get_ship_nav
def get_ship_nav(ship_symbol):
    request_url = f"{config.base_url}/my/ships/{ship_symbol}/nav"
    response = requests.get(request_url, headers=config.headers)
    return check_response(response)

def warp_ship(ship_symbol, waypoint):
    request_url = f"{config.base_url}/my/ships/{ship_symbol}/warp"
    payload = {
        "waypointSymbol": waypoint,
    }
    response = requests.post(request_url, headers=config.headers, json=payload)
    return check_response(response)

def sell_cargo(ship_symbol, goods_symbol, units):
    request_url = f"{config.base_url}/my/ships/{ship_symbol}/sell"
    payload = {
        "symbol": goods_symbol,
        "units": units,
    }
    response = requests.post(request_url, headers=config.headers, json=payload)
    return check_response(response)

def scan_systems(ship_symbol):
    request_url = f"{config.base_url}/my/ships/{ship_symbol}/scan/systems"
    response = requests.post(request_url, headers=config.headers,)
    return check_response(response)

# TODO: scan_waypoints

# TODO: scan_ships

def refuel_ship(ship_symbol, units=None, fromCargo=False):
    request_url = f"{config.base_url}/my/ships/{ship_symbol}/refuel"
    if units is not None and units < 1:
        print(f"Refuel Ship: Units specified and less than 1: {units}")

    payload = {
        "units": units,
        "fromCargo": fromCargo,
    }
    if payload["units"] == "":
        del payload["units"]
    if payload["fromCargo"] == "":
        del payload["fromCargo"]

    response = requests.post(request_url, headers=config.headers, json=payload)
    return check_response(response)

# TODO: purchase_cargo

def transfer_cargo(ship_symbol, destination_ship, trade_symbol, units):
    request_url = f"{config.base_url}/my/ships/{ship_symbol}/transfer"
    payload = {
        "shipSymbol": destination_ship,
        "tradeSymbol": trade_symbol,
        "units": units,
    }
    response = requests.post(request_url, headers=config.headers, json=payload)
    return check_response(response)

def negotiate_contract(ship_symbol):
    request_url = f"{config.base_url}/my/ships/{ship_symbol}/negotiate/contract"
    response = requests.post(request_url, headers=config.headers)
    return check_response(response)

# TODO: get_mounts

# TODO: install_mount

# TODO: remove_mount

if __name__ == "__main__":
    print("This file is not meant to be run directly.")
