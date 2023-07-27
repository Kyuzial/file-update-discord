import toml

class ConfigReader:
    def __init__(self, config_file="config.toml"):
        self.config_file = config_file
        self.read_config()
    
    def read_config(self):
        try:
            with open(self.config_file, "r") as config_file:
                self.config = toml.load(config_file)
        except FileNotFoundError:
            raise FileNotFoundError("Config file not found")
        
    def get(self, key):
        return self.config[key]