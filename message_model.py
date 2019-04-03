from db import DB

db = DB()


class MessageModel:
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS messages 
                                (
                                 message_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                 sender_id INTEGER,
                                 adressee_id INTEGER,
                                 message VARCHAR(10000)
                                 )''')
        cursor.close()
        self.connection.commit()

    def send(self, sender_id, adressee_id, message): # add message in db
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO messages 
                          (sender_id, adressee_id,  message) 
                          VALUES (?,?,?)''', (
            str(sender_id), str(adressee_id),
            message))
        cursor.close()
        self.connection.commit()

    def get_all_between_pair(self, sender_id, adressee_id): # get all messages in dialog
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT * FROM messages WHERE sender_id = ? AND adressee_id = ? OR sender_id = ? AND adressee_id = ?",
            (str(sender_id), str(adressee_id), str(adressee_id), str(
                sender_id)))
        rows = cursor.fetchall()
        return rows

    def get_all(self, sender_id):
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT * FROM messages WHERE sender_id = ? OR adressee_id = ?",
            (str(sender_id), str(sender_id))
        )
        rows = cursor.fetchall()
        return rows
