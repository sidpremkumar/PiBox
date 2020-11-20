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