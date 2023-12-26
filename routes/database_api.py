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
    # 'password': 'passwd',
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
            return user_info
    except Exception as e:
        print(e)


def get_coupon():
    try:
        with connect(**connectionString) as con:
            cursor = con.cursor()
            sql = "SELECT * FROM mileage_category where category='coupon' order by usepoint"
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
            sql = "SELECT * FROM mileage_category where category='donation' order by usepoint"
            cursor.execute(sql)
            donation_list = cursor.fetchall()
            con.commit()
            return donation_list
    except Exception as e:
        print(e)


def use_coupon(user_email, coupon_id):
    try:
        with connect(**connectionString) as con:
            cursor = con.cursor()
            sql = "SELECT usepoint FROM mileage_category where id = %s"
            cursor.execute(sql, (coupon_id,))
            result = cursor.fetchall()
            use_point = result[0]['usepoint']
            con.commit()
        with connect(**connectionString) as con:
            cursor = con.cursor()
            mileage_before_sql = "SELECT mileage FROM user WHERE email = %s"
            cursor.execute(mileage_before_sql, (user_email,))
            result = cursor.fetchall()
            con.commit()
            mileage_before = result[0]['mileage']
            mileage_after = mileage_before - use_point

            sql = "UPDATE user SET mileage = mileage - %s WHERE email = %s"
            cursor.execute(sql, (use_point, user_email))
            result = cursor.fetchone()
            con.commit()
            affected_rows = cursor.rowcount
            if affected_rows > 0:
                # additional_sql = "SELECT mileage FROM user where email = %s"
                # cursor.execute(additional_sql, (user_email,))
                # use_point = cursor.fetchall()[0]['mileage']
                # con.commit()
                mileage_tracking_sql = "INSERT INTO milege_tracking (user_email, mileage_category_id, before_mileage, after_mileage) VALUES (%s, %s, %s, %s)"
                cursor.execute(mileage_tracking_sql, (user_email, coupon_id, mileage_before, mileage_after))
                con.commit()
                return mileage_after
    except Exception as e:
        print(e)
        return 500


def use_donation(user_email, donation_id):
    try:
        with connect(**connectionString) as con:
            cursor = con.cursor()
            sql = "SELECT usepoint FROM mileage_category where id = %s"
            cursor.execute(sql, (donation_id,))
            result = cursor.fetchall()
            use_point = result[0]['usepoint']
            con.commit()
        with connect(**connectionString) as con:
            cursor = con.cursor()
            mileage_before_sql = "SELECT mileage FROM user WHERE email = %s"
            cursor.execute(mileage_before_sql, (user_email,))
            result = cursor.fetchall()
            con.commit()
            mileage_before = result[0]['mileage']
            mileage_after = mileage_before - use_point

            sql = "UPDATE user SET mileage = mileage - %s WHERE email = %s"
            cursor.execute(sql, (use_point, user_email))
            result = cursor.fetchone()
            con.commit()
            affected_rows = cursor.rowcount
            if affected_rows > 0:
                # additional_sql = "SELECT mileage FROM user where email = %s"
                # cursor.execute(additional_sql, (user_email,))
                # use_point = cursor.fetchall()[0]['mileage']
                # con.commit()
                mileage_tracking_sql = "INSERT INTO milege_tracking (user_email, mileage_category_id, before_mileage, after_mileage) VALUES (%s, %s, %s, %s)"
                cursor.execute(mileage_tracking_sql, (user_email, donation_id, mileage_before, mileage_after))
                con.commit()
                return mileage_after
    except Exception as e:
        print(e)
        return 500

