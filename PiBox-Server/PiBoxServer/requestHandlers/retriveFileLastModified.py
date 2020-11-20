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