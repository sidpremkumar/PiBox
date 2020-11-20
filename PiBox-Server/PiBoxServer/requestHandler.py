import time


def requestHandlerMain(eventQueue):
    while True:
        if (eventQueue.qsize() != 0):
            # Get the next event
            event = eventQueue.get()
            if (event.returnsFile):
                # If we're returning a file we have to add the attachment_filename and absolutePath
                status_code, response, absolutePath, attachment_filename = event.requestFunction(event.params)
                event.absolutePath = absolutePath
                event.attachment_filename = attachment_filename
            elif (event.uploadsFile):
                # If we're uploading a file, we have to pass that file as well
                status_code, response = event.requestFunction(event.params, event.fileToUpload)
            else:
                # Else just status_code and response works
                status_code, response = event.requestFunction(event.params)

            # Add the response and status code to the event
            event.status_code = status_code
            event.response = response 

            # Mark the event as done
            event.isDone = True
        
        time.sleep(1)
