import pytest
from bot.bot import load_config


def test_load_env():
    with pytest.raises(FileNotFoundError):
        load_config
