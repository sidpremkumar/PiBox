import json

class requestEvent():
    def __init__(self, params, requestFunction):
        self.params = params
        self.requestFunction = requestFunction
        self.isDone = False
        self.status_code = 500
        self.response = json.dumps({})