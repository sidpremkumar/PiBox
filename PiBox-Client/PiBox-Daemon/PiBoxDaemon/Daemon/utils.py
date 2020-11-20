"""Common utils"""
import requests

import os
from urllib.parse import urljoin

from PiBoxDaemon.config import SERVER_URL, DIRECTORY, TO_IGNORE

def uploadFile(files, path):
    """Helper function to upload a file"""
    responseUpload = requests.post(urljoin(SERVER_URL, "uploadFile"), files=files, data={'path': path})
    if (responseUpload.status_code not in [200, 201]):
        print(f"Error uploading {path}: {responseUpload.text}")

def uploadLocalFiles(directory):
    """
    Recursive function to upload local files
    :param str directory: Directory to look at, relative (i.e. '.' or 'Test/test2')
    """
    directory = directory.strip("/")
    for localFile in os.listdir(os.path.join(DIRECTORY, directory)):
        if (directory == "."):
            filePath = os.path.join(DIRECTORY, localFile)
        else:
            filePath = os.path.join(DIRECTORY, directory, localFile)

        # Check if the event is in TO_IGNORE
        skip = False
        for extension in TO_IGNORE:
            if (extension in filePath):
                skip = True
        if skip:
            continue

        if (os.path.isdir(filePath)):
            # Call recursivly
            # TODO: This needs to be made
            return uploadLocalFiles(filePath.split(DIRECTORY)[1].replace("/", ""))
        elif (os.path.isfile(filePath)):
            # Else make sure we have syned the most up to date version
            # Make a call to our server to check if the file exists/last modified time
            responseFileLastModified = requests.get(urljoin(SERVER_URL, "retriveFileLastModified"), data={'path': os.path.join(directory, localFile)})

            if (responseFileLastModified.status_code == 400):
                # The file does not exist. Grab the base path
                files = {'file': open(filePath, 'rb')}

                # Upload the file
                uploadFile(files, os.path.join(directory, localFile))
            elif (responseFileLastModified.status_code == 200):
                # We have the file uploaded, compare the timestamps to see if we need to reupload
                timestamp = responseFileLastModified.json()['timestamp']
                if (timestamp < os.path.getmtime(filePath)):
                    # We need to reupload. Grab the base path
                    files = {'file': open(filePath, 'rb')}

                    # Upload the file
                    uploadFile(files, os.path.join(directory, localFile))