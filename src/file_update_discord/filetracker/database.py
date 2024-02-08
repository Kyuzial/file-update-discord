import sqlite3

import file_update_discord.filetracker.filetracker as filetracker
import validators
from file_update_discord.utils.config_reader import ConfigReader

dbConfig = ConfigReader().config.get("filetracker")


class Database(object):
    DATABASE = dbConfig["dbPath"]

    def __init__(self):
        self.connection = sqlite3.connect(self.DATABASE)
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS files "
            "(hash TEXT PRIMARY KEY, url TEXT, fileName TEXT, userId INT)"
        )
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS updates "
            "(hash TEXT PRIMARY KEY, url TEXT, fileName TEXT, userId INT)"
        )

    def add_file(self, file):
        self.cursor.execute(
            "INSERT INTO files (hash, url, fileName, userId) VALUES (?, ?, ?, ?)",
            (file.hash, file.url, file.fileName, file.userId),
        )
        self.connection.commit()

    def file_exists(self, url):
        if not validators.url(url):
            raise ValueError(f"Invalid URL: {url}")
        else:
            self.cursor.execute("SELECT * FROM files WHERE url=?", [url])
            return self.cursor.fetchone() is not None

    def remove_file(self, url):
        if not self.file_exists(url):
            raise ValueError(f"URL {url} is not tracked")
        else:
            self.cursor.execute("DELETE FROM files WHERE url=?", [url])
            self.connection.commit()

    def get_author(self, url):
        if not self.file_exists(url):
            raise ValueError(f"URL {url} is not tracked")
        else:
            self.cursor.execute("SELECT userId FROM files WHERE url=?", [url])
            return self.cursor.fetchone()[0]

    def update_all_files_hash(self):
        print("Updating all files hash")
        self.cursor.execute("SELECT url FROM files")
        urls = self.cursor.fetchall()
        for url in urls:
            self.cursor.execute("SELECT * FROM files WHERE url=?", [url[0]])
            file = self.cursor.fetchone()
            file_object = filetracker.File(file[1], file[3])
            new_hash = file_object.getHash()
            if new_hash != file[0]:
                self.cursor.execute(
                    "UPDATE files SET hash=? WHERE url=?", [new_hash, file[1]]
                )
                self.cursor.execute(
                    "INSERT INTO updates (hash, url, fileName, userId) VALUES (?, ?, ?, ?)",
                    (new_hash, file[1], file[2], file[3]),
                )
                self.connection.commit()
        self.cursor.execute("SELECT * FROM updates")
        updated = self.cursor.fetchall()
        return updated

    def clear_updates(self):
        self.cursor.execute("DELETE FROM updates")
        self.connection.commit()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.connection.close()
