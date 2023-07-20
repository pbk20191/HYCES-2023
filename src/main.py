# This is a sample Python script.
import asyncio
import sys
from Application import Application
import uvloop
import click
import commands
import os, sys
import traceback

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

async def main():    
    reader = asyncio.StreamReader(loop=asyncio.get_running_loop())
    _, _ = await asyncio.get_running_loop().connect_read_pipe(
        lambda: 
            asyncio.StreamReaderProtocol(
                stream_reader=reader, 
                loop=asyncio.get_running_loop()
            ), 
        sys.stdin
    )
    while True:
        print("enter command or --help: ")
        value = (await reader.readline()).decode()
        if not value.endswith("\n"):
            raise EOFError
        value = value.rstrip("\n")
        if value == 'exit':
            break
        args = value.split(" ")
        
        if args is None or len(args) < 1:
            click.echo("wrong command input", err=True)
            continue
        try:
            await commands.run_command(args)
        except click.UsageError as err:
            traceback.print_exception(err)
            click.echo(message=err, err=True)
    raise sys.exit(os.EX_OK)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    with Application(debug=True) as run:
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
        run(main())

# See PyCharm help at https://www.jetbrains.com/help/pycharm/