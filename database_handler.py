import sqlite3

from database_creator import DatabaseCreator
from database_updater import DatabaseUpdater
from database_fetcher import DatabaseFetcher


class DatabaseHandler:
    connection = sqlite3.connect('Database.db', check_same_thread=False)
    database_creator = DatabaseCreator(connection)
    database_updater = DatabaseUpdater(connection)
    database_fetcher = DatabaseFetcher(connection)

    def create_table_members(self):
        self.database_creator.create_table_members()

    def create_table_links(self):
        self.database_creator.create_table_links()

    def create_table_codes(self):
        self.database_creator.create_table_codes()

    def update_table_members(self, first_name, last_name, chat_id):
        self.database_updater.update_table_members(first_name, last_name, chat_id)

    def update_table_links(self, photo, owner, chat_id):
        self.database_updater.update_table_links(photo, owner, chat_id)

    def update_table_codes(self, code, discount):
        self.database_updater.update_table_codes(code, discount)

    def get_latest_photos(self, quantity):
        return self.database_fetcher.get_latest_photos(quantity)

    def get_all_codes(self):
        return self.database_fetcher.get_codes()
