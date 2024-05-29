import asyncio
from Configuration import config
from logger import log, error


async def client_handler(reader, writer):
    pass


async def main():
    host = config.get("ip", "0.0.0.0")
    port = config.get("port", 1024)
    server = await asyncio.start_server(client_handler, host=host, port=port, start_serving=False)
    log("Server created!")
    async with server:
        log("Started serving!")
        await server.serve_forever()

asyncio.run(main())
