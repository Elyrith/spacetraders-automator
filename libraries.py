import datetime
import json
import time

import api.contracts as contracts
import api.ships as ships
import api.systems as systems


def calculate_time(departureTime, arrivalTime):
    departureTime = datetime.datetime.strptime(departureTime, "%Y-%m-%dT%H:%M:%S.%fZ")
    arrivalTime = datetime.datetime.strptime(arrivalTime, "%Y-%m-%dT%H:%M:%S.%fZ")

    # Calculate the difference in seconds
    return (arrivalTime - departureTime).total_seconds()


def dock_and_refuel(ship):
    print("Docking and refueling.")
    dock = ships.dock(ship['symbol'])
    if 'error' not in dock: # We check because if there was an error (we were flying or something) then we don't want to continue.
        if dock['data']['nav']['status'] == "DOCKED":
            print("Docked!")
            refuel = ships.refuel_ship(ship['symbol'])
            if 'error' in refuel:
                print(refuel['error']['message'])
            else:
                if refuel['data']['fuel']['current'] == refuel['data']['fuel']['capacity']:
                    print(f"Fuel at full! Cost was: {refuel['data']['transaction']['totalPrice']}")


def travel_to_waypoint(ship, waypoint):
    # We're going to get the ship to it's destination, even if it's already going somewhere else first.

    # Get the most up-to-date data about the ship
    ship = ships.get_ship(ship['symbol'])['data']

    # Do nothing if the ship is already at the desired waypoint.
    if ship['nav']['waypointSymbol'] == waypoint and ship['nav']['status'] != 'IN_TRANSIT':
        print(f"Attempted to have {ship['symbol']} travel to {waypoint}, but it was already there.")
        return True

    # If the ship is already traveling somewhere...
    if ship['nav']['status'] == "IN_TRANSIT":

        # Find out how long much longer before it gets to it's current destination.
        navigate = ships.navigate(ship['symbol'], waypoint)['error']['data']
        seconds_to_arrival = navigate['secondsToArrival']
        print("The ship is already traveling...")

        # Is the ship already going to the desired waypoint?
        if navigate['destinationSymbol'] == waypoint:
            # It's already going where we want, so we can return True now that we've already waited out the travel time.
            print(f"The good news is: it's already traveling to our destination. It will take {seconds_to_arrival} seconds. Waiting...")
            time.sleep(seconds_to_arrival)
            return True
        else:
            # It's not going where we want, so we need to dock, refuel, travel again, then wait again.
            print(f"The bad news is: it's traveling to {navigate['destinationSymbol']} rather than {waypoint}. It will take {seconds_to_arrival}. Waiting before initiating our travel request...")
            time.sleep(seconds_to_arrival)

            print(f"Wait time is over. The ship should have arrived by now. Proceeding with refuel and next travel to {waypoint}.")

    # First, lets find out if the current location sells fuel. (Do we care? So far everywhere sells fuel for cheap.)
#    fuel_for_sale = False
#    last_dash_index = waypoint.rfind("-") # Find the last dash in the string so we can get the system name.
#    system_waypoint = waypoint[:last_dash_index]
#    market_info = systems.get_market(system_waypoint, waypoint)
#    print(json.dumps(market_info, indent=2))
#    for exchanges in market_info['data']['exchange']:
#        if exchanges['symbol'] == "FUEL":
#            fuel_for_sale = True
#            break
#    if fuel_for_sale: # Fuel up if it's available.
    dock_and_refuel(ship)

    # Go to orbit, just in case we're docked.
    ships.orbit(ship['symbol'])

    # We are now ready to travel.

    ship = ships.get_ship(ship['symbol'])['data']
    # Initiate travel to the desired waypoint now.
    navigate = ships.navigate(ship['symbol'], waypoint)

    # Check how long it's going to take, and wait that long.
#    print(json.dumps(navigate, indent=2))
#    print(json.dumps(navigate, indent=2))
    if "error" not in navigate:
        time_difference = calculate_time(navigate['data']['nav']['route']['departureTime'], navigate['data']['nav']['route']['arrival'])
    else:
        if navigate['error']['code'] == 4203:
            print(navigate['error']['message'])
            return False
        else:
            time_difference = calculate_time(navigate['error']['data']['departureTime'], navigate['error']['data']['arrival'])
    print(f"{ship['symbol']} is now traveling to {waypoint}. It's going to take {time_difference} seconds. Waiting...")
    # Technically, we should run a check every so often (or just at the end) to see if it's done and only return True when it's done.
    time.sleep(time_difference)
    print(f"{ship['symbol']} is now orbiting {waypoint}.")
    return True


def get_list_of_active_contracts():
    # Get all contracts/missions we have
    contract_list = contracts.list_contracts()['data']

    # Get the current datetime
    current_datetime = datetime.datetime.utcnow()

    # Remove all fulfilled and expired contracts
    current_datetime = datetime.datetime.utcnow()
    current_contracts = [
        contract for contract in contract_list
        if contract.get('accepted') is True
        and contract.get('fulfilled') is False
        and datetime.fromisoformat(contract.get('expiration').replace('Z', '+00:00')) > current_datetime
    ]
    return current_contracts


