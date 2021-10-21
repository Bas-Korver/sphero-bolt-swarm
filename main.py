from __future__ import annotations
from http import HTTPStatus
from sphero.sphero_bolt import SpheroBolt
from flask import Flask, render_template, Response, jsonify, request, abort
import numpy as np
from cv2 import cv2
from typing import List, Type
import json
import helper
from flask_cors import CORS, cross_origin
from bleak import BleakError
from asyncio import TimeoutError
import webbrowser
import os

app = Flask(__name__)

CORS(app)

CAPTURE = None
BOLTS = []
BOLTS_HSV_PREVIEW = {}


@app.route('/bolts/')
def getConnectedBolts():
    bolts = []

    for bolt in BOLTS:
        bolts.append({
            'name': bolt.name,
            'address': bolt.address,
            'color': bolt.color,
            'low_hsv': bolt.low_hsv,
            'high_hsv': bolt.high_hsv
        })

    return jsonify(bolts)


@app.route('/bolts/<name>')
def getBolt(name):
    if request.method == "GET":
        global BOLTS_HSV_PREVIEW

        for bolt in BOLTS:
            if bolt.name == name:
                BOLTS_HSV_PREVIEW[bolt.name] = {
                    'low_hsv': bolt.low_hsv,
                    'high_hsv': bolt.high_hsv
                }

                return {
                    'name': bolt.name,
                    'address': bolt.address,
                    'color': bolt.color,
                    'low_hsv': bolt.low_hsv,
                    'high_hsv': bolt.high_hsv
                }

        return abort(404)
    elif request.method == "POST":
        print("[!] SAVING SETTINGS...")

        for bolt in BOLTS:
            if bolt.name == name:
                data = get_json_data()
                print(f"[!] DATA: {data}")

                bolt.color = data['color']
                bolt.low_hsv = data['low_hsv']
                bolt.high_hsv = data['high_hsv']

                # TODO: Save to JSON file


@app.route('/bolts/<name>/feed')
def getBoltHSVFeed(name):
    global BOLTS_HSV_PREVIEW

    for bolt in BOLTS:
        if bolt.name == name:
            return Response(video(BOLTS_HSV_PREVIEW[name]['low_hsv'], BOLTS_HSV_PREVIEW[name]['high_hsv']), mimetype='multipart/x-mixed-replace; boundary=frame')

    return abort(404)


@app.route('/bolts/<name>/hsv')
def boltHSV(name):
    global BOLTS_HSV_PREVIEW

    hsv_values = request.get_json()
    for bolt in BOLTS:
        if bolt.name == name:
            hue = hsv_values['hue']
            saturation = hsv_values['saturation']
            value = hsv_values['value']

            BOLTS_HSV_PREVIEW[bolt.name] = {
                'low_hsv': [hue[0], saturation[0], value[0]],
                'high_hsv': [hue[1], saturation[1], value[1]]
            }

    return abort(404)


@app.route('/bolts/available')
def getAvailableBolts():
    return jsonify(get_json_data("bolt_addresses.json"))


@app.route('/bolts/connect', methods=["POST"])
async def connectBolts():
    global BOLTS, BOLTS_HSV_PREVIEW

    bolt_names = request.get_json()

    BOLTS = []
    BOLTS_HSV_PREVIEW = {}
    for bolt_name in bolt_names:
        print(f"[!] Connecting with BOLT {bolt_name}")

        bolt = await connectBolt(bolt_name)
        connect_tries = 0
        tries = 10
        while connect_tries < tries:
            connect_tries += 1
            try:
                error = await bolt.connect()
                break
            except (BleakError, TimeoutError) as e:
                if connect_tries == tries:
                    print(f"[ERROR] : {e}")
                    return Response('Not able to connect to the selected '
                                    'BOLTs right now, are the selected BOLTs '
                                    'empty or too far away?',
                                    status=500)
            except Exception as e:
                error = str(e)
                if 'HRESULT: 0x800710DF' in error:
                    print('Uw bluetooth staat niet aan', '\n')
                    return Response('Please check if you turned on '
                                    'your bluetooth.',
                                    status=500)
                else:
                    raise e

        await bolt.resetYaw()
        await bolt.wake()

        BOLTS.append(bolt)
        BOLTS_HSV_PREVIEW[bolt.name] = {
            'low_hsv': bolt.low_hsv,
            'high_hsv': bolt.high_hsv
        }

    return jsonify({"Status": "Success"})


