# Cryptocurrency Price Viewer

This project is a simple command-line application that allows users to fetch and display cryptocurrency prices. It retrieves data from the CoinMarketCap API and caches it locally for efficient access.

## Files

- **main.py**: The main application script that provides an interactive menu for fetching and displaying cryptocurrency prices.
- **price_fetcher.py**: Contains functions for fetching cryptocurrency data from the CoinMarketCap API, managing API keys, caching, and data validation.

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd crypto_prices
   ```

2. Install the required packages:
   ```
   pip install requests
   ```

3. Create a configuration directory:
   ```
   mkdir -p ~/.crypto_prices
   ```

4. Run the application:
   ```
   python main.py
   ```

5. When prompted, enter your CoinMarketCap API key. You can also set the API key in the environment variable `CMC_API_KEY` to avoid prompts.

## Usage

- **Fetch and cache cryptocurrency data**: Select option 1 from the menu to fetch the latest cryptocurrency prices and cache the data locally.
- **Show price of a specific cryptocurrency**: Select option 2 to enter the name or symbol of a cryptocurrency and view its current price and other details.
- **Exit**: Select option 3 to exit the application.

## Configuration

The application will prompt for the API key and cache expiry time on the first run. The configuration will be saved in `~/.crypto_prices/config.json`. You can modify this file directly if needed.

## Notes

- Ensure you have a valid CoinMarketCap API key to fetch data.
- The cached data will be stored in `~/.crypto_prices/crypto_data.json` and will be used for subsequent requests until it expires based on the configured expiry time.

## License

This is Provided for learning purposes only, You are free to use it if you wish.
