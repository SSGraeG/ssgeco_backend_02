import pymysql
from pymysql import connect
from datetime import datetime
import pytz


connectionString = {
    # 'host': '127.0.0.1',
    'host': 'eco-rds.cykey8vytdto.ap-northeast-2.rds.amazonaws.com',
    'port': 3306,
    'database': 'company_2',
    'user': 'admin',
    # 'user': 'root',
    # 'password': '1234',
    'password': 'password',
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
            cursor.fetchone()
            con.commit()

            affected_rows = cursor.rowcount
            if affected_rows > 0:
                kst = pytz.timezone('Asia/Seoul')
                current_date = datetime.now(kst).strftime('%Y-%m-%d')
                mileage_tracking_sql = "INSERT INTO mileage_tracking (user_email, mileage_category_id, before_mileage, after_mileage, use_date) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(mileage_tracking_sql, (user_email, coupon_id, mileage_before, mileage_after, current_date))
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
            cursor.fetchone()
            con.commit()
            affected_rows = cursor.rowcount
            if affected_rows > 0:
                kst = pytz.timezone('Asia/Seoul')
                current_date = datetime.now(kst).strftime('%Y-%m-%d')
                mileage_tracking_sql = "INSERT INTO mileage_tracking (user_email, mileage_category_id, before_mileage, after_mileage, current_date) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(mileage_tracking_sql, (user_email, donation_id, mileage_before, mileage_after, current_date))
                con.commit()
                return mileage_after
    except Exception as e:
        print(e)
        return 500


# 사용자 현재 마일리지 잔액 가져오기
def get_user_mileage(user_email):
    try:
        with connect(**connectionString) as con:
            cursor = con.cursor()

            sql = "SELECT mileage FROM user where email = %s"
            cursor.execute(sql, (user_email,))
            user_mileage = cursor.fetchone()['mileage']

            return user_mileage

    except Exception as e:
        print(e)



# def get_tracking(user_email, start_date, end_date):
#     try:
#         with connect(**connectionString) as con:
#             cursor = con.cursor()
#
#             start_date = datetime.strptime(start_date, '%Y-%m-%d')
#             end_date = datetime.strptime(end_date, '%Y-%m-%d')
#
#             select_sql = "SELECT  * FROM mileage_tracking WHERE use_date BETWEEN %s AND %s AND user_email = %s"
#             cursor.execute(select_sql, (start_date, end_date, user_email))
#
#             result = cursor.fetchall()
#             combined_result = []
#
#             for row in result:
#                 mileage_category_id = row['mileage_category_id']
#                 select_sql_category = "SELECT * FROM mileage_category WHERE id = %s"
#                 cursor.execute(select_sql_category, (mileage_category_id,))
#                 result_category = cursor.fetchall()
#
#                 combined_row = {
#                     "mileage_tracking": row,
#                     "mileage_category": result_category
#                 }
#                 combined_result.append(combined_row)
#             print(combined_result)
#             return combined_result
#             # return result
#
#     except Exception as e:
#         print(e)
def get_tracking(user_email, start_date, end_date):
    try:
        with connect(**connectionString) as con:
            cursor = con.cursor()

            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')

            select_sql = ("SELECT mt.*, mc.* FROM mileage_tracking mt JOIN mileage_category mc "
                          "ON mt.mileage_category_id = mc.id "
                          "WHERE mt.use_date BETWEEN %s AND %s AND mt.user_email = %s "
                          "ORDER BY mt.use_date DESC")
            cursor.execute(select_sql, (start_date, end_date, user_email))

            result = cursor.fetchall()
            combined_result = []

            for row in result:
                combined_row = {
                    "id": row['id'],
                    "use_date": row['use_date'].strftime('%Y-%m-%d'),
                    "user_email": row['user_email'],
                    "mileage_category_id": row['mileage_category_id'],
                    "before_mileage": row['before_mileage'],
                    "after_mileage": row['after_mileage'],
                    "mileage_category": {
                        "id": row['id'],
                        "name": row['name'],
                        "usepoint": row['usepoint'],
                        "category": row['category']
                    }
                }
                combined_result.append(combined_row)

            print(combined_result)
            return combined_result

    except Exception as e:
        print(e)
        return None


def get_all_tracking(user_email):
    try:
        with connect(**connectionString) as con:
            cursor = con.cursor()

            select_sql = ("SELECT mt.*, mc.* FROM mileage_tracking mt JOIN mileage_category mc "
                          "ON mt.mileage_category_id = mc.id "
                          "WHERE mt.user_email = %s "
                          "ORDER BY mt.use_date DESC")
            cursor.execute(select_sql, (user_email))

            result = cursor.fetchall()
            combined_result = []

            for row in result:
                combined_row = {
                    "id": row['id'],
                    "use_date": row['use_date'].strftime('%Y-%m-%d'),
                    "user_email": row['user_email'],
                    "mileage_category_id": row['mileage_category_id'],
                    "before_mileage": row['before_mileage'],
                    "after_mileage": row['after_mileage'],
                    "mileage_category": {
                        "id": row['id'],
                        "name": row['name'],
                        "usepoint": row['usepoint'],
                        "category": row['category']
                    }
                }
                combined_result.append(combined_row)

            print(combined_result)
            return combined_result

    except Exception as e:
        print(e)
        return None
# 사용자 현재 마일리지 잔액 가져오기
def get_user_mielage(user_email):
    try:
        with connect(**connectionString) as con:
            cursor = con.cursor()

            sql = "SELECT mileage FROM user where email = %s"
            cursor.execute(sql, (user_email,))
            user_mileage = cursor.fetchone()['mileage']

            return user_mileage

    except Exception as e:
        print(e)


# AI 판독 성공 후 마일리지 적립
def add_mileage(user_email):
    try:
        with connect(**connectionString) as con:
            cursor = con.cursor()

            sql = "UPDATE user SET mileage = mileage + 100 WHERE email = %s"
            cursor.execute(sql, (user_email, ))
            con.commit()

            select_sql = "SELECT mileage FROM user WHERE email = %s"
            cursor.execute(select_sql, (user_email,))
            updated_mileage = cursor.fetchone()['mileage']

            return updated_mileage

    except Exception as e:
        print(e)