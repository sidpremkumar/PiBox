from flask import Flask
app = Flask(__name__)

# Directory where files will be stored 
DIRECTORY="./"

@app.route('/upload', methods=["post"])
def upload():
    """
    Upload endpoint to upload new files
    """
    return 'Hello, World!'

@app.route('/retrive', method=["get"])
def get():
    """
    Get endpoint to retrive a file
    """
    return 'Hello, World!'

if __name__ == "__main__":
    app.run()