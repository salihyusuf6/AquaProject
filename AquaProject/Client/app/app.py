import websockets
import threading
import asyncio
import subprocess
import socket
import time

class App:
    def __init__(self):
        self.ip = socket.gethostbyname(socket.gethostname())
        self.manager = socket.gethostbyname(socket.gethostname())
        self.className = self.getname()
        self.isAppOpen = False
        self.password = ""
        self.Setİp()

    def Setİp(self):
        with open(r"release/ip.txt", "w", encoding="utf-8") as file:
            file.write(socket.gethostbyname(socket.gethostname()))
    def getname(self):
        while True:
            try:
                with open(r"release/sinif.txt", "r", encoding="utf-8") as file:
                    return file.read().replace(" ", "").replace("/", "-")
            except:
                continue

    def ListenLockScreen(self):
        port = 3854
        host = socket.gethostbyname(socket.gethostname())
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((host, port))
        server_socket.listen(24)
        print(f"Sunucu başlatıldı, {host}:{port} üzerinde dinleniyor...")

        def handle_client(client_socket, client_address):
            print(f"Yeni bağlantı: {client_address}")
            data = client_socket.recv(1024).decode("utf-8")
            if data:
                print(f"Alınan şifre: {data}")
                if str(data) == str(self.password):
                    self.OpenScreen()
            client_socket.close()

        try:
            while True:
                client_socket, client_address = server_socket.accept()
                client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
                client_thread.start()
        finally:
            server_socket.close()

    async def TimeController(self):
        sonSaat = None
        while True:
            while not self.isAppOpen:
                with open("saat.txt", "r") as file:
                    saatler = file.read().split("\n")
                    saat_dakika = time.strftime("%H:%M")
                    for i in range(len(saatler)):
                        if saat_dakika == saatler[i] and saatler[i] != sonSaat:
                            sonSaat = saatler[i]
                            self.LockScreen()
                await asyncio.sleep(2)

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

    def LockScreen(self):
        if not self.isAppOpen:
            self.isAppOpen = True
            subprocess.run("cd release && Aqua.exe",shell=True)
            print("close")
    def OpenScreen(self):
        if self.isAppOpen:
            self.isAppOpen = False
            subprocess.run('taskkill /IM "Aqua.exe" /F', shell=True)
            print("open")

    async def ConnectionManager(self, websocket):
        print("logined here")
        work = await websocket.recv()        
        if work == "open":
            self.OpenScreen()
        elif work == "close":
            thread = threading.Thread(target=self.LockScreen, daemon=True)
            thread.start()
        elif work == "clear":
            with open(r"release/duyuru.txt", "w", encoding="utf-8") as file:
                file.write("")
            with open(r"release/isDuyuru.txt", "w", encoding="utf-8") as file:
                file.write("0")
        else:
            print("else")
            with open(r"release/duyuru.txt", "w", encoding="utf-8") as file:
                file.write(work)
            with open(r"release/isDuyuru.txt", "w", encoding="utf-8") as file:
                file.write("1")

    async def Connection(self):
        async with websockets.serve(self.ConnectionManager, self.ip, 4747):
            print("Server started")
            await asyncio.Future()

    async def HandShake(self):
        async with websockets.connect(f"ws://{self.manager}:4646") as websocket:
            await websocket.send(self.ip)
            await websocket.send(self.className)
            print("data sended")

    def start_async_tasks(self, loop):
        """Thread içinde çalışacak olan async fonksiyonları başlatır."""
        asyncio.set_event_loop(loop)
        loop.run_forever()

    async def Main(self):
        loop = asyncio.new_event_loop()
        threading.Thread(target=self.start_async_tasks, args=(loop,), daemon=True).start()
        threading.Thread(target=self.LockScreen,daemon=True).start()
        asyncio.run_coroutine_threadsafe(self.TimeController(), loop)
        asyncio.run_coroutine_threadsafe(self.PasswordMaker(), loop)
        threading.Thread(target=self.ListenLockScreen, daemon=True).start()
        await asyncio.gather(self.HandShake(), self.Connection())


app = App()
asyncio.run(app.Main())