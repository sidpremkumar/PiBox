import requests
from watchdog.events import FileDeletedEvent, DirDeletedEvent

import os
from urllib.parse import urljoin

from PiBoxDaemon.config import SERVER_URL, DIRECTORY

def on_deleted(event):
        # Determine if its a File delete or Dir delete
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
