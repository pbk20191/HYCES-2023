# This is a sample Python script.
import asyncio
import uvloop
import aiorun
import click
import aioconsole
import commands


# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


async def main():
    asyncio.get_running_loop().set_debug(True)
    while True:
        print("enter command: ")
        value = await aioconsole.ainput(loop=asyncio.get_running_loop())
        if value == 'exit':
            break
        args = value.split(" ")
        if args is None or len(args) < 1:
            click.echo("wrong command input")
            continue
        await commands.run_command(args)
    asyncio.get_running_loop().stop()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    aiorun.run(main(), use_uvloop=True, stop_on_unhandled_errors=True)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
