import asyncio
import os.path
import fnmatch
import urlparse

import aiohttp
import aiofiles
import async_generator


@async_generator
async def recursive_stream(base_url, session=None, include=None, exclude=None,
                           max_connections=100, **kwargs):
    """Stream file contents"""
    try:
        from itsybitsy.async import crawl_async
    except ImportError:
        raise ImportError("itsybitsy must be installed for recursive downloading")

    limiter = asyncio.Semaphore(max_connections)

    if isinstance(include, str):
        include = [include]
    if isinstance(exclude, str):
        exclude = [exclude]

    if session is None:
        connector = aiohttp.TCPConnector(limit=None)
        session = aiohttp.Session()
        close_session = True
    else:
        close_session = False

    try:
        async for link in crawl_async(base_url, **kwargs):

            async with limiter:


    finally:
        if close_session:
            session.close()


def recursive_download(base_url, directory=".", username=None, password=None,
                       include=None, exclude=None, download_jobs=None, **kwargs):
    """
    """
    if kwargs.get("session") is None:
        session = requests.Session()
        if username and password:
            session.auth = (username, password)
        kwargs["session"] = session
    else:
        session = kwargs["session"]

    loop = asyncio.get_event_loop()
    coro = recursive_stream(...)

    for loop_over_async(coro, loop):
