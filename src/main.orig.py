# core
import argparse
from contextlib import asynccontextmanager
import json
import logging
import os
import sched
import subprocess
import sys
import time
from threading import Thread

# community
import fastapi


INTERVAL_RUN = 3

logger = None

def initLogger():
  global logger
  logger = logging.getLogger(__name__)
  logging.basicConfig(stream=sys.stdout, 
    format='%(asctime)s %(filename)s:%(levelname)s - %(message)s',
    level=logging.DEBUG)
  # hStream = logging.StreamHandler(sys.stdout)
  # logger.addHandler(hStream)

def ping(host):
  return subprocess.run(['ping', '-c', '1', host], stdout=subprocess.DEVNULL).returncode == 0

def parseArgs():
  parser = argparse.ArgumentParser()
  args = parser.parse_args()

def doCheck():
  logger.info ('checking...')
  resp = subprocess.run(['vnstat','--json'], capture_output=True)
  try:
    data = json.loads(resp.stdout.decode('utf-8'))
    logger.debug(json.dumps(data, indent=2))
  except Exception as e:
    logger.error(e)

  sch.enter(INTERVAL_RUN, 1, doCheck)

@asynccontextmanager
async def lifespan(app: fastapi.FastAPI):
  # service startup
  logger.info('Starting scheduler')
  thread = Thread(target=sch.run)
  thread.start()

  logger.info('Starting service')
  yield
  # service shutdown
  logger.info('Stopping service')

initLogger()
logger.info (f'Current dir: {os.getcwd()}')
parseArgs()

sch = sched.scheduler(time.time, time.sleep)
sch.enter(INTERVAL_RUN, 1, doCheck)

app = fastapi.FastAPI(lifespan=lifespan)
