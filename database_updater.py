
class DatabaseUpdater:

    def __init__(self, connection):
        self.connection = connection

    def update_table_members(self, first_name, last_name, chat_id):
        cursor = self.connection.cursor()
        sql = "INSERT OR IGNORE INTO members " \
              "(first_name, last_name, chat_id) " \
              "VALUES (?, ?, ?)"
        val = (first_name, last_name, chat_id)
        cursor.execute(sql, val)
        self.connection.commit()
        cursor.close()

    def update_table_links(self, photo, owner, chat_id):
        cursor = self.connection.cursor()
        sql = "INSERT OR IGNORE INTO links " \
              "(photo, owner, chat_id) " \
              "VALUES (?, ?, ?)"
        val = (photo, owner, chat_id)
        cursor.execute(sql, val)
        self.connection.commit()
        cursor.close()

    def update_table_codes(self, code, discount):
        cursor = self.connection.cursor()
        sql = "INSERT OR IGNORE INTO codes " \
              "(code, discount) " \
              "VALUES (?, ?)"
        val = (code, discount)
        cursor.execute(sql, val)
        self.connection.commit()
        cursor.close()