import socket
import websockets
import asyncio
import time
from DB import DBHack as db
"""
managere ip$işlem şeklinde gönderilecek
"""
class Server:
    def __init__(self):
        self.connections = {}
        self.db = db()
        self.requests = asyncio.Queue()
        self.password = "pls wait a moment"
        self.ip = socket.gethostbyname(socket.gethostname())
    
    async def AdminServerManagment(self,websocket):
        print("admin")
        schoolName = await websocket.recv()
        work = await websocket.recv()
        print(work)
    
    async def AdminServer(self):
        async with websockets.serve(self.AdminServerManagment,self.ip,4848):
            print("admin menu server is now running")
            await asyncio.Future()

    async def ConnectManagerManager(self, websocket):
        try:
            print("Connection established")
            client_id = await websocket.recv()
            self.connections[client_id] = websocket

            while True:
                await websocket.recv()
                await asyncio.sleep(5)

        except websockets.ConnectionClosed:
            print(f"Connection lost: {client_id}")
        finally:
            self.connections.pop(client_id, None)


    async def ConnecManager(self):#Managmenta emir gödnerme server
        async with websockets.serve(self.ConnectManagerManager,self.ip,4545):
            print("sending server started")
            await asyncio.Future()


    async def ConnectionManager2(self,websocket):#tahtaların ip ve class adı alma kısmı managment
        print("maneging connections")
        data = await websocket.recv()
        data = data.replace(" ","").split("$")
        if f"{data[0]}_teacher_info".lower() in self.db.GetTables():
            if self.db.IsUsing(data[0],data[2],3):
                self.db.NewSmartBorad(data[0],data[2],data[1])
            else:
                self.db.UpdateData("board",data[0],ip = data[1],a = data[2])
        else:
            self.db.MakeNewSchool(data[0])
            self.db.NewSmartBorad(data[0],data[2],data[1])

    async def Connection2(self):#tahtaların ip ve class adı alma kısmı server
        async with websockets.serve(self.ConnectionManager2,self.ip,4444):
            print("listening Server started")
            await asyncio.Future()


    async def PasswordMaker(self):
        times = [f"{(i * 3) // 60:02}:{(i * 3) % 60:02}" for i in range(480)]
        lastTime = None
        while True:
            print("password maker")
            saat_dakika = time.strftime("%H:%M")
            if saat_dakika in times and saat_dakika != lastTime:
                lastTime = saat_dakika
                with open("sifre.txt", "r") as file:
                    password = file.read().replace(" ", "").split("\n")
                    self.password = password[times.index(saat_dakika)]
            await asyncio.sleep(5)

            
    async def WebSiteServerManagment(self,websocket):
        try:
            print("web is coming")
            data = await websocket.recv()
            data = data.split("$")
            if data[-1] == "login":
                feedback = self.db.GetWholeData(data[0],data[1])
                if feedback == "0":
                    websocket.send("False")
                else:
                    name = feedback[1]
                    password = feedback[2]
                    if name == data[1]:
                        if password == data[2]:
                            await websocket.send(name)
                        else:
                            await websocket.send("False")
                    else:
                        await websocket.send("False")
            if data[-1] == "givepass":
                await websocket.send(self.password)
            else:
                await self.requests.put(data)
        except Exception as e:
            print(f"an error accour : {e}")

    async def WebSiteServer(self):
        async with websockets.serve(self.WebSiteServerManagment,self.ip,4949):
            print("Website server is now running")
            await asyncio.Future()

    async def codeController(self):
        while True:
            await asyncio.sleep(1)
            print("1 second later")

    async def GetRequest(self):
        while True:
            data = await self.requests.get()  # Boşsa bekler, CPU harcamaz
            try:
                print("doing request")
                target = data[0]
                request = f"{self.db.GetIp(target, data[1]) if not self.db.IsUsing(data[0], data[1], 3) else (print('an error occurred') or '')}${data[2]}"
                if target in self.connections:
                    await self.connections[target].send(request)
                else:
                    print("Target not found")
            except Exception as e:
                print(f"An error occurred while processing the request: {e}")


    async def Main(self):
        tasks = [
            asyncio.create_task(self.GetRequest()),
            asyncio.create_task(self.ConnecManager()),
            asyncio.create_task(self.Connection2()),
            asyncio.create_task(self.AdminServer()),
            asyncio.create_task(self.WebSiteServer()),
            asyncio.create_task(self.PasswordMaker()),
            # asyncio.create_task(self.codeController()),
        ]
        await asyncio.gather(*tasks)
server = Server()
asyncio.run(server.Main())