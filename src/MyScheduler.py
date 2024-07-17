# core
import logging
import sched
import subprocess
import time
from threading import Thread

# community
import yaml
try:
  from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
  from yaml import Loader, Dumper

# custom
import util
import glob

INTERVAL_RUN = 3
FILE_APP = 'conf/restracker.yaml'

logger = logging.getLogger(__name__)
AppConfig = {
  'hosts': []
}

util.initLogger(logger)
logger.debug(f"__file__: {__file__}")

def loadConfig():
  with open(FILE_APP, 'r') as stream:
    global AppConfig 
    AppConfig = yaml.load(stream, Loader=Loader)

def ping(host):
  return subprocess.run(['ping', '-c', '1', host], stdout=subprocess.DEVNULL).returncode == 0

def doCheck():
  logger.info ('checking...')
  for host in AppConfig['hosts']:
    isHostAlive = ping (host['addr'])
    print (f"Host {host['name']}: {isHostAlive}")
  print (f"gMyValue: {glob.MyValue}")
  time.sleep(10)
  # resp = subprocess.run(['vnstat','--json'], capture_output=True)
  # try:
  #   data = json.loads(resp.stdout.decode('utf-8'))
  #   logger.debug(json.dumps(data, indent=2))
  # except Exception as e:
  #   logger.error(e)

  sch.enter(INTERVAL_RUN, 1, doCheck)

def start():
  loadConfig()
  thread = Thread(target=sch.run)
  thread.start()

sch = sched.scheduler(time.time, time.sleep)
sch.enter(INTERVAL_RUN, 1, doCheck)
