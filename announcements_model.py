class AnnouncementsModel:
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS announcements 
                                (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                 title VARCHAR(100),
                                 cost INTEGER,
                                 content VARCHAR(1000),
                                 category VARCHAR(1000),
                                 user_id INTEGER,
                                 image INTEGER
                                 )''') #add announcement's img number
        cursor.close()
        self.connection.commit()

    def insert(self, title, cost, content, category, user_id, image):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO announcements 
                          (title, cost, content, category, user_id, image) 
                          VALUES (?,?,?,?,?,?)''', (title, cost, content, category, str(user_id), image))
        cursor.close()
        self.connection.commit()

    def get(self, news_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM announcements WHERE id = ?", (str(news_id)))
        row = cursor.fetchone()
        return row

    def get_all(self, user_id=None):
        cursor = self.connection.cursor()
        if user_id:
            cursor.execute("SELECT * FROM announcements WHERE user_id = ?", (str(user_id)))
        else:
            cursor.execute("SELECT * FROM announcements")
        rows = cursor.fetchall()
        return rows

    def get_all_category(self, category=None): # after will add function in main (now it's useless)
        cursor = self.connection.cursor()
        if category:
            cursor.execute("SELECT * FROM announcements WHERE category = ?", category)
        else:
            cursor.execute("SELECT * FROM announcements")
        rows = cursor.fetchall()
        return rows

    def delete(self, news_id):
        print(news_id)
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM announcements WHERE id = {}'''.format((str(news_id))))
        cursor.close()
        self.connection.commit()