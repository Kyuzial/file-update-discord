import pytest
from file_update_discord.utils.config_reader import ConfigReader

def test_load_config():
    with pytest.raises(FileNotFoundError):
        ConfigReader("nonexistent.toml")

