import asyncio
import threading
import functools
from typing import Coroutine, Generator, Any
import asyncio.exceptions


class Application:

    def __init__(self, debug: bool | None = None):
        self.__event_loop: None | asyncio.AbstractEventLoop = None
        self.__debug = debug
        super().__init__()

    def get_event_loop(self) -> None | asyncio.AbstractEventLoop:
        return self.__event_loop

    @staticmethod
    def __handle_exception(queue: asyncio.Queue, loop: asyncio.AbstractEventLoop, context: dict[str, any]) -> None:
        exception = context.get("exception")
        if not isinstance(exception, Exception) and isinstance(exception, BaseException):
            raise exception
        loop.create_task(queue.put(context))

    def __run_with_startup(self, coro: Coroutine[Any, Any, None] | Generator[Any, None, None]) -> None:
        """
        create and run the main event loop. This method unlikely to return
        """
        if threading.main_thread() is not threading.current_thread():
            raise ApplicationError("app.run() can only be called on main thread")
        if self.__event_loop is not None:
            raise ApplicationError("app.run() should be called at most once at a time")
        try:
            with asyncio.Runner(debug=self.__debug) as runner:
                queue = asyncio.Queue(1)
                exception_handler = functools.partial(self.__handle_exception, queue)
                self.__event_loop = runner.get_loop()
                runner.get_loop().set_exception_handler(handler=exception_handler)

                async def parking() -> None:
                    while True:
                        context: dict[str, any] = await queue.get()
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
                    await asyncio.gather(coro, parking())

                runner.run(__app__())
        finally:
            self.__event_loop = None

    def __enter__(self):
        return self.__run_with_startup

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class ApplicationError(RuntimeError):
    pass
