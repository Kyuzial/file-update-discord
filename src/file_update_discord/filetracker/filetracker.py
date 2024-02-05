import hashlib
import tempfile
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

import validators


class FileDownloadError(Exception):
    pass


class FileHashError(Exception):
    pass


class File:
    def __init__(self, url, author):
        if not validators.url(url):
            raise ValueError(f"Invalid URL: {url}")
        else:
            self.url = url
            self.fileName = None
            self.getFileName()
            self.hash = self.getHash()
            self.userId = author.id

    def getFileName(self):
        path = urlparse(self.url).path
        self.fileName = Path(path).name

    def getHash(self):
        with tempfile.NamedTemporaryFile() as file:
            try:
                file.write(urllib.request.urlopen(self.url).read())
                file.seek(0)
                return hashlib.sha256(file.read()).hexdigest()
            except urllib.error.HTTPError as exc:
                raise FileDownloadError(f"Error while downloading file: {exc}")
            except Exception as exc:
                raise FileHashError(f"Error while hashing file: {exc}")
