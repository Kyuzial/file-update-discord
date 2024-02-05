import sqlite3

from file_update_discord.utils.config_reader import ConfigReader

dbConfig = ConfigReader().config.get("filetracker")


class Database(object):
    DATABASE = dbConfig["dbPath"]

    def __init__(self):
        self.connection = sqlite3.connect(self.DATABASE)
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS files (hash TEXT, url TEXT, fileName TEXT, userId INT)"
        )

    def add_file(self, file):
        print(file.userId)
        self.cursor.execute(
            "INSERT INTO files (hash, url, fileName, userId) VALUES (?, ?, ?, ?)",
            (file.hash, file.url, file.fileName, file.userId),
        )
        self.connection.commit()

    def file_exists(self, url):
        self.cursor.execute("SELECT * FROM files WHERE url=?", [url])
        return self.cursor.fetchone() is not None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.connection.close()
