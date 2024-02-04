import sqlite3

from file_update_discord.utils import ConfigReader

config = ConfigReader()
dbConfig = config.get("filetracker")


class Database(object):
    DATABASE = dbConfig["dbPath"]

    def __init__(self):
        self.connection = sqlite3.connect(self.DATABASE)
        self.cursor = self.connection.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.connection.close()


if __name__ == "__main__":
    with Database() as db:
        db.cursor.execute("SELECT * FROM files")
        print(db.cursor.fetchall())
