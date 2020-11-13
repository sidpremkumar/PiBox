"""Handler class for our Daemon"""
from watchdog.events import FileSystemEventHandler, FileDeletedEvent, DirDeletedEvent
import requests

from datetime import datetime, timedelta
from urllib.parse import urljoin
import os

from config import DIRECTORY, SERVER_URL

class FileHandler(FileSystemEventHandler):
    def __init__(self):
        # To prevent events being called twice
        self.last_modified = datetime.now()

    def on_modified(self, event):
        # Always check for last modified
        if checkLastModified(self.last_modified):
            return
        else:
            self.last_modified = datetime.now()
        print(f"modifing {event.src_path}")
    
    def on_created(self, event):
        # Always check for last modified
        if checkLastModified(self.last_modified):
            return
        else:
            self.last_modified = datetime.now()
        
        # Extract our path
        fullPath = os.path.relpath(event.src_path, DIRECTORY) # i.e. sid/somefolder/test.txt
        basePath = os.path.dirname(fullPath) # i.e. sid/somefolder

        # Make a call to our server to check if the file exists/last modified time
        responseFileLastModified = requests.get(urljoin(SERVER_URL, "retriveFileLastModified"), data={'path': fullPath})

        if (responseFileLastModified.status_code == 400):
            # The file does not exist. Grab the base path
            files = {'file': open(event.src_path, 'rb')}

            # Upload the file
            uploadFile(files, basePath)
        elif (responseFileLastModified.status_code == 200):
            # We have the file uploaded, compare the timestamps to see if we need to reupload
            timestamp = responseFileLastModified.json()['timestamp']
            if (timestamp < os.path.getmtime(event.src_path)):
                # We need to reupload. Grab the base path
                files = {'file': open(event.src_path, 'rb')}

                # Upload the file
                uploadFile(files, basePath)

        print(f"Uploaded/Updated {fullPath}")

    def on_deleted(self, event):
        # Always check for last modified
        if checkLastModified(self.last_modified):
            return
        else:
            self.last_modified = datetime.now()
        
        if (type(event) == FileDeletedEvent):
            # Extract our path
            fullPath = os.path.relpath(event.src_path, DIRECTORY) # i.e. sid/somefolder/test.txt
            
            # Make our call to delete
            responseDelete = requests.post(urljoin(SERVER_URL, "deleteFile"), data={'path': fullPath})

            if responseDelete.status_code == 400:
                print("The file already does not exist on the server!")
            elif (responseDelete.status_code == 500):
                print("Error deleting the file")
            else:
                print(f"Deleted file {fullPath}")
        elif (type(event) == DirDeletedEvent):
            # Extract our path
            fullPath = os.path.relpath(event.src_path, DIRECTORY) # i.e. sid/

            # Make our call to delete
            responseDelete = requests.post(urljoin(SERVER_URL, "deleteFolder"), data={'path': fullPath})

            if responseDelete.status_code == 400:
                print("The file already does not exist on the server!")
            elif (responseDelete.status_code == 500):
                print("Error deleting the file")
            else:
                print(f"Deleted file {fullPath}")



    def on_moved(self, event):
        # Always check for last modified
        if checkLastModified(self.last_modified):
            return
        else:
            self.last_modified = datetime.now()
        print(f"ok ok ok, someone moved {event.src_path} to {event.dest_path}")


def checkLastModified(last_modified, time_difference=1):
    return datetime.now() - last_modified < timedelta(seconds=time_difference)

def uploadFile(files, path):
    """Helper function to upload a file"""
    responseUpload = requests.post(urljoin(SERVER_URL, "uploadFile"), files=files, data={'path': path})
    if (responseUpload.status_code not in [200, 201]):
        print(f"Error uploading {path}: {responseUpload.text}")