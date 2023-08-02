# This is a sample Python script.
import asyncio
import sys
from typing import NoReturn
from Application import ApplicationMain
import uvloop
import click
import commands
import os, sys
import traceback
import click.parser as click_parser
import stdconsole
# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

@ApplicationMain
async def main() -> NoReturn:   
    async for value in stdconsole.input_sequence():
        print("enter command or --help: ")
        if value == 'exit':
            break
        args = click_parser.split_arg_string(value)
    
        try:
            await commands.run_command(args)
        except click.UsageError as err:
            traceback.print_exception(err)
            click.echo(message=err, err=True)

    sys.exit(os.EX_OK)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    uvloop.install()
    print(os.getenv('GPIOZERO_PIN_FACTORY'))
    main(debug=True)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/