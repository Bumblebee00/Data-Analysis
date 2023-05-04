import requests
import json

hashrate = requests.get('https://api.blockchain.info/stats').json()['hash_rate']
print(f"Current hashrate: {round(hashrate/10**9, 2)} TH/s")