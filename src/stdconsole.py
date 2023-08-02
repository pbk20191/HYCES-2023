from contextlib import asynccontextmanager, contextmanager
import io, sys, os, asyncio
from typing import Generator, AsyncGenerator, Any
import platform


@asynccontextmanager
async def alloc_stdin_stream() -> Generator[asyncio.StreamReader, None, None]:
    loop = asyncio.get_running_loop()
    transport = None
    try:
        with io.open(file=os.dup(sys.stdin.fileno()), mode='r', encoding='utf-8') as file:
            reader = asyncio.StreamReader(loop=loop)
            print("fd file is ", file.fileno())
            transport, protocol = await loop.connect_read_pipe(
                lambda: asyncio.StreamReaderProtocol(stream_reader=reader, loop=loop),
                pipe=file
            )
            yield reader
    finally:
        transport.close()
        idle_token = asyncio.futures.Future()
        loop.call_soon(lambda: idle_token.set_result(None))
        if loop.is_running():
            await idle_token
        pass


async def input_sequence() -> AsyncGenerator[str, Any] :
    loop = asyncio.get_running_loop()
    event = asyncio.Event()
    message: str | None | Exception = None
    with os.fdopen(fd=os.dup(sys.stdin.fileno())) as file:
        os.set_blocking(file.fileno(), False)
        def callback():
            nonlocal message
            if event.is_set():
                return
            try:
                message = file.readline()
            except:
                message = sys.exception()       
            event.set()
        loop.add_reader(file, callback)
        try:
            while True:
                await event.wait()
                print(message)
                if isinstance(message, str):
                    value: str = message
                    if value == '':
                        break
                    else:
                        yield value.removesuffix('\n')
                elif message is None:
                    pass
                else:
                    raise message
                message = None
                event.clear()
        finally:
            loop.remove_reader(file)

async def readLine(file:io.TextIOWrapper) -> str:
    loop = asyncio.get_running_loop()
    token = loop.create_future()
    def callback():
        try:
            message = file.readline()
            if message == '':
                raise EOFError
            else:
                token.set_result(message.removesuffix('\n'))
        except:
            token.set_exception(sys.exception())     
    loop.add_reader(file, callback)
    try:
        return await token
    finally:
        loop.remove_reader(file)
    
async def read_std_in() -> str:
    loop = asyncio.get_running_loop()
    token = loop.create_future()
