from flask import Flask, request, Response, send_file

import os
import json
import shutil

# Flask App Info
app = Flask(__name__)

# Directory where files will be stored 
DIRECTORY="/Users/sidpremkumar/PiBox-Data"

@app.route('/createFolder', method=["post"])
def createFolder():
    """
    Creates a folder 
    Returns:
        * 200: If upload was succssful 
        * 500: If there is a server error
    """
    try:
        # First grab our path
        path = request.values['path'].strip("/")
        relativePath = os.path.join(DIRECTORY, path)

        # Check if it exists already
        if (os.path.isdir(relativePath)):
            # The folder already exists
            return Response(status=200)
        
         # Create the folders
        relativePathFolder = DIRECTORY
        for folder in path.split("/"):
            relativePathFolder = os.path.join(relativePathFolder, folder)
            os.mkdir(relativePathFolder)
        
        # Return 200! 
        return Response(status=200)
    

    except Exception as e: 
            # Something went wrong, return 500 along with the error
            data = {'error': str(e)}
            return Response(response=json.dumps(data), status=500)

@app.route('/uploadFile', methods=["post"])
def uploadFile():
    """
    Upload endpoint to upload new files
    Returns: 
        * 200: If upload was succssful 
        * 500: If there is a server error
    """
    try:
        # First grab our file and path
        toUpload = request.files['file']
        path = request.values['path'].strip("/")
        relativePath = os.path.join(DIRECTORY, path)
        finalPath = os.path.join(relativePath, toUpload.filename)

        if (os.path.isfile(finalPath)):
            # The file exists already, delete it so we can reupload
            os.remove(finalPath)

        # Check the directory exists 
        if (not os.path.isdir(relativePath)):
            # Create the folders
            relativePathFolder = DIRECTORY
            for folder in path.split("/"):
                relativePathFolder = os.path.join(relativePathFolder, folder)
                os.mkdir(relativePathFolder)
        
        # Finally save the file
        toUpload.save(finalPath)

        # Return 200! 
        return Response(status=200)
    except Exception as e: 
        # Something went wrong, return 500 along with the error
        data = {'error': str(e)}
        return Response(response=json.dumps(data), status=500)

@app.route('/deleteFile', methods=["post"])
def deleteFile():
    """
    Delete endpoint to delete a single file
    Returns: 
        * 200: If delete was succssful 
        * 400: If the file does not exist
        * 500: If there is a server error
    """
    try: 
        # First grab our path
        path = request.values['path']
        relativePath = os.path.join(DIRECTORY, path)

        # Now ensure it exists
        if (not os.path.isfile(relativePath)):
            # The file does not exists
            data = {'error': 'File does not exist!'}
            return Response(response=json.dumps(data), status=400)
        
        # Then delete the file
        os.remove(relativePath)

        # Return 200!
        return Response(status=200)
    except Exception as e:
        # Something went wrong, return 500 along with the error
        data = {'error': str(e)}
        return Response(response=json.dumps(data), status=500)

@app.route('/deleteFolder', methods=["post"])
def deleteFolder():
    """
    Delete endpoint to delete a single folder
    Returns: 
        * 200: If delete was succssful 
        * 400: If the folder does not exist
        * 500: If there is a server error
    """
    try: 
        # First grab our path
        path = request.values['path']
        relativePath = os.path.join(DIRECTORY, path)

        # Now ensure it exists
        if (not os.path.isdir(relativePath)):
            # The folder does not exists
            data = {'error': 'Folder does not exist!'}
            return Response(response=json.dumps(data), status=400)
        
        # Then delete the file
        shutil.rmtree(relativePath)

        # Return 200!
        return Response(status=200)
    except Exception as e:
        # Something went wrong, return 500 along with the error
        data = {'error': str(e)}
        return Response(response=json.dumps(data), status=500)

@app.route('/retriveFile', methods=["get"])
def retriveFile():
    """
    Get endpoint to retrive a file
    Returns: 
        * 200: If we're able to return the file
        * 400: If the file does not exist
        * 500: If there is a server error
    """
    try:
        # First grab our path
        path = request.values['path']
        relativePath = os.path.join(DIRECTORY, path)

        # Check if the file exists
        if (not os.path.isfile(relativePath)):
            # The file does not exists
            data = {'error': 'File does not exist!'}
            return Response(response=json.dumps(data), status=400)
        
        # Return the file
        return send_file(relativePath, attachment_filename=os.path.basename(relativePath))

    except Exception as e:
        # Something went wrong, return 500 along with the error
        data = {'error': str(e)}
        return Response(response=json.dumps(data), status=500)

@app.route('/retriveFileLastModified', methods=["get"])
def retriveFileLastModified():
    """
    Get the timestamp of when a file was last modified
    Returns:
        * 200: If we're able to return the last modified time
        * 400: If the files does not exists
        * 500: If there is a server error
    """
    try:
        # First grab our path
        path = request.values['path']
        relativePath = os.path.join(DIRECTORY, path)

        # Check if the file exists
        if (not os.path.isfile(relativePath)):
            # The file does not exists
            data = {'error': 'File does not exist!'}
            return Response(response=json.dumps(data), status=400)

        # Return the last modified timestamp 
        data = {'timestamp': os.path.getmtime(relativePath)}
        return Response(response=json.dumps(data), status=200)
        
    except Exception as e:
        # Something went wrong, return 500 along with the error
        data = {'error': str(e)}
        return Response(response=json.dumps(data), status=500)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)