import sqlite3


class Users:

    def __init__(self):
        self.conn = sqlite3.connect('users.db') 
        self.c = self.conn.cursor()
        self.id = 0

    def createUserTable(self):
        query = "CREATE TABLE IF NOT EXISTS USERS(id integer NOT NULL PRIMARY KEY AUTOINCREMENT, username varchar(255), password varchar(255), CONSTRAINT uniqUsers UNIQUE (username,password));"
        self.c.execute(query)
        print("Users Table created Successfully.")

    def createUser(self,username,password):
        self.c.execute(''' INSERT INTO USERS(username,password) values(?,?) ''',(username,password))
        self.conn.commit()

    def getUser(self,username,password):
        self.c.execute(''' SELECT id FROM USERS WHERE username = ? and password = ? ''',(username,password))
        for row in self.c.fetchall():
            self.id = row
        return self.id


if __name__ == "__main__":
    pass