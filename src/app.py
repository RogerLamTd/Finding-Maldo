from flask import Flask
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    return 'Hello, World!'

#@app.before_first_request()
#def getBaseImage():


if __name__ == '__main__':
   app.run(host='0.0.0.0', port=80)