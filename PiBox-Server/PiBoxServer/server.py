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
    # Add the event to the queue
    event = requestEvent(params=(request.values['path'].strip("/")), requestFunction=requestHandlers.getSyncManifest)
    eventQueue.put(event)

    # Wait till the event is done
    while(not event.isDone):
        time.sleep(0.1)

    # Return the event and its status code
    return Response(status=event.status_code, response=event.response)

@app.route('/moveFile', methods=["post"])
def moveFile():
    return Response(status=201)
            
@app.route('/createFolder', methods=["post"])
def createFolder():
    pass

@app.route('/uploadFile', methods=["post"])
def uploadFile():
    pass

@app.route('/deleteFile', methods=["post"])
def deleteFile():
    pass

@app.route('/deleteFolder', methods=["post"])
def deleteFolder():
    pass

@app.route('/retriveFile', methods=["get"])
def retriveFile():
    pass

@app.route('/retriveFileLastModified', methods=["get"])
def retriveFileLastModified():
    pass
