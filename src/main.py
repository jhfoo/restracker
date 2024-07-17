# core
import argparse
from contextlib import asynccontextmanager
import json
import logging
import os
import sys
import time

# community
import fastapi

# custom
import MyScheduler
import util
import glob

logger = logging.getLogger(__name__)
util.initLogger(logger)

def parseArgs():
  parser = argparse.ArgumentParser()
  args = parser.parse_args()



@asynccontextmanager
async def lifespan(app: fastapi.FastAPI):
  # service startup
  logger.info('Starting scheduler')
  MyScheduler.start()

  logger.info('Starting service')
  yield
  # service shutdown
  logger.info('Stopping service')

logger.info (f'Current dir: {os.getcwd()}')
# parseArgs()

with glob.MyValueLock:
  glob.MyValue = 100
app = fastapi.FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
  with glob.MyValueLock:
    glob.MyValue = time.time()
  return {"Hello": glob.MyValue}
