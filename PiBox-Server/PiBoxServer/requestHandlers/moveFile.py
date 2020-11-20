def moveFile():
    """
    Moves a file or folder
    Returns:
        * 200: If upload was succssful 
        * 500: If there is a server error
    """
    try:
        # Grab our origin and destination
        origin = request.values['origin'].strip("/")
        destination = request.values['destination'].strip("/")

        # Make them relativePaths
        relativeOrigin = os.path.join(DIRECTORY, origin)
        relativeDestination = os.path.join(DIRECTORY, destination)


        # Move the files
        shutil.move(relativeOrigin,relativeDestination)

        # Return 200!
        return Response(status=200)
    except Exception as e: 
                # Something went wrong, return 500 along with the error
                data = {'error': str(e)}
                return Response(response=json.dumps(data), status=500)