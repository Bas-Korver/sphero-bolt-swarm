APIV2_CHARACTERISTIC = "00010002-574f-4f20-5370-6865726f2121"
ANTIDOS_CHARACTERISTIC = "00020005-574f-4f20-5370-6865726f2121"
DEVICE_NAME_UUID = "00002A00-0000-1000-8000-00805f9b34fb"

API_CONSTANTS = {
    "startOfPacket": 141,
    "escape": 171,
    "endOfPacket": 216,
    "escapeMask": 136,
    "escapedStartOfPacket": 5,
    "escapedEscape": 35,
    "escapedEndOfPacket": 80,
}

DEVICE_ID = {
    "apiProcessor": 16,
    "systemInfo": 17,
    "powerInfo": 19,
    "driving": 22,
    "sensor": 24,
    "userIO": 26,
}

DRIVING_COMMAND_IDS = {
    "rawMotor": 1,
    "driveAsRc": 2,
    "driveAsSphero": 4,
    "resetYaw": 6,
    "driveWithHeading": 7,
    "tankDrive": 8,
    "stabilization": 12,
}

FLAGS = {
    "isResponse": 1,
    "requestsResponse": 2,
    "requestsOnlyErrorResponse": 4,
    "resetsInactivityTimeout": 8,
    "commandHasTargetId": 16,
    "commandHasSourceId": 32
}

POWER_COMMAND_IDS = {"wake": 13}

USER_IO_COMMAND_IDS = {
    "allLEDs": 28,
    "matrixPixel": 45,
    "matrixColor": 47,
    "printChar": 66
}
