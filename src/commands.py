import concurrent.futures.thread
import sys
import threading
import time
import click
import asyncio


@click.group()
def cli():
    pass


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


@cli.command()
async def async_run() -> None:
    # Use a breakpoint in the code line below to debug your script.
    while True:
        print('async_run')  # Press ⌘F8 to toggle the breakpoint.
        await asyncio.sleep(2)


@cli.command()
def sync_run() -> None:
    # Use a breakpoint in the code line below to debug your script.
    while True:
        print('sync_run')  # Press ⌘F8 to toggle the breakpoint.
        time.sleep(2)

@cli.command()
@click.argument('message')
def echo(message):
    click.echo(message=message)


async def run_command(args):
    acceptor = asyncio.Future()
    loop = asyncio.get_running_loop()

    def submit():
        try:
            asyncio.set_event_loop(loop)
            value = cli.main(args=args, standalone_mode=False)
            if asyncio.iscoroutine(value) or asyncio.isfuture(value):
                acceptor.set_result(value)
            else:
                acceptor.set_result(None)
        except click.exceptions.UsageError:
            click.echo(sys.exception(), err=True)
            

    await asyncio.to_thread(submit)
    if not acceptor.done():
        acceptor.set_result(None)
    awaitable = await acceptor
    if awaitable is not None:
        await awaitable