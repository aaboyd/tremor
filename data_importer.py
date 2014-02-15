from twisted.internet import reactor
from twisted.internet.task import LoopingCall

import time
import traceback

def fetch_data():
    print 'Time : ', time.time()

def execute_fetch(*args, **kwargs):
    try:
        fetch_data()
    except Exception:
        print(traceback.format_exc())

    reactor.callLater(10, execute_fetch);

def start():
    print 'Running fetch in 10 : ', time.time()
    reactor.callLater(10, execute_fetch);
