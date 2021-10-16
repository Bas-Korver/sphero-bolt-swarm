from __future__ import annotations
from sphero.sphero_bolt import SpheroBolt
from flask import Flask, render_template, Response
import numpy as np
from cv2 import cv2
from typing import List
import json
import asyncio

app = Flask(__name__)

# CAPTURE = cv2.VideoCapture(0, cv2.CAP_DSHOW)
BOLTS = []


def video():
    CAPTURE = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    while CAPTURE.isOpened():
        # Capture frame-by-frame
        ret, img = CAPTURE.read()
        if ret:
            img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)
            frame = cv2.imencode('.jpg', img)[1].tobytes()
            yield b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'
        else:
            break
    if not CAPTURE.isOpened():
        print("[ERROR] can't connect to the camera feed")
    CAPTURE.release()


#
# Default page (= html)
#
@app.route("/")
def index():
    return render_template("index.html")


#
# Detections feed
#
@app.route('/feed')
def feed():
    return Response(video(), mimetype='multipart/x-mixed-replace; boundary=frame')


# TODO: fix this week 8 V
@app.route("/colors/<name>")
def colorForBolt(name=None):
    global BOLTS

    if name is None:
        return "Dit moet stoppen nu!!!!!!!!!!"

    bolt = None
    for bolt_x in BOLTS:
        if bolt_x.name == name:
            bolt = bolt_x
            break

    if bolt is None:
        return f"Voer een geldige naam in! {BOLTS}"

    return Response(colorVideoForBolt(bolt), mimetype='multipart/x-mixed-replace; boundary=frame')


def colorVideoForBolt(bolt):
    global CAPTURE

    ret, img = CAPTURE.read()
    while CAPTURE.isOpened():
        print("[!] Capture opened!")
        ret, img = CAPTURE.read()
        if ret:
            hsv_frame = cv2.medianBlur(cv2.cvtColor(img, cv2.COLOR_BGR2HSV), 9)

            lower = np.array(bolt.low_hsv, np.uint8)
            upper = np.array(bolt.high_hsv, np.uint8)
            mask = cv2.inRange(hsv_frame, lower, upper)
            result = cv2.bitwise_and(img, img, mask=mask)

            frame = cv2.imencode('.jpg', result)[1].tobytes()
            yield b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'
        else:
            break


@app.route('/connect')
async def connectBolts():
    global BOLTS

    BOLTS = [await connectBolt("SB-D4A1"), await connectBolt("SB-E9BE"), await connectBolt("SB-67EA"),
             await connectBolt("SB-BD23"), await connectBolt("SB-B198"), await connectBolt("SB-4D1E")]

    for bolt in BOLTS:
        await bolt.connect()
        await bolt.resetYaw()
        await bolt.wake()

    return f"BOLTs successfully connected! {BOLTS}"


def get_json_data(file: str) -> List[dict[str, str]]:
    """Reads json file and returns a list of dictionaries.

    Parameters
    ----------
    file : str
        location of the json file.

    Returns
    -------
    list[dict[str, str]]
        list with one or more dictionaries.
    """
    with open(file) as json_file:
        return json.load(json_file)


async def connectBolt(name):
    addresses = get_json_data("bolt_addresses.json")

    bolt_json_data = next(
        item for item in addresses if item['name'] == name)

    return SpheroBolt(bolt_json_data['address'], name, bolt_json_data['color'], bolt_json_data['low_hsv'],
                      bolt_json_data['high_hsv'])


# async def run():
#     global BOLTS
#
#     app.run(host="", debug=True, use_reloader=True)


if __name__ == "__main__":
    app.run(host="", debug=True, use_reloader=True)

    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(run())