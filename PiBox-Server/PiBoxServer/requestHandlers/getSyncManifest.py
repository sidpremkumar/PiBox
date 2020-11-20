from flask import request, Response

import os
import json

from PiBoxServer.config import DIRECTORY

def getSyncManifest(path):
    """
    Returns a JSON of all files in the server along with last modified timestamps
    Returns:
        * 200: If succsesful
        * 500: If there is a server error
    """
    try:
        # First grab the path we're looking at
        files = getFiles(os.path.join(DIRECTORY, path))
        data = {'files': files}
        return (200, json.dumps(data))
    except Exception as e: 
        # Something went wrong, return 500 along with the error
        data = {'error': str(e)}
        return (500, json.dumps(data))

    
def getFiles(directory):
    """
    Helper function to get all files in a directory
    param string directory: Directory we're looking at
    """
    listOfFile = os.listdir(directory)
    completeFileList = list()
    for singleFile in listOfFile:
        completePath = os.path.join(directory, singleFile)
        if os.path.isdir(completePath):
            completeFileList = completeFileList + getFiles(completePath)
        else:
            # Return only the realtive path to the file
            completePath = os.path.relpath(completePath, DIRECTORY) # i.e. ubuntu/test/test.txt -> test/test.txt
            completeFileList.append(completePath)
    return completeFileList