import numpy as np
import math
import asyncio
import json
from cv2 import cv2
from sphero.sphero_bolt import SpheroBolt
import asyncio

point_list = []
center_location_frame = None
active_bolt = None


def pointsInCircle(center=(0, 0), r=25, n=25):
    pi = math.pi
    return [
        (
            center[0] + (math.cos(2 * pi / n * x) * r),  # x
            center[1] + (math.sin(2 * pi / n * x) * r)  # y

        ) for x in range(0, n + 1)]


# used for calculating the nearest point for the bolt
def calculate_nearest_point(_x, _y):
    dis = 0
    closest = float("inf")
    for p in point_list:
        if dis < math.sqrt((p[0] - _x) ** 2 + (p[1] - _y) ** 2):
            dis = math.sqrt((p[0] - _x) ** 2 + (p[1] - _y) ** 2)
            closest = point_list.index(p)
    return point_list[closest]


# used for controlling the bolt
def control_bolt(_x1, _x2, _y1, _y2, _closest_point):
    lat1 = math.radians(_x1)
    lat2 = math.radians(_closest_point[0])

    diff_long = math.radians(_closest_point[1] - _y1)

    x = math.sin(diff_long) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)
                                           * math.cos(lat2) * math.cos(diff_long))

    initial_bearing = math.atan2(x, y)

    initial_bearing = math.degrees(initial_bearing)
    round_bearing = (initial_bearing + 360) % 360
    return round_bearing


# ToDo finish this command
async def send_command(_speed,_direction):
    global active_bolt
    print("command send, roll: ", _direction)
    await active_bolt.roll(_speed, int(_direction))


# check if bolt is in richt position
async def checker(_x1, _y1, _x2, _y2):
    radius = 0
    correct_position = False
    # check if bolt is in the position
    for i in point_list:
        if _x1 < int(i[0]) < _x2 and _y1 < int(i[1]) < _y2:
            # print("Bolt in position")
            correct_position = True
            await send_command(0, 0)
    if not correct_position:
        # look for the nearest point for the bolt
        closest_point = calculate_nearest_point(_x1, _y1)
        distance = math.sqrt(((_x1 - closest_point[0]) ** 2) + ((_y1 - closest_point[1]) ** 2))
        radius = control_bolt(_x1, _x2, _y1, _y2, closest_point)
        if radius != 0:
            await send_command(40, radius)
            new_distance = math.sqrt(((_x1 - closest_point[0]) ** 2) + ((_y1 - closest_point[1]) ** 2))
            if new_distance > distance:
                await send_command(40, (radius+180))


# function for the webcam
async def openWebcam(_radius, _webcam=0, _tracking=True):
    global point_list
    global center_location_frame

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Could not load the camera stream")
        return

    while cap.isOpened():
        # ret is a boolean regarding whether or not there was a return at all
        ret, frame = cap.read()
        (height, width) = frame.shape[:2]
        (circleCenterH, circleCenterW) = (height//2, width//2)

        # get the center location of the frame as a global variable
        center_location_frame = (circleCenterH, circleCenterW)

        # color is via BGR
        cv2.circle(frame, (circleCenterW, circleCenterH), _radius, (0, 0, 255), 2)

        # get all locations on the line
        if not point_list:
            point_list = pointsInCircle((circleCenterW, circleCenterH), _radius, 10)

        # ToDO: for visualizing, get rid of this when done
        for i in point_list:
            cv2.circle(frame, (int(i[0]), int(i[1])), 10, (255, 0, 0))

        if _tracking:
            hsv_frame = cv2.medianBlur(cv2.cvtColor(frame, cv2.COLOR_BGR2HSV), 9)

            # use sliders.py for specific values for the situation
            lower = np.array([99, 118, 133], np.uint8)
            upper = np.array([117, 255, 202], np.uint8)
            mask = cv2.inRange(hsv_frame, lower, upper)

            contours, hierarchy = cv2.findContours(mask,
                                                   cv2.RETR_TREE,
                                                   cv2.CHAIN_APPROX_SIMPLE)
            for pic, contour in enumerate(contours):
                area = cv2.contourArea(contour)
                if area > 300:
                    x, y, w, h = cv2.boundingRect(contour)
                    frame = cv2.rectangle(frame, (x, y),
                                               (x + w, y + h),
                                               (0, 255, 0), 2)
                    # check if the position of the bolt is correct
                    await checker(x, y, (x + w), (y + h))
                else:
                    # set bolt to default
                    await send_command(0, 0)

        # ToDo: get rid of hsv_frame when done
        cv2.imshow("edit", hsv_frame)
        cv2.imshow("frame", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            # clean all windows en stop capturing the camera feed
            cap.release()
            cv2.destroyAllWindows()


async def bolt_connect():
    # call function]
    global active_bolt
    active_bolt = SpheroBolt("CC:0F:9D:DF:88:98")
    await active_bolt.connect()
    await active_bolt.wake()
    await active_bolt.resetYaw()
    await active_bolt.setMatrixLED(255, 0, 0)

    await openWebcam(100, 1)

if __name__ == "__main__":
    # call function
    loop = asyncio.get_event_loop()
    loop.set_debug(False)
    loop.run_until_complete(bolt_connect())

