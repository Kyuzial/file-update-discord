import pytest
from file_update_discord.filetracker.filetracker import (
    File,
    FileHashError,
)


class TestFile:
    def test_init_valid_url(self):
        file = File("https://getsamplefiles.com/download/txt/sample-1.txt", 1)
        assert file.url == "https://getsamplefiles.com/download/txt/sample-1.txt"
        assert file.userId == 1

    def test_init_invalid_url(self):
        with pytest.raises(ValueError):
            File("not a url", 1)

    def test_getFileName(self):
        file = File("https://getsamplefiles.com/download/txt/sample-1.txt", 1)
        assert file.fileName == "sample-1.txt"

    def test_getHash(self):
        file = File("https://getsamplefiles.com/download/txt/sample-1.txt", 1)
        assert isinstance(file.hash, str)

    def test_getHash_download_error(self):
        with pytest.raises(FileHashError):
            File("http://dqdqfweferf.com/nonexistentfile.txt", 1)
