import json

import websockets

import IObserver


class BinanceClient:
    isReceivingData: bool = False
    observer: IObserver

    async def startStream(self, streamType: str):
        self.isReceivingData = True
        async with websockets.connect(streamType) as socket:
            await self.subscribeTicker(socket)
            await self.receiveTicker(socket)

    async def subscribeTicker(self, socket: websockets.client):
        subscribe = dict({"method": "LIST_SUBSCRIPTIONS"}, {"id": 3})
        await socket.send(json.dumps(subscribe))

    async def receiveTicker(self, socket: websockets.client):
        while self.isReceivingData:
            resp = await socket.recv()
            self.observer.handleResponse(resp)
