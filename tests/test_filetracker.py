import pytest
from file_update_discord.filetracker.filetracker import (
    File,
    FileHashError,
)


class TestFile:
    def test_init_valid_url(self):
        file = File("https://raw.githubusercontent.com/Kyuzial/file-update-discord/main/LICENSE", 1)
        assert file.url == "https://raw.githubusercontent.com/Kyuzial/file-update-discord/main/LICENSE"
        assert file.userId == 1

    def test_init_invalid_url(self):
        with pytest.raises(ValueError):
            File("not a url", 1)

    def test_getFileName(self):
        file = File("https://raw.githubusercontent.com/Kyuzial/file-update-discord/main/LICENSE", 1)
        assert file.fileName == "LICENSE"

    def test_getHash(self):
        file = File("https://raw.githubusercontent.com/Kyuzial/file-update-discord/main/LICENSE", 1)
        assert isinstance(file.hash, str)

    def test_getHash_download_error(self):
        with pytest.raises(FileHashError):
            File("http://dqdqfweferf.com/nonexistentfile.txt", 1)
