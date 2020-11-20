import os
import json
import shutil

from PiBoxServer.config import DIRECTORY


def deleteFolder(path):
    """
    Delete endpoint to delete a single folder
    Returns: 
        * 200: If delete was succssful 
        * 400: If the folder does not exist
        * 500: If there is a server error
    """
    try: 
        # Make the path absolute
        absolutePath = os.path.join(DIRECTORY, path)

        # Now ensure it exists
        if (not os.path.isdir(absolutePath)):
            # The folder does not exists
            data = {'error': 'Folder does not exist!'}
            return (400, json.dumps(data))
        
        # Then delete the file
        shutil.rmtree(absolutePath)

        # Return 200!
        return (400, json.dumps({}))
    except Exception as e:
        # Something went wrong, return 500 along with the error
        data = {'error': str(e)}
        return (500, json.dumps(data))