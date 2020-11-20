import os
import json

from PiBoxServer.config import DIRECTORY


def createFolder(path):
    """
    Creates a folder 
    Returns:
        * 200: If upload was succssful 
        * 500: If there is a server error
    """
    try:
        # Make our path relative
        relativePath = os.path.join(DIRECTORY, path)

        # Check if it exists already
        if (os.path.isdir(relativePath)):
            # The folder already exists
            return (200, json.dumps({}))
        
         # Create the folders
        relativePathFolder = DIRECTORY
        for folder in path.split("/"):
            relativePathFolder = os.path.join(relativePathFolder, folder)
            os.mkdir(relativePathFolder)
        
        # Return 200! 
        return (200, json.dumps({}))
    

    except Exception as e: 
            # Something went wrong, return 500 along with the error
            data = {'error': str(e)}
            return (200, json.dumps(data))