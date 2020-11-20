import time

def requestHandlerMain(eventQueue):
    while True:
        if (eventQueue.qsize() != 0):
            event = eventQueue.get()
            status_code, response = event.requestFunction(event.params)
            event.isDone = True
            event.status_code = status_code
            event.response = response
        time.sleep(1)