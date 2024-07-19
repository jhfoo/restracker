# core
import threading

MyValue = 10
MyValueLock = threading.Lock()

hosts = {}
HostLock = threading.Lock()