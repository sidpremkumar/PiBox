"""Queue watcher, will pull from the queue and deal with events as they come"""
import time

from watchdog.events import FileSystemEventHandler, FileDeletedEvent, DirDeletedEvent, FileCreatedEvent, DirCreatedEvent, DirModifiedEvent, FileModifiedEvent, FileMovedEvent, DirMovedEvent

from PiBoxDaemon.Daemon.events import on_moved, on_created, on_deleted, on_modify

def queueHandlerMain(eventQueue):
    # Build our queue mapping object
    queueHandler = QueueHandler(eventQueue)

    while True:
        if (eventQueue.qsize() != 0):
            # There is an event to consume
            event = eventQueue.get()

            # Call the appropriate function
            if (type(event) == DirModifiedEvent or type(event) == FileModifiedEvent):
                queueHandler.handle_on_modify(event)
            elif (type(event) == DirCreatedEvent or type(event) == FileCreatedEvent):
                queueHandler.handle_on_create(event)
            elif (type(event) == DirDeletedEvent or type(event) == FileDeletedEvent):
                queueHandler.handle_on_delete(event)
            elif (type(event) == DirMovedEvent or type(event) == FileMovedEvent):
                queueHandler.handle_on_moved(event)
            else:
                print(f"Unknown event encountered {event}")

class QueueHandler():
    def __init__(self, eventQueue):
        self.eventQueue = eventQueue
    
    def handle_on_create(self, event):
        on_created(event)

    def handle_on_delete(self, event):
        on_deleted(event)

    def handle_on_modify(self, event):
        on_modify(event)

    def handle_on_moved(self, event):
        on_moved(event)
