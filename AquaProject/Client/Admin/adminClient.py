import websockets
import asyncio
class Client:
    def __init__(self):
        pass

    async def SendRequest(self,message = "working"):
        async with websockets.connect("ws://localhost:4848") as websocket:
            await websocket.send("Fcal")
            await websocket.send(message)
    async def Main(self):
        await asyncio.gather(self.SendRequest())

cl = Client()
asyncio.run(cl.Main())