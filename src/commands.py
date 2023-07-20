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
    """print "Hi, name"

    Args:
        name (str, optional): _description_. Defaults to "PyCharm".
    """
    print(f'Hi, {name}')


@cli.command()
@click.option("--check", is_flag=True, default=False)
def checkout(check="PyCharm") -> None:
    """
    print if flags is checked or not
    """
    print(f'check, {check}')

@cli.command()
async def async_run() -> None:
    """
        run infinite nonblocking loop printing "async-run" every 2 seconds
    """
    while True:
        print('async_run')
        await asyncio.sleep(2)


@cli.command()
def sync_run() -> None:
    """
        run infinite blocking loop printing "sync-run" every 2 seconds
    """
    while True:
        print('sync_run')
        time.sleep(2)

@cli.command()
@click.argument('message')
def echo(message):
    """
    print back the message
    """
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