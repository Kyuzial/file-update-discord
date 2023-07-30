from dotenv import load_dotenv
from utils.config_reader import ConfigReader


def load_env():
    """Load environment variables from .env file"""
    try:
        load_dotenv()
    except FileNotFoundError as exc:
        raise FileNotFoundError("Env file not found") from exc
    except Exception as exc:
        raise Exception("Error loading env file") from exc


def load_config():
    """Load config file"""
    try:
        config = ConfigReader()
        config.read_config()
    except FileNotFoundError as exc:
        raise FileNotFoundError("Config file not found") from exc
    except Exception as exc:
        raise Exception("Error loading config file") from exc
    return config


if __name__ == "__main__":
    load_env()
    load_config()
