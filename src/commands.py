import time
import click
import asyncio
import inspect
import gpiozero

@click.group()
def cli():
    pass

@cli.command()
@click.argument('message')
def echo(message):
    """
    print back the message
    """
    click.echo(message=message)

__led17: gpiozero.LED = None

@cli.command()
def toggle_led17():
    global __led17
    if __led17 is None:
        __led17 = gpiozero.LED(17)
    __led17.toggle()
    print(__led17)


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


