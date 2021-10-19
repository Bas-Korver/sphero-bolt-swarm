import struct
import asyncio
import threading
import queue
from datetime import datetime, timedelta
from sphero import sphero_constants
from bleak import BleakClient, BleakError

class CustomError(Exception):
    pass

class SpheroBolt:
    def __init__(self, address, name, color=[255, 255, 255], low_hsv=[0, 0, 0], high_hsv=[0, 0, 0]):
        self.sequence = 0
        self.address = address
        self.name = name
        self.color = color
        self.low_hsv = low_hsv
        self.high_hsv = high_hsv
        self.notificationPacket = []
        self.q = queue.Queue()


    async def queueRun(self):
        while True:
            task = self.q.get()
            
            func = task[0]            
            args = task[1:]
            
            await func(*args)
            
            self.q.task_done()
            
            
    async def connect(self):
        """
        Connects to a Sphero Bolt of a specified MAC address if it can find it.
        """

        self.client = BleakClient(self.address)
        await self.client.connect()
        print("Connected: {0}".format(self.client.is_connected))

        # cancel if not connected
        if not self.client.is_connected:
            return False

        # get device name
        try:
            DEVICE_NAME_UUID = "00002A00-0000-1000-8000-00805f9b34fb"
            device_name = await self.client.read_gatt_char(DEVICE_NAME_UUID)
            print("Device Name: {0}".format("".join(map(chr, device_name))))
        except Exception:
            pass

        # self.sphero_constants.APIV2_CHARACTERISTIC = "00010002-574f-4f20-5370-6865726f2121"
        AntiDOS_characteristic = "00020005-574f-4f20-5370-6865726f2121"

        # Unlock code: prevent the sphero mini
        # from going to sleep again after 10 seconds
        print("[INIT] Writing AntiDOS characteristic unlock code")
        await self.client.write_gatt_char(AntiDOS_characteristic,
                                          b"usetheforce...band",
                                          response=True)

        thread = threading.Thread(target=asyncio.run, args=(self.queueRun(),))
        thread.start()

        await self.setMatrixLED(self.color[0], self.color[1], self.color[2])
        await self.setFrontLEDColor(255, 255, 255)
        await self.setBackLEDColor(255, 0, 0)

        print("[INIT] Initialization complete\n")

        return True

    async def disconnect(self):
        """
        Disconnects the Sphero Bolt
        """
        return await self.client.disconnect()

    async def send(self, characteristic=None, devID=None,
                   commID=None, targetId=None, data=[]):
        """
        Generate databytes of command using input dictionary
        This protocol copied completely from JS library
        Messages are represented as:
        [start flags targetID sourceID deviceID commandID seqNum data
        checksum end]
        The flags byte indicates which fields are populated.
        The checksum is the ~sum(message[1:-2]) | 0xff.
        """
        self.sequence = (self.sequence + 1) % 256
        running_sum = 0
        command = []
        command.append(sphero_constants.API_CONSTANTS["startOfPacket"])
        if targetId is None:
            cmdflg = (sphero_constants.FLAGS["requestsResponse"] |
                      sphero_constants.FLAGS["resetsInactivityTimeout"] |
                      0)
            command.append(cmdflg)
            running_sum += cmdflg
        else:
            cmdflg = (sphero_constants.FLAGS["requestsResponse"] |
                      sphero_constants.FLAGS["resetsInactivityTimeout"] |
                      targetId)
            command.append(cmdflg)
            running_sum += cmdflg
            command.append(targetId)
            running_sum += targetId

        command.append(devID)
        running_sum += devID
        command.append(commID)
        running_sum += commID
        command.append(self.sequence)
        running_sum += self.sequence

        if data is not None:
            for datum in data:
                self.checkBytes(command, datum)
                running_sum += datum
        checksum = (~running_sum) & 0xff
        self.checkBytes(command, checksum)

        command.append(sphero_constants.API_CONSTANTS["endOfPacket"])

        await self.client.write_gatt_char(characteristic, command)

    async def wake(self):
        """
        Bring device out of sleep mode (can only be done if device was in
        sleep, not deep sleep).\n
        If in deep sleep, the device should be connected to USB power to wake.
        """
        print("[SEND {}] Waking".format(self.sequence))

        await self.send(
            characteristic=sphero_constants.APIV2_CHARACTERISTIC,
            devID=sphero_constants.DEVICE_ID["powerInfo"],
            commID=sphero_constants.POWER_COMMAND_IDS["wake"],
            data=[])  # empty payload

    async def setBothLEDColors(self, red=None, green=None, blue=None):
        """
        Set device LED color based on RGB vales
        (each can  range between 0 and 0xFF).
        """
        print("[SEND {}] Setting front LED colour to [{}, {}, {}]".format(
            self.sequence, red, green, blue))

        await self.send(characteristic=sphero_constants.APIV2_CHARACTERISTIC,
                        devID=sphero_constants.DEVICE_ID["userIO"],
                        commID=sphero_constants.USER_IO_COMMAND_IDS["allLEDs"],
                        data=[0x3f, red, green, blue, red, green, blue])

    async def setFrontLEDColor(self, red=None, green=None, blue=None):
        """
        Set device front LED color based on RGB vales
        (each can  range between 0 and 0xFF).
        """
        print("[SEND {}] Setting front LED colour to [{}, {}, {}]".format(
            self.sequence, red, green, blue))

        await self.send(characteristic=sphero_constants.APIV2_CHARACTERISTIC,
                        devID=sphero_constants.DEVICE_ID["userIO"],
                        commID=sphero_constants.USER_IO_COMMAND_IDS["allLEDs"],
                        data=[0x07, red, green, blue])

    async def setBackLEDColor(self, red=None, green=None, blue=None):
        """
        Set device back LED color based on RGB vales
        (each can  range between 0 and 0xFF).
        """
        print("[SEND {}] Setting back LED colour to [{}, {}, {}]".format(
            self.sequence, red, green, blue))

        await self.send(characteristic=sphero_constants.APIV2_CHARACTERISTIC,
                        devID=sphero_constants.DEVICE_ID["userIO"],
                        commID=sphero_constants.USER_IO_COMMAND_IDS["allLEDs"],
                        data=[0x38, red, green, blue])

    async def setMatrixLED(self, red=None, green=None, blue=None):
        """
        Set the LED matrix based on RBG values.
        """
        print("[SEND {}] Setting matrix LED colour to [{}, {}, {}]".format(
            self.sequence, red, green, blue))
        await self.send(
            characteristic=sphero_constants.APIV2_CHARACTERISTIC,
            devID=sphero_constants.DEVICE_ID["userIO"],
            commID=sphero_constants.USER_IO_COMMAND_IDS["matrixColor"],
            targetId=0x012,
            data=[red, green, blue]
        )

    async def setMatrixLEDChar(self, char=None, red=None,
                               green=None, blue=None):
        """
        Write a character to the LED matrix, with a colour based on RGB values.
        """
        print('setting matrix color')
        print("[SEND {}] Setting matrix char to ' {} \
              ' LED colour to [{}, {}, {}]".format(
            self.sequence, char, red, green, blue))
        await self.send(
            characteristic=sphero_constants.APIV2_CHARACTERISTIC,
            devID=sphero_constants.DEVICE_ID["userIO"],
            commID=sphero_constants.USER_IO_COMMAND_IDS["printChar"],
            targetId=0x012,
            data=[red, green, blue, ord(char)]
        )

    async def roll(self, speed: int, heading: int, time: int = None):
        """        Rolls the device at a specified speed (int between 0 and 255)
        heading (int between 0 and 359) and time (int in seconds).
        Data is format [speed, heading byte 1, heading byte 2,
        direction (0-forward, 1-back)].

        Parameters
        ----------
        speed : int
            Speed of the bot.
        heading : int
            Heading of the bot.
        time : int, optional
            Let the bot drive for an amount of time, by default None.
        """

        if time:
            run_command_till = datetime.now() + timedelta(seconds=time)
            while datetime.now() + timedelta(seconds=1) < run_command_till:
                await self.roll(speed, heading)
        else:
            # print("[SEND {}] Rolling with speed {} and heading {}".format(
            #     self.sequence, speed, heading))
            await self.send(
                characteristic=sphero_constants.APIV2_CHARACTERISTIC,
                devID=sphero_constants.DEVICE_ID["driving"],
                commID=sphero_constants.DRIVING_COMMAND_IDS["driveWithHeading"],
                targetId=0x012,
                data=[speed, (heading >> 8) & 0xff, heading & 0xff, 0]
            )

            # await asyncio.sleep(2)

    async def resetYaw(self):
        print("[SEND {}] Resetting yaw".format(self.sequence))

        await self.send(
            characteristic=sphero_constants.APIV2_CHARACTERISTIC,
            devID=sphero_constants.DEVICE_ID["driving"],
            commID=sphero_constants.DRIVING_COMMAND_IDS["resetYaw"],
            data=[]
        )

    def bitsToNum(self, bits):
        """
        This helper function decodes bytes from sensor packets into single
        precision floats. Encoding follows the
        the IEEE-754 standard.
        """
        num = int(bits, 2).to_bytes(len(bits) // 8, byteorder='little')
        num = struct.unpack('f', num)[0]
        return num

    def checkBytes(self, command: list, byte: int) -> list:
        if byte == sphero_constants.API_CONSTANTS["startOfPacket"]:
            command.extend([
                sphero_constants.API_CONSTANTS["escape"],
                sphero_constants.API_CONSTANTS["escapedStartOfPacket"]
            ])
            return command

        elif byte == sphero_constants.API_CONSTANTS["escape"]:
            command.extend([
                sphero_constants.API_CONSTANTS["escape"],
                sphero_constants.API_CONSTANTS["escapedEscape"]
            ])
            return command

        elif byte == sphero_constants.API_CONSTANTS["endOfPacket"]:
            command.extend([
                sphero_constants.API_CONSTANTS["escape"],
                sphero_constants.API_CONSTANTS["escapedEndOfPacket"]
            ])
            return command

        else:
            return command.append(byte)
