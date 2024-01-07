# TODO: This will carry out the tasks for a satellite ship.

# Ideally:
# Choose somewhere with a market that doesn't already have a satellite ship at it.
# Go to that location and dock.
# Do nothing... though...
# Sometimes (every 2 hours?), do a quick check to make sure we haven't accidentally sent another satellite to the same spot. They are quite slow, after all.
# If there are, the satellite with the highest SHIPNAME-number gets to stay. The rest start over at the beginning to find somewhere new.

# It may be easier to just do loop through all the destinations of all the other satellites to ensure we're not doubling up...
# It's still nice to check that we haven't screwed up, though.
import random
import api.ships as ships
import api.systems as systems

class ShipSatellite:

    def satellite_thread(self, ship):
        # Wait a random number of seconds so we don't have all the satellite ships finding new homes at the same time.

        # First, check if we're the only satellite at the current location, and that it's a marketplace. If so, lets just stay here!

        # Find out where I have satellite ships
        satellite_ships = ships.list_ships()['data']
        satellite_ships = [ship for ship in satellite_ships if ship['registration']['role'] == 'SATELLITE'] # Leave only SATELLITE ships in the list

        ships_with_me = -1 # Lazy accounting.
        for satellite_ship in satellite_ships:
            if satellite_ship['nav']['waypointSymbol'] == ship['nav']['waypointSymbol']:
                ships_with_me = ships_with_me + 1

        if ships_with_me > -1: # Testing with 0. Change to 1 for production.
            marketplaces_with_no_satellites = self.find_somewhere_else_to_be(ship)

            if marketplaces_with_no_satellites is not None:
                print(f"Found at least one marketplace with no satellite: {marketplaces_with_no_satellites[0]['symbol']}")
            else:
                print("All marketplaces have satellites.")

            market_index_random = random.randrange(marketplaces_with_no_satellites.count())
            return marketplaces_with_no_satellites[market_index_random]

        return

    def find_somewhere_else_to_be(self, ship):
        # Choose somewhere with a market that doesn't already have a satellite ship at it.

        # Find out where I have satellite ships
        satellite_ships = ships.list_ships()['data']
        satellite_ships = [ship for ship in satellite_ships if ship['registration']['role'] == 'SATELLITE'] # Leave only SATELLITE ships in the list
        satellite_ships = [ship for ship in satellite_ships if ship['registration']['name'] == ship['symbol']] # Exclude the current ship

        # Find all markets in the same system as the current ship. As of 2023-12-01, satellites can't jump systems, so there's no point looking outside the current system. I may not understand Jump Gates, though.
        marketplaces = systems.list_waypoints_in_system(ship['nav']['systemSymbol'], limit=3, traits="MARKETPLACE")['data']

        # Remove from marketplaces all waypoints where we currently have a satellite ship
        # The small loop is marketplaces so it whittles down the list as it goes. If the big loop was marketplaces, we would check every marketplace for every ship, even if we already removed the current marketplace from the marketplaces list.
        for satellite_ship in satellite_ships:
            for marketplace in marketplaces:
                if marketplace['symbol'] == satellite_ship['nav']['route']['destination']:
                    marketplaces.remove(marketplace)
                    print(f"Marketplaces left: {marketplaces.count()}")
                    break
        # In future, we may want to check if any satellite ships are currently travelling somewhere and remove those, too. That may be complicated since the ['nav']['waypointSymbol'] is usually for the last place a ship was while travelling. Depending on how the ['route']['destination']['symbol'] data behaves, that may be best to use instead of ['nav']['waypointSymbol'].

        return marketplaces


if __name__ == "__main__":
    print("This file is not meant to be run directly.")
