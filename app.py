import base64
import numpy as np
import cv2
from flask import Flask, request, jsonify, Response

from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/design-checker', methods=['GET', 'POST'])
def design_checker():
    front = request.json['front']
    back = request.json['back']
    front_nparr = np.fromstring(base64.b64decode(front), np.uint8)
    front_image = cv2.imdecode(front_nparr, cv2.IMREAD_COLOR)
    back_nparr = np.fromstring(base64.b64decode(back), np.uint8)
    back_image = cv2.imdecode(back_nparr, cv2.IMREAD_COLOR)

    boundaries = [
        ([100, 0, 0], [255, 0, 0]),
    ]
    # loop over the boundaries
    for (lower, upper) in boundaries:
        # create NumPy arrays from the boundaries
        lower = np.array(lower, dtype = "uint8")
        upper = np.array(upper, dtype = "uint8")
        front_mask = cv2.inRange(front_image, lower, upper)
        back_mask = cv2.inRange(back_image, lower, upper)
        if np.sum(front_mask) > 100 or np.sum(back_mask) > 100:
            return Response(status=406)

    return Response(status=200)
