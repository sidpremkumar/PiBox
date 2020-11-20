import os
import json

from PiBoxServer.config import DIRECTORY


def uploadFile(path, toUpload):
    """
    Upload endpoint to upload new files
    Returns: 
        * 200: If upload was succssful 
        * 500: If there is a server error
    """
    try:
        # Make our path absolute
        absolutePath = os.path.join(DIRECTORY, path)

        if (os.path.isfile(absolutePath)):
            # The file exists already, delete it so we can reupload
            os.remove(absolutePath)

        # Check the directory exists 
        if (not os.path.exists(absolutePath)):
            os.makedirs(absolutePath)
        
        # Finally save the file
        toUpload.save(absolutePath)

        # Return 200! 
        return (200, json.dumps({}))
    except Exception as e: 
        # Something went wrong, return 500 along with the error
        data = {'error': str(e)}
        return (500, json.dumps(data))