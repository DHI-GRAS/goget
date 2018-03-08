import asyncio

def async_for(coro, loop=None):
    if loop is None:
        loop = asyncio.get_event_loop()
    try:
        coro_generator = coro.__aiter__()
    except AttributeError:
        raise ValueError("Wrapped argument must be an async generator")
    try:
        while True:
            task = coro_generator.__anext__()
            yield loop.run_until_complete(task)
    except StopAsyncIteration:
        raise StopIteration
    finally:
        loop.run_until_complete(coro_generator.aclose())
