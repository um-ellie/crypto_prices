from price_fetcher import CONFIG_DIR, CRYPTO_DATA_FILE
from price_fetcher import fetch_crypto_data
import json
import os
import sys



MESSAGES = {
    "menu": {
        "title": "Cryptocurrency Price Viewer",
        "options": [
            "1. Fetch and cache cryptocurrency data",
            "2. Show price of a specific cryptocurrency",
            "3. Exit",
        ],
        "prompt": "Enter your choice (1-3): ",
        "invalid_choice": "Invalid choice. Please enter 1, 2, or 3.",
    },
    "errors": {
        "no_cache": "No cached data found. Please fetch data first.",
        "read_cache": "Error reading cached data: {error}",
        "invalid_crypto": "Invalid input. Please enter a valid cryptocurrency name or symbol.",
        "not_found": "Cryptocurrency '{name}' not found in the cached data.",
        "fetch_failed": "Failed to fetch data.",
    },
    "info": {
        "fetching": "Fetching cryptocurrency data...",
        "fetched": "Data fetched and cached successfully.",
        "top5_title": "Top 5 Cryptocurrencies by Market Cap:",
        "exit": "Exiting the program.",
    },
    "prompts": {
        "crypto_name": "Enter the cryptocurrency name or symbol: ",
        "back": "\nPress Enter to return to the menu...",
    },
}


def clear_console():
    """Clear the console for better readability."""
    os.system('cls' if os.name == 'nt' else 'clear')


def price_show(crypto_name: str) -> None:
    """Fetch and display the price of a specific cryptocurrency from cached data."""
    if not CRYPTO_DATA_FILE.exists():
        print(MESSAGES["errors"]["no_cache"])
        return

    try:
        with open(CRYPTO_DATA_FILE, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except (json.JSONDecodeError, OSError) as e:
        print(MESSAGES["errors"]["read_cache"].format(error=e))
        return

    for crypto in data.get('data', []):
        if crypto_name.lower() in (
            crypto.get('name', '').lower(),
            crypto.get('symbol', '').lower(),
        ):
            usd_data = crypto.get("quote", {}).get("USD", {})
            price = usd_data.get("price")
            market_cap = usd_data.get("market_cap")
            volume_24h = usd_data.get("volume_24h")
            percent_change_24h = usd_data.get("percent_change_24h")

            print(f"\nName: {crypto.get('name', 'N/A')}")
            print(f"Symbol: {crypto.get('symbol', 'N/A')}")
            print(f"Price: ${price:,.2f}" if price else "Price: N/A")
            print(f"Market Cap: ${market_cap:,.2f}" if market_cap else "Market Cap: N/A")
            print(f"24h Volume: ${volume_24h:,.2f}" if volume_24h else "24h Volume: N/A")
            print(f"24h Change: {percent_change_24h:.2f}%" if percent_change_24h else "24h Change: N/A")
            return

    print(MESSAGES["errors"]["not_found"].format(name=crypto_name))


def fetch_and_display_top() -> None:
    """Fetch crypto data and display top 5 by market cap."""
    print(MESSAGES["info"]["fetching"])
    data = fetch_crypto_data()
    if not data:
        input(f"{MESSAGES['errors']['fetch_failed']} {MESSAGES['prompts']['back']}")
        return

    print(MESSAGES["info"]["fetched"])
    print()
    print(MESSAGES["info"]["top5_title"])

    sorted_data = sorted(
        data.get('data', []),
        key=lambda x: x.get('quote', {}).get('USD', {}).get('market_cap', 0),
        reverse=True,
    )

    for crypto in sorted_data[:5]:
        name = crypto.get("name", "N/A")
        symbol = crypto.get("symbol", "N/A")
        price = crypto.get("quote", {}).get("USD", {}).get("price")
        market_cap = crypto.get("quote", {}).get("USD", {}).get("market_cap")
        print(f"{name} ({symbol}): Price: ${price:,.2f}, Market Cap: ${market_cap:,.2f}")

    input(MESSAGES["prompts"]["back"])


def show_specific_price() -> None:
    """Prompt user for a cryptocurrency and show its price."""
    crypto_name = input(MESSAGES["prompts"]["crypto_name"]).strip()
    if not crypto_name:
        print(MESSAGES["errors"]["invalid_crypto"])
    else:
        price_show(crypto_name)
    input(MESSAGES["prompts"]["back"])


def main():
    """Main interactive menu."""
    while True:
        clear_console()
        print("=" * 30)
        print(MESSAGES["menu"]["title"])
        print("=" * 30)
        for option in MESSAGES["menu"]["options"]:
            print(option)

        choice = input(MESSAGES["menu"]["prompt"]).strip()

        match choice:
            case "1":
                fetch_and_display_top()
            case "2":
                show_specific_price()
            case "3":
                print(MESSAGES["info"]["exit"])
                sys.exit(0)
            case _:
                print(MESSAGES["menu"]["invalid_choice"])
                input(MESSAGES["prompts"]["back"])


if __name__ == "__main__":
    main()
