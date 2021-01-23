
class DatabaseCreator:

    def __init__(self, connection):
        self.connection = connection

    def create_table_members(self):
        cursor = self.connection.cursor()
        sql = "CREATE TABLE IF NOT EXISTS members " \
              "(first_name TEXT, last_name TEXT, chat_id INTEGER UNIQUE)"
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()

    def create_table_links(self):
        cursor = self.connection.cursor()
        sql = "CREATE TABLE IF NOT EXISTS links" \
              "(number INTEGER PRIMARY KEY AUTOINCREMENT, photo TEXT, owner TEXT, " \
              "chat_id INTEGER)"
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()

    def create_table_codes(self):
        cursor = self.connection.cursor()
        sql = "CREATE TABLE IF NOT EXISTS codes" \
              "(code TEXT PRIMARY KEY, discount INTEGER)"
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()