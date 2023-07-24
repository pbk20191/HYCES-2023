import time
import click
import asyncio
import inspect

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
        asyncio.set_event_loop(loop)
        try:
            value = cli(args=args, standalone_mode=False)
        except:
            acceptor.set_result(None)
            raise
        if inspect.isawaitable(value):
            acceptor.set_result(value)
        else:
            acceptor.set_result(None)
    await asyncio.to_thread(submit)
    awaitable = await acceptor
    if awaitable is not None:
        await awaitable