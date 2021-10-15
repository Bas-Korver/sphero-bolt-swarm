from __future__ import annotations
from sphero.sphero_bolt import SpheroBolt
import asyncio
import json
import threading

# [dict[str, str]]


def get_json_data(file: str) -> list[dict[str, str]]:
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


async def run(address_dict):
    bolts = []

    bot_address = next(
        item for item in address_dict if item["name"] == "SB-D4A1")['address']
    bolt = SpheroBolt(bot_address)
    bolts.append(bolt)

    bot_address = next(
        item for item in address_dict if item["name"] == "SB-BD23")['address']
    bolt = SpheroBolt(bot_address)
    bolts.append(bolt)

    bot_address = next(
        item for item in address_dict if item["name"] == "SB-B198")['address']
    bolt = SpheroBolt(bot_address)
    bolts.append(bolt)

    for bolt in bolts:
        connected = await bolt.connect()
        if not connected:
            bolts.remove(bolt)
        else:
            await bolt.wake()
            await bolt.resetYaw()

    bolt.q.put([bolt. setMatrixLEDChar, 'A', 255, 255, 0])
    bolt.q.put([bolt. setMatrixLEDChar, 'B', 255, 255, 0])
    bolt.q.put([bolt. setMatrixLEDChar, 'C', 255, 255, 0])

    for bolt in bolts:        
        bolt.q.put([bolt.setBothLEDColors, 255, 255, 0])

    for bolt in bolts:
        bolt.q.put([bolt.roll, 50, 0, 10])
        bolt.q.put([bolt.roll, 50, 180, 10])

    # await asyncio.sleep(1)

    # for bolt in bolts:
    #     print(bolt)
    #
    #     await asyncio.sleep(0.05)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    # loop.set_debug(True)
    loop.run_until_complete(run(get_json_data('bolt_addresses.json')))
