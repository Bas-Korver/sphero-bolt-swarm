import asyncio
import json
import threading
from sphero.sphero_bolt import SpheroBolt


# [dict[str, str]]
def get_json_data(file: str) -> list:
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

    bot = next(
        item for item in address_dict if item["name"] == "SB-36C3")['address']
    bolts.append(SpheroBolt(bot))
    bot = next(
        item for item in address_dict if item["name"] == "SB-5D9D")['address']
    bolts.append(SpheroBolt(bot))

    try:
        for bolt in bolts:
            connected = await bolt.connect()
            if not connected:
                bolts.remove(bolt)
            else:
                await bolt.wake()
                await bolt.resetYaw()

        for bolt in bolts:
            await bolt.setMatrixLED(255, 255, 0)
            await bolt.setBothLEDColors(255, 255, 0)

        threads = []

        for bolt in bolts:
            thread = threading.Thread(
                target=asyncio.run, args=(bolt.roll(200, 0, 5),))
            threads.append(thread)

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        threads = []

        for bolt in bolts:
            thread = threading.Thread(
                target=asyncio.run, args=(bolt.roll(200, 180, 5),))
            threads.append(thread)

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

    finally:
        for bolt in bolts:
            await bolt.disconnect()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    loop.run_until_complete(run(get_json_data('bolt_addresses.json')))
