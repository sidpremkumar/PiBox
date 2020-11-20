import os
import json

from PiBoxServer.config import DIRECTORY


def moveFile(origin, destination):
    """
    Moves a file or folder
    Returns:
        * 200: If upload was succssful 
        * 500: If there is a server error
    """
    try:
        # Make them relativePaths
        relativeOrigin = os.path.join(DIRECTORY, origin)
        relativeDestination = os.path.join(DIRECTORY, destination)

        # Move the files
        shutil.move(relativeOrigin,relativeDestination)

        # Return 200!
        return (200, json.dumps({}))
    except Exception as e: 
        # Something went wrong, return 500 along with the error
        data = {'error': str(e)}
        return (500, json.dumps(data))