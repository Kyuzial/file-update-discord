import pytest

from bot.utils.config_reader import ConfigReader


def test_load_config():
    with pytest.raises(FileNotFoundError):
        ConfigReader("does_not_exist.toml")
