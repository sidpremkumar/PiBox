import redis
from flask import Flask, request, Response, send_file

import os
import json
import shutil
import queue
import time

from PiBoxServer import requestHandlers, utils
from PiBoxServer.requestEvent import requestEvent
from PiBoxServer.config import DIRECTORY

# Flask App Info
app = Flask(__name__)

# Create our event queue
eventQueue = queue.Queue()

def startServer():
    app.run(host='0.0.0.0', port=5000)

@app.route('/getSyncManifest', methods=["get"])
def getSyncManifest():
    # First grab our path
    path = request.values['path'].strip("/")

    # Add the event to the queue
    event = requestEvent(params=(path), requestFunction=requestHandlers.getSyncManifest)
    eventQueue.put(event)

    # Wait till the event is done
    while(not event.isDone):
        time.sleep(0.1)

    # Return the event and its status code
    return Response(status=event.status_code, response=event.response)

@app.route('/moveFile', methods=["post"])
def moveFile():
    # Grab our origin and destination
    origin = request.values['origin'].strip("/")
    destination = request.values['destination'].strip("/")

    # Add the event to the queue
    event = requestEvent(params=(origin, destination), requestFunction=requestHandlers.moveFile)
    eventQueue.put(event)

    # Wait till the event is done
    while(not event.isDone):
        time.sleep(1)

    # Return the event and its status code
    return Response(status=event.status_code, response=event.response)
            
@app.route('/createFolder', methods=["post"])
def createFolder():
    # First grab our path
    path = request.values['path'].strip("/")

    # Add the event to the queue
    event = requestEvent(params=(path), requestFunction=requestHandlers.createFolder)
    eventQueue.put(event)

    # Wait till the event is done
    while(not event.isDone):
        time.sleep(0.1)

    # Return the event and its status code
    return Response(status=event.status_code, response=event.response)

@app.route('/uploadFile', methods=["post"])
def uploadFile():
    # First grab our file and path
    toUpload = request.files['file']
    path = request.values['path'].strip("/")

    # Add the event to the queue
    event = requestEvent(params=path, requestFunction=requestHandlers.uploadFile, fileToUpload=toUpload, uploadsFile=True)
    eventQueue.put(event)

    # Wait till the event is done
    while(not event.isDone):
        time.sleep(1)

    # Return the event and its status code
    return Response(status=event.status_code, response=event.response)

@app.route('/deleteFile', methods=["post"])
def deleteFile():
    # First grab our path
    path = request.values['path']

    # Add the event to the queue
    event = requestEvent(params=(path), requestFunction=requestHandlers.deleteFile)
    eventQueue.put(event)

    # Wait till the event is done
    while(not event.isDone):
        time.sleep(1)

    # Return the event and its status code
    return Response(status=event.status_code, response=event.response)

@app.route('/deleteFolder', methods=["post"])
def deleteFolder():
    # First grab our path
    path = request.values['path']

    # Add the event to the queue
    event = requestEvent(params=(path), requestFunction=requestHandlers.deleteFolder)
    eventQueue.put(event)

    # Wait till the event is done
    while(not event.isDone):
        time.sleep(1)

    # Return the event and its status code
    return Response(status=event.status_code, response=event.response)

@app.route('/retriveFile', methods=["get"])
def retriveFile():
    # First grab our path
    path = request.values['path']

    # Add the event to the queue
    event = requestEvent(params=(path), requestFunction=requestHandlers.retriveFile, returnsFile=True)
    eventQueue.put(event)

    # Wait till the event is done
    while(not event.isDone):
        time.sleep(1)

    # Return the event and its status code
    if (event.status_code == 200):
        return send_file(event.absolutePath, attachment_filename=event.attachment_filename)
    
    # Unless an error came up
    return Response(status=event.status_code, response=event.response)

@app.route('/retriveFileLastModified', methods=["get"])
def retriveFileLastModified():
    # First grab our path
    path = request.values['path']

    # Add the event to the queue
    event = requestEvent(params=(path), requestFunction=requestHandlers.retriveFileLastModified)
    eventQueue.put(event)

    # Wait till the event is done
    while(not event.isDone):
        time.sleep(1)

    # Return the event and its status code
    return Response(status=event.status_code, response=event.response)
