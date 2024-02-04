import pytest
from file_update_discord.utils import config_reader


def test_load_config():
    with pytest.raises(FileNotFoundError):
        config_reader.ConfigReader("nonexistent.toml")
