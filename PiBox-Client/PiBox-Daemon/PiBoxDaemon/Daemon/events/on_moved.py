import requests

import os
from urllib.parse import urljoin

from PiBoxDaemon.config import DIRECTORY, SERVER_URL


def on_moved(event):
# Get the orgin/destination relative paths
    relativeOrigin = os.path.relpath(event.src_path, DIRECTORY)
    relativeDestination = os.path.relpath(event.dest_path, DIRECTORY)

    # Make a call to our server to 
    responseMoveFile = requests.post(urljoin(SERVER_URL, "moveFile"), data={'origin': relativeOrigin, 'destination': relativeDestination})
    
    if (responseMoveFile.status_code != 200):
        print(f"Error moving {event.src_path} to {event.dest_path}")
        return
    print(f"Moved {event.src_path} to {event.dest_path}")