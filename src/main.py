# This is a sample Python script.
import asyncio
import sys
import threading
import concurrent.futures.thread
import uvloop
import aiorun
import click
import selectors
import aioconsole


# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


@click.group()
def cli():
    pass


def run_command(args):
    try:
        cli.main(args=args, standalone_mode=False)
    except click.exceptions.UsageError:
        click.echo(sys.exception(), err=True)


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
        await asyncio.to_thread(lambda: run_command(args))
    asyncio.get_running_loop().stop()


@cli.command()
@click.argument("name")
def print_hi(name="PyCharm") -> None:
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


@cli.command()
@click.option("--check", is_flag=True, default=False)
def checkout(check="PyCharm") -> None:
    # Use a breakpoint in the code line below to debug your script.
    print(f'check, {check}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    aiorun.run(main(), use_uvloop=True, stop_on_unhandled_errors=True)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
