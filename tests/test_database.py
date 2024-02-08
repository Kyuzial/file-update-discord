import pytest
from file_update_discord.filetracker.database import Database


def test_validation_bad_url():
    with pytest.raises(ValueError):
        Database().file_exists("grgredfgsde")


def test_validation_good_url():
    assert Database().file_exists("https://google.com") is False
