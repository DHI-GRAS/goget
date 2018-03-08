import aiohttp


def default_session():
    connector = aiohttp.TCPConnector(limit=None, verify_ssl=False)
    session = aiohttp.ClientSession(connector=connector)
    return session
