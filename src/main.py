# core
import argparse
import json
import logging
import os
import sched
import subprocess
import sys
import time

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

initLogger()
logger.info (f'Current dir: {os.getcwd()}')
parseArgs()

sch = sched.scheduler(time.time, time.sleep)
sch.enter(INTERVAL_RUN, 1, doCheck)
sch.run()
