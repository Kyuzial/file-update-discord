import tomllib
from dotenv import load_dotenv


class ConfigReader:
    def __init__(self, config_file="config.toml"):
        self.config_file = config_file
        self.read_config()

    def read_config(self):
        try:
            with open(self.config_file, "rb") as config_file:
                self.config = tomllib.load(config_file)
        except FileNotFoundError:
            raise FileNotFoundError("Config file not found")
        except Exception as exc:
            raise Exception("Error loading config file") from exc

    def get(self, key):
        return self.config.get(key)


def load_env():
    """Load environment variables from .env file"""
    try:
        load_dotenv()
    except FileNotFoundError as exc:
        raise FileNotFoundError("Env file not found") from exc
    except Exception as exc:
        raise Exception("Error loading env file") from exc
