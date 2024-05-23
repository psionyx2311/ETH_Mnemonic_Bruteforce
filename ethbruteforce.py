import random
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from bip_utils import Bip39SeedGenerator, Bip39MnemonicGenerator, Bip44, Bip44Coins, Bip44Changes
import time
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

# Constants
ETHERSCAN_API_KEY = 'INSERT_API_KEY_HERE'
OUTPUT_FILE = 'discovery.txt'
ETHERSCAN_API_URL = 'https://api.etherscan.io/api'
API_CALL_LIMIT = 100000
API_CALLS_PER_SECOND = 5

def generate_mnemonic():
    return Bip39MnemonicGenerator().FromWordsNumber(12)

def get_eth_address_from_mnemonic(mnemonic):
    seed_bytes = Bip39SeedGenerator(mnemonic).Generate()
    bip44_mst = Bip44.FromSeed(seed_bytes, Bip44Coins.ETHEREUM)
    bip44_acc = bip44_mst.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0)
    return bip44_acc.PublicKey().ToAddress(), bip44_acc.PrivateKey().Raw().ToHex()

def check_transaction_history(address):
    params = {
        'module': 'account',
        'action': 'txlist',
        'address': address,
        'startblock': 0,
        'endblock': 99999999,
        'sort': 'asc',
        'apikey': ETHERSCAN_API_KEY
    }
    
    session = requests.Session()
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
    session.mount('https://', HTTPAdapter(max_retries=retries))
    
    try:
        response = session.get(ETHERSCAN_API_URL, params=params)
        response.raise_for_status()
        data = response.json()
        # Verify the response structure and status
        if data['status'] == '1' and 'result' in data:
            return data['result']
    except requests.exceptions.RequestException as e:
        print(f"Error checking transaction history for address {address}: {e}")
    return []

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def process_address():
    mnemonic = generate_mnemonic()
    address, private_key = get_eth_address_from_mnemonic(mnemonic)
    
    transactions = check_transaction_history(address)
    return {
        "address": address,
        "mnemonic": mnemonic,
        "private_key": private_key,
        "transactions": transactions
    }

def main():
    api_call_count = 0
    last_checked = None

    with ThreadPoolExecutor(max_workers=API_CALLS_PER_SECOND) as executor:
        futures = []

        while api_call_count < API_CALL_LIMIT:
            if len(futures) < API_CALLS_PER_SECOND:
                futures.append(executor.submit(process_address))
                time.sleep(1 / API_CALLS_PER_SECOND)  # Spread out the calls slightly
            else:
                for future in as_completed(futures):
                    result = future.result()
                    api_call_count += 1
                    last_checked = result

                    clear_terminal()
                    print(f'Wallets checked: {api_call_count}\n')
                    print(f'Public Key: {last_checked["address"]}')
                    print(f'Mnemonic: {last_checked["mnemonic"]}')
                    print(f'Private Key: {last_checked["private_key"]}\n')

                    if last_checked['transactions']:
                        with open(OUTPUT_FILE, 'a') as f:
                            f.write(f'Mnemonic: {last_checked["mnemonic"]}\n')
                            f.write(f'Address: {last_checked["address"]}\n')
                            f.write(f'Private Key: {last_checked["private_key"]}\n\n')
                            #f.write(f'Transactions: {last_checked["transactions"]}\n\n')
                        print(f'Found transactions for address {last_checked["address"]}. Details saved to {OUTPUT_FILE}')
                        input("Press Enter to continue generating/scanning ETH addresses.")
                    else:
                        print(f'No transactions found for address {last_checked["address"]}')

                    futures.remove(future)
                    break  # Exit the inner loop to submit more tasks if needed

    print("100k daily limit reached or address found.")

if __name__ == '__main__':
    main()
