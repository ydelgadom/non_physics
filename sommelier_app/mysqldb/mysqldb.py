#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import uuid
import datetime
import MySQLdb as mdb
import MySQLdb.cursors
import sys

import mysqldb_util

class Base():
    conn = None
    cursor = None
    dict_cursor = MySQLdb.cursors.DictCursor

    def __init__(self):
        # Start connection to the database
        self.conn = mdb.Connection('localhost', 'root', 'fresito82', 'winesdb')
        self.cursor = self.conn.cursor(self.dict_cursor)


class Users(Base):
    def insert(self, real_name, username, email, password):
        try:
            sql = ("INSERT INTO winesdb.users"
                   " (userid, real_name, username, email, password, created)"
                   " VALUES (%s, %s, %s, %s, %s, %s)")
            userid = unicode(uuid.uuid4())
            print userid
            created = datetime.datetime.utcnow()
            params = (userid, real_name, username, email, password, created)
            self.cursor.execute(sql, params)
            self.conn.commit()
            return userid
        except Exception as e:
            print "Error inserting in winesdb.users %s" % e
            return None

    def get_by_userid(self, userid):
        sql = ("SELECT * FROM winesdb.users"
               " WHERE userid=%s")
        params = (userid, )
        self.cursor.execute(sql, params)
        return self.cursor.fetchone()

    def get_by_email(self, email):
        sql = ("SELECT * FROM winesdb.users"
               " WHERE email=%s")
        params = (email, )
        self.cursor.execute(sql, params)
        return self.cursor.fetchone()

    def get_by_username(self, username):
        sql = ("SELECT * FROM winesdb.users"
               " WHERE username=%s")
        params = (username, )
        self.cursor.execute(sql, params)
        return self.cursor.fetchone()

    def delete_by_username(self, username):
        try:
            sql = ("DELETE FROM winesdb.users"
                   " WHERE username=%s")
            params = (username, )
            self.cursor.execute(sql, params)
            self.conn.commit()
            return True
        except Exception as e:
            print e
            return False


class Wines(Base):
    def insert(self, userid, name, typed, pics, general_info, fruit_family,
               fruit_quality, non_fruit_quality, structure, notes):
        try:
            sql = ("INSERT INTO winesdb.wines"
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
            self.cursor.execute(sql, params)
            self.conn.commit()
            return True
        except Exception as e:
            print "Error inserting in winesdb.users %s" % e
            return False

    def get_by_userid(self, userid):
        sql = ("SELECT * FROM winesdb.wines"
               " WHERE userid=%s")
        params = (userid, )        
        self.cursor.execute(sql, params)
        res = self.cursor.fetchall()
        return mysqldb_util.convert_list_to_json(res)

    def get_by_name(self, name):
        sql = ("SELECT * FROM winesdb.wines"
               " WHERE name=%s")
        params = (name, )
        self.cursor.execute(sql, params)
        res = self.cursor.fetchone()
        return mysqldb_util.convert_to_json(res)

    def get_by_wineid(self, wineid):
        sql = ("SELECT * FROM winesdb.wines"
               " WHERE wineid=%s")
        params = (wineid, )
        self.cursor.execute(sql, params)
        res = self.cursor.fetchone()
        return mysqldb_util.convert_to_json(res)

    def delete_by_wineid(self, wineid):
        try:
            sql = ("DELETE FROM winesdb.wines"
                   " WHERE wineid=%s")
            params = (wineid,)
            self.cursor.execute(sql, params)
            self.conn.commit()
            return True
        except Exception as e:
            print "Error deleting from winesdb.users %s" % e
            return False        
