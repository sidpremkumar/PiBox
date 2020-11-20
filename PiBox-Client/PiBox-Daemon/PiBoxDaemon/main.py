"""The Main entrypoint to the daemon
TODO: Make it to it prompts a setup wizard"""
import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

import threading
import queue

from PiBoxDaemon.config import DIRECTORY
from PiBoxDaemon.Daemon.fileHandler import FileHandler
from PiBoxDaemon.Daemon.sync import syncDirectory
from PiBoxDaemon.Daemon.queueHandler import queueHandlerMain

def main():
    # First run a sync between the server and the client
    print("Starting sync...")
    syncDirectory(".")
    print("Done syncing!")
    
    eventQueue = queue.Queue()

    # Start the observer
    fileObserverProcess = start_observer(eventQueue)

    # Start our queueHandler
    queueHandlerProcess = threading.Thread(target=queueHandlerMain, args=(eventQueue,))
    
    # Start our processes
    fileObserverProcess.start()
    queueHandlerProcess.start()

    try:
        # Sleep forever
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        fileObserverProcess.stop()
        fileObserverProcess.join()
        queueHandlerProcess.join()
    
    


def start_observer(eventQueue):
    """Code to start our observer"""
    # Create our observer
    observer = Observer()

    # Define our event_handler
    event_handler = FileHandler(eventQueue)

    # Create and start our listener
    observer.schedule(event_handler, DIRECTORY, recursive=True)
    
    # Return the observer
    return observer