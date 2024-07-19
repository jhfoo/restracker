# core
import logging
import time

# community
from fastapi import APIRouter
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

  HostGauge = Gauge('UpDown', 'Host up/down status', ['host'], registry = registry)
  with glob.HostLock:
    for host in glob.hosts.values():
      HostGauge.labels(host = host['name']).set(host['isUp'])

  return generate_latest(registry)

