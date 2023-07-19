# This is a sample Python script.
import asyncio
from typing import Final
from Application import Application
import aiorun
import uvloop
import os, traceback, sys

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


async def async_main() -> None:
    print_hi('PyCharm')


def print_hi(name) -> None:
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}', app.get_event_loop() is asyncio.get_running_loop())  # Press ⌘F8 to toggle the breakpoint.


app: Final[Application] = Application(debug=True)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    aiorun.run(
        async_main(),
        use_uvloop=True,
        stop_on_unhandled_errors=True
    )
    # with app as park:
    #     park(async_main())


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
