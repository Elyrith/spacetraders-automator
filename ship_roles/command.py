# TODO: Replace what this ship does with whatever we decide a COMMAND shp does. Until then, it's a miner+hauler in one.

import logging
import math
import time
from logging.handlers import RotatingFileHandler

import api.ships as ships
import api.systems as systems
import libraries

loop = 10

def setup_logging(ship_name) -> None:
    log = logging.getLogger()

    try:
        # __enter__
        max_bytes = 32 * 1024 * 1024  # 32 MiB
        logging.getLogger(f'spacetraders.{ship_name}').setLevel(logging.INFO)

        log.setLevel(logging.INFO)
        handler = RotatingFileHandler(filename=f'logs/spacetraders-command-{ship_name}.log', encoding='utf-8', mode='w', maxBytes=max_bytes, backupCount=5)
        dt_fmt = '%Y-%m-%d %H:%M:%S'
        fmt = logging.Formatter('[{asctime}] [{levelname:<7}] {name}: {message}', dt_fmt, style='{')
        handler.setFormatter(fmt)
        log.addHandler(handler)

        yield
    finally:
        # __exit__
        handlers = log.handlers[:]
        for hdlr in handlers:
            hdlr.close()
            log.removeHandler(hdlr)


class ShipCommand:

    def command_thread(self, ship):

        # Start logging
        setup_logging(ship['symbol'])
        self.log = logging.getLogger(f"spacetraders.{ship['symbol']}")

    # Step 1: Get stuff to sell
    #While not full: (If full, skip to selling and submitting to contract.)
    # Check if the ship is full

        loop_count = loop

        while loop_count > 0:

            # Get ship inventory so we can decide what we need to do
            ship = ships.get_ship(ship['symbol'])['data']
            print(f"{ship['symbol']} cargo: {ship['cargo']['units']}/{ship['cargo']['capacity']}")

            if ship['cargo']['units'] < ship['cargo']['capacity']:
                # If the cargo is not full, let's go mining
                self.log.info(f"{ship['symbol']} is going mining!")
                print(f"{ship['symbol']} is going mining!")
                self.go_mining(ship)
            else:
                # If the cargo is full, let's go empty it
                print(f"{ship['symbol']} is full!")
                libraries.process_inventory(ship)

            loop_count = loop_count - 1

# END OF MAIN FUNCTION

    def go_mining(self, ship):
        # Let's go mine some stuff.

    #Travel to a place for mining
    #    Wait for travel to finish
    #Dock and refuel (if possible)
    #Undock (orbit)
    #Attempt mining, then wait out the timer.

        # Find somewhere nearby to mine. (Currently limited to the ship's current system.)
        mining_waypoints = systems.list_waypoints_in_system(ship['nav']['systemSymbol'], limit=20, traits="COMMON_METAL_DEPOSITS")['data']
        if not isinstance(mining_waypoints, list):
            print(f"No waypoints found with COMMON_METAL_DEPOSITS in {ship['nav']['systemSymbol']}")
            return # Nevermind. Nowhere to mine. Maybe try some other traits?

        # Pick the closest destination.
        ship = ships.get_ship(ship['symbol'])['data']
        current_location_data = systems.get_waypoint(ship['nav']['systemSymbol'], ship['nav']['waypointSymbol'])['data']
        closest_waypoint_distance = 1000000 # Setting it super-high so we'll always find somewhere closer.
        closest_waypoint_symbol = ""

        for mining_waypoint in mining_waypoints: # Look though the wayponts and calculate distance. Record the closest.
            distance = math.sqrt((mining_waypoint['x'] - current_location_data['x'])**2 + (mining_waypoint['y'] - current_location_data['y'])**2)
            if distance < closest_waypoint_distance:
                closest_waypoint_distance = distance
                closest_waypoint_symbol = mining_waypoint['symbol']
        print(f"The closest waypoint is {closest_waypoint_symbol} at {int(closest_waypoint_distance)}")

        travel = libraries.travel_to_waypoint(ship, closest_waypoint_symbol) # This function returns True once we get there, even if we're already there.

        if travel: # Only mine if we successfully travelled.
            # Mine until we're full
            ship_cargo_units = ship['cargo']['units']
            ship_cargo_capacity = ship['cargo']['capacity']
            while ship_cargo_units < ship_cargo_capacity:
                mining = ships.extract_resources(ship['symbol'])
                print(f"{ship['symbol']} successfully mined {mining['data']['extraction']['yield']['units']} units of {mining['data']['extraction']['yield']['symbol']} from {closest_waypoint_symbol}! Cooldown: {mining['data']['cooldown']['remainingSeconds']} seconds.")
                ship_cargo_units = mining['data']['cargo']['units']
                ship_cargo_capacity = mining['data']['cargo']['capacity']
                if ship_cargo_units < ship_cargo_capacity:
                    time.sleep(mining['data']['cooldown']['remainingSeconds'])

            print(f"Ship {ship['symbol']} is now full. ({ship_cargo_units}/{ship_cargo_capacity})")

if __name__ == "__main__":
    print("This file is not meant to be run directly.")
