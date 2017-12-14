import sqlite3

class Database():
    def __init__(self):
        db = sqlite3.connect("alchemy.sqlite")
        try:
            cursor = db.cursor()
            #cursor.execute("DROP TABLE IF EXISTS users")
            cursor.execute("CREATE TABLE IF NOT EXISTS users(userID INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT, password TEXT, name TEXT, favorites TEXT)")
            db.commit()
            cursor.execute("CREATE TABLE IF NOT EXISTS active(userID INTEGER)")
            db.commit()
            print("created table Users")
        except Exception as e:
            print(e)
        db.close()

class Users():
    def __init__(self):
        Database()
        self.database = sqlite3.connect("alchemy.sqlite")
        self.cursor = self.database.cursor()

    def addUser(self, user_email, user_password, user_name):
        name = str(user_name) .upper()
        email = user_email
        pw = user_password
        self.cursor.execute("INSERT INTO users(name, email, password) VALUES (?, ?, ?)", [name, email, pw])
        self.database.commit()
        self.cursor.execute("SELECT * FROM users")
        user = self.cursor.fetchall()
        #print(user)
        return (user)

    def deleteUser(self, user_id):
        id = int(user_id)
        self.cursor.execute("DELETE FROM users WHERE userID=?",[id])
        self.database.commit()

    def getUserInfoEmail(self, user_email):
        email = user_email
        self.cursor.execute("SELECT * FROM users WHERE email=?",[email])
        user_info = self.cursor.fetchall()
        return user_info

    def getUserInfoID(self, user_id):
        id = user_id
        self.cursor.execute("SELECT * FROM users WHERE userID=?",[id])
        user_info = self.cursor.fetchall()
        return user_info


    def getAllUsers(self):
        self.cursor.execute("SELECT * FROM users")
        user = self.cursor.fetchall()
        #print(user)
        return (user)

    def checkEmail(self, user_email):
        email = user_email
        self.cursor.execute("SELECT * FROM users WHERE email=?",[email])
        is_email = self.cursor.fetchall()
        if not is_email:
            return ("None")
        else:
            return ("Found")


    def closeDatabase(self):
        self.database.close()

class ActiveUser():
    def __init__(self):
        Database()
        self.database = sqlite3.connect("alchemy.sqlite")
        self.cursor = self.database.cursor()

    def setActiveUser(self, user_id):
        id = user_id
        self.cursor.execute("INSERT INTO active(userID) VALUES (?)", [id])
        self.database.commit()

    def getActiveUser(self):
        self.cursor.execute("SELECT * FROM active")
        active_user = self.cursor.fetchall()
        if not active_user:
            return "None"
        else:
            return active_user[0][0]

    def removeActiveUser(self,user_id):
        id = user_id
        self.cursor.execute("DELETE FROM active WHERE userID = ?", [id])
        self.database.commit()

    def closeDatabase(self):
        self.database.close()