def get_list_of_mission_items(ship):
    # Get all contracts/missions we have
    contract_list = get_list_of_active_contracts()

    # Check if we have any items for a contract
    mission_items = {}
    for inventory in ship['cargo']['inventory']: # Loop through our inventory
        for contract in contract_list: # Loop through all our contracts
            if contract['type'] == "PROCUREMENT": # Only proceed for PROCUREMENT contracts
                for contract_item in contract['terms']['deliver']: # Loop through all items in the contract
                    if inventory['symbol'] == contract_item['tradeSymbol']:
                        mission_items[inventory['symbol']] = inventory['units']
    print(f"{ship['symbol']} has {len(mission_items)} mission items:")
    for item in mission_items:
        print(f"\t{item}")
    return mission_items


def get_list_of_non_mission_items(ship):
    # Get all contracts/missions we have
    contract_list = get_list_of_active_contracts()

    # Check if we have any items for a contract
    non_mission_items = {}
    for inventory in ship['cargo']['inventory']: # Loop through our inventory
        if contract_list:
            for contract in contract_list: # Loop through all our contracts
                if contract['type'] == "PROCUREMENT": # Only proceed for PROCUREMENT contracts
                    for contract_item in contract['terms']['deliver']: # Loop through all items in the contract
                        if inventory['symbol'] != contract_item['tradeSymbol']:
                            non_mission_items[inventory['symbol']] = inventory['units']
        else:
            non_mission_items[inventory['symbol']] = inventory['units']
    print(f"{ship['symbol']} has {len(non_mission_items)} non-mission items:")
    for item in non_mission_items:
        print(f"\t{item}")
    return non_mission_items

def process_inventory(ship):
    print(f"Processing inventory for {ship['symbol']}!")

    # Get all contracts/missions we have
#    our_contracts = contracts.list_contracts()['data']

    # Send ship into orbit
    ships.orbit(ship['symbol'])

    # Check if we have any items for a contract
    mission_items = get_list_of_mission_items(ship)
    if mission_items:
        print("Delivering mission items.")
        deliver_mission_items(ship, mission_items)

    # Get list of all non-mission items
    non_mission_items = get_list_of_non_mission_items(ship)
    if non_mission_items:
        print(f"Proceeding with sales with {ship['symbol']}.")
        sell_items(ship, non_mission_items)


def deliver_mission_items(ship, items):
    # Get details of all contracts
    contract_list = contracts.list_contracts()['data']

    # Remove all fulfilled and expired contracts
    current_datetime = datetime.datetime.utcnow()
    contract_list = [
        cmd for cmd in contract_list 
        if not (cmd.get('fulfilled', False) or 
            datetime.fromisoformat(cmd.get('expiration').replace('Z', '+00:00')) < current_datetime)
    ]

    # For each contract, check if we have any items that match the contract
    for contract in contract_list:
        for delivery in contract['terms']['deliver']:

            # If yes, go deliver what we have
            if delivery['tradeSymbol'] in items:
                travel_to_waypoint(ship, delivery['destinationSymbol'])
                dock_and_refuel(ship)
                contract_delivery = contracts.deliver_cargo_to_contract(contract['id'], ship['symbol'], delivery['tradeSymbol'], items.get(delivery['tradeSymbol'], 0))
                print(json.dumps(contract_delivery, indent=2))

                # If all items are delivered for the contract, fulfill it
                if contract_delivery['data']['contract']['fulfilled']:
                    fulfill = contracts.fulfill_contract(contract['id'])
                    if 'error' not in fulfill:
                        print(f"Contract {contract['id']} completed and fulfilled!")
                    print(json.dumps(fulfill, indent=2))


def sell_items(ship, items):
    system = ship['nav']['systemSymbol']
    market_list = systems.list_waypoints_in_system(system, traits="MARKETPLACE")['data']
    for market in market_list:
        market_items = systems.get_market(market['systemSymbol'], market['symbol'])['data']
#        print(json.dumps(market_items, indent=2))
        if market_items['exchange'] != []:
            print(f"{market_items['symbol']} has exchange goods.")
            for exchanges in market_items['exchange']:
#                print(f"\t{imports['symbol']}")
                for inventory in items:
                    if inventory == exchanges['symbol']:
                        print(f"Match: {inventory}")

                        # Travel to waypoint we found
                        travel_to_waypoint(ship, market_items['symbol'])

                        # Dock and refuel
                        dock_and_refuel(ship)

                        # Sell the cargo
                        sell = ships.sell_cargo(ship['symbol'], inventory, items[inventory])
#                        print(json.dumps(sell, indent=2))
                        if 'error' in sell:
                            print(json.dumps(sell, indent=2))
                        else:
                            print(f"Sale successful: {items[inventory]} units sold of {inventory} for a total of {sell['data']['transaction']['totalPrice']}.")



if __name__ == "__main__":
    print("This file is not meant to be run directly.")
    exit(0)