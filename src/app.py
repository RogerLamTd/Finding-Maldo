from flask import Flask
from flask import send_from_directory
from flask import render_template
import requests
from PIL import Image
from io import BytesIO
import crop
import base64
import random

app = Flask(__name__, static_url_path="")

#@app.route('/favicon.ico')
#def favicon():
    #return send_from_directory(os.path.join(app.root_path, 'static'),
                               #'favicon.ico', mimetype='image/vnd.microsoft.icon')

images = ["https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fwww.goodnewsunlimited.com%2Fwp-content%2Fuploads%2FCrowd.jpg&f=1&nofb=1",
        "https://external-content.duckduckgo.com/iu/?u=http%3A%2F%2Fwww.gannett-cdn.com%2F-mm-%2F279e76e11f691d6589f96f1782362c72d2b182f4%2Fc%3D0-208-4096-2522%26r%3Dx1803%26c%3D3200x1800%2Flocal%2F-%2Fmedia%2F2015%2F01%2F11%2FUSATODAY%2FUSATODAY%2F635565865838731514-EPA-FRANCE-PARIS-SOLIDARITY-RALLY.jpg&f=1&nofb=1"]

@app.route('/')
def login():
    return render_template('tutorial.html')

@app.route('/bernie-time')
def bernie_time():
    url = images[random.randint(0, len(images) - 1)]
    baseReq = requests.get(url, stream = True)
   # baseReq.content.decode = True
    baseBytes = BytesIO(baseReq.content)
    img64 = base64.b64encode(baseBytes.getvalue())
    print(baseReq.headers) 
    print(type(baseReq.content))
    #baseImg = Image.frombytes("RGB", len(baseReq.content),baseReq.content)
    baseImg = Image.open(baseBytes)


    maskImg, xOffset, yOffset, maskSize = crop.get_Mask(baseImg)
    #xOffset = 2229
    #yOffset = 815
    #maskImg = Image.open("static/mask.png")
   # maskSize = (50,50)
    print(xOffset, yOffset)
    print(maskSize)
    
    byte_buf = BytesIO()
    maskImg.save(byte_buf, "PNG")
    mask64 = base64.b64encode(byte_buf.getvalue())
    return render_template('index.html', base=img64.decode('utf-8'), mask=mask64.decode('utf-8'), mask_x = "{}px".format(xOffset), mask_y = "{}px".format(yOffset),
        mask_w = "{}px".format(maskSize[0]), mask_h = "{}px".format(maskSize[1]))

@app.route('/winnerwinnterchickendinner')
def winner():
    return render_template('winner.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
