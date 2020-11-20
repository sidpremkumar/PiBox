import queue
import threading
import time

from PiBoxServer.server import startServer, eventQueue
from PiBoxServer.requestHandler import requestHandlerMain

def main():
    # Create our server in one thread
    serverProcess = threading.Thread(target=startServer, args=())

    # Create our requestHandler thread
    requestHandlerProcess = threading.Thread(target=requestHandlerMain, args=(eventQueue,))

    # Start our processes
    serverProcess.start()
    requestHandlerProcess.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        serverProcess.join()
        requestHandlerProcess.join()
