from __future__ import annotations
import asyncio
import math
import json
import threading
from sphero.sphero_bolt import SpheroBolt
import numpy as np
from cv2 import cv2
from typing import List

# CAP = None
CURRENT_COORDINATES = {}


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


async def viewMovement():
    print("VIEW MOVEMENTS!")

    global CAP
    global CURRENT_COORDINATES

    if CAP is None or not CAP.isOpened():
        print("[Error] Could not open the main webcam stream.")
        return

    while CAP.isOpened():
        ret, main_frame = CAP.read()

        for bolt_address in list(CURRENT_COORDINATES):
            bolt = CURRENT_COORDINATES[bolt_address]
            # color is via BGR
            cv2.circle(main_frame, (int(bolt.get('coordinate')[0]), int(bolt.get('coordinate')[1])), 5,
                       (int(bolt.get('color')[2]), int(bolt.get('color')[1]), int(bolt.get('color')[0])), 2)

        cv2.circle(main_frame, (320, 240), 10, (255, 255, 255), 3)

        cv2.imshow("Movement Viewer", main_frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            CAP.release()
            cv2.destroyAllWindows()


def findDirection(_point_a, _point_b):
    direction1 = _point_b[0] - _point_a[0]
    direction2 = _point_b[1] - _point_a[1]
    if direction1 == 0:
        if direction2 == 0:  # same points?
            degree = 0
        else:
            degree = 0 if _point_a[1] > _point_b[1] else 180
    elif direction2 == 0:
        degree = 90 if _point_a[0] < _point_b[0] else 270
    else:
        degree = math.atan(direction2 / direction1) / math.pi * 180
        lowering = _point_a[1] < _point_b[1]
        if (lowering and degree < 0) or (not lowering and degree > 0):
            degree += 270
        else:
            degree += 90
    return degree


def getSquareCoordinates(_center=(0, 0), _r=10, _n=10):
    if _n < 4:
        _n = 4
    if _n == 4:
        return [[_center[0] + _r, _center[1] - _r], [_center[0] + _r, _center[1] + _r],
                [_center[0] - _r, _center[1] + _r], [_center[0] - _r, _center[1] - _r]]
    elif 4 < _n <= 6:
        return [[_center[0] + _r, _center[1] - _r], [_center[0] + _r, _center[1]],
                [_center[0] + _r, _center[1] + _r], [_center[0] - _r, _center[1] + _r],
                [_center[0] - _r, _center[1]], [_center[0] - _r, _center[1] - _r]]
    elif 6 < _n <= 8:
        return [[_center[0] + _r, _center[1] - _r], [_center[0] + _r, _center[1]],
                [_center[0] + _r, _center[1] + _r], [_center[0], _center[1] + _r],
                [_center[0] - _r, _center[1] + _r], [_center[0] - _r, _center[1]],
                [_center[0] - _r, _center[1] - _r], [_center[0], _center[1] - _r]]
    elif 8 < _n <= 10:
        return [[_center[0] + _r, _center[1] - _r], [_center[0] + _r, _center[1]],
                [_center[0] + _r, _center[1] + _r], [_center[0] + _r* 0.5, _center[1] + _r],
                [_center[0] - _r * 0.5, _center[1] + _r], [_center[0] - _r, _center[1] + _r], [_center[0] - _r, _center[1]],
                [_center[0] - _r, _center[1] - _r], [_center[0] - _r * 0.5, _center[1] - _r],
                [_center[0] + _r * 0.5, _center[1] - _r]]


def getTriangleCoordinates(_center=(0, 0), _r=10, _n=10):
    if _n < 3:
        _n = 3
    if _n == 3:
        return [[_center[0], _center[1] + _r], [_center[0] - _r/2, _center[1] - _r],
                [_center[0] + _r/2, _center[1] - _r]]
    elif 3 < _n <= 6:
        return [[_center[0], _center[1] + _r],
                [(_center[0] + (_center[0] - _r / 2)) / 2, (_center[1] + _r + _center[1] - _r) / 2],
                [_center[0] - _r / 2, _center[1] - _r],
                [((_center[0] - _r / 2) + (_center[0] + _r / 2)) / 2, (_center[1] - _r + _center[1] - _r) / 2],
                [_center[0] + _r / 2, _center[1] - _r],
                [(_center[0] + (_center[0] + _r / 2))/2, (_center[1] + _r + _center[1] - _r)/2]]
    elif 6 < _n <= 10:
        return [[_center[0], _center[1] + _r*1.5,
                [_center[0], _center[1] + _r*0.75],
                [(_center[0] + (_center[0] - _r / 2)) / 2, (_center[1] + _r + _center[1] - _r) / 2],
                [_center[0], _center[1]],
                [_center[0] - _r, _center[1] - _r],
                [_center[0] - _r / 2, _center[1] - _r],
                [((_center[0] - _r / 2) + (_center[0] + _r / 2)) / 2, (_center[1] - _r + _center[1] - _r) / 2],
                [_center[0] + _r / 2, _center[1] - _r],
                [_center[0] + _r, _center[1] - _r],
                [(_center[0] + (_center[0] + _r / 2))/2, (_center[1] + _r + _center[1] - _r)/2]]]


def getCircleCoordinates(_center=(0, 0), _r=10, _n=10):
    if _n < 4:
        _n = 4
    return [
        [
            _center[0] + (math.cos(2 * math.pi / _n * x) * _r),  # x
            _center[1] + (math.sin(2 * math.pi / _n * x) * _r)  # y
        ] for x in range(0, _n)]


async def sendToCoordinates(bolts, coordinates, CAPTURE):
    global CURRENT_COORDINATES

    threads = []
    for bolt in bolts:
        await bolt.setMatrixLED(0, 0, 0)
        await bolt.setFrontLEDColor(0, 0, 0)
        await bolt.setBackLEDColor(0, 0, 0)

    for i in range(len(bolts)):
        if i >= len(coordinates):
            break

        thread = threading.Thread(target=asyncio.run, args=(sendToCoordinate(bolts[i], coordinates[i], CAPTURE),))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    for bolt in bolts:
        await bolt.setMatrixLED(bolt.color[0], bolt.color[1], bolt.color[2])
        await bolt.setFrontLEDColor(255, 255, 255)
        await bolt.setBackLEDColor(255, 0, 0)


async def sendToCoordinate(bolt, coordinate, CAPTURE):
    global CURRENT_COORDINATES

    print(f"[!] Sending bolt {bolt.address} to X: {coordinate[0]}, Y: {coordinate[1]}")

    if CAPTURE is None or not CAPTURE.isOpened():
        print("[Error] Could not open webcam.")
        return

    CURRENT_COORDINATES[bolt.address] = {
        'color': bolt.color,
        'coordinate': coordinate
    }

    correct_coordinate = False
    while CAPTURE.isOpened() and not correct_coordinate:
        ret, main_frame = CAPTURE.read()

        cv2.circle(main_frame, (int(coordinate[0]), int(coordinate[1])), 5, (0, 0, 255), 2)
        hsv_frame = cv2.medianBlur(cv2.cvtColor(main_frame, cv2.COLOR_BGR2HSV), 9)

        lower = np.array(bolt.low_hsv, np.uint8)
        upper = np.array(bolt.high_hsv, np.uint8)
        mask = cv2.inRange(hsv_frame, lower, upper)

        contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        if len(contours) > 0:
        # for pic, contour in enumerate(contours):
            contour = max(contours, key=cv2.contourArea)
            area = cv2.contourArea(contour)
            if area >= 25:
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(main_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                direction = findDirection([x, y], coordinate)

                # in right position
                if x < coordinate[0] < x + h and y < coordinate[1] < y + h:
                    # to be sure that the bolt gets the command
                    for i in range(10):
                        await bolt.roll(0, 0)

                    correct_coordinate = True
                    CURRENT_COORDINATES.pop(bolt.address, None)
                else:
                    await bolt.roll(35, int(direction))

        cv2.imshow(f"Detection for {bolt.name}, coordinates: {coordinate}", main_frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            CAP.release()
            cv2.destroyAllWindows()