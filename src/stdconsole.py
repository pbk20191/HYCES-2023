import io, sys, os, asyncio
from typing import Generator, AsyncGenerator, Any


async def input_sequence() -> AsyncGenerator[str, Any] :
    loop = asyncio.get_running_loop()
    with os.fdopen(fd=os.dup(sys.stdin.fileno())) as file:
        if sys.platform == "win32":
            from msvcrt import get_osfhandle
            from asyncio.windows_events import ProactorEventLoop, IocpProactor
            proactor: None | IocpProactor = None
            if isinstance(loop, ProactorEventLoop):
                proactor = loop._proactor
                if isinstance(proactor, IocpProactor):
                    pass
                else:
                    raise RuntimeError(f'loop._proactor is not {IocpProactor} but {loop._proactor} found')
                pass
            else:
                raise RuntimeError("running loop must be a ProactorEventLoop")
            file_handle = get_osfhandle(file.fileno())
            while await proactor.wait_for_handle(file_handle):
                value = file.readline()
                if value == '' or value == '\0':
                    break
                yield value.removesuffix('\n')
        else:
            os.set_blocking(file.fileno(), False)
            reader = asyncio.StreamReader(loop=loop)
            r_transport, r_protocol = await loop.connect_read_pipe(
                lambda: asyncio.StreamReaderProtocol(reader, loop=loop),
                file
            )
            try:
                while not reader.at_eof():
                    value = (await reader.readline()).decode()
                    if not reader.at_eof():
                        yield value.removesuffix('\n')
            finally:
                r_transport.close()
                event = asyncio.Event()
                loop.call_soon(event.set)
                await event.wait()
