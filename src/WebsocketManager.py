# core
import logging

# custom
import util

logger = logging.getLogger(__name__)
util.initLogger(logger)


clients = []

async def addClient(websocket):
  await websocket.accept()

  global clients
  clients.append(websocket)

async def broadcast(message:str):
  global clients

  # logger.debug(f"client count: {len(clients)}")
  for client in clients:
    await client.send_text(message)

def removeClient(websocket):
  global clients
  clients.remove(websocket)

  return len(clients)