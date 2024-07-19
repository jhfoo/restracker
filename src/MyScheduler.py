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

  with glob.HostLock:
    for host in AppConfig['hosts']:
      glob.hosts[host['name']] = {
        'addr': host['addr'],
        'name': host['name'],
        'isUp': False
      }

def ping(host):
  return subprocess.run(['ping', '-c', '1', host], stdout=subprocess.DEVNULL).returncode == 0

def doCheck():
  logger.info ('checking...')
  for HostId in glob.hosts:
    host = glob.hosts[HostId]
    try:
      isHostAlive = ping (host['addr'])
      if isHostAlive != host['isUp']:
        logger.info (f"New state for {host['name']}: {isHostAlive}")
        host['isUp'] = isHostAlive
    except Exception as err:
      logger.warn (f"WARNING for {host['name']}: {err}")

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
