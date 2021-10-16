from __future__ import annotations
import asyncio
import math
import json
import threading
from sphero.sphero_bolt import SpheroBolt
import numpy as np
from cv2 import cv2
from typing import List

CAP = None
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

        for bolt_address in CURRENT_COORDINATES:
            bolt = CURRENT_COORDINATES[bolt_address]
            # color is via BGR
            cv2.circle(main_frame, (int(bolt.get('coordinate')[0]), int(bolt.get('coordinate')[1])), 5,
                       (int(bolt.get('color')[2]), int(bolt.get('color')[1]), int(bolt.get('color')[0])), 2)

        # TODO: Middel point for testing (del later)
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


def getCircleCoordinates(_center=(0, 0), _r=10, _n=10):
    return [
        [
            _center[0] + (math.cos(2 * math.pi / _n * x) * _r),  # x
            _center[1] + (math.sin(2 * math.pi / _n * x) * _r)  # y
        ] for x in range(0, _n)]


async def sendToCoordinates(bolts, coordinates):
    global CURRENT_COORDINATES
    global CURRENT_COORDINATES

    threads = []
    for i in range(len(bolts)):
        if i >= len(coordinates):
            break

        thread = threading.Thread(target=asyncio.run, args=(sendToCoordinate(bolts[i], coordinates[i]),))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()


async def sendToCoordinate(bolt, coordinate):
    global CAP, CURRENT_COORDINATES

    await bolt.setMatrixLED(0, 0, 0)
    await bolt.setFrontLEDColor(0, 0, 0)
    await bolt.setBackLEDColor(0, 0, 0)

    print(f"[!] Sending bolt {bolt.address} to X: {coordinate[0]}, Y: {coordinate[1]}")

    if CAP is None or not CAP.isOpened():
        print("[Error] Could not open webcam.")
        return

    CURRENT_COORDINATES[bolt.address] = {
        'color': bolt.color,
        'coordinate': coordinate
    }

    correct_coordinate = False
    while CAP.isOpened() and not correct_coordinate:
        ret, main_frame = CAP.read()

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
            if area > 100:
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(main_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                direction = findDirection([x, y], coordinate)

                # in right position
                if x < coordinate[0] < x + h and y < coordinate[1] < y + h:
                    # to be sure that the bolt gets the command
                    for i in range(10):
                        await bolt.roll(0, 0)

                    await bolt.setMatrixLED(bolt.color[0], bolt.color[1], bolt.color[2])
                    await bolt.setFrontLEDColor(255, 255, 255)
                    await bolt.setBackLEDColor(255, 0, 0)

                    correct_coordinate = True
                    CURRENT_COORDINATES.pop(bolt.address, None)
                else:
                    await bolt.roll(35, int(direction))

        cv2.imshow(f"Detection for {bolt.name}, coordinates: {coordinate}", main_frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            CAP.release()
            cv2.destroyAllWindows()


async def connectBolt(name):
    addresses = get_json_data("bolt_addresses.json")

    bolt_json_data = next(
        item for item in addresses if item['name'] == name)

    return SpheroBolt(bolt_json_data['address'], name, bolt_json_data['color'], bolt_json_data['low_hsv'],
                      bolt_json_data['high_hsv'])


async def run():
    global CAP

    print("[!] Starting Program")

    # Color bolts:
    # SB-B198: Red
    # SB-D4A1: Purple
    # SB-67EA: Green
    # SB-BD23: Blue
    # SB-E9BE: Gold
    # SB-4D1E: Yellow

    # bolts = [await connectBolt("SB-B198"), await connectBolt("SB-D4A1"), await connectBolt("SB-67EA"),
    #          await connectBolt("SB-BD23"), await connectBolt("SB-5D9D"), await connectBolt("SB-E9BE")]
    bolts = [await connectBolt("SB-D4A1"), await connectBolt("SB-E9BE"), await connectBolt("SB-67EA"),
             await connectBolt("SB-BD23"), await connectBolt("SB-B198"), await connectBolt("SB-4D1E")]
    for bolt in bolts:
        await bolt.connect()
        await bolt.resetYaw()
        await bolt.wake()

    print("[!] Starting camera, please wait a few moments...")
    CAP = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    thread = threading.Thread(target=asyncio.run, args=(viewMovement(),))
    thread.start()

    coordinates = getCircleCoordinates((320, 240), 175, 6)
    for i in range(0, 6):
        coordinates = [coordinates[-1]] + coordinates[:-1]

        await sendToCoordinates(bolts, coordinates)

        await asyncio.sleep(2)

    print("[!] Program completed!")

    thread.join()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())