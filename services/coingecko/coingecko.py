import os
import requests
from dotenv import load_dotenv
from typing import Dict, Any, Optional, List

# Load environment variables from the .env file
load_dotenv()

COINGECKO_API_KEY = os.getenv("COINGECKO_API_KEY")
BASE_URL = 'https://pro-api.coingecko.com/api/v3'

headers = {
            "Content-Type": "application/json",
            "x-cg-pro-api-key": COINGECKO_API_KEY,
        }

def get_list_of_coins(coin_names: Optional[List[str]] = None, coin_symbols: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Retrieve a list of all available coins from the CoinGecko API or check for specific coins.

    This function makes a GET request to the CoinGecko API to fetch a comprehensive
    list of all cryptocurrencies available on the platform. Each coin in the list
    includes basic information such as id, symbol, and name. If specific coin_names
    or coin_symbols are provided, it checks if those coins are available in the list
    and they are returned if found.

    Args:
        coin_names (List[str], optional): The names of the coins to check for availability.
        coin_symbols (List[str], optional): The symbols of the coins to check for availability.

    Returns:
        Dict[str, Any]: A dictionary containing:
            - 'coins' (List[Dict]): A list of dictionaries, each representing a coin
              with keys 'id', 'symbol', and 'name', if the request is successful.
            - 'length' (int): The length of the list of tokens.
            - 'success' (bool): True if the API call was successful, False otherwise.
            - 'error' (str): Error message or additional information if the request fails.
    """
    result = {
        'coins': [],
        'length': 0,
        'success': False,
    }

    try:
        response = requests.get(f'{BASE_URL}/coins/list', headers=headers, timeout=10)
        response.raise_for_status()  # Raises an HTTPError for bad responses

        all_coins = response.json()
        result['length'] = len(all_coins)
        result['success'] = True

        filtered_coins = []

        if coin_symbols:
            coin_symbols_lower = [symbol.lower() for symbol in coin_symbols]
            for coin in all_coins:
                if coin['symbol'].lower() in coin_symbols_lower:
                    filtered_coins.append(coin)

        if coin_names:
            coin_names_lower = [name.lower() for name in coin_names]
            for coin in all_coins:
                if coin['name'].lower() in coin_names_lower:
                    filtered_coins.append(coin)

        # Remove duplicates by converting to a set of tuples and back to a list
        unique_coins = {coin['id']: coin for coin in filtered_coins}.values()

        result['coins'] = list(unique_coins)
        result['length'] = len(result['coins'])

    except requests.exceptions.RequestException as e:
        raise Exception(f"Error in CoinGecko API request in get_list_of_coins: {str(e)}")
    except ValueError as e:
        raise Exception(f"Error decoding JSON response in get_list_of_coins: {str(e)}")
    except Exception as e:
        raise Exception(f"Unexpected error in get_list_of_coins: {str(e)}")

    return result


def get_coin_data(name: Optional[str] = None, symbol: Optional[str] = None) -> Dict[str, Any]:
    """
    Retrieve data for a specific coin from the CoinGecko API.

    This function makes a GET request to the CoinGecko API to fetch a comprehensive
    list of all cryptocurrencies and then filters for the specific coin based on
    the provided name or symbol.

    Args:
        name (str, optional): The name of the coin to search for.
        symbol (str, optional): The symbol of the coin to search for.

    Returns:
        Dict[str, Any]: A dictionary containing:
            - 'coin' (Dict): A dictionary representing the coin with keys 'id', 'symbol', and 'name',
              if the coin is found.
            - 'success' (bool): True if the API call was successful and the coin was found, False otherwise.
            - 'error' (str): Error message or additional information if the request fails or the coin is not found.
    """
    result = {
        'coin': None,
        'success': False,
        'error': None
    }

    if not name and not symbol:
        result['error'] = "Either name or symbol must be provided"
        return result

    try:
        response = requests.get(f'{BASE_URL}/coins/list', headers=headers, timeout=10)
        response.raise_for_status()  # Raises an HTTPError for bad responses

        all_coins = response.json()

        for coin in all_coins:
            if (name and coin['name'].lower() == name.lower()) and (symbol and coin['symbol'].lower() == symbol.lower()):
                result['coin'] = coin
                result['success'] = True
                break

        if not result['success']:
            result['error'] = "No exact match found for both name and symbol"

    except requests.exceptions.RequestException as e:
        result['error'] = f"Error in CoinGecko API request: {str(e)}"
    except ValueError as e:
        result['error'] = f"Error decoding JSON response: {str(e)}"
    except Exception as e:
        result['error'] = f"Unexpected error: {str(e)}"

    return result

# Example usage:
# result=get_coin_data(symbol='dot', name='Polkadot')
# print("result: ", result) 




























