import os
import json
import requests
from pathlib import Path
from requests.exceptions import RequestException, HTTPError, Timeout

"""
This script fetches cryptocurrency prices from the CoinMarketCap API.
It handles API key management, including loading from environment variables,
a config file, or prompting the user.
It also caches the fetched data locally to minimize API calls.
"""

# Constants
CONFIG_DIR = Path.home() / '.price_fetcher'
CONFIG_FILE = CONFIG_DIR / 'config.json'
CRYPTO_DATA_FILE = CONFIG_DIR / 'crypto_data.json'

def load_api_key() -> str | None:

    """Load the API key from environment variable, config file, or prompt the user."""

    # Check environment variable
    api_key = os.getenv('CMC_API_KEY')
    if api_key:
        return api_key.strip()
    
    # Check config file
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as file:
                config = json.load(file)
                api_key = config.get("api_key")
                if api_key:
                    return api_key.strip()
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error reading config file: {e}")

    # Prompt user for API key
    api_key = input("Enter your CoinMarketCap API key: ").strip()
    if not api_key:
        print("API key cannot be empty.")
        return None
    
    # Save API key to config file
    save = input("Would you like to save this API key for future use? (y/n): ").strip().lower()
    if save == 'y':
        try:
            CONFIG_DIR.mkdir(parents=True, exist_ok=True)
            with open(CONFIG_FILE, 'w', encoding='utf-8') as file:
                json.dump({"api_key": api_key}, file, indent=4)
                print("API key saved successfully.")

        except (IOError, TypeError) as e:
            print(f"Error saving config file: {e}")
    return api_key

def fetch_crypto_data(limit: int = 50, convert: str = 'USD', refresh: bool = False):

    """Fetch cryptocurrency data from CoinMarketCap API or local cache."""

    api_key = load_api_key()
    if not api_key:
        print("No API key available. Exiting.")
        return None
    

    # Check if data file exists and refresh is not requested
    if CRYPTO_DATA_FILE.exists() and not refresh:
        try:
            with open(CRYPTO_DATA_FILE, 'r', encoding='utf-8') as file:
                data = json.load(file)
                print("Loaded data from local cache.")
                return data
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error reading local data file: {e}")

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
    data = fetch_crypto_data(limit=10, refresh=True)
    if data:
        for crypto in data.get('data', []):
            name = crypto.get('name')
            symbol = crypto.get('symbol')
            price = crypto.get('quote', {}).get('USD', {}).get('price')
            print(f"{name} ({symbol}): ${price:.2f}")