@app.route("/bolts/actions/triangle")
async def makeTriangle():
    global CAPTURE

    print("[!] Sending BOLTs to circle formation.")

    coordinates = helper.getTriangleCoordinates((320, 240), 175, len(BOLTS))
    print(f"Coordinates: { len(coordinates) }")

    for i in range(0, len(coordinates)):
        print(f"[!] Sending BOLTs to {i} coordinates.")
        coordinates = [coordinates[-1]] + coordinates[:-1]

        await helper.sendToCoordinates(BOLTS, coordinates, CAPTURE)

    print("[!] Completed circle formation.")
    return jsonify({"Status": "Completed"})


@app.route("/bolts/actions/square")
async def makeSquare():
    global CAPTURE

    print("[!] Sending BOLTs to circle formation.")

    coordinates = helper.getSquareCoordinates((320, 240), 175, len(BOLTS))
    print(f"Coordinates: { len(coordinates) }")

    for i in range(0, len(coordinates)):
        print(f"[!] Sending BOLTs to {i} coordinates.")
        coordinates = [coordinates[-1]] + coordinates[:-1]

        await helper.sendToCoordinates(BOLTS, coordinates, CAPTURE)

    print("[!] Completed circle formation.")
    return jsonify({"Status": "Completed"})


@app.route("/bolts/actions/circle")
async def makeCircle():
    global CAPTURE

    print("[!] Sending BOLTs to circle formation.")

    coordinates = helper.getCircleCoordinates((320, 240), 175, len(BOLTS))
    print(f"Coordinates: {len(coordinates)}")

    for i in range(0, len(coordinates)):
        print(f"[!] Sending BOLTs to {i} coordinates.")
        coordinates = [coordinates[-1]] + coordinates[:-1]

        await helper.sendToCoordinates(BOLTS, coordinates, CAPTURE)

    print("[!] Completed circle formation.")
    return jsonify({"Status": "Completed"})


def video(low_hsv=None, high_hsv=None):
    global CAPTURE

    if CAPTURE is None:
        CAPTURE = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    while CAPTURE.isOpened():
        ret, img = CAPTURE.read()
        if ret:
            #img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)
            frame = cv2.imencode('.jpg', img)[1].tobytes()

            if low_hsv and high_hsv:
                hsv_frame = cv2.medianBlur(cv2.cvtColor(img, cv2.COLOR_BGR2HSV), 9)

                mask = cv2.inRange(hsv_frame, np.array(low_hsv, np.uint8), np.array(high_hsv, np.uint8))

                result = cv2.bitwise_and(img, img, mask=mask)
                result_frame = cv2.imencode('.jpg', result)[1].tobytes()
                yield b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + result_frame + b'\r\n'

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


# @app.route('/connect')
# async def connectBolts():
#     global BOLTS
#
#     BOLTS = [await connectBolt("SB-D4A1"), await connectBolt("SB-E9BE"), await connectBolt("SB-67EA"),
#              await connectBolt("SB-BD23"), await connectBolt("SB-B198"), await connectBolt("SB-4D1E")]
#
#     for bolt in BOLTS:
#         await bolt.connect()
#         await bolt.resetYaw()
#         await bolt.wake()
#
#     return f"BOLTs successfully connected! {BOLTS}"


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

def main():
    
    # The reloader has not yet run - open the browser
    if not os.environ.get("WERKZEUG_RUN_MAIN"):
        webbrowser.open_new('http://127.0.0.1:5000/')

    # Otherwise, continue as normal
    app.run(host="127.0.0.1", use_reloader=True)

if __name__ == "__main__":
    main()

    # app.run(host="", debug=True, use_reloader=True)    
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(run())
