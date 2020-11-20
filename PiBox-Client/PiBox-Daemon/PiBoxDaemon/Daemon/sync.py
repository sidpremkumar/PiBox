import requests

import os
from urllib.parse import urljoin

from PiBoxDaemon.config import DIRECTORY, SERVER_URL, TO_IGNORE
from PiBoxDaemon.Daemon import utils

def syncDirectory(directory):
    """Sync the clinet to the server at the provided directory"""
    # First upload any files we have locally
    utils.uploadLocalFiles(directory)

    # First make a call to our server to get the manifest
    allFilesResponse = requests.get(urljoin(SERVER_URL, "getSyncManifest"), data={'path': directory})

    # Throw an error if we did nto get the right response
    if (allFilesResponse.status_code != 200):
        print("Error pulling sync manifest!")
        return

    # Extract all the files
    files = allFilesResponse.json()['files']
    
    # Loop over all the files and make sure they are synced
    for singleFile in files:
        absolutePath = os.path.join(DIRECTORY, singleFile).strip("/")
        if (not os.path.exists(os.path.join(DIRECTORY, singleFile))):
            # Make sure the folder exists
            relativePath = DIRECTORY

            # Go till [:-1] as we don't want the file, just the folders leading up to it 
            relativePathFolder = relativePath
            for folder in singleFile.strip("/").split("/")[:-1]:
                relativePathFolder = os.path.join(relativePathFolder, folder)
                if (not os.path.isdir(relativePathFolder)):
                    os.mkdir(relativePathFolder)
            
            # Then pull and copy the file
            data = {'path': singleFile}
            singleFileResponse = requests.get(urljoin(SERVER_URL, "retriveFile"), data=data)

            # Throw an error if we were unable to get a response and continue
            if (singleFileResponse.status_code != 200):
                print(f"Error syncing file {singleFile}")
                continue

            # Else open the file we're going to be writing 
            # TODO: This should not be a f-string 
            fileToWrite = open(f"/{absolutePath}", "wb")
            fileToWrite.write(singleFileResponse.content)
            fileToWrite.close()
        
        elif (os.path.isfile(os.path.join(DIRECTORY, singleFile))):
            # Else make sure we have syned the most up to date version
            # Make a call to our server to check if the file exists/last modified time
            responseFileLastModified = requests.get(urljoin(SERVER_URL, "retriveFileLastModified"), data={'path': os.path.join(DIRECTORY, singleFile)})

            if (responseFileLastModified.status_code == 400):
                # The file does not exist. Grab the base path
                files = {'file': open(os.path.join(DIRECTORY, singleFile), 'rb')}

                # Upload the file
                utils.uploadFile(files, singleFile)
            elif (responseFileLastModified.status_code == 200):
                # We have the file uploaded, compare the timestamps to see if we need to reupload
                timestamp = responseFileLastModified.json()['timestamp']
                if (timestamp < os.path.getmtime(os.path.join(DIRECTORY, singleFile))):
                    # We need to reupload. Grab the base path
                    files = {'file': open(os.path.join(DIRECTORY, singleFile), 'rb')}

                    # Upload the file
                    utils.uploadFile(files, singleFile)
