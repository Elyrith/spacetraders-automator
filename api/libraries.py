# This file contains all the libraries needed by the API functions.

# TODO: Have one function that does all the API calls and makes sure we don't blow over the API call limits.

import json
import os

from config import api_version

def check_response(response):
    # Special: get_ship_cooldown but no cooldown
    if response.status_code == 204:
        response = {
            "data": {
                "remainingSeconds": 0,
            }
        }
        return response

    # All other scenarios
    if response.status_code > 199 and response.status_code < 300:
        return response.json()
    else:
        print(f"Status code: {response.status_code}")
        print(f"Error message: {response.text}")
        return response.json()

# Check if we have an existing cache file and return it's contents if it exists
def load_cache_data(cache_filename):
    # Check if cache_filename exists
    if os.path.isfile(cache_filename):
        # If the file exists, check the contents of the file for the JSON data "api_version"
        with open(cache_filename, "r") as cache:
            cache_data = json.load(cache)
            if "cache_api_version" in cache_data:
                # If the cache file's API version is the same as the current API version, then we can use the cache file
                if cache_data["cache_api_version"] == api_version:
                    del cache_data["cache_api_version"]
                    return cache_data
    else:
        return False

# Save the result to a cache file
def save_cache_data(result, cache_file):
    try:
        # Check if the cache_file exists
        if os.path.isfile(cache_file):
            # If the file exists, check the contents of the file for the JSON data "api_version"
            with open(cache_file, "r") as cache:
                cache_data = json.load(cache)
                if "cache_api_version" in cache_data:
                    # If the cache file's API version is the same as the current API version, then we can use the cache file
                    if cache_data["cache_api_version"] == result["api_version"]:
                        return True
                else:
                    # If the file does not contain the JSON data "api_version", then we can't use the cache file
                    cache_data = False
            if not cache_data:
                os.remove(cache_file)

        # Add the API version to the result
        result["cache_api_version"] = api_version

        # Create cache_file and write the result to it
        with open(cache_file, "w") as cache:
            json.dump(result, cache)
            return True
    except Exception as e:
        print(e)
        return False

if __name__ == "__main__":
    print("This file is not meant to be run directly.")
