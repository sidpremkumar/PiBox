import os
import json

from PiBoxServer.config import DIRECTORY


def deleteFile(path):
    """
    Delete endpoint to delete a single file
    Returns: 
        * 200: If delete was succssful 
        * 400: If the file does not exist
        * 500: If there is a server error
    """
    try:    
        # Make our path absolute
        absolutePath = os.path.join(DIRECTORY, path)

        # Now ensure it exists
        if (not os.path.isfile(absolutePath)):
            # The file does not exists
            data = {'error': 'File does not exist!'}
            return (400, json.dumps(data))
        
        # Then delete the file
        os.remove(absolutePath)

        # Return 200!
        return (200, json.dumps({}))
    except Exception as e:
        # Something went wrong, return 500 along with the error
        data = {'error': str(e)}
        return (500, json.dumps(data))