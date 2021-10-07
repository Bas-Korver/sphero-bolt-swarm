from __future__ import annotations
import asyncio
import math
import json
import threading

import numpy as np
from cv2 import cv2
from typing import List

from sphero.sphero_bolt import SpheroBolt


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


async def control_bolt(_radius, _cap, _low_sat, _high_sat, _bolt, _point_x, _point_y):
    if not _cap.isOpened():
        print("Could not load the camera stream")
        return

    while _cap.isOpened():
        # ret is a boolean regarding whether or not there was a return at all
        ret, main_frame = _cap.read()

        # get middel point of image
        (height, width) = main_frame.shape[:2]
        (centerY, centerX) = (height // 2, width // 2)
        center_location_frame = (centerX, centerY)
        cv2.circle(main_frame, (centerX, centerY), 5, (0, 0, 255), 2)
        cv2.circle(main_frame, (_point_x, _point_y), 5, (0, 0, 255), 2)
        hsv_frame = cv2.medianBlur(cv2.cvtColor(main_frame, cv2.COLOR_BGR2HSV), 9)

        # use sliders.py for specific values for the situation
        lower = np.array(_low_sat, np.uint8)
        upper = np.array(_high_sat, np.uint8)
        mask = cv2.inRange(hsv_frame, lower, upper)

        contours, hierarchy = cv2.findContours(mask,
                                               cv2.RETR_TREE,
                                               cv2.CHAIN_APPROX_SIMPLE)

        # find contours and draw them
        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if area > 500:
                x, y, w, h = cv2.boundingRect(contour)
                frame = cv2.rectangle(main_frame, (x, y),
                                      (x + w, y + h),
                                      (0, 255, 0), 2)

                direction = find_direction((x, y), (_point_x, _point_y))

                # in right position
                if x < int(_point_x) < x + h and y < int(_point_y) < y + h:
                    await _bolt.roll(0, 0)
                else:
                    await _bolt.roll(50, int(direction))

        cv2.imshow("frame", main_frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            # clean all windows en stop capturing the camera feed
            _cap.release()
            cv2.destroyAllWindows()


def find_direction(_point_a, _point_b):
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
    pi = math.pi
    return [
        (
            _center[0] + (math.cos(2 * pi / _n * x) * _r),  # x
            _center[1] + (math.sin(2 * pi / _n * x) * _r)  # y
        ) for x in range(0, _n + 1)]


async def sendCoordinates(_bolts, _coordinates):
    if len(_bolts) != len(_coordinates):
        raise Exception("Amount of bolts is not equal to the amount of coordinates.")

    # for i in range(_bolts):
    # # Make thread to send BOLT to a coordinate.
    # sendCoordinate()


async def sendCoordinate(_bolt, _coordinate):
    print(f"[!] Sending bolt {_bolt.address} to X: {_coordinate[0]}, Y: {_coordinate[1]}")


async def run():
    print("Running...")
    address_dict = get_json_data('bolt_addresses.json')
    bot_address = next(
        item for item in address_dict if item['name'] == 'SB-8898')['address']
    bot_color = next(
        item for item in address_dict if item['name'] == 'SB-8898')['color']
    bot_low_sat = next(
        item for item in address_dict if item['name'] == 'SB-8898')['lowSat']
    bot_high_sat = next(
        item for item in address_dict if item['name'] == 'SB-8898')['highSat']

    bolt = SpheroBolt(bot_address, bot_color)

    await bolt.connect()
    await bolt.resetYaw()
    await bolt.wake()

    cap = cv2.VideoCapture(0)
    thread1 = threading.Thread(target=asyncio.run, args=(control_bolt(100, cap, bot_low_sat, bot_high_sat, bolt, 320, 240),))
    thread1.start()
    thread1.join()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
