import pymysql
from pymysql import connect
from datetime import datetime


connectionString = {
    'host': '127.0.0.1',
    'port': 3306,
    'database': 'eco',
    # 'user': 'user1',
    # 'password': '1234',
    'user': 'root',
    # 'password': '1234',
    'charset': 'utf8',
    'cursorclass': pymysql.cursors.DictCursor
}


def get_all():
    try:
        with connect(**connectionString) as con:
            cursor = con.cursor()
            sql = "SELECT * FROM USER"
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
    except Exception as e:
        print(e)


def id_check(user_id, pwd):
    try:
        with connect(**connectionString) as con:
            cursor = con.cursor()
            sql = "SELECT * FROM user " + "where email = %s and password = %s;"
            cursor.execute(sql, [user_id, pwd])
            result = cursor.fetchall()
            return result
    except Exception as e:
        print(e)


def id_duplicate_check(email):
    try:
        with connect(**connectionString) as con:
            cursor = con.cursor()
            sql = "SELECT * FROM user where email = %s;"
            cursor.execute(sql,[email])
            result = cursor.fetchone()
            return result
    except Exception as e:
        print(e)


def sign_up(email, name, password, address):
    try:
        with connect(**connectionString) as con:
            cursor = con.cursor()
            sql = "INSERT INTO user (email, name, password, address) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (email, name, password, address))
            user_info = cursor.fetchall()
            con.commit()
            return user_info, 200, {'Content-Type': 'application/json'}
    except Exception as e:
        print(e)


def get_user(email):
    try:
        with connect(**connectionString) as con:
            cursor = con.cursor()
            sql = "SELECT * FROM user where email = %s;"
            cursor.execute(sql, (email))
            user_info = cursor.fetchone()
            con.commit()
            return user_info, 200, {'Content-Type': 'application/json'}
    except Exception as e:
        print(e)


def get_coupon():
    try:
        with connect(**connectionString) as con:
            cursor = con.cursor()
            sql = "SELECT * FROM coupon order by usepoint"
            cursor.execute(sql)
            coupon_list = cursor.fetchall()
            con.commit()
            return coupon_list
    except Exception as e:
        print(e)


def get_donation():
    try:
        with connect(**connectionString) as con:
            cursor = con.cursor()
            sql = "SELECT * FROM coupon order by usepoint"
            cursor.execute(sql)
            coupon_list = cursor.fetchall()
            con.commit()
            return coupon_list
    except Exception as e:
        print(e)


def use_coupon():
    try:
        with connect(**connectionString) as con:
            cursor = con.cursor()
            sql = "SELECT * FROM coupon order by usepoint"
            cursor.execute(sql)
            coupon_list = cursor.fetchall()
            con.commit()
            return coupon_list
    except Exception as e:
        print(e)


