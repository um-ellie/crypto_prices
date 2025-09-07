import os
import json
import requests
from pathlib import Path
from requests.exceptions import RequestException, HTTPError, Timeout
from datetime import datetime, timedelta

"""
This script fetches cryptocurrency prices from the CoinMarketCap API.
It handles API key management, including loading from environment variables,
a config file, or prompting the user.
It also caches the fetched data locally to minimize API calls.
"""

# Constants
CONFIG_DIR = Path.home() / '.crypto_prices'
CONFIG_FILE = CONFIG_DIR / 'config.json'
CRYPTO_DATA_FILE = CONFIG_DIR / 'crypto_data.json'


DEFAULT_CACHE_EXPIRY_MINUTES = 60  # minutes (1 hour)

def ask_until_non_empty(prompt: str) -> str:
    """Prompt the user until a non-empty input is received."""
    response = input(prompt).strip()
    while not response:
        response = input(f"Input cannot be empty. {prompt}").strip()
    return response


def crypto_prices_config() -> dict:

    """Load configuration from file or environment variables."""

    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as file:
                config = json.load(file)
                return config
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error reading config file: {e}")

    api_key = ask_until_non_empty("Enter your CoinMarketCap API key: ")

    try:
        expiry_minute = int(
            input(f"Enter cache expiry time in minutes (default {DEFAULT_CACHE_EXPIRY_MINUTES}): ").strip()
            or DEFAULT_CACHE_EXPIRY_MINUTES
        )
        if expiry_minute <= 0:
            print("Expiry time must be positive. Using default.")
            expiry_minute = DEFAULT_CACHE_EXPIRY_MINUTES
    except ValueError:
        print(f"Invalid input. Using default cache expiry time: {DEFAULT_CACHE_EXPIRY_MINUTES} minutes.")
        expiry_minute = DEFAULT_CACHE_EXPIRY_MINUTES


    config = {
        "api_key": api_key,
        "expiry_minute": expiry_minute
    }

    # Save config to file
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as file:
            json.dump(config, file, indent=4)
            print(f"Configuration saved successfully to {CONFIG_FILE}.")
    except IOError as e:
        print(f"Error saving config file: {e}")

    return config


def is_cache_valid(file_path: Path, expiry_minutes: int) -> bool:
    """Check if the cache file exists and is still valid based on expiry time."""

    if not file_path.exists():
        return False
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            timestamp = data.get('timestamp')
            if not timestamp:
                return False
            cache_time = datetime.fromtimestamp(timestamp)
            return datetime.now() - cache_time < timedelta(minutes=expiry_minutes)
    except (json.JSONDecodeError, IOError, ValueError) as e:
        print(f"Error reading cache file: {e}")
        return False




def fetch_crypto_data(limit: int = 5000, convert: str = 'USD') -> dict | None:
    """Fetch cryptocurrency data from CoinMarketCap API or local cache."""

    print("\nFetching cryptocurrency data...")
    print("Note: You can get a free API key from https://coinmarketcap.com/api/")
    print("If you have already set an environment variable 'CMC_API_KEY', it will be used.\n")
    print("Fetching data may take a few seconds...\n")
    print("=" * 30)
    config = crypto_prices_config()
    api_key = os.getenv('CMC_API_KEY') or config.get("api_key")
    expiry_minutes = config.get("expiry_minute", DEFAULT_CACHE_EXPIRY_MINUTES)

    # Check if cache is valid
    if is_cache_valid(CRYPTO_DATA_FILE, expiry_minutes):
        try:
            with open(CRYPTO_DATA_FILE, 'r', encoding='utf-8') as file:
                data = json.load(file)
                print(f"Loaded data from cache valid for {expiry_minutes} minutes.")
                return data
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error reading cache file: {e}")

    # Fetch data from API
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': api_key,
    }
    params = {
        'start': '1',
        'limit': str(limit),
        'convert': convert,
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()

        # Add timestamp to data
        data['timestamp'] = datetime.now().timestamp()


        # Save data to local file
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        with open(CRYPTO_DATA_FILE, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)
            print("Data fetched and saved to local cache.")
        return data
    
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Timeout:
        print("The request timed out.")
    except RequestException as req_err:
        print(f"Request error occurred: {req_err}")
    except (IOError, TypeError) as e:
        print(f"Error saving data file: {e}")
    except (KeyError, json.JSONDecodeError) as parse_err:
        print(f"Error parsing JSON response: {parse_err}")

    return None


# Example usage
if __name__ == "__main__":
    data = fetch_crypto_data()
    if data:
        print(f"Fetched {len(data.get('data', []))} cryptocurrencies.\n")
        
        # Print the first 5 cryptocurrencies
        print("=" * 30)
        print("Top 5 Cryptocurrencies:")
        for crypto in data.get('data', [])[:5]:
            print(f"{crypto['name']} ({crypto['symbol']}): ${crypto['quote']['USD']['price']:.2f}")
        print("=" * 30)