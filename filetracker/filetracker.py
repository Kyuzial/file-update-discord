import urllib.request
import os.path
import hashlib
import tempfile
from urllib.parse import urlparse


class File:
    def __init__(self, url):
        self.url = url
        self.fileName = None
        self.getFileName()
        self.hash = self.getHash()

    def getFileName(self):
        path = urlparse(self.url).path
        self.fileName = os.path.basename(path)

    def getHash(self):
        with tempfile.NamedTemporaryFile() as file:
            file.write(urllib.request.urlopen(self.url).read())
            file.seek(0)
            return hashlib.sha256(file.read()).hexdigest()
