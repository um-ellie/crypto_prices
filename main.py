from price_fetcher import CONFIG_DIR, CRYPTO_DATA_FILE
from price_fetcher import fetch_crypto_data
import json
import os


def clear_console():
    """Clear the console for better readability."""
    os.system('cls' if os.name == 'nt' else 'clear')


def price_show(crypto_name: str):

    """Fetch and display the price of a specific cryptocurrency from data."""

    data_file = CRYPTO_DATA_FILE
    if not data_file.exists():
        print("No cached data found. Please fetch data first.")
        return

    try:
        with open(data_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error reading cached data: {e}")
        return
    
    # Search for the cryptocurrency by name or symbol and display its price and details.
    found = False
    for crypto in data.get('data', []):
        if crypto_name.lower() in (crypto.get('name', '').lower(), crypto.get('symbol', '').lower()):
            price = crypto.get('quote', {}).get('USD', {}).get('price')
            market_cap = crypto.get('quote', {}).get('USD', {}).get('market_cap')
            volume_24h = crypto.get('quote', {}).get('USD', {}).get('volume_24h')
            percent_change_24h = crypto.get('quote', {}).get('USD', {}).get('percent_change_24h')
            print(f"Name: {crypto.get('name')}")
            print(f"Symbol: {crypto.get('symbol')}")
            print(f"Price: ${price:,.2f}" if price else "Price: N/A")
            print(f"Market Cap: ${market_cap:,.2f}" if market_cap else "Market Cap: N/A")
            print(f"24h Volume: ${volume_24h:,.2f}" if volume_24h else "24h Volume: N/A")
            print(f"24h Change: {percent_change_24h:.2f}%" if percent_change_24h else "24h Change: N/A")
            found = True
            break
    if not found:
        print(f"Cryptocurrency '{crypto_name}' not found in the cached data.")
        return

if __name__ == "__main__":
    while True:
        clear_console()
        print("=" * 30)
        print("This module provides the price_show function to display cryptocurrency prices.")
        print("Menu:","=" * 30)
        print("1. Fetch and cache cryptocurrency data")
        print("2. Show price of a specific cryptocurrency")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ").strip()

        if choice == '1':
            print("Fetching cryptocurrency data...")
            data = fetch_crypto_data()
            if data:
                print("Data fetched and cached successfully.")
                # Display top 5 cryptocurrencies by market cap
                print("\nTop 5 Cryptocurrencies by Market Cap:")
                sorted_data = sorted(data.get('data', []), key=lambda x: x.get('quote', {}).get('USD', {}).get('market_cap', 0), reverse=True)
                for crypto in sorted_data[:5]:
                    name = crypto.get('name')
                    symbol = crypto.get('symbol')
                    price = crypto.get('quote', {}).get('USD', {}).get('price')
                    market_cap = crypto.get('quote', {}).get('USD', {}).get('market_cap')
                    print(f"{name} ({symbol}): Price: ${price:,.2f}, Market Cap: ${market_cap:,.2f}")
                input("\nPress Enter to back to the menu...")
            else:
                input("Failed to fetch data. Press Enter to back to the menu...")

        elif choice == '2':
            crypto_name = input("Enter the cryptocurrency name or symbol: ").strip()
            if crypto_name:
                price_show(crypto_name)
                input("\nPress Enter to back to the menu...")
            else:
                print("Invalid input. Please enter a valid cryptocurrency name or symbol.")
                input("Press Enter to back to the menu...")
        elif choice == '3':
            print("Exiting the program.")
            exit()
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
            input("Press Enter to back to the menu...")