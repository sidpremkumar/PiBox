import json

class requestEvent():
    def __init__(self, params, requestFunction, returnsFile=False, uploadsFile=False, fileToUpload=None):
        self.params = params
        self.requestFunction = requestFunction
        self.isDone = False
        self.status_code = 500
        self.response = json.dumps({})
        self.returnsFile = returnsFile
        self.absolutePath = None 
        self.attachment_filename = None
        self.uploadsFile = uploadsFile
        self.fileToUpload = fileToUpload