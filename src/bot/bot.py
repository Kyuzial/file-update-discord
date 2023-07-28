from utils.config_reader import ConfigReader
from dotenv import load_dotenv

try:
    load_dotenv()
except FileNotFoundError as exc:
    raise FileNotFoundError("Env file not found") from exc
except Exception as exc:
    raise Exception("Error loading env file") from exc

config_reader = ConfigReader()
