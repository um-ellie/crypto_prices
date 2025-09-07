# crypto_prices

A simple Python script to fetch and cache cryptocurrency prices from the CoinMarketCap API.

## Features

- Retrieves latest cryptocurrency data using the CoinMarketCap API.
- Caches results locally to minimize API calls.
- Handles API key configuration via environment variable or user prompt.

## Usage

1. **Install dependencies:**
    ```bash
    pip install requests
    ```

2. **Run the script:**
    ```bash
    python price_fetcher.py
    ```

3. **API Key Setup:**
    - The script will prompt for your CoinMarketCap API key on first run.
    - You can also set your API key as an environment variable:
        ```bash
        export CMC_API_KEY=your_api_key_here
        ```

## Files

- `price_fetcher.py`: Main script for fetching and caching crypto prices.

## License

This is Provided for learning purposes only, You are free to use it if you wish.
