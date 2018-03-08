import asyncio
import os.path
import fnmatch
import urllib.parse as urlparse
import logging
import warnings

import aiohttp
import aiofiles
from async_generator import async_generator, yield_

from goget.download import download_from_response
from goget.utilities.session import default_session

logger = logging.getLogger(__name__)


async def stream_recursive(base_url, session=None, include=None, exclude=None,
                           max_connections=100, **kwargs):
    """Stream file contents"""
    try:
        from itsybitsy import crawl_async
    except ImportError:
        raise ImportError("itsybitsy must be installed for recursive downloading")

    close_session = False
    if session is None:
        session = default_session()
        close_session = True

    limiter = asyncio.Semaphore(max_connections)

    if isinstance(include, str):
        include = [include]
    if isinstance(exclude, str):
        exclude = [exclude]

    crawler = crawl_async(base_url, session=session, **kwargs)

    #base_url_normalized = await crawler.__anext__()
    base_path = "%s#%s" % (urlparse.urlparse(base_url).path, urlparse.urlparse(base_url).fragment)
    print(base_path)

    try:
        async for url in crawler:
            logger.debug("> found link: %s", url)
            url_parts = urlparse.urlparse(url)
            file_path = url_parts.path
            if not file_path.startswith(base_path):
                warnings.warn("File {} does not match base path {} - skipping"
                              .format(file_path, base_path))
                continue

            target_localpath = os.path.normpath(file_path[len(base_path):])

            if include and not any(fnmatch.fnmatch(target_localpath, pattern) for pattern in include):
                logger.debug(">> skipping due to include pattern")
                continue
            if exclude and any(fnmatch.fnmatch(target_localpath, pattern) for pattern in exclude):
                logger.debug(">> skipping due to exclude pattern")
                continue

            logger.debug(">> downloading")
            async with limiter:
                async with session.get(url) as response:
                    yield (target_localpath, response)

    finally:
        if close_session:
            session.close()


async def download_recursive(base_url, directory=".", session=None, include=None, exclude=None,
                             max_connections=100, **kwargs):
    """
    """
    close_session = False
    if session is None:
        session = default_session()
        close_session = True

    try:
        async for target_path, response in stream_recursive(base_url, session=session, include=include,
                                                            exclude=exclude, max_connections=max_connections,
                                                            **kwargs):
            target_path = os.path.join(directory, target_path)
            try:
                os.makedirs(os.path.dirname(target_path))
            except OSError:
                pass
            await download_from_response(response, target_path)
    finally:
        if close_session:
            session.close()
