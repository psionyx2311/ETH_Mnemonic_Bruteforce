# ETH_Mnemonic_Bruteforce

# Ethereum Wallet Discovery Tool

This project is a Python script designed to generate Ethereum wallets, check their transaction histories using the Etherscan API, and save any wallets with transactions to a file. The script leverages concurrent processing to handle multiple API calls efficiently.

## Features

***Etherscan.io API key required, sign up for free at https://etherscan.io***

- **Mnemonic Generation**: Uses the `bip_utils` library to generate 12-word mnemonics.
- **Wallet Derivation**: Derives Ethereum addresses and private keys from the generated mnemonics.
- **Transaction History Check**: Queries the Etherscan API to check the transaction history of each generated address.
- **Concurrency**: Utilizes `ThreadPoolExecutor` for concurrent processing of API calls.
- **Error Handling**: Implements retries for API calls to handle rate limiting and transient errors.
- **Output**: Saves the details of wallets with transaction histories to a text file called discovery.txt.

## Dependencies

- Python 3.x
- `requests` library
- `bip_utils` library

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/ETH_Mnemonic_Bruteforce.git
    cd ETH_Mnemonic_Bruteforce
    ```

2. Install the required Python packages:
    ```sh
    pip install -r requirements.txt

    (pip3 for Linux)
    ```

## Usage

1. Set your Etherscan API key in the `ETHERSCAN_API_KEY` variable within the ethbruteforce.py file.
2. Run the script:
    ```sh
    python ethbruteforce.py

    (python3 for Linux)
    ```

## Configuration

- `ETHERSCAN_API_KEY`: Your Etherscan API key (keep the '' around your API key).
- `OUTPUT_FILE`: The file where wallet details will be saved (`discovery.txt` by default).
- `ETHERSCAN_API_URL`: The Etherscan API endpoint.
- `API_CALL_LIMIT`: Maximum number of API calls to make (set to 100,000 by default).
- `API_CALLS_PER_SECOND`: Rate limit for API calls (set to 5 calls per second by default).

## How It Works

1. **Mnemonic Generation**: The script generates a 12-word mnemonic using `Bip39MnemonicGenerator`.
2. **Wallet Derivation**: The mnemonic is used to derive the Ethereum address and private key.
3. **Transaction Check**: The script checks the transaction history of the derived address using the Etherscan API.
4. **Concurrency Management**: Multiple API calls are handled concurrently, respecting the rate limit.
5. **Output**: If transactions are found, the wallet details are saved to `discovery.txt`.

## Note

- Ensure you respect the API call limits set by Etherscan to avoid being banned.
- This script is for educational purposes only. Use responsibly and ethically.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contributions

Contributions are welcome! Feel free to open an issue or submit a pull request.
