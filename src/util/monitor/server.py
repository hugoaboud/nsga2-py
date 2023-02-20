import asyncio
import websockets
from websockets import client as wsclient
from multiprocessing import Queue
from queue import Empty
from src.util.log import Log

PORT = 5642 # nSGA2

class MonitorServer:

    def __init__(self, queue):
        Log.logger.info("[MonitorServer] Starting...")
        self.queue = queue
        self.client_queues = []
        self.bus_task = None

    async def handler(self, ws):
        Log.logger.info('[MonitorServer] New client connected')
        queue = Queue()
        self.client_queues.append(queue)
        while True:
            try:
                data = queue.get_nowait()
                await ws.send(data)
            except Empty:
                await asyncio.sleep(0.1)
            except Exception as e:
                Log.logger.error('[MonitorServer] Client disconnected')
                Log.logger.error('\t' + str(e))
                break
        self.client_queues.remove(queue)

    async def bus(self):
        while True:
            try:
                data = self.queue.get_nowait()
                for client_queue in self.client_queues:
                    client_queue.put(data)
            except Empty:
                await asyncio.sleep(0.1)

    async def run(self):
        Log.logger.info("[MonitorServer] Online")
        while True:
            try:
                bus_task = asyncio.create_task(self.bus())
                async with websockets.serve(self.handler, "", PORT):
                    await bus_task
            except Exception as e:
                Log.logger.error('[MonitorServer] Tick server is down, reopening...')
                Log.logger.error('\t' + str(e))

    @classmethod
    def process(self, queue):
        server = MonitorServer(queue)
        asyncio.run(server.run())

class MonitorClient:

    def __init__(self, server_ip, queue):
        Log.logger.info('[MonitorClient] Starting...')
        self.server_ip = server_ip
        self.queue = queue
        pass

    async def connect(self):
        Log.logger.info('[MonitorClient] Connecting...')
        self.connection = await wsclient.connect(f"ws://{self.server_ip}:{PORT}")
        if self.connection.open:
            Log.logger.info('[MonitorClient] Connected')

    async def receiveMessage(self, connection):
        while True:
            data = await connection.recv()
            self.queue.put(data)
            
    async def run(self):
        while (True):
            try:
                await self.connect()
                await self.receiveMessage(self.connection)
            except Exception as e:
                Log.logger.error('[MonitorClient] Connection with server closed, reopening...')
                Log.logger.error('\t' + str(e))

    @classmethod
    def process(self, server_ip, queue):
        client = MonitorClient(server_ip, queue)
        asyncio.run(client.run())