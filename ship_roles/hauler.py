# TODO: This will carry out the tasks for a hauler ship.

# Ideally:
# Choose somewhere that one or more of the miners are operating. Don't choose one where there's already a hauler operating, if possible.
# Go to where a miner is and dock there. Wait for the hauler to dock.
# (Loop while not full)
#  Find a ship of type EXCAVATOR (or COMMAND for now) that is docked where we are.
#  One at a time, transfer the miner's goods to the hauler. (Checking our available space each time, and not over-transferring by accident.)
# When full, process_inventory (submit contract goods and sell the rest, maybe deliver some for refining later?).
# When empty, return to the location where the mining was happening and start again.
#  There may be somewhere new we started mining, so we should double-check there's a hauler at each mining site and move to a new site if necessary.
import json
import time
import api.ships as ships
#import api.systems as systems
import libraries

class ShipHauler:

    def hauler_thread(self, ship):

        while True is True:
            
            # Choose somewhere that one or more of the miners are operating. Don't choose one where there's already a hauler operating, if possible.
            # X1-TX89-B37 - Temp value for testing. This is where we'll do mining.
            mining_waypoint = "X1-TX89-H53"
#            mining_system = "X1-TX89"

            # Go to where a miner is and dock there. Wait for the hauler to dock.
            libraries.travel_to_waypoint(ship, mining_waypoint)
            ships.dock(ship['symbol'])

            # (Loop while not full)
            hauler_cargo_units_available = ship['cargo']['capacity'] - ship['cargo']['units']
            loop = 3
            while hauler_cargo_units_available > 0 and loop > 0:

            #  Find a ship of type EXCAVATOR (or COMMAND for now) that is docked where we are.
                all_ships = ships.list_ships()['data']
                filtered_ships = [
                    ship for ship in all_ships
                    if ship.get('nav', {}).get('waypointSymbol') == ship['nav']['waypointSymbol']
                    and ship.get('registration', {}).get('role') == 'EXCAVATOR'
                ]

                for extraction_ship in filtered_ships:
                    if extraction_ship['nav']['status'] == "DOCKED":
                        for cargo_item in extraction_ship['cargo']['inventory']:

                            # Check if we're too close to max inventory on hauler.
                            if cargo_item['units'] > hauler_cargo_units_available:
                                transfer_quantity = hauler_cargo_units_available
                            else:
                                transfer_quantity = cargo_item['units']

                            # Transfer cargo from extractor ship to hauler.
                            transfer_cargo = ships.transfer_cargo(extraction_ship['registration']['name'], ship['symbol'], cargo_item['symbol'], transfer_quantity)
                            if "error" not in transfer_cargo:
                                hauler_cargo_units_available = hauler_cargo_units_available - transfer_quantity

                            # Exit looping through cargo if hauler is full.
                            if hauler_cargo_units_available == 0:
                                break

                    # Exit looping through ships if hauler is full.
                    if hauler_cargo_units_available == 0:
                        break

                loop = loop - 1

                time.sleep(60) # Wait 60 seconds before continuing 

            # When full, process_inventory (submit contract goods and sell the rest, maybe deliver some for refining later?).
            libraries.process_inventory(ship['symbol'])

            # When empty, return to the location where the mining was happening and start again.
            #  There may be somewhere new we started mining, so we should double-check there's a hauler at each mining site and move to a new site if necessary.

            # For now we just return to the beginning of the loop, which takes us to the same location. TODO: Dynamically choose/remember location.

        return # hauler_thread


if __name__ == "__main__":
    print("This file is not meant to be run directly.")
    print(json.dumps(0, indent=2))