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