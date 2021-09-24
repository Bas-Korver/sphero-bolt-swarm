import asyncio

from sphero_bolt import SpheroBolt


async def run():
    # mac address of sphero bolt
    address1 = (
        "C7:40:82:E0:B0:7F"
    )
    address2 = (
        "FE:45:A2:E7:B1:98"
    )

    # connect to sphero bolt
    my_sphero1 = SpheroBolt(address1)
    my_sphero2 = SpheroBolt(address2)
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
            await my_sphero1.roll(50, 90 * i)
            await my_sphero2.roll(50, 90 * i)
            await asyncio.sleep(2)

    finally:
        await my_sphero1.disconnect()
        await my_sphero2.disconnect()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    loop.run_until_complete(run())
