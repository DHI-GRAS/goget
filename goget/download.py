import aiohttp
import aiofiles

async def download_file(url, target, session=None):
    if session is None:
        session = requests.Session()
    with session.get(url, stream=True) as response:
        response.raise_for_status()
        with open(target, "wb") as target_file:
            shutil.copyfileobj(response.raw, target_file)
    print("Saved file {local_filename} ({local_filesize:d})".format(
            local_filename=target,
            local_filesize=os.path.getsize(target)))
    return target


async def download_from_response(response, filepath):
    async with aiofiles.open(filepath, 'wb') as f:
        while True:
            chunk = await response.content.read(1024)
            if not chunk:
                break
            await f.write(chunk)
    return await response.release()
