# core
import logging
import time

# community
from fastapi import APIRouter, WebSocket
from fastapi.responses import PlainTextResponse
from prometheus_client import Gauge, CollectorRegistry, generate_latest

# custom
import glob
import util

logger = logging.getLogger(__name__)
util.initLogger(logger)

router = APIRouter()

@router.get("/")
def read_root():
  with glob.MyValueLock:
    glob.MyValue = time.time()
  return {"Hello": glob.MyValue}

@router.get('/prometheus', response_class=PlainTextResponse)
def getPrometheus():
  registry = CollectorRegistry()

  HostGauge = Gauge('UpDown', 'Host up/down status', ['host', 'group'], registry = registry)
  with glob.HostLock:
    for host in glob.hosts.values():
      HostGauge.labels(host = host['name'], group = host['group']).set(host['isUp'])

  return generate_latest(registry)

@router.websocket('/ws')
async def websocket_endpoint(websocket: WebSocket):
  await websocket.accept()
  while True:
    msg = websocket.receive_text()
    logger.debug(f"websocket received: {msg}")
    await websocket.send_text(glob.MyValue)
    # await websocket.close()