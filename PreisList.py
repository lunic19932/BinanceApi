import websockets
import requests
import constants
import json
import asyncio

class PreisList:
    liste: dict
    symbols = []
    #socket: websockets.WebSocketClientProtocol
    def __init__(self):
        self.liste=dict()
        self.getData()
        #self.printSymbols()

    def getData(self):
        resp = requests.get(constants.TICKER24_URL).json()
        for re in resp:
            symbol=re.get("symbol")
            if symbol.endswith("BTC") and (float(re.get("lastPrice"))!=0):
                self.symbols.append(symbol)
                self.liste.update({symbol:float(re.get("lastPrice"))})



    def printSymbols(self):
        print(self.symbols)

    async def startStream(self):
        async with websockets.connect(constants.MARKETTICKER_STREAM) as socket:
            await self.sendTicker(socket)
            await self.receiveTicker(socket)

    async def sendTicker(self,socket):
        listening=dict()
        listening.update({"method" : "LIST_SUBSCRIPTIONS"})
        listening.update({"id": 3})
        param=json.dumps(listening)
        await socket.send(param)

    async def receiveTicker(self,socket):
        while True:
            resp=await socket.recv()
            re=json.loads(resp)
            for i in re:
                if (type(i) is dict) and (i.get("s").endswith("BTC")):
                    self.liste.update({i.get("s"): float(i.get("c"))})


                #if symbol.endswith("BTC"):
                #
            print(self.liste)


list=PreisList()
asyncio.get_event_loop().run_until_complete(list.startStream())
