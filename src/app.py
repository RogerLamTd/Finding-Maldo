from flask import Flask
from flask import send_from_directory
from flask import render_template
import requests
from PIL import Image
from io import BytesIO
import crop

app = Flask(__name__, static_url_path="")

#@app.route('/favicon.ico')
#def favicon():
    #return send_from_directory(os.path.join(app.root_path, 'static'),
                               #'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/')
def login():
    url = "https://external-content.duckduckgo.com/iu/?u=http%3A%2F%2Fwww.gannett-cdn.com%2F-mm-%2F279e76e11f691d6589f96f1782362c72d2b182f4%2Fc%3D0-208-4096-2522%26r%3Dx1803%26c%3D3200x1800%2Flocal%2F-%2Fmedia%2F2015%2F01%2F11%2FUSATODAY%2FUSATODAY%2F635565865838731514-EPA-FRANCE-PARIS-SOLIDARITY-RALLY.jpg&f=1&nofb=1"
    baseReq = requests.get(url, stream = True)
    baseImg = Image.open(BytesIO(baseReq.content))
    maskImg, xOffset, yOffset = crop.getMask(baseImg)
    return render_template('index.html', base=baseImg, mask=maskImg)


if __name__ == '__main__':
   app.run(host='0.0.0.0', port=80)
