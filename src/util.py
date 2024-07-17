# core
import logging
import sys

def initLogger(logger):
  logging.basicConfig(stream=sys.stdout, 
    format='%(asctime)s %(filename)s:%(levelname)s - %(message)s',
    level=logging.DEBUG)
  # hStream = logging.StreamHandler(sys.stdout)
  # logger.addHandler(hStream)