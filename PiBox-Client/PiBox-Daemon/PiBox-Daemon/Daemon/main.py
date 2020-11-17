"""This is the actual Daemon Program that will be run"""
import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

from handler import FileHandler
from config import DIRECTORY
from sync import syncDirectory

def main(): 
    """Main Entrypoint into the Daemon"""
    # First run a sync between the server and the client
    syncDirectory(DIRECTORY)
    
    # Create our observer
    observer = Observer()

    # Define our event_handler
    event_handler = FileHandler()

    # Create and start our listener
    observer.schedule(event_handler, DIRECTORY, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()



if __name__ == "__main__":
    main()