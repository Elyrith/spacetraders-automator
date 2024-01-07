# Plan: I want to create a multi-threaded application that will play spacetraders.io for me.
# The API documentation is here: https://spacetraders.stoplight.io/docs/spacetraders/11f2735b75b02-space-traders-api
# Here's the intro guide: https://docs.spacetraders.io/
# ChatGPT Conversation: https://chat.openai.com/c/aa60d40e-cde4-404f-b4f9-3c7ab448c87b

#Current plan:
# Each ship type will have tasks it does. We'll break each ship out into it's own thread so it can do them as required/able.
# FABRICATOR: TODO
# HARVESTER: TODO
# HAULER: 
# INTERCEPTOR: TODO
# EXCAVATOR: 
# TRANSPORT: TODO
# REPAIR: TODO
# SURVEYOR: TODO
# COMMAND: (Same as miner for now, until haulers and excavators are separated.)
# CARRIER: TODO
# PATROL: TODO
# SATELLITE: TODO
# EXPLORER: TODO
# REFINERY: TODO

#import json
import logging
import threading
from logging.handlers import RotatingFileHandler

import api.agents as agents
import api.ships as ships
from ship_roles.command import ShipCommand
from ship_roles.hauler import ShipHauler

# Create class items
ship_command_class = ShipCommand()
ship_hauler_class = ShipHauler()

def setup_logging() -> None:
    log = logging.getLogger()

    try:
        # __enter__
        max_bytes = 32 * 1024 * 1024  # 32 MiB
        logging.getLogger('spacetraders').setLevel(logging.INFO)

        log.setLevel(logging.INFO)
        handler = RotatingFileHandler(filename='logs/spacetraders.log', encoding='utf-8', mode='w', maxBytes=max_bytes, backupCount=5)
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

def ship_check(ship):
    print(f"Ship Symbol: {ship['symbol']} has role {ship['registration']['role']} at {ship['nav']['waypointSymbol']}")
    if ship['cargo']['capacity'] > 0:
        print(f"Ship Cargo: {ship['cargo']['units']}/{ship['cargo']['capacity']}")
    if ship['fuel']['capacity'] > 0:
        print(f"Ship Fuel: {ship['fuel']['current']}/{ship['fuel']['capacity']}")
    print("")

if __name__ == "__main__":
    setup_logging()
    log = logging.getLogger('spacetraders')

    # Start main thread


    # Perform tasks for each ship asynchronously

    # First, find out how many ships we have
    agent = agents.get_agent()
    if not isinstance(agent, dict):
        log.error("Issue getting agent info. Quitting.")
        print("Issue getting agent info. Quitting.")
        exit(1)

    credits_starting = agent['data']['credits']

    # Get details for each ship and launch a thread for each
    if agent["data"]["shipCount"] > 0:
        ships_list = ships.list_ships()
        if isinstance(ships_list, dict):
            threads = []
            for ship in ships_list["data"]:
                ship_check(ship)

                # Create a thread for each ship depending on it's type
                match ship['registration']['role']:
                    case "COMMAND":
                        t = threading.Thread(target=ship_command_class.command_thread, args=(ship,))
                        threads.append(t)
                        t.start()
                    case "HAULER":
                        t = threading.Thread(target=ship_hauler_class.hauler_thread, args=(ship,))
                        threads.append(t)
                        t.start()

            # Wait for all threads to complete, then start them.
            for t in threads:
                t.join()

        else:
            log.error("There are no ships in this account.")
            print("There are no ships in this account.")
            exit(1)

    # Report our profit/loss
    agent = agents.get_agent()
    credits_change = agent['data']['credits'] - credits_starting
    print(f"Change in credits during this run: {credits_change}. New total: {agent['data']['credits']}")
