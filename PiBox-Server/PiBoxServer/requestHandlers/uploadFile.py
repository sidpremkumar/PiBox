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
        return Response(status=200)
    except Exception as e: 
        # Something went wrong, return 500 along with the error
        data = {'error': str(e)}
        return Response(response=json.dumps(data), status=500)