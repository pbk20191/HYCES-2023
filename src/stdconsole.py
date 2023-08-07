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
                from win32event import WaitForMultipleObjects, INFINITE, CreateEvent, SetEvent
                from msvcrt import get_osfhandle
                from win32con import WAIT_TIMEOUT, WAIT_FAILED, WAIT_OBJECT_0, WAIT_ABANDONED_0
                from win32api import GetLastError, CloseHandle
                event_handle = CreateEvent(None, True, False, None)
                final_event = asyncio.Event()
                queue = asyncio.Queue()
                file_handle = get_osfhandle(file.fileno())
                try:
                    def callback():
                        try:
                            while loop.is_running():
                                code = WaitForMultipleObjects([file_handle, event_handle], False, INFINITE)
                                if code == WAIT_TIMEOUT:
                                    continue
                                if code == WAIT_FAILED:
                                    win_error = GetLastError()
                                    error = WindowsError(None, os.strerror(win_error), None, win_error, None)
                                    loop.call_soon_threadsafe(lambda: loop.create_task(queue.put(error)))
                                    return
                                if code == WAIT_OBJECT_0:
                                    value = file.readline()
                                    if value == '' or value == '\0':
                                        loop.call_soon_threadsafe(lambda: loop.create_task(queue.put('')))
                                        break
                                    else:
                                        loop.call_soon_threadsafe(lambda: loop.create_task(queue.put(value)))
                                    continue
                                if code == WAIT_OBJECT_0 + 1:
                                    loop.call_soon_threadsafe(lambda: loop.create_task(queue.put(None)))
                                    return
                        finally:
                            loop.call_soon_threadsafe(final_event.set)
                    job = asyncio.to_thread(callback)
                    loop.create_task(job)
                    while True:
                        item = await queue.get()
                        if item is None:
                            break
                        if item == '\0':
                            return
                        if isinstance(item, Exception):
                            raise item
                        if isinstance(item, str):
                            yield item.removesuffix('\n')
                finally:
                    SetEvent(event_handle)
                    await final_event.wait()
                    CloseHandle(event_handle)
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
   
