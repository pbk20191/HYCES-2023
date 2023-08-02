# This is a sample Python script.
import asyncio
import sys
from Application import ApplicationMain
import uvloop
import click
import commands
import os, sys
import traceback
import logging
from click.parser import split_arg_string
import stdconsole

@ApplicationMain
async def main():    
    logger = logging.getLogger().getChild("command")

    await commands.run_command(None)
    async for message in stdconsole.input_sequence():
        if message == 'exit':
            break
        args = split_arg_string(message)
        
        if args is None or len(args) < 1:
            click.echo("wrong command input", err=True)
            continue
        try:
            await commands.run_command(args)
        except click.UsageError as err:
            logger.exception(err)
            click.echo(message=err, err=True)
    raise sys.exit()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    uvloop.install()
    main(debug=True)