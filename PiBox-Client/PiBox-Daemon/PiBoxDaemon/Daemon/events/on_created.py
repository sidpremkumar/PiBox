import requests
from watchdog.events import DirCreatedEvent, FileCreatedEvent

import os
from urllib.parse import urljoin

from PiBoxDaemon.config import SERVER_URL, DIRECTORY
from PiBoxDaemon.Daemon import utils

def on_created(event):
        # Extract our path
        fullPath = os.path.relpath(event.src_path, DIRECTORY) # i.e. sid/somefolder/test.txt

        if (type(event) == DirCreatedEvent):
            # A Directory has been created
            # Make a call to our server to create the folder 
            responseFolderCreated = requests.post(urljoin(SERVER_URL, "createFolder"), data={'path': fullPath})

            if (responseFolderCreated.status_code != 200):
                print("Error creating folder")
                return
            
        elif (type(event) == FileCreatedEvent):
            # A File has been created
            # Make a call to our server to check if the file exists/last modified time
            responseFileLastModified = requests.get(urljoin(SERVER_URL, "retriveFileLastModified"), data={'path': fullPath})

            if (responseFileLastModified.status_code == 400):
                # The file does not exist. Grab the base path
                files = {'file': open(event.src_path, 'rb')}

                # Upload the file
                utils.uploadFile(files, fullPath)
            elif (responseFileLastModified.status_code == 200):
                # We have the file uploaded, compare the timestamps to see if we need to reupload
                timestamp = responseFileLastModified.json()['timestamp']
                if (timestamp < os.path.getmtime(event.src_path)):
                    # We need to reupload. Grab the base path
                    files = {'file': open(event.src_path, 'rb')}

                    # Upload the file
                    utils.uploadFile(files, fullPath)

        print(f"Uploaded/Updated {fullPath}")