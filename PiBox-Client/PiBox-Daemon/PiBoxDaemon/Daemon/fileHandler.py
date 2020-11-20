"""File watcher handler class"""
from watchdog.events import FileSystemEventHandler, FileDeletedEvent, DirDeletedEvent, FileCreatedEvent, DirCreatedEvent
import requests

from datetime import datetime, timedelta
from urllib.parse import urljoin
import os

from PiBoxDaemon.config import DIRECTORY, SERVER_URL, TO_IGNORE
from PiBoxDaemon.Daemon.sync import syncDirectory

class FileHandler(FileSystemEventHandler):
    def __init__(self, eventQueue):
        self.eventQueue = eventQueue

    def on_modified(self, event):
        print(f"Modified: {event.src_path}")
        self.eventQueue.put(event)

    def on_created(self, event):
        print(f"Created: {event.src_path}")
        self.eventQueue.put(event)

    def on_deleted(self, event):
        print(f"Deleted: {event.src_path}")
        self.eventQueue.put(event)

    def on_moved(self, event):
        print(f"Moved: {type(event)}")
        self.eventQueue.put(event)

def uploadFile(files, path):
    """Helper function to upload a file"""
    responseUpload = requests.post(urljoin(SERVER_URL, "uploadFile"), files=files, data={'path': path})
    if (responseUpload.status_code not in [200, 201]):
        print(f"Error uploading {path}: {responseUpload.text}")