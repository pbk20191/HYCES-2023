import asyncio
import threading
import functools
from typing import Coroutine, Generator, Any, NoReturn
import asyncio.exceptions
import contextvars
import sys
import inspect


class ApplicationError(RuntimeError):
    pass


def ApplicationMain(entrypoint):
    """
    wrap the function as main entry point
    """
    def __handle_exception(queue: asyncio.Queue, loop: asyncio.AbstractEventLoop, context: dict[str, any]) -> None:
        exception = context.get("exception")
        if not isinstance(exception, Exception) and isinstance(exception, BaseException):
            raise exception
        loop.create_task(queue.put(context)).add_done_callback(lambda task: task.exception())

    @functools.wraps(entrypoint)
    def wrapper(*args, debug: bool | None = None, context: contextvars.Context | None = None, **kwargs) -> NoReturn:
        if threading.main_thread() is not threading.current_thread():
            raise ApplicationError("app.run() can only be called on main thread")
        with asyncio.Runner(debug=debug) as runner:
                queue = asyncio.Queue(1)
                exception_handler = functools.partial(__handle_exception, queue)
                runner.get_loop().set_exception_handler(exception_handler)
                async def parking() -> None:
                    while True:
                        context = {}                        
                        try:
                            context: dict[str, any] = await queue.get()
                        except asyncio.CancelledError:
                            break
                        try:
                            exception: Exception | None = context.get("exception")
                            if isinstance(exception, Exception):
                                raise ApplicationError("uncaught exception occur on main event loop") from exception
                            elif isinstance(exception, BaseException):
                                raise exception
                            else:
                                asyncio.get_running_loop().default_exception_handler(context)
                        finally:
                            queue.task_done()

                async def __app__():
                    if inspect.iscoroutinefunction(entrypoint):
                        await asyncio.gather(entrypoint(*args, **kwargs), parking())
                    else:
                        await parking()
                try:
                    if not inspect.iscoroutinefunction(entrypoint):
                        runner.get_loop().call_soon(functools.partial(entrypoint, *args, **kwargs), context=context)
                    runner.run(coro=__app__(), context=context)
                except RuntimeError as err:
                    if err.args.count == 1 and err.args[0] == 'Event loop stopped before Future completed.':
                        pass
                    else:
                        raise
        pass
    
    if inspect.iscoroutinefunction(entrypoint) or inspect.isfunction(entrypoint):
        return wrapper
    else:
        raise ApplicationError("ApplicationMain only support function")