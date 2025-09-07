from price_fetcher import CONFIG_DIR, CRYPTO_DATA_FILE
import json



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

    print("\nThis module provides the price_show function to display cryptocurrency prices.")
    print("Menu:","=" * 30)
    print("1. Show price of a specific cryptocurrency")
    print("2. Exit")
    choice = input("Enter your choice (1-2): ").strip()

    match choice:
        case '1':
            crypto_name = input("Enter the cryptocurrency name or symbol: ").strip()
            if crypto_name:
                price_show(crypto_name)
            else:
                print("Invalid input. Please enter a valid cryptocurrency name or symbol.")
        case '2':
            print("Exiting the program.")
            exit()
        case _:
            print("Invalid choice. Please enter 1 or 2.")