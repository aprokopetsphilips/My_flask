import math
import sqlite3



class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def getMenu(self):
        sql = '''SELECT * FROM mainmenu'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res: return res
        except:
            print('did not read')

        return []

    def addPost(self, title, text):
        try:

            self.__cur.execute('INSERT INTO posts VALUES(NULL, ?, ?)', (title, text))
            self.__db.commit()

        except sqlite3.Error as e:
            print('Ошибка добавления статьи в БД' + str(e))
            return False

        return True

    def getPost(self, post_id):
        try:
            self.__cur.execute(f'SELECT title, text FROM posts WHERE id = {post_id} LIMIT 1')
            res = self.__cur.fetchone()
            if res:
                return res
        except sqlite3.Error as e:
            print('Ошибка получения статьи из БД' + str(e))

        return (False, False)

    def getPostsAnonce(self):
        try:
            self.__cur.execute(f'SELECT id, title, text FROM posts ORDER BY id DESC')
            res = self.__cur.fetchall()
            if res:
                return res
        except sqlite3.Error as e:
            print('Ошибка получения статьи из БД' + str(e))

        return []
