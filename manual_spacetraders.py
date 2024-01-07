import json
import time

import api.agents as agents
import api.contracts as contracts
import api.root as root
import api.ships as ships
import api.systems as systems
import libraries

import ship_roles.satellite as satellite

commandship_name = "SAMPLE-1"
probeship_name = "SAMPLE-2"
excavatorship_name = "SAMPLE-3"
good = "SAMPLE"
system = "SAMPLE"

mining_system = "SAMPLE-BZ5C"
selling_system = "SAMPLE-B7"

departure_time = "2023-11-23T01:44:23.898Z"
arrival_time = "2023-11-23T01:49:21.898Z"



def get_market_data(good):
    market_list = systems.list_waypoints_in_system(system, traits="MARKETPLACE")['data']
    for market in market_list:
        market_items = systems.get_market(market['systemSymbol'], market['symbol'])['data']
        if market_items['exchange'] != []:
            for market_exchange in market_items['exchange']:
                if market_exchange['symbol'] == good:
                    print(f"{market_items['symbol']} offers {good} at it's exchange.")
                    return True
    return False

if __name__ == "__main__":
# Register new agent
#    command = root.register_new_agent("SAMPLE", "sample@example.com")

# Root API calls
    command = root.get_status()

#    command = agents.get_agent()


# Ships API calls
#    command = ships.list_ships()['data']
#    ship = ships.get_ship(commandship_name)['data']
#    ship = ships.get_ship(probeship_name)['data']
#    ship = ships.get_ship(excavatorship_name)['data']
#    command = ship
#    command = ships.get_ship_cooldown(ship['symbol'])
#    if command['data']['remainingSeconds'] > 0:
#        print(f"Ship {ship['symbol']} has a remaining cooldown of {command['data']['remainingSeconds']}. Waiting...")
#        time.sleep(command['data']['remainingSeconds'])
#    command = ships.dock(ship['symbol'])
#    command = ships.get_ship_nav(ship['symbol'])
#    command = ships.patch_ship_nav(ship['symbol'], "BURN")
#    command = ships.refuel_ship(ship['symbol'])
#    command = ships.create_survey(ship['symbol'])
#    command = ships.get_ship_cargo(ship['symbol'])
#    command = ships.transfer_cargo(excavatorship_name, commandship_name, good, 4)
#    command = ships.scan_systems(ship['symbol'])
#    command = ships.ship_refine(ship['symbol'], "COPPER")
#    command = ships.get_ship_cargo(ship['symbol'])
#    command = ships.orbit(ship['symbol'])
#    command = ships.warp_ship(ship['symbol'], "X1-RY96-FE2E")
#    command = ships.purchase_ship("SHIP_PROBE", "X1-TX89-A2")
#    command = ships.get_ship_nav(ship['symbol'])
#    command = ships.navigate(ship['symbol'], "X1-TX89-C42")
#    command = ships.negotiate_contract(ship['symbol'])
#    command = libraries.travel_to_waypoint(ship, "X1-TX89-A2")


# Custom
#     command = get_market_data(good)

#    non_mission_items = libraries.get_list_of_non_mission_items(ship['symbol'])
#    command = libraries.sell_items(ship['symbol'])

#    command = libraries.calculate_time(departure_time, arrival_time)

#    command = libraries.get_list_of_active_contracts()


# Systems API calls
#    waypoint = selling_system
#    last_dash_index = waypoint.rfind("-") # Find the last dash in the string so we can get the system name.
#    command = systems.get_market(waypoint[:last_dash_index], waypoint)

#    command = systems.list_waypoints_in_system("X1-TX89", traits="SHPYARD")
#    command = systems.get_shipyard("X1-TX89", "X1-TX89-A2")
# X1-TX89-H53 (Mining: 49320, Surveyor: 29146),
# X1-TX89-A2 (Probe: 19502, Light Shuttle: 102227, Light Hauler: 337911)
# X1-TX89-C42 (Probe: 22585, Siphon: 34899)


# Contracts API calls
#    command = contracts.list_contracts()['data']

#    command = [contract for contract in command if not contract.get('fulfilled', False)]
#    command = contracts.accept_contract("clpbs7vem0qrqs60cjrrrqgen")


# Surveys API calls
#    command = ships.create_survey(commandship_name)


# Bot Stuff
#    ship_satellite_class = satellite.ShipSatellite()
#    command = ship_satellite = ship_satellite_class.satellite_thread(ship)

# Print output
    print(json.dumps(command, indent=2))
