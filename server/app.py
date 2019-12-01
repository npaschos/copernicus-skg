import os
import base64

from PIL import Image

from flask import Flask
from flask import request
from flask import send_file
from flask import Response


app = Flask(__name__)

ASSETS_FOLDER = 'assets'

@app.route('/images/<img>', methods=['GET'])
def get_img(img):
    try:
        image = "{}/{}".format(ASSETS_FOLDER, img)
        return send_file(image, mimetype='image/png')
    except FileNotFoundError:
        return Response("{'error':'File not found.'}",
                        status=404,
                        mimetype='application/json')
    except Exception as e:
        return Response("{'error': 'Unknown exception encountered.'}",
                        status=500,
                        mimetype='application/json')


if __name__ == '__main__':
    app.run(debug=True)
