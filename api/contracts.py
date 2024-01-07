import requests
from api.libraries import check_response
import config

def list_contracts(limit=10, page=1):
    request_url = f"{config.base_url}/my/contracts"
    params = {
        "limit": limit,
        "page": page,
    }
    response = requests.get(request_url, headers=config.headers, params=params)
    return check_response(response)

def get_contract(contract_id):
    request_url = f"{config.base_url}/my/contracts/{contract_id}"
    response = requests.get(request_url, headers=config.headers)
    return check_response(response)

def accept_contract(contract_id):
    request_url = f"{config.base_url}/my/contracts/{contract_id}/accept"
    response = requests.post(request_url, headers=config.headers)
    return check_response(response)

def deliver_cargo_to_contract(contract_id, shipSymbol, tradeSymbol, units):
    request_url = f"{config.base_url}/my/contracts/{contract_id}/deliver"
    payload = {
        "shipSymbol": shipSymbol,
        "tradeSymbol": tradeSymbol,
        "units": units,
    }
    response = requests.post(request_url, headers=config.headers, json=payload)
    return check_response(response)

def fulfill_contract(contract_id):
    request_url = f"{config.base_url}/my/contracts/{contract_id}/fulfill"
    response = requests.post(request_url, headers=config.headers)
    return check_response(response)

if __name__ == "__main__":
    print("This file is not meant to be run directly.")
