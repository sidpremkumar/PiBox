import os
import json

from PiBoxServer.config import DIRECTORY


def retriveFileLastModified(path):
    """
    Get the timestamp of when a file was last modified
    Returns:
        * 200: If we're able to return the last modified time
        * 400: If the files does not exists
        * 500: If there is a server error
    """
    try:
        # Make our path absolute
        absolutePath = os.path.join(DIRECTORY, path)

        # Check if the file exists
        if (not os.path.isfile(absolutePath)):
            # The file does not exists
            data = {'error': 'File does not exist!'}
            return (400, json.dumps(data))

        # Return the last modified timestamp 
        data = {'timestamp': os.path.getmtime(absolutePath)}
        return (200, json.dumps(data))
        
    except Exception as e:
        # Something went wrong, return 500 along with the error
        data = {'error': str(e)}
        return (500, json.dumps(data))