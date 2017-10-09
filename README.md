# goget, a real go-getter
Think a multi-threaded, streaming-capable `wget` for Python 3.

## Requirements

`goget` uses the powerful coroutine syntax (`async def` / `await`) introduced in Python 3.5. As such, **it is not compatible to any Python version below 3.5**.

`goget` only depends on a couple of third-party packages, the most important one being `aiohttp`. You can install it via

```
pip install aiohttp
```

To use recursive downloading of a HTML tree, you will also have to install [itsybitsy](https://github.com/DHI-GRAS/itsybitsy) and its dependencies.
