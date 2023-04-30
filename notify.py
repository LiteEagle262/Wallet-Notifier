import requests, time, webbrowser, sys, os.path, json
from plyer import notification
import tkinter as tk
from datetime import datetime, timedelta
from tkinter import messagebox
import pyperclip

#--CAN EDIT BELOW THIS LINE--#
copytoclipboard = False #auto copy txid of transaction to clipboard
btc_address = 'bc1qvycuvdsrx5zatr7qvzlsnkej0d65fpsmrqv3m7' #only crypto supported so far
# eth_address = '0x4e37e749a61f22e5b64C625D41830416E043D829'
# xmr_address = '4AKraeGnLtgcaG1utNBVaBbVMRj1UotzDTbx1CiRTLgebxLhUiwYk8bfKzwdnG5uxDfUCDhnoiw58jgDP7AfRYVdFFtk8QN'
# doge_address = 'DD1WLdFoWk6BKcHaegVvhgfH5xkkfuvrjc'
# ltc_address = 'LS9L28s8xbBNYzsWgBq3jxpVmprBH5Ep19'
#--CAN EDIT ABOVE THIS LINE--#

def sendtoast(coin):
    if coin == "btc":
        notification_title = 'BTC incoming transaction detected'
        notification_message = f'You have received a new BTC transaction at {btc_address}!'
        response = requests.get("https://pngimg.com/d/bitcoin_PNG48.png")
        img = Image.open(BytesIO(response.content))
        notification.notify(
            title=notification_title,
            message=notification_message,
            app_icon=img,
            timeout=10,
            toast=True,
        )
    elif coin == "eth":
        notification_title = 'ETH incoming transaction detected'
        notification_message = f'You have received a new ETH transaction at {eth_address}!'
        response = requests.get("https://cloudfront-us-east-1.images.arcpublishing.com/coindesk/ZJZZK5B2ZNF25LYQHMUTBTOMLU.png")
        img = Image.open(BytesIO(response.content))
        notification.notify(
            title=notification_title,
            message=notification_message,
            app_icon=img,
            timeout=10,
            toast=True,
        )
    elif coin == "xmr":
        notification_title = 'XMR incoming transaction detected'
        notification_message = f'You have received a new XMR transaction at {xmr_address}!'
        response = requests.get("https://cdn4.iconfinder.com/data/icons/crypto-currency-and-coin-2/256/monero_xmr-512.png")
        img = Image.open(BytesIO(response.content))
        notification.notify(
            title=notification_title,
            message=notification_message,
            app_icon=img,
            timeout=10,
            toast=True,
        )
    elif coin == "doge":
        notification_title = 'DOGE incoming transaction detected'
        notification_message = f'You have received a new DOGE transaction at {doge_address}!'
        response = requests.get("https://upload.wikimedia.org/wikipedia/en/d/d0/Dogecoin_Logo.png")
        img = Image.open(BytesIO(response.content))
        notification.notify(
            title=notification_title,
            message=notification_message,
            app_icon=img,
            timeout=10,
            toast=True,
        )
    elif coin == "ltc":
        notification_title = 'LTC incoming transaction detected'
        notification_message = f'You have received a new LTC transaction at {ltc_address}!'
        response = requests.get("https://s3.coinmarketcap.com/static/img/portraits/630c5fcaf8184351dc5c6ee5.png")
        img = Image.open(BytesIO(response.content))
        notification.notify(
            title=notification_title,
            message=notification_message,
            app_icon=img,
            timeout=10,
            toast=True,
        )

transactions_file = 'transactions.txt'

def btc():
    url = f"https://blockstream.info/api/address/{btc_address}/txs"
    response = requests.get(url)
    transactions = json.loads(response.content)
    with open(transactions_file, 'r') as f:
        previous_transactions = f.read().splitlines()
    latest_tx = transactions[0]
    tx_time = datetime.utcfromtimestamp(latest_tx['status']['block_time'])
    time_diff = datetime.utcnow() - tx_time
    if time_diff < timedelta(minutes=2):
        if latest_tx['txid'] not in previous_transactions:
            previous_transactions.append(latest_tx['txid'])
            with open(transactions_file, 'a') as f:
                f.write(latest_tx['txid'] + "\n")
                if copytoclipboard:
                    pyperclip.copy(latest_tx['txid'])
                print(f"BTC transaction detected at {address}")
                sendtoast("btc")

if not os.path.exists(transactions_file):
    open(transactions_file, 'w').close()

root = tk.Tk()
root.withdraw()
messagebox.showinfo(title="Crypto Notifier", message="Crypto Notifier now running in the background!")
while True:
    try:
        btc()
        time.sleep(20)
    except Exception as e:
        print(f"Error: {e}")
        messagebox.showerror(title="Error", message="An error has occurred please restart if this doesnt go away.\n\nError: " + str(e))
        time.sleep(10)