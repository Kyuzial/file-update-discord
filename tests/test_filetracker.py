from unittest.mock import Mock

import pytest
from file_update_discord.filetracker.filetracker import (
    File,
    FileHashError,
)


class TestFile:
    @pytest.fixture
    def author(self):
        author = Mock()
        author.id = 1
        return author

    def test_init_valid_url(self, author):
        file = File("https://getsamplefiles.com/download/txt/sample-1.txt", author)
        assert file.url == "https://getsamplefiles.com/download/txt/sample-1.txt"
        assert file.userId == 1

    def test_init_invalid_url(self, author):
        with pytest.raises(ValueError):
            File("not a url", author)

    def test_getFileName(self, author):
        file = File("https://getsamplefiles.com/download/txt/sample-1.txt", author)
        assert file.fileName == "sample-1.txt"

    def test_getHash(self, author):
        file = File("https://getsamplefiles.com/download/txt/sample-1.txt", author)
        assert isinstance(file.hash, str)

    def test_getHash_download_error(self, author):
        with pytest.raises(FileHashError):
            File("http://dqdqfweferf.com/nonexistentfile.txt", author)
