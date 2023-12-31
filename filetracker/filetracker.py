import hashlib
import tempfile
import urllib.request
from pathlib import Path
from urllib.parse import urlparse


class File:
    def __init__(self, url, author):
        result = urlparse(url)
        if all([result.scheme, result.netloc]):
            self.url = url
        else:
            raise ValueError("Invalid URL")
        self.fileName = None
        self.getFileName()
        self.hash = self.getHash()
        self.author = author

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
                print(f"Error while downloading file: {exc}")
                return None
            except Exception as exc:
                print(f"Error while hashing file: {exc}")
                return None
