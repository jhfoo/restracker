# core
import argparse
import logging
import os
import sched
import sys
import time

INTERVAL_RUN = 3

def initLogger():
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
  logging.info ('checking...')
  sch.enter(INTERVAL_RUN, 1, doCheck)

initLogger()
logging.info (f'Current dir: {os.getcwd()}')
parseArgs()

sch = sched.scheduler(time.time, time.sleep)
sch.enter(INTERVAL_RUN, 1, doCheck)
sch.run()
