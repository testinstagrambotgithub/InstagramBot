class DatabaseFetcher:

    def __init__(self, connection):
        self.connection = connection

    def get_latest_photos(self, quantity):
        cursor = self.connection.cursor()
        sql = "SELECT photo FROM (SELECT * FROM links ORDER BY number DESC) LIMIT {}".format(quantity)
        cursor.execute(sql)
        data = cursor.fetchall()
        self.connection.commit()
        cursor.close()
        return data

    def get_codes(self):
        cursor = self.connection.cursor()
        sql = "SELECT * FROM codes"
        cursor.execute(sql)
        data = cursor.fetchall()
        self.connection.commit()
        cursor.close()
        return data
