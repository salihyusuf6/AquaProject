import websockets
import asyncio
import threading
import socket

class Manager:
    def __init__(self):
        self.schoolName = "Fevzi"
        self.requests = asyncio.Queue()
        self.ip = "185.240.104.86"


    async def Listen(self):#ana sunucudan emir alma
        async with websockets.connect(f"ws://{self.ip}:4545") as websocket:
            await websocket.send(self.schoolName)
            while True:
                await websocket.send("")
                await self.requests.put(await websocket.recv())
                print("request geted")


    async def Send(self,ip,className):#ana sunucuya tahta bilgilerini gönderme
        async with websockets.connect(f"ws://{self.ip}:4444") as websocket:
            await websocket.send(f"{self.schoolName}${ip}${className}")


    async def HandShakeManager(self,websocket):#tahtalardan bilgileri alma manager
        ip = await websocket.recv()
        className = await websocket.recv()
        print(f"Connection established with {ip} {className}")
        await self.Send(ip,className)


    async def HandShake(self):#Tahtlardan bilgileri alma server
        async with websockets.serve(self.HandShakeManager,socket.gethostbyname(socket.gethostname()),4646):
            print("Server started")
            await asyncio.Future()

    async def AsncRun(self,requset0,request1):
        print(requset0)        
        async with websockets.connect(f"ws://{requset0}:4747") as websocket:
            print("here")
            await websocket.send(request1)
            print("sended")

    def RunThread(self,requset0,request1):
        asyncio.run(self.AsncRun(requset0,request1))

    async def RequestManager(self):#sunucudan gelen isteklerin yönetimi
        while True:
                request = await self.requests.get()
                request = request.replace(" ","").split("$")
                print("doing request")
                if request[0] == "message":
                    print(request[1])
                try:
                    threading.Thread(target=self.RunThread,daemon=True,args=(request[0],request[1])).start()
                    print("request doed")
                except:
                    print("An error occurred while connecting to the smart board.")


    async def Main(self):
        await asyncio.gather(self.Listen(),self.RequestManager(),self.HandShake())


manager = Manager()
asyncio.run(manager.Main())