import json
import uuid
import datetime
import psycopg2
import psycopg2.extras

class Base():
    conn = None
    cursor_factory = psycopg2.extras.RealDictCursor

    def __init__(self):
        # Start connection to the database
        self.conn = psycopg2.connect("dbname=cata user=ydelgado")


class Users(Base):
    def __iter__(self):
        name = str(uuid.uuid4())
        cursor = self.conn.cursor(name, cursor_factory=self.cursor_factory)
        cursor.execute("SELECT * FROM winedb.users")
        cursor.itersize = 1
        return cursor

    def insert(self, real_name, username, email, password):
        try:
            cursor = self.conn.cursor(cursor_factory=self.cursor_factory)
            sql = ("INSERT INTO winedb.users"
                   " (userid, real_name, username, email, password, created)"
                   " VALUES (%s, %s, %s, %s, %s, %s)")
            userid = unicode(uuid.uuid4())
            created = datetime.datetime.utcnow()
            params = (userid, real_name, username, email, password, created)
            cursor.execute(sql, params)
            self.conn.commit()
            return userid
        except Exception as e:
            print "Error inserting in winedb.users %s" % e
            return None

    def get_by_userid(self, userid):
        name = str(uuid.uuid4())
        cursor = self.conn.cursor(name, cursor_factory=self.cursor_factory)
        sql = ("SELECT * FROM winedb.users"
               " WHERE userid=%s")
        params = (userid, )
        cursor.execute(sql, params)
        return cursor.fetchone()

    def get_by_email(self, email):
        name = str(uuid.uuid4())
        cursor = self.conn.cursor(name, cursor_factory=self.cursor_factory)
        sql = ("SELECT * FROM winedb.users"
               " WHERE email=%s")
        params = (email, )
        cursor.execute(sql, params)
        return cursor.fetchone()

    def get_by_username(self, username):
        name = str(uuid.uuid4())
        cursor = self.conn.cursor(name, cursor_factory=self.cursor_factory)
        sql = ("SELECT * FROM winedb.users"
               " WHERE username=%s")
        params = (username, )
        cursor.execute(sql, params)
        return cursor.fetchone()


class Wines(Base):
    def __iter__(self):
        name = str(uuid.uuid4())
        cursor = self.conn.cursor(name, cursor_factory=self.cursor_factory)
        cursor.execute("SELECT * FROM winedb.wines")
        cursor.itersize = 1
        return cursor

    def insert(self, userid, name, typed, pics, general_info, fruit_family,
               fruit_quality, non_fruit_quality, structure, notes):
        try:
            cursor = self.conn.cursor(cursor_factory=self.cursor_factory)
            sql = ("INSERT INTO winedb.wines"
                   " (wineid, userid, name, typed, pics, general_info,"
                   " fruit_family, fruit_quality, non_fruit_quality,"
                   " structure, notes, created)"
                   " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

            wineid = unicode(uuid.uuid4())
            created = datetime.datetime.utcnow()
            pics = json.dumps(pics)
            general_info = json.dumps(general_info)
            fruit_family = json.dumps(fruit_family)
            fruit_quality = json.dumps(fruit_quality)
            non_fruit_quality = json.dumps(non_fruit_quality)
            structure = json.dumps(structure)

            params = (wineid, userid, name, typed, pics, general_info,
                      fruit_family, fruit_quality, non_fruit_quality,
                      structure, notes, created)
            cursor.execute(sql, params)
            self.conn.commit()
            return True
        except Exception as e:
            print "Error inserting in winedb.users %s" % e
            return False

    def get_by_userid(self, userid):
        name = str(uuid.uuid4())
        cursor = self.conn.cursor(name, cursor_factory=self.cursor_factory)

        sql = ("SELECT * FROM winedb.wines"
               " WHERE userid=%s")
        params = (userid, )        
        cursor.execute(sql, params)
        
        return cursor.fetchall()

    def get_by_name(self, name):
        name = str(uuid.uuid4())
        cursor = self.conn.cursor(name, cursor_factory=self.cursor_factory)
        sql = ("SELECT * FROM winedb.wines"
               " WHERE name=%s")
        params = (name, )
        cursor.execute(sql, params)
        return cursor.fetchone()

    def get_by_wineid(self, wineid):
        name = str(uuid.uuid4())
        cursor = self.conn.cursor(name, cursor_factory=self.cursor_factory)
        sql = ("SELECT * FROM winedb.wines"
               " WHERE wineid=%s")
        params = (wineid, )
        cursor.execute(sql, params)
        return cursor.fetchone()

    def delete_by_wineid(self, wineid):
        try:
            cursor = self.conn.cursor(cursor_factory=self.cursor_factory)
            sql = ("DELETE FROM winedb.wines"
                   " WHERE wineid=%s")

            params = (wineid,)
            cursor.execute(sql, params)
            self.conn.commit()
            return True
        except Exception as e:
            print "Error deleting from winedb.users %s" % e
            return False