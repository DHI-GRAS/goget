import os.path
import shutil
import fnmatch
from concurrent.futures import ThreadPoolExecutor, wait, as_completed


def recursive_download(base_url, directory=".", username=None, password=None, include=None, exclude=None, download_jobs=None, **kwargs):
    """
    """
    if kwargs.get("session") is None:
        session = requests.Session()
        if username and password:
            session.auth = (username, password)
        kwargs["session"] = session
    else:
        session = kwargs["session"]

    crawler = crawl_page(base_url, **kwargs)
    base_url_normalized = next(crawler)
    base_path = urlparse.urlparse(base_url_normalized).path

    if isinstance(include, str):
        include = [include]
    if isinstance(exclude, str):
        exclude = [exclude]

    futures = []
    with ThreadPoolExecutor(max_workers=download_jobs) as executor:
        for url in crawler:
            url_parts = urlparse.urlparse(url)
            file_path = url_parts.path
            assert file_path.startswith(base_path)
            target_filename = os.path.join(directory, os.path.normpath(file_path[len(base_path):]))

            if include and not any(fnmatch.fnmatch(target_filename, pattern) for pattern in include):
                continue
            if exclude and any(fnmatch.fnmatch(target_filename, pattern) for pattern in exclude):
                continue

            try:
                os.makedirs(os.path.dirname(target_filename))
            except OSError:
                pass

            futures.append(executor.submit(download_file, url, target_filename, session=session))
        wait(futures)
