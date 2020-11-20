import os
import json

from PiBoxServer.config import DIRECTORY


def retriveFile(path):
    """
    Get endpoint to retrive a file
    Returns: 
        * 200: If we're able to return the file
        * 400: If the file does not exist
        * 500: If there is a server error
    """
    try:
        # Make our path absolute
        absolutePath = os.path.join(DIRECTORY, path)

        # Check if the file exists
        if (not os.path.isfile(absolutePath)):
            # The file does not exists
            data = {'error': 'File does not exist!'}
            return (400, json.dumps(data), None, None)
        
        # Return the file
        return (200, json.dumps({}), absolutePath, os.path.basename(absolutePath))

    except Exception as e:
        # Something went wrong, return 500 along with the error
        data = {'error': str(e)}
        return (500, json.dumps(data), None, None)