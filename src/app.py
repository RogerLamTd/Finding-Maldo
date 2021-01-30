from flask import Flask
from flask_cors import CORS
import requests
from PIL import Image
from io import BytesIO
import crop

app = Flask(__name__)
CORS(app)

@app.route('/', )
def hello_world():
    return 'Hello, World!'

@app.before_request
def before_request():
    url = "https://external-content.duckduckgo.com/iu/?u=http%3A%2F%2Fwww.gannett-cdn.com%2F-mm-%2F279e76e11f691d6589f96f1782362c72d2b182f4%2Fc%3D0-208-4096-2522%26r%3Dx1803%26c%3D3200x1800%2Flocal%2F-%2Fmedia%2F2015%2F01%2F11%2FUSATODAY%2FUSATODAY%2F635565865838731514-EPA-FRANCE-PARIS-SOLIDARITY-RALLY.jpg&f=1&nofb=1"
    baseReq = requests.get(url, stream = True)
    if baseReq.status_code == 200:
        baseImg = Image.open(BytesIO(baseReq.content))
        tagImg, xOffset, yOffset = crop.crop_image(baseImg)
        print(xOffset, yOffset)
    else:
        print("Failed to download image")


if __name__ == '__main__':
   app.run(host='0.0.0.0', port=80)