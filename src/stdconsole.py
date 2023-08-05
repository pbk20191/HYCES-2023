from contextlib import asynccontextmanager, contextmanager
import io, sys, os, asyncio
from typing import Generator, AsyncGenerator, Any
import platform
import threading, multiprocessing, contextlib

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
    with os.fdopen(fd=os.dup(sys.stdin.fileno())) as file:
        if sys.platform == "win32":
            mp_r_pipe, mp_w_pipe = multiprocessing.Pipe(False)
            with mp_r_pipe, mp_w_pipe:
                reader = asyncio.StreamReader(loop=loop)
                r_transport, r_protocol = await loop.connect_read_pipe(
                    lambda: asyncio.StreamReaderProtocol(reader, loop=loop),
                    mp_r_pipe
                )
                reader_process = multiprocessing.Process(target=__input_worker, name=None, daemon=True, args=[mp_w_pipe, sys.stdin.fileno()])
                try:
                    reader_process.start()
                    while not reader.at_eof():
                        value = (await reader.readline()).decode()
                        if reader.at_eof() :
                            break
                        yield value.removesuffix('\n')
                finally:
                    reader_process.terminate()
                    r_transport.close()
                    event = asyncio.Event()
                    loop.call_soon(event.set)
                    await event.wait()
        else:
            event = asyncio.Event()
            message: str | None | Exception = None
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

if sys.platform == 'win32':
    from multiprocessing.connection import PipeConnection as mp_pipe_connection
    def __input_worker(mp_pipe: mp_pipe_connection, fd:int):
        with os.fdopen(fd=fd, mode='rt', closefd=False) as file:
            sys.stdin = file
            while True:
                value = None
                try:
                    value = input('\0')
                except EOFError:
                    mp_pipe.send_bytes(''.encode())
                    return
                except:
                    mp_pipe.send_bytes(''.encode())
                    raise
                if value == '' or value == '\0':
                    mp_pipe.send_bytes('\n'.encode())
                else:
                    mp_pipe.send_bytes(value.removesuffix('\n').encode())
                    mp_pipe.send_bytes('\n'.encode())
            

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
