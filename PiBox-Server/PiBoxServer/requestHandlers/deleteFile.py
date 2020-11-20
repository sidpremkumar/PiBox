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