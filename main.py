import asyncio
import json

from sphero_bolt import SpheroBolt


def get_json_data(directory: str) -> dict:
    with open(directory) as json_file:
        return json.load(json_file)


async def run(_data):
    # mac address of sphero bolt
    bot1 = next(item for item in _data if item["name"] == "SB-B07F")['address']
    bot2 = next(item for item in _data if item["name"] == "SB-698B")['address']
    # connect to sphero bolt
    my_sphero1 = SpheroBolt(bot1)
    my_sphero2 = SpheroBolt(bot2)
    
    try:
        await my_sphero1.connect()
        await my_sphero2.connect()

        # wake sphero
        await my_sphero1.wake()
        await my_sphero2.wake()

        await my_sphero1.resetYaw()
        await my_sphero2.resetYaw()
        await asyncio.sleep(2)

        # roll in a square
        for i in range(4):
            await my_sphero1.roll(200, 90 * i)
            await my_sphero2.roll(200, 90 * i)
            await asyncio.sleep(2)

    finally:
        await my_sphero1.disconnect()
        await my_sphero2.disconnect()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    loop.run_until_complete(run(_data=get_json_data('bolt_addresses.json')))
