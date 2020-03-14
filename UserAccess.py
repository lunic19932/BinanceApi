import asyncio
import base64
import json
from urllib.parse import urlencode

import ntplib
import requests
import websockets
from datetime import datetime
import constants
import hashlib
import hmac

from time import ctime


class UserAccess:
    ha = "f"



#a =bytes(constants.SECRET_KEY,'UTF-8')
#print (a)


header = {
    "X-MBX-APIKEY": constants.API_KEY,
}


param = dict()



request_url= 'https://api.binance.com/api/v3/myTrades?'
timestamp = int(datetime.now().timestamp() *1000)
querystring=urlencode({'symbol': 'ETHBTC', 'timestamp':timestamp})
signature= hmac.new(
    bytes(constants.SECRET_KEY, 'utf-8'),
    bytes(querystring, 'utf-8'),
    digestmod=hashlib.sha256
).hexdigest()
request_url+= querystring + '&signature=' + signature

resp = requests.get(request_url, headers=header).json()
print(request_url)
print(resp)
print(timestamp)
