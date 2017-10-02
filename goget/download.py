def download_file(url, target, session=None):
